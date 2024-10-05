#!/usr/bin/env python3

import argparse
import csv
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request


def verbose_print(message, verbose):
    if verbose:
        print(f"> {message}", file=sys.stderr)

def get_domain(url):
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc
    return domain

def get_topic(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip('/').split('/')
    return '_'.join(path)

def guess_filename(url):
    domain = get_domain(url)
    topic = get_topic(url)
    return f"{domain}/{domain}_{topic}.md"

def load_url2path_csv(csv_db='url2path.csv', verbose=False):
    url2path = {}
    verbose_print(f"Loading {csv_db} URLs to paths mapping", verbose)
    try:
        with open(csv_db, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                url2path[row[0]] = row[1]
    except Exception as e:
        verbose_print(f"Error loading CSV: {e}", verbose)
    return url2path

def load_url2path_csv_robust(csv_db='url2path.csv', verbose=False):
    try:
        url2path = load_url2path_csv(csv_db, verbose)
    except Exception:
        url2path = {}
    return url2path

def save_url2path_csv(url2path, csv_db='url2path.csv', verbose=False):
    verbose_print(f"Saving URL to path mapping to {csv_db}", verbose)
    try:
        with open(csv_db, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['url', 'path'])  # Write the header
            for url, path in url2path.items():
                writer.writerow([url, path])
    except Exception as e:
        verbose_print(f"Error saving CSV: {e}", verbose)

def add_to_url2path_csv(url, path, csv_db='url2path.csv', verbose=False):
    verbose_print(f"Adding record to {csv_db}", verbose)
    try:
        with open(csv_db, 'a') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['url', 'path'])  # Write the header if file is empty
            writer.writerow([url, path])
    except Exception as e:
        verbose_print(f"Error adding record to CSV: {e}", verbose)

def get_path_from_mapping_or_default(url, default_path, url2path=None, verbose=False):
    if url2path is None:
        url2path = load_url2path_csv_robust()
    verbose_print(f"Getting path for {url}", verbose)
    try:
        return url2path.get(url, default_path)
    except Exception as e:
        verbose_print(f"Path not found (error: {e}), using default path.", verbose)
        return default_path

def download_markdown(url, api_key=None, verbose=False):
    # Ensure the URL is correctly formatted
    if url.startswith("http"):
        req_url = f"https://r.jina.ai/{url}"
    else:
        verbose_print(f"ERROR: Url does not start with http(s) : '{url}'", True) # always be verbose with URL error
        sys.exit(1)

    verbose_print(f"Sending Request({req_url}) ...", verbose)
    
    req = urllib.request.Request(req_url)
   
    #req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    req.add_header("User-Agent", "curl/8.8.0")
     
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")
    
    try:
        with urllib.request.urlopen(req) as response:
            response_decoded = response.read().decode('utf-8')
            verbose_print(f"Received response (decode('utf-8')='{response_decoded}')", verbose)
            return response_decoded
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
    
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Download and save webpage as Markdown")
    parser.add_argument("url", nargs="?", help="URL to download")
    parser.add_argument("path", nargs="?", help="Path to save the file")
    parser.add_argument("-b", "--batch-csv", help="CSV file with url,path columns to process in batch")
    parser.add_argument("-y", "--no-interactive", action="store_true", help="Non-interactive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-w", "--overwrite", action="store_true", default=False, help="Enforce overwrite without asking in interactive mode")
    args = parser.parse_args()


    if not args.url and not args.batch_csv:
        print(f"Usage: {sys.argv[0]} [path...] URL [--no-interactive|-y] [-v|--verbose]")
        sys.exit(1)

    api_key = os.environ.get("JINAAI_API_KEY")

    if args.batch_csv:
        url2path = load_url2path_csv(args.batch_csv)
        for url, filename in url2path.items():
            content = download_markdown(url, api_key, args.verbose)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            written_characters = 0 
            with open(filename, 'w', encoding='utf-8') as f:
                written_characters += f.write(content)    
            if os.path.exists(filename) and written_characters > 0:
                verbose_print(f"File saved as {filename}", args.verbose)
                add_to_url2path_csv(args.url, filename, 'url2path.csv', args.verbose)
            else:
                verbose_print("ERROR: File was not saved successfully.", True) # This error case always display verbose
        return

    content = download_markdown(args.url, api_key, args.verbose)

    if args.path:
        filename = args.path
    else:
        filename = guess_filename(args.url)
        filename = get_path_from_mapping_or_default(url=args.url, default_path=filename)
        if not args.no_interactive:
            print(f"Guessed path:\n{filename}")
            user_input = input("Provide path [empty enter uses guessed path]:\n")
            if user_input:
                filename = user_input
    
    overwrite_flag = args.overwrite
    while os.path.exists(filename) and not overwrite_flag:
        print(f"Path already exists:\n{filename}")
        user_input = input("Provide other path OR 'overwrite'/'yes' to overwrite OR 'no'/'exit' to cancel")
        if user_input.lower() in ['overwrite', 'yes']:
            overwrite_flag = True
        elif user_input.lower() in ['no', 'exit']:
            break
        else:
            filename = user_input

    os.makedirs(os.path.dirname(filename), exist_ok=True)
   
    written_characters = 0 
    with open(filename, 'w', encoding='utf-8') as f:
        written_characters += f.write(content)
    
    if os.path.exists(filename) and written_characters > 0:
        verbose_print(f"File saved as {filename}", args.verbose)
        add_to_url2path_csv(args.url, filename, 'url2path.csv', args.verbose)
    else:
        verbose_print("ERROR: File was not saved successfully.", True) # This error case always display verbose

    # Save copy of raw input that was downloaded,
    # so later can be checked with diff, if manual modifications
    # with $EDITor were applied:
    raw_filename = os.path.join("raw", filename)
    os.makedirs(os.path.dirname(raw_filename), exist_ok=True)
    with open(raw_filename, 'w', encoding='utf-8') as f:
        f.write(content)

    if not args.no_interactive:
        editor = os.environ.get("EDITOR", "vim")
        subprocess.call([editor, filename])

if __name__ == "__main__":
    main()

# This script: (TODO - update those notes about script)
# 
# 1. Uses only standard Python libraries for maximum portability.
# 2. Includes a shebang for Python 3.
# 3. Handles command-line arguments as specified.
# 4. Implements the logic for guessing filenames based on the URL.
# 5. Downloads content using the Jina AI API.
# 6. Supports both interactive and non-interactive modes.
# 7. Opens the downloaded file in an editor if in interactive mode.
# 8. Includes verbose output when requested.
# 9. Exits with status code 1 if the download fails.
# 
# To use this script, save it to a file (e.g., `download_markdown.py`), make it executable (`chmod +x download_markdown.py`), and run it from the command line.

