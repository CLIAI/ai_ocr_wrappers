Title: vwtyler/ocr-pdf – Replicate

URL Source: https://replicate.com/vwtyler/ocr-pdf/api/schema

vwtyler/ocr-pdf – API reference
===============

======================================

### [vwtyler](https://replicate.com/vwtyler) / ocr-pdf

simple pdf to text from a url using tesseract

[Run with an API](https://replicate.com/vwtyler/ocr-pdf/api)

### If using via REST call directly:

Input Schema

```
{
  "type": "object",
  "title": "Input",
  "required": [
    "url"
  ],
  "properties": {
    "url": {
      "type": "string",
      "title": "Url",
      "x-order": 0,
      "description": "URL of the PDF to extract text from"
    }
  }
}
```

Output Schema

```
{
  "type": "string",
  "title": "Output"
}
```

### If using via replicate library

Then returned object is output object not json, and one needs
to follow API reference.
