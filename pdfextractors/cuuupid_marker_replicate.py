#!/usr/bin/env python3

import argparse
import os
import sys
import requests
import replicate
import time
import json

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

def check_existing_file(base_name):
    """Check if a file with the given base name (markdown extension) exists."""
    return os.path.exists(f"{base_name}.md")

def generate_output_filename(input_file, output):
    """Generate output filename based on input file or output flag."""
    if output:
        return os.path.splitext(output)[0]
    else:
        return normalize_filename(input_file)

def convert_pdf_to_markdown(input_file, output_file, verbose=False, force=False):
    """Convert PDF to Markdown using Replicate API."""
    verbose_print(f"Converting PDF to Markdown: {input_file}", verbose)

    base_name = generate_output_filename(input_file, output_file)
    final_output_file = f"{base_name}.md"

    if not force and check_existing_file(base_name):
        print(f"SKIPPING: File '{final_output_file}' already exists.", file=sys.stderr)
        return

    try:
        output = replicate.run(
            "cuuupid/marker:9c67051309f6d10ca139489f15fcb5ebc4866a3734af537c181fb13bc719d280",
            input={
                "document": input_file,
                "parallel_factor": 10
            }
        )

        if isinstance(output, dict) and 'markdown' in output:
            markdown_url = output['markdown']
            response = requests.get(markdown_url)
            response.raise_for_status()
            content = response.text

            with open(final_output_file, "w", encoding="utf-8") as f:
                f.write(content)

            verbose_print(f"Markdown saved as: {final_output_file}", verbose)
            print(f"{final_output_file}")
        else:
            print("Error: Unexpected output format from the API.", file=sys.stderr)
            sys.exit(1)

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
    convert_pdf_to_markdown(args.input, args.output, args.verbose, args.force)

if __name__ == "__main__":
    main()
