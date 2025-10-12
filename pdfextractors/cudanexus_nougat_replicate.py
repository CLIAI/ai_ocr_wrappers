#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "replicate>=0.25.0",
#   "requests>=2.31.0",
# ]
# requires-python = ">=3.11"
# ///

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
        return normalize_filename(input_filename) + ".md"

def encode_file_to_base64(file_path):
    """Encode the input file to base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def convert_pdf_to_markdown(input_file, output_file, verbose=False, force=False):
    """Convert PDF to Markdown using Replicate API."""
    verbose_print(f"Converting PDF to Markdown: {input_file}", verbose)

    final_output_file = generate_output_filename(input_file, output_file)

    if not force and os.path.exists(final_output_file):
        print(f"SKIPPING: File '{final_output_file}' already exists.", file=sys.stderr)
        return

    try:
        # Encode the input file to base64
        encoded_file = encode_file_to_base64(input_file)

        # Prepare the input for the API
        api_input = {
            "pdf_file": f"data:application/pdf;base64,{encoded_file}"
        }

        output = replicate.run(
            "cudanexus/nougat:d0b4e90da423598ff84debc9115bf891dd819843600ad842c0c178e3571f9e76",
            input=api_input
        )

        print("Error: Unexpected output format from the API.", file=sys.stderr)
        response = requests.get(output)
        response.raise_for_status()
        content = response.text

        with open(final_output_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        verbose_print(f"Output saved as: {final_output_file}", verbose)
        

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown using Replicate API")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite existing files")
    args = parser.parse_args()

    check_api_token()
    convert_pdf_to_markdown(
        args.input,
        args.output,
        args.verbose,
        args.force
    )

if __name__ == "__main__":
    main()
