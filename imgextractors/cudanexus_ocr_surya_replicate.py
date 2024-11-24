#!/usr/bin/env python3

import argparse
import os
import sys
import requests
import replicate
import base64

def verbose_print(message, verbose=False):
    """Print message if verbose mode is enabled."""
    if verbose:
        print(message, file=sys.stderr)

def check_api_token():
    """Check if REPLICATE_API_TOKEN is set."""
    if "REPLICATE_API_TOKEN" not in os.environ:
        print("ERROR: REPLICATE_API_TOKEN is not set", file=sys.stderr)
        sys.exit(1)

def normalize_filename(filename, max_length=64):
    """Normalize filename to a valid format."""
    base = os.path.splitext(os.path.basename(filename))[0]
    normalized = ''.join(c.lower() if c.isalnum() else '_' for c in base)
    return normalized[:max_length]

def generate_output_filename(input_filename, output_filename):
    """Generate output filename based on input file or output flag."""
    if output_filename:
        return output_filename
    else:
        return normalize_filename(input_filename) + ".txt"

def encode_file_to_base64(file_path):
    """Encode the input file to base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def extract_text_from_image(input_file, output_file, verbose=False, force=False):
    """Extract text from image using Replicate's OCR-Surya API."""
    verbose_print(f"Extracting text from image: {input_file}", verbose)

    final_output_file = generate_output_filename(input_file, output_file)

    if not force and os.path.exists(final_output_file):
        print(f"SKIPPING: File '{final_output_file}' already exists.", file=sys.stderr)
        return

    try:
        # Encode the input file to base64
        encoded_file = encode_file_to_base64(input_file)

        # Prepare the input for the API
        api_input = {
            "image": f"data:image/jpeg;base64,{encoded_file}",
            "action": "Run OCR"
        }

        output = replicate.run(
            "cudanexus/ocr-surya:7ab5bedee2cd1f0c82b2df6718d19bf0b473f738f9db062f122e47e1467f96ce",
            input=api_input
        )

        if isinstance(output, dict) and 'text' in output:
            content = output['text']
            
            with open(final_output_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            verbose_print(f"Text saved as: {final_output_file}", verbose)
            print(f"{final_output_file}")
        else:
            print("Error: Unexpected output format from the API.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Extract text from images using Replicate's OCR-Surya API")
    parser.add_argument("input", help="Input image file")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite existing files")
    args = parser.parse_args()

    check_api_token()
    extract_text_from_image(
        args.input,
        args.output,
        args.verbose,
        args.force
    )

if __name__ == "__main__":
    main()
