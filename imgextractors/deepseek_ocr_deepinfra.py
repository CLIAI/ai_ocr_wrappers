#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "openai>=1.0.0",
#   "requests>=2.31.0",
# ]
# requires-python = ">=3.11"
# ///

"""
DeepSeek-OCR wrapper for DeepInfra API

This script provides a command-line interface to the DeepSeek-OCR model
hosted on DeepInfra using their OpenAI-compatible API. It supports various
OCR tasks including text extraction, markdown conversion, and figure parsing.

Usage:
    ./deepseek_ocr_deepinfra.py input_image.jpg
    ./deepseek_ocr_deepinfra.py --task "Parse Figure" chart.png
    ./deepseek_ocr_deepinfra.py --prompt "Extract all tables" document.jpg -o output.md
"""

import argparse
import os
import sys
import base64
from openai import OpenAI

def verbose_print(message, verbose=False):
    """Print message if verbose mode is enabled."""
    if verbose:
        print(message, file=sys.stderr)

def check_api_token(key_file=None):
    """Check if DEEPINFRA_API_TOKEN is set or load from key file."""
    if key_file:
        # Expand ~ to user home directory
        key_file = os.path.expanduser(key_file)
        if not os.path.exists(key_file):
            print(f"ERROR: Key file not found: {key_file}", file=sys.stderr)
            sys.exit(1)

        # Source the file and extract DEEPINFRA_API_TOKEN or DEEPINFRA_TOKEN
        try:
            with open(key_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('export '):
                        line = line[7:]  # Remove 'export '
                    if line.startswith('DEEPINFRA_API_TOKEN=') or line.startswith('DEEPINFRA_TOKEN='):
                        token = line.split('=', 1)[1].strip().strip('"').strip("'")
                        os.environ['DEEPINFRA_API_TOKEN'] = token
                        break
        except Exception as e:
            print(f"ERROR: Failed to read key file: {e}", file=sys.stderr)
            sys.exit(1)

    if "DEEPINFRA_API_TOKEN" not in os.environ and "DEEPINFRA_TOKEN" not in os.environ:
        print("ERROR: DEEPINFRA_API_TOKEN is not set", file=sys.stderr)
        print("Set it via environment variable or use --key-file option", file=sys.stderr)
        sys.exit(1)

    # Use either token
    if "DEEPINFRA_API_TOKEN" not in os.environ and "DEEPINFRA_TOKEN" in os.environ:
        os.environ['DEEPINFRA_API_TOKEN'] = os.environ['DEEPINFRA_TOKEN']

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

def encode_image_to_base64(file_path):
    """Encode the input image to base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def get_task_prompt(task_type, custom_prompt=None):
    """Generate prompt based on task type."""
    if custom_prompt:
        return custom_prompt

    prompts = {
        "Convert to Markdown": "<image>\n<|grounding|>Convert the document to markdown.",
        "Free OCR": "<image>\nFree OCR.",
        "Parse Figure": "<image>\nParse the figure.",
        "Extract Tables": "<image>\nExtract all tables from this document.",
        "Extract Formulas": "<image>\nExtract all mathematical formulas in LaTeX format.",
    }

    return prompts.get(task_type, "<image>\nFree OCR.")

def extract_with_deepseek_ocr(
    input_file,
    output_file,
    task_type="Convert to Markdown",
    custom_prompt=None,
    max_tokens=8192,
    temperature=0.0,
    verbose=False,
    force=False
):
    """Extract text/data from image using DeepSeek-OCR via DeepInfra API."""
    verbose_print(f"Processing image with DeepSeek-OCR: {input_file}", verbose)
    verbose_print(f"Task type: {task_type}", verbose)

    final_output_file = generate_output_filename(input_file, output_file, task_type)

    if not force and os.path.exists(final_output_file):
        print(f"SKIPPING: File '{final_output_file}' already exists.", file=sys.stderr)
        return

    try:
        # Initialize OpenAI client with DeepInfra endpoint
        api_token = os.environ.get('DEEPINFRA_API_TOKEN')
        client = OpenAI(
            api_key=api_token,
            base_url="https://api.deepinfra.com/v1/openai"
        )

        # Encode image
        base64_image = encode_image_to_base64(input_file)
        verbose_print(f"Encoded image to base64 ({len(base64_image)} chars)", verbose)

        # Determine image MIME type
        ext = os.path.splitext(input_file)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
        }
        mime_type = mime_types.get(ext, 'image/jpeg')

        # Get prompt
        prompt = get_task_prompt(task_type, custom_prompt)
        verbose_print(f"Using prompt: {prompt}", verbose)

        # Call the API
        verbose_print("Calling DeepInfra API...", verbose)
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-OCR",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }],
            max_tokens=max_tokens,
            temperature=temperature
        )

        verbose_print(f"API response received", verbose)

        # Extract content
        content = response.choices[0].message.content

        if verbose:
            verbose_print(f"Extracted {len(content)} characters", verbose)
            verbose_print(f"Tokens used: {response.usage.total_tokens} (prompt: {response.usage.prompt_tokens}, completion: {response.usage.completion_tokens})", verbose)

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
        description="Extract text/data from images using DeepSeek-OCR via DeepInfra API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert document to markdown (default)
  %(prog)s document.jpg

  # Parse a figure/chart
  %(prog)s --task "Parse Figure" chart.png

  # Free OCR
  %(prog)s --task "Free OCR" scan.png

  # Custom prompt
  %(prog)s --prompt "Extract all tables and format them in markdown" document.jpg

  # Use custom API key file
  %(prog)s --key-file ~/.env.deepinfra document.jpg

Task Types:
  - "Convert to Markdown" (default): Convert document to markdown format
  - "Free OCR": Extract text without specific formatting
  - "Parse Figure": Extract information from charts/figures
  - "Extract Tables": Extract tables from document
  - "Extract Formulas": Extract mathematical formulas

Note: DeepInfra uses OpenAI-compatible API, so responses follow OpenAI format.
      Rate limits: ~200 concurrent requests by default.
"""
    )

    parser.add_argument("input", help="Input image file (jpg, png, etc.)")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument(
        "-t", "--task",
        choices=["Convert to Markdown", "Free OCR", "Parse Figure", "Extract Tables", "Extract Formulas"],
        default="Convert to Markdown",
        help="Task type to perform (default: Convert to Markdown)"
    )
    parser.add_argument(
        "-p", "--prompt",
        help="Custom prompt (overrides task type)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=8192,
        help="Maximum tokens in response (default: 8192)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperature for generation (default: 0.0 for deterministic)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite existing files")
    parser.add_argument(
        "--key-file",
        help="Path to file containing DEEPINFRA_API_TOKEN (e.g., ~/.env.deepinfra)"
    )

    args = parser.parse_args()

    check_api_token(args.key_file)
    extract_with_deepseek_ocr(
        args.input,
        args.output,
        args.task,
        args.prompt,
        args.max_tokens,
        args.temperature,
        args.verbose,
        args.force
    )

if __name__ == "__main__":
    main()
