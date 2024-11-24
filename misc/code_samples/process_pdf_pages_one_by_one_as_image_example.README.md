Example usage:

```
$ python3 process_pdf_pages_one_by_one_as_image_example.py --dpi 400 -O /tmp/tmpout -vvv ../../testdata/v00/test_latex_page_with_table.pdf
DEBUG: Getting page count for ../../testdata/v00/test_latex_page_with_table.pdf
DEBUG: Trying PyPDF2 for ../../testdata/v00/test_latex_page_with_table.pdf
DEBUG: PyPDF2 failed: No module named 'PyPDF2'
DEBUG: Trying pypdf for ../../testdata/v00/test_latex_page_with_table.pdf
VERBOSE: Page count: 2
Size of PNG file for pages in ../../testdata/v00/test_latex_page_with_table.pdf:
DEBUG: Trying ImageMagick for page 1
Page 1: 213.2KB
INFO: Copied intermediate file to /tmp/tmpout/page-1.png
DEBUG: Trying ImageMagick for page 2
Page 2: 61.4KB
INFO: Copied intermediate file to /tmp/tmpout/page-2.png
```
