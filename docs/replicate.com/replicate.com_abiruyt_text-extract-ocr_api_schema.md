Title: abiruyt/text-extract-ocr – Replicate

URL Source: https://replicate.com/abiruyt/text-extract-ocr/api/schema

Markdown Content:
abiruyt/text-extract-ocr – API reference
===============

## When making REST request here is schema for abiruyt/text-extract-ocr – API reference

## Input schema

TableJSON

```json
{
  "type": "object",
  "title": "Input",
  "required": [
    "image"
  ],
  "properties": {
    "image": {
      "type": "string",
      "title": "Image",
      "format": "uri",
      "x-order": 0,
      "description": "Image to process"
    }
  }
}
```

Copy

## Output schema

TableJSON

```json
{
  "type": "string",
  "title": "Output"
}
```
