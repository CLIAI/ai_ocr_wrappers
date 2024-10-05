Title: cudanexus/nougat – Replicate

URL Source: https://replicate.com/cudanexus/nougat/api/schema

Markdown Content:
cudanexus/nougat – API reference
===============

### Input

```json
{
  "type": "object",
  "title": "Input",
  "required": [
    "pdf_file"
  ],
  "properties": {
    "pdf_file": {
      "type": "string",
      "title": "Pdf File",
      "format": "uri",
      "x-order": 0,
      "description": "input the pdf"
    }
  }
}
```

### Output

```json
{
  "type": "string",
  "title": "Output",
  "format": "uri"
}
```
