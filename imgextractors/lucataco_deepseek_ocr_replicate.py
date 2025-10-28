#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "replicate>=0.25.0",
#   "requests>=2.31.0",
# ]
# requires-python = ">=3.11"
# ///

"""
DeepSeek-OCR wrapper for Replicate API (lucataco/deepseek-ocr)

This script provides a command-line interface to the DeepSeek-OCR model
hosted on Replicate. It supports various OCR tasks including text extraction,
markdown conversion, figure parsing, and object localization.

Usage:
    ./lucataco_deepseek_ocr_replicate.py input_image.jpg
    ./lucataco_deepseek_ocr_replicate.py --task-type "Parse Figure" chart.png
    ./lucataco_deepseek_ocr_replicate.py --resolution Large document.jpg -o output.md
"""

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

def check_api_token(key_file=None):
    """Check if REPLICATE_API_TOKEN is set or load from key file."""
    if key_file:
        # Expand ~ to user home directory
        key_file = os.path.expanduser(key_file)
        if not os.path.exists(key_file):
            print(f"ERROR: Key file not found: {key_file}", file=sys.stderr)
            sys.exit(1)

        # Source the file and extract REPLICATE_API_TOKEN
        try:
            with open(key_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('export '):
                        line = line[7:]  # Remove 'export '
                    if line.startswith('REPLICATE_API_TOKEN='):
                        token = line.split('=', 1)[1].strip().strip('"').strip("'")
                        os.environ['REPLICATE_API_TOKEN'] = token
                        break
        except Exception as e:
            print(f"ERROR: Failed to read key file: {e}", file=sys.stderr)
            sys.exit(1)

    if "REPLICATE_API_TOKEN" not in os.environ:
        print("ERROR: REPLICATE_API_TOKEN is not set", file=sys.stderr)
        print("Set it via environment variable or use --key-file option", file=sys.stderr)
        sys.exit(1)

def normalize_filename(filename, max_length=64):
    """Normalize filename to a valid format."""
    base = os.path.splitext(os.path.basename(filename))[0]
    normalized = ''.join(c.lower() if c.isalnum() else '_' for c in base)
    return normalized[:max_length]

def generate_output_filename(input_filename, output_filename, task_type):
    """Generate output filename based on input file, output flag, and task type."""
    if output_filename:
        return output_filename
    else:
        # Determine extension based on task type
        if "markdown" in task_type.lower():
            ext = ".md"
        else:
            ext = ".txt"
        return normalize_filename(input_filename) + ext

def encode_file_to_base64(file_path):
    """Encode the input file to base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def truncate_long_string(data, max_length=1024):
    """Truncate long strings for verbose output."""
    if len(data) > max_length:
        return f"{data[:64]} (...) {data[-64:]}"
    return data

def extract_with_deepseek_ocr(
    input_file,
    output_file,
    task_type="Convert to Markdown",
    resolution_size="Base",
    verbose=False,
    force=False
):
    """Extract text/data from image using DeepSeek-OCR via Replicate API."""
    verbose_print(f"Processing image with DeepSeek-OCR: {input_file}", verbose)
    verbose_print(f"Task type: {task_type}", verbose)
    verbose_print(f"Resolution: {resolution_size}", verbose)

    final_output_file = generate_output_filename(input_file, output_file, task_type)

    if not force and os.path.exists(final_output_file):
        print(f"SKIPPING: File '{final_output_file}' already exists.", file=sys.stderr)
        return

    try:
        # Read and prepare the image
        with open(input_file, "rb") as f:
            image_data = f.read()

        verbose_print(f"Read {len(image_data)} bytes from {input_file}", verbose)

        # Prepare the input for the API
        api_input = {
            "image": open(input_file, "rb"),
            "task_type": task_type,
            "resolution_size": resolution_size
        }
        verbose_print(f"API input prepared with task_type={task_type}, resolution_size={resolution_size}", verbose)

        # Call the API
        verbose_print("Calling Replicate API...", verbose)
        output = replicate.run(
            "lucataco/deepseek-ocr:deedb3f2ecdf38e90c79e79befd926ba8e95077cfef92ffec06f2f3494f1ce82",
            input=api_input
        )
        verbose_print(f"API output received: {type(output)}", verbose)

        # Handle different output formats
        if isinstance(output, str):
            # Direct string output
            content = output
            verbose_print(f"Got string output: {truncate_long_string(content)}", verbose)
        elif isinstance(output, list) and len(output) > 0:
            # List of strings - join them
            content = '\n'.join(str(item) for item in output)
            verbose_print(f"Got list output with {len(output)} items", verbose)
        else:
            print(f"Error: Unexpected output format: {type(output)}", file=sys.stderr)
            print(f"Output: {output}", file=sys.stderr)
            sys.exit(1)

        # Write output to file
        with open(final_output_file, "w", encoding="utf-8") as f:
            f.write(content)

        verbose_print(f"Output saved as: {final_output_file}", verbose)
        print(f"{final_output_file}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        if verbose:
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Extract text/data from images using DeepSeek-OCR via Replicate API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert document to markdown (default)
  %(prog)s document.jpg

  # Parse a figure/chart
  %(prog)s --task-type "Parse Figure" chart.png

  # Free OCR with high resolution
  %(prog)s --task-type "Free OCR" --resolution Large scan.png

  # Use custom API key file
  %(prog)s --key-file ~/.env.replicate document.jpg

Task Types:
  - "Convert to Markdown" (default): Convert document to markdown format
  - "Free OCR": Extract text without specific formatting
  - "Parse Figure": Extract information from charts/figures
  - "Locate Object by Reference": Find specific objects in image

Resolution Sizes:
  - Tiny (512x512): 64 tokens, fastest
  - Small (640x640): 100 tokens, fast
  - Base (1024x1024): 256 tokens, balanced (default)
  - Large (1280x1280): 400 tokens, best quality
  - Gundam: Dynamic resolution for complex documents
"""
    )

    parser.add_argument("input", help="Input image file (jpg, png, etc.)")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument(
        "-t", "--task-type",
        choices=["Convert to Markdown", "Free OCR", "Parse Figure", "Locate Object by Reference"],
        default="Convert to Markdown",
        help="Task type to perform (default: Convert to Markdown)"
    )
    parser.add_argument(
        "-r", "--resolution",
        choices=["Tiny", "Small", "Base", "Large", "Gundam"],
        default="Base",
        help="Resolution size (default: Base)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite existing files")
    parser.add_argument(
        "--key-file",
        help="Path to file containing REPLICATE_API_TOKEN (e.g., ~/.env.replicate)"
    )

    args = parser.parse_args()

    check_api_token(args.key_file)
    extract_with_deepseek_ocr(
        args.input,
        args.output,
        args.task_type,
        args.resolution,
        args.verbose,
        args.force
    )

if __name__ == "__main__":
    main()
