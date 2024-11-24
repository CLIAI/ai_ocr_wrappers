#!/usr/bin/env python3

"""
Educational example demonstrating PDF processing in Python.

This script illustrates different approaches to process PDF files using:
1. Python libraries (PyPDF2, pypdf) if available
2. External command-line tools (imagemagick, poppler-utils/pdftoppm) as fallback

Requirements:
* Uses command line flags for control
* -v|--verbose allows to turn extra logging (can be stacked: -vvv)
* Expects PDF filename as mandatory parameter
* Optional -f|--first and -l|--last page parameters
* Implements fallback mechanism between different libraries/tools
* Uses high-level API functions with specialized wrappers
"""

import argparse
import os
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

# Verbose levels constants
QUIET = 0
INFO = 1
VERBOSE = 2
VERBOSE2 = 3
DEBUG = 4

verbose_level = INFO  # Default verbose level

def vprint(level, *args, **kwargs):
    """Print message if current verbose level is >= specified level."""
    if verbose_level >= level:
        prefix = {
            INFO: "INFO",
            VERBOSE: "VERBOSE",
            VERBOSE2: "VERBOSE2",
            DEBUG: "DEBUG"
        }.get(level, "")
        print(f"{prefix}:", *args, file=sys.stderr, **kwargs)

def get_no_of_pages_pdf_with_PyPDF2(pdf_filename):
    """Try to get number of pages using PyPDF2 library."""
    vprint(DEBUG, f"Trying PyPDF2 for {pdf_filename}")
    try:
        import PyPDF2
        with open(pdf_filename, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            return reader.numPages
    except (ImportError, Exception) as e:
        vprint(DEBUG, f"PyPDF2 failed: {str(e)}")
        return None

def get_no_of_pages_pdf_with_pypdf(pdf_filename):
    """Try to get number of pages using pypdf library."""
    vprint(DEBUG, f"Trying pypdf for {pdf_filename}")
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_filename)
        return len(reader.pages)
    except (ImportError, Exception) as e:
        vprint(DEBUG, f"pypdf failed: {str(e)}")
        return None

def get_no_of_pages_pdf_with_pdfinfo(pdf_filename):
    """Try to get number of pages using pdfinfo command-line tool."""
    vprint(DEBUG, f"Trying pdfinfo for {pdf_filename}")
    try:
        result = subprocess.run(['pdfinfo', pdf_filename], 
                              capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'Pages:' in line:
                return int(line.split(':')[1].strip())
    except (subprocess.SubprocessError, ValueError, Exception) as e:
        vprint(DEBUG, f"pdfinfo failed: {str(e)}")
        return None

get_no_of_pages_pdf_ALL = [
    get_no_of_pages_pdf_with_PyPDF2,
    get_no_of_pages_pdf_with_pypdf,
    get_no_of_pages_pdf_with_pdfinfo
]

def get_no_of_pages_pdf(pdf_filename):
    """Get number of pages using all available methods."""
    vprint(DEBUG, f"Getting page count for {pdf_filename}")
    
    no_of_pages = None
    for method in get_no_of_pages_pdf_ALL:
        no_of_pages = method(pdf_filename)
        if no_of_pages is not None:
            break
    
    vprint(VERBOSE, f"Page count: {no_of_pages}")
    return no_of_pages

def pdf_page_as_png_image_with_imagemagick(pdf_filename, page_no, tmp_png, dpi=400):
    """Convert PDF page to PNG using ImageMagick."""
    vprint(DEBUG, f"Trying ImageMagick for page {page_no}")
    try:
        subprocess.run(['magick', '-density', str(dpi), f'{pdf_filename}[{page_no-1}]', tmp_png], check=True)
        return True
    except subprocess.SubprocessError as e:
        vprint(DEBUG, f"ImageMagick failed: {str(e)}")
        return False

def pdf_page_as_png_image_with_pdftoppm(pdf_filename, page_no, tmp_png, dpi=400):
    """Convert PDF page to PNG using pdftoppm."""
    vprint(DEBUG, f"Trying pdftoppm for page {page_no}")
    try:
        temp_prefix = tmp_png.rsplit('.', 1)[0]
        subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(page_no), '-l', str(page_no), '-png', pdf_filename, temp_prefix], check=True)
        # Rename output to match expected filename
        os.rename(f"{temp_prefix}-1.png", tmp_png)
        return True
    except subprocess.SubprocessError as e:
        vprint(DEBUG, f"pdftoppm failed: {str(e)}")
        return False

pdf_page_as_png_image_ALL = [
    pdf_page_as_png_image_with_imagemagick,
    pdf_page_as_png_image_with_pdftoppm
]

def pdf_page_as_png_image(pdf_filename, page_no, tmp_png, dpi=400, page_extractors=pdf_page_as_png_image_ALL):
    """Convert PDF page to PNG using available methods."""
    for method in page_extractors:
        if method(pdf_filename, page_no, tmp_png, dpi):
            return True
    return False

def filesize_of_each_page_image_export_as_pdf(pdf_filename, first_page=None, last_page=None, output_dir=None, dpi=400):
    """Process PDF file and print size of each page when converted to PNG."""
    no_of_pages = get_no_of_pages_pdf(pdf_filename)
    if not isinstance(no_of_pages, int):
        raise ValueError(f"Could not determine page count for {pdf_filename}")

    first_page = first_page or 1
    last_page = last_page or no_of_pages

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        tmp_png = tmp.name
        
    try:
        print(f"Size of PNG file for pages in {pdf_filename}:")
        for page_no in range(first_page, last_page + 1):
            if pdf_page_as_png_image(pdf_filename, page_no, tmp_png, dpi):
                size_kb = os.path.getsize(tmp_png) / 1024
                print(f"Page {page_no}: {size_kb:.1f}KB")
            else:
                print(f"Page {page_no}: conversion failed")
            if output_dir:
                output_file = os.path.join(output_dir, f"page-{page_no}.png")
                shutil.copy(tmp_png, output_file)
                vprint(INFO, f"Copied intermediate file to {output_file}")
    finally:
        if os.path.exists(tmp_png):
            os.unlink(tmp_png)

def main():
    parser = argparse.ArgumentParser(description='PDF page size analyzer')
    parser.add_argument('pdf_file', help='PDF file to process')
    parser.add_argument('-f', '--first', type=int, help='First page to process')
    parser.add_argument('-l', '--last', type=int, help='Last page to process')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Increase verbosity level')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress all diagnostic output')
    parser.add_argument('-O', '--output-dir', default=None, help='Output directory for intermediate files')
    parser.add_argument('-d', '--dpi', type=int, default=400, help='Resolution in dpi')

    args = parser.parse_args()

    global verbose_level
    verbose_level = QUIET if args.quiet else min(DEBUG, args.verbose + 1)

    if not os.path.isfile(args.pdf_file):
        print(f"Error: File {args.pdf_file} does not exist", file=sys.stderr)
        sys.exit(1)

    try:
        filesize_of_each_page_image_export_as_pdf(args.pdf_file, args.first, args.last, args.output_dir, args.dpi)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# This implementation includes all requested features and follows best practices:
# - Proper error handling and fallback mechanisms
# - Comprehensive logging with multiple verbosity levels
# - Clean temporary file management
# - Command-line argument parsing
# - Modular design with separate functions for different approaches
# - Detailed documentation and comments
# 
# To use it, you would need at least one of:
# - PyPDF2 or pypdf Python library
# - poppler-utils (for pdfinfo and pdftoppm)
# - ImageMagick
# 
# The script will automatically use whatever is available, falling back to alternatives if the preferred method fails.
# 
