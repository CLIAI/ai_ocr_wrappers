#!/bin/bash

set -e

VERBOSE=0
FORCE=0

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

normalize_filename() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]/_/g' | cut -c1-64
}

check_existing_file() {
    for ext in webp jpg png; do
        if [ -f "${1}.${ext}" ]; then
            return 0
        fi
    done
    return 1
}

generate_output_filename() {
    local prompt="$1"
    local output="$2"
    
    if [ -n "$output" ]; then
        echo "${output%.*}"
    else
        normalize_filename "$prompt"
    fi
}

determine_file_format() {
    local file="$1"
    local mime_type=$(file -b --mime-type "$file")
    case "$mime_type" in
        image/png) echo "png" ;;
        image/jpeg) echo "jpg" ;;
        image/webp) echo "webp" ;;
        *) echo "unknown" ;;
    esac
}

generate_image() {
    local prompt="$1"
    local output_file="$2"
    
    verbose "Generating image for prompt: $prompt"

    local base_name=$(generate_output_filename "$prompt" "$output_file")

    if [ "$FORCE" -eq 0 ] && check_existing_file "$base_name"; then
        echo "SKIPPING: File with base name '$base_name' already exists." >&2
        exit 1
    fi

    local response=$(curl -s -X POST \
        -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"input\":{\"prompt\":\"$prompt\"}}" \
        https://api.replicate.com/v1/predictions)

    local prediction_id=$(echo "$response" | jq -r '.id')
    verbose "Prediction ID: $prediction_id"

    local status="starting"
    while [ "$status" == "starting" ] || [ "$status" == "processing" ]; do
        sleep 5
        response=$(curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
            https://api.replicate.com/v1/predictions/$prediction_id)
        status=$(echo "$response" | jq -r '.status')
        verbose "Status: $status"
    done

    if [ "$status" != "succeeded" ]; then
        echo "Error: Prediction failed. Please check the logs for more details." >&2
        exit 1
    fi

    local output_url=$(echo "$response" | jq -r '.output[0]')
    if [ -z "$output_url" ] || [ "$output_url" == "null" ]; then
        echo "Error: No output URL received from the API." >&2
        exit 1
    fi

    verbose "Downloading image from $output_url"
    local tmp_file=$(mktemp)
    curl -s -o "$tmp_file" "$output_url"

    local ext=$(determine_file_format "$tmp_file")
    if [ "$ext" == "unknown" ]; then
        echo "Error: Unable to determine file format." >&2
        rm "$tmp_file"
        exit 1
    fi

    local final_output_file="${base_name}.${ext}"
    mv "$tmp_file" "$final_output_file"
    verbose "Image saved as: $final_output_file"
}

main() {
    local prompt=""
    local output_file=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -v|--verbose) VERBOSE=1; shift ;;
            -f|--force) FORCE=1; shift ;;
            -o|--output) output_file="$2"; shift 2 ;;
            *) prompt="$1"; shift ;;
        esac
    done

    if [ -z "$prompt" ] && [ -t 0 ]; then
        echo "Error: prompt is required if not piping input" >&2
        exit 1
    fi

    if [ -z "$prompt" ]; then
        prompt=$(cat)
    fi

    check_api_token
    generate_image "$prompt" "$output_file"
}

main "$@"
