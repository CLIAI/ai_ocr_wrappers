Title: cuuupid/marker – Replicate

URL Source: https://replicate.com/cuuupid/marker/api/schema

Markdown Content:
cuuupid/marker – API reference
===============

### Input Schema

```json
{
  "type": "object",
  "title": "Input",
  "properties": {
    "dpi": {
      "type": "integer",
      "title": "Dpi",
      "default": 400,
      "x-order": 4,
      "description": "The DPI to use for OCR."
    },
    "lang": {
      "enum": [
        "English",
        "Spanish",
        "Portuguese",
        "French",
        "German",
        "Russian"
      ],
      "type": "string",
      "title": "lang",
      "description": "Provide the language to use for OCR.",
      "default": "English",
      "x-order": 3
    },
    "document": {
      "type": "string",
      "title": "Document",
      "format": "uri",
      "x-order": 0,
      "description": "Provide your input file (PDF, EPUB, MOBI, XPS, FB2)."
    },
    "max_pages": {
      "type": "integer",
      "title": "Max Pages",
      "x-order": 1,
      "description": "Provide the maximum number of pages to parse."
    },
    "enable_editor": {
      "type": "boolean",
      "title": "Enable Editor",
      "default": false,
      "x-order": 5,
      "description": "Enable the editor model."
    },
    "parallel_factor": {
      "type": "integer",
      "title": "Parallel Factor",
      "default": 1,
      "x-order": 2,
      "description": "Provide the parallel factor to use for OCR."
    }
  }
}
```

### Output Schema

```json
{
  "type": "object",
  "title": "ModelOutput",
  "required": [
    "markdown",
    "metadata"
  ],
  "properties": {
    "markdown": {
      "type": "string",
      "title": "Markdown",
      "format": "uri"
    },
    "metadata": {
      "type": "string",
      "title": "Metadata"
    }
  }
}
```
