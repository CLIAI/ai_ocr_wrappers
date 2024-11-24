#!/bin/bash

# Function to display usage information
display_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Run test suites with different scopes"
    echo
    echo "OPTIONS:"
    echo "  -l, --local-only     Run only local tests (no external services)"
    echo "  -c, --with-rest      Include tests against REST APIs (may incur costs)"
    echo "  --with-replicate, --with-openai Include tests against Replicate, OpenAI... API (may incur costs)"
    echo "  --with-ollama Include tests against Ollama Local API"
    echo "  -h, --help           Display this help message"
    echo
    echo "WARNING: Running tests against external APIs (Replicate, REST) may incur costs."
    echo "You must explicitly enable these tests using the appropriate flags."
}

# Check if no parameters provided
if [ $# -eq 0 ]; then
    echo "Error: No parameters provided"
    echo
    display_usage
    exit 1
fi

# Initialize flags
LOCAL_TESTS=false
REPLICATE_TESTS=false
OPENAI_TESTS=false
OLLAMA_TESTS=false
REST_TESTS=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--local-only)
            LOCAL_TESTS=true
            shift
            ;;
        --with-ollama)
            OLLAMA_TESTS=true
            shift
            ;;
        --with-replicate)
            REPLICATE_TESTS=true
            shift
            ;;
        --with-openai)
            OPENAI_TESTS=true
            shift
            ;;
        -c|--with-rest)
            REST_TESTS=true
            shift
            ;;
        -h|--help)
            display_usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option $1"
            display_usage
            exit 1
            ;;
    esac
done

if [ -n "$USETMPDIR" ]; then
  tmpdir="$USETMPDIR"
  echo "USING_TMPDIR:$$USETMPDIR=$tmpdir"
else
  tmpdir="$(mktemp -d)"
fi

function cleanup() { 
  # keep files if there is /tmp/KEEPTMP marker file
  if [ ! -f /tmp/KEEPTMP ]; then
    rm -r "$tmpdir"
  else
    INFO "Detected /tmp/KEEPTMP file, keeping temporary files in $tmpdir"
  fi
}

trap cleanup EXIT HUP INT QUIT PIPE TERM

# Function to check if the current directory name matches the provided parameter
function is_cwd_name() {
    if [[ "$(basename "$PWD")" == "$1" ]]; then
        return 0
    else
        return 1
    fi
}

# Change directory if current directory name matches certain parameters
if is_cwd_name "integration_on_production" ; then cd .. ; fi
if is_cwd_name "tests" ; then cd .. ; fi

# Function to assert that a provided path exists
function assert_path() {
    if [[ ! -e $1 ]]; then
        echo "ERROR:PATH_NOT_EXISTS:$1" >&2
    fi
}

# Assert certain paths exist
assert_path testdata
assert_path pdfextractors/cudanexus_nougat_replicate.py
assert_path pdfextractors/cuuupid_marker_replicate.py
assert_path imgextractors/cudanexus_ocr_surya_replicate.py

# Functions to log information
function INFO() {
    echo "INFO:$@"
}

function ERROR() {
    echo "ERROR:$@" >&2
}

# Function to check if all provided words are in a given file
function are_all_contained() {
    local filename="$1"
    shift 1
    local missing_words=0
    local found_words=0
    while (( "$#" )); do
        local word="$1"
        #echo "DEB:CHECKING:$word" >&2
        shift
        if ! grep -i -q "$word" "$filename"; then
            #echo "FAILED:MISSING_WORD:FILENAME:$filename:WORD:$word" >&2
            echo "FAILED:MISSING_WORD:$word" >&2
            missing_words=$((missing_words + 1))
        else
            found_words=$((found_words + 1))
        fi
    done
    local total_words=$((missing_words + found_words))
    echo "INFO:WORDS_FOUND/TOTAL:${found_words}/${total_words}" >&2
    return $missing_words
}

# Function to check if words are contained in a file and log the result
function check_are_words_contained() {
    local testname="$1"
    shift 1
    if are_all_contained "$@"; then
        INFO "OK:$testname"
    else
        INFO "FAILED:NOT_ALL_WORDS_CONTAINED:$testname"
    fi
}

## ##### Shared parameters for all tests ####

TESTPDF000='testdata/v00/test_latex_page_with_table.pdf'
function check_testpdf000_ocr() {
local extractor="$1"
local ocrfile="$2"
check_are_words_contained "000:$extractor" "$ocrfile" Example Document John Doe Introduction Lorem ipsum nunc Column Row Data Table Conclusion generate Markdown YAML PDF A4 pandoc xelatex
}

## ##### Run the tests based on flags ##### ##

# REPLICATE TESTS #########################################
if $REPLICATE_TESTS || $REST_TESTS; then

INFO "# Running Replicate API tests..."

function INFOEXTRACTOR() {
    local status="$1"
    echo
    INFO "${status}:EXTRACTOR:$@"
}

EXTRACTOR='cudanexus_nougat_replicate'
OUTPUTFILE="$tmpdir/$EXTRACTOR.out"
if [ -f "$OUTPUTFILE" ]; then
INFOEXTRACTOR SKIPPING "$EXTRACTOR:OUTPUTFILE_EXISTS:$OUTPUTFILE"
else
INFOEXTRACTOR TESTING "$EXTRACTOR"
(set -x
pdfextractors/cudanexus_nougat_replicate.py --verbose -o "$OUTPUTFILE" "$TESTPDF000"
)
fi
check_testpdf000_ocr "$EXTRACTOR" "$OUTPUTFILE"

EXTRACTOR='cuuupid_marker_replicate'
OUTPUTFILE="$tmpdir/$EXTRACTOR.out"
if [ -f "$OUTPUTFILE" ]; then
INFOEXTRACTOR SKIPPING "$EXTRACTOR:OUTPUTFILE_EXISTS:$OUTPUTFILE"
else
INFOEXTRACTOR TESTING "$EXTRACTOR"
(set -x
pdfextractors/cuuupid_marker_replicate.py --verbose -o "$OUTPUTFILE" --lang English --dpi 400 --max-pages 1 --parallel-factor 4 "$TESTPDF000"
)
fi
check_testpdf000_ocr "$EXTRACTOR" "$OUTPUTFILE"

# IMAGE2TXT TESTS #########################################
EXTRACTOR='cudanexus_ocr_surya_replicate'
OUTPUTFILE1="$tmpdir/${EXTRACTOR}_1.out"
OUTPUTFILE2="$tmpdir/${EXTRACTOR}_2.out"
FINAL_OUTPUTFILE="$tmpdir/${EXTRACTOR}_final.out"

if [ -f "$FINAL_OUTPUTFILE" ]; then
INFOEXTRACTOR SKIPPING "$EXTRACTOR:OUTPUTFILE_EXISTS:$FINAL_OUTPUTFILE"
else
INFOEXTRACTOR TESTING "$EXTRACTOR"
(set -x
imgextractors/cudanexus_ocr_surya_replicate.py --verbose -o "$OUTPUTFILE1" testdata/v00/test_latex_page_with_table-1.png
imgextractors/cudanexus_ocr_surya_replicate.py --verbose -o "$OUTPUTFILE2" testdata/v00/test_latex_page_with_table-2.png
cat "$OUTPUTFILE1" "$OUTPUTFILE2" > "$FINAL_OUTPUTFILE"
)
fi
check_testpdf000_ocr "$EXTRACTOR" "$FINAL_OUTPUTFILE"

fi
