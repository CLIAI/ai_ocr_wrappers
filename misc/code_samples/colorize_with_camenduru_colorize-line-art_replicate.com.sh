#!/bin/bash

VERBOSE=0

verbose() {
    if [ "$VERBOSE" -eq 1 ]; then
        echo "$@" >&2
    fi
}

check_api_token() {
    if [ -z "$REPLICATE_API_TOKEN" ]; then
        echo "ERROR: REPLICATE_API_TOKEN is not set" >&2
        exit 1
    fi
    verbose "REPLICATE_API_TOKEN is set"
}

check_output_file() {
    local in_fn="$1"
    local base_fn="$2"
    
    local existing_files=$(ls "${base_fn}.out."* 2> /dev/null)
    if [ -n "$existing_files" ]; then
        echo "SKIPPING: $in_fn as $existing_files exists" >&2
        return 1
    fi
    return 0
}

check_input_file() {
    local in_fn="$1"
    
    if [ ! -r "$in_fn" ]; then
        echo "ERROR: $in_fn is not readable" >&2
        return 1
    fi
    return 0
}

generate_output_filename() {
    local in_fn="$1"
    local base_fn="$2"
    
    if [ -z "$base_fn" ]; then
        local filename=$(basename "$in_fn")
        local name="${filename%.*}"
        base_fn="${name}"
    fi
    echo "$base_fn"
}

cleanup_tempfile() {
    if [ -n "$tmp_json" ] && [ -f "$tmp_json" ]; then
        rm -f "$tmp_json"
    fi
}

# TODO: add model that will do image2text and another llm that will generate out of this image description a desription of colorful lineart image.

replicate_image2image_model() {
    local in_fn="$1"
    local base_fn=$(generate_output_filename "$1" "$2")
    
    verbose "Checking API token..."
    check_api_token || return 1
    verbose "Checking output file..."
    check_output_file "$in_fn" "$base_fn" || return 1
    verbose "Checking input file..."
    check_input_file "$in_fn" || return 1
    
    # Create a temporary JSON file
    local tmp_json=$(mktemp)
    cat > "$tmp_json" << EOF
{
    "version": "59575cca43435fec91bf2016648a36db03ab0c1556490974e3c483274076a6ec",
    "input": {
        "det": "None",
        "eta": 1,
        "seed": 4,
        "scale": 9,
        "prompt": "colorful lineart drawing",
        "a_prompt": "masterpiece, best quality, ultra-detailed, illustration",
        "n_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, pubic hair,extra digit, fewer digits, cropped, worst quality, low quality",
        "strength": 1,
        "ddim_steps": 25,
        "input_image": "data:image/jpeg;base64,
EOF
    # Convert local file to base64 and append to the temporary JSON file
    base64 -w 0 "$in_fn" >> "$tmp_json"
    cat >> "$tmp_json" << EOF
",
        "image_resolution": 1024,
        "detect_resolution": 1024
    }
}
EOF

    # Set a trap to cleanup the temporary file on exit
    trap cleanup_tempfile EXIT

    verbose "Making API call..."
    # Make the API call and extract the prediction ID from the response
    local response=$(curl -s -X POST \
      -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
      -H "Content-Type: application/json" \
      -d "@$tmp_json" \
      https://api.replicate.com/v1/predictions)
    verbose "API call completed. Received JSON: $(echo "$response" | jq -c .)"
    local prediction_id=$(echo "$response" | jq -r '.id')
    verbose "Prediction ID: $prediction_id. Received JSON: $(echo "$response" | jq -c .)"

    # Poll the API for the status of the prediction
    local status="starting"
    while [ "$status" == "starting" ] || [ "$status" == "processing" ]; do
        sleep 5
        response=$(curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
          https://api.replicate.com/v1/predictions/$prediction_id)
        status=$(echo "$response" | jq -r '.status')
        verbose "Status: $status. Received JSON: $(echo "$response" | jq -c .)"
        if [ "$status" == "failed" ]; then
            echo "Error: Prediction failed. Please check the logs for more details." >&2
            return 1
        fi
    done

    # Once the prediction is complete, fetch the output image
    local output=$(echo "$response" | jq -r '.output')
    
    if [ "$output" == "null" ]; then
        echo "Error: No output returned from the API. The prediction may not be ready yet, or an error may have occurred." >&2
        return 1
    fi

    local output_url
    if [[ "$output" == "["* ]]; then
        output_url=$(echo "$output" | jq -r '.[0]')
    elif [[ "$output" == "http"* ]]; then
        output_url="$output"
    else
        echo "Error: Unexpected output format from the API: $output" >&2
        return 1
    fi

    if [ "$output_url" == "null" ] || [ -z "$output_url" ]; then
        echo "Error: No valid output URL from the API." >&2
        return 1
    fi

    verbose "Downloading output image..."
    # Download the output image to a temporary file
    local tmp_out_fn=$(mktemp)
    verbose "Output URL: $output_url"
    curl -s -o "$tmp_out_fn" "$output_url"
    if [ $? -eq 0 ]; then
        verbose "Image saved to $tmp_out_fn"
    else
        echo "Error: Failed to download image from $output_url" >&2
        return 1
    fi
    verbose "Download completed"

    # Identify the file format of the downloaded image
    local ext=$(file --mime-type "$tmp_out_fn" | awk -F' ' '{print $NF}' | awk -F'/' '{print $NF}')
    verbose "Identified file format: $ext"

    # Rename the temporary file with the appropriate extension and move it to the final destination
    local out_fn="${base_fn}.out.${ext}"
    verbose "Moving $tmp_out_fn to $out_fn"
    mv "$tmp_out_fn" "$out_fn"
    if [ $? -eq 0 ]; then
        verbose "Image moved to $out_fn"
    else
        echo "Error: Failed to move image to $out_fn" >&2
        return 1
    fi
}

# Main execution
while true; do
    case "$1" in
        -v|--verbose) VERBOSE=1; shift ;;
        *) break ;;
    esac
done
echo "Starting script..."
replicate_image2image_model "$@"
echo "Script finished."
