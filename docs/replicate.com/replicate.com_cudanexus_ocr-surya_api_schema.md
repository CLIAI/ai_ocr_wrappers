Title: cudanexus/ocr-surya – Replicate

URL Source: https://replicate.com/cudanexus/ocr-surya/api/schema

Markdown Content:
cudanexus/ocr-surya – API reference
===============

## When calling cudanexus/ocr-surya directly REST request, below schemas

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
      "description": "Upload PDF or Image"
    },
    "action": {
      "enum": [
        "Run Text Detection",
        "Run OCR"
      ],
      "type": "string",
      "title": "action",
      "description": "Action",
      "default": "Run Text Detection",
      "x-order": 4
    },
    "page_number": {
      "type": "integer",
      "title": "Page Number",
      "default": 1,
      "x-order": 1,
      "description": "Page Number"
    },
    "languages_input": {
      "type": "string",
      "title": "Languages Input",
      "default": "English",
      "x-order": 3,
      "description": "Languages (comma-separated list)"
    },
    "languages_choices": {
      "enum": [
        "Afrikaans",
        "Albanian",
        "Amharic",
        "Arabic",
        "Armenian",
        "Assamese",
        "Azerbaijani",
        "Basque",
        "Belarusian",
        "Bengali",
        "Bosnian",
        "Breton",
        "Bulgarian",
        "Burmese",
        "Catalan",
        "Chinese",
        "Croatian",
        "Czech",
        "Danish",
        "Dutch",
        "English",
        "Esperanto",
        "Estonian",
        "Finnish",
        "French",
        "Galician",
        "Georgian",
        "German",
        "Greek",
        "Gujarati",
        "Hausa",
        "Hebrew",
        "Hindi",
        "Hungarian",
        "Icelandic",
        "Indonesian",
        "Irish",
        "Italian",
        "Japanese",
        "Javanese",
        "Kannada",
        "Kazakh",
        "Khmer",
        "Korean",
        "Kurdish",
        "Kyrgyz",
        "Lao",
        "Latin",
        "Latvian",
        "Lithuanian",
        "Macedonian",
        "Malagasy",
        "Malay",
        "Malayalam",
        "Marathi",
        "Mongolian",
        "Nepali",
        "Norwegian",
        "Oriya",
        "Oromo",
        "Pashto",
        "Persian",
        "Polish",
        "Portuguese",
        "Punjabi",
        "Romanian",
        "Russian",
        "Sanskrit",
        "Scottish Gaelic",
        "Serbian",
        "Sindhi",
        "Sinhala",
        "Slovak",
        "Slovenian",
        "Somali",
        "Spanish",
        "Sundanese",
        "Swahili",
        "Swedish",
        "Tagalog",
        "Tamil",
        "Telugu",
        "Thai",
        "Turkish",
        "Ukrainian",
        "Urdu",
        "Uyghur",
        "Uzbek",
        "Vietnamese",
        "Welsh",
        "Western Frisian",
        "Xhosa",
        "Yiddish"
      ],
      "type": "string",
      "title": "languages_choices",
      "description": "Languages",
      "default": "English",
      "x-order": 2
    }
  }
}
```

Copy

## Output schema

TableJSON

```json
{
  "type": "object",
  "title": "Output",
  "required": [
    "image"
  ],
  "properties": {
    "image": {
      "type": "string",
      "title": "Image",
      "format": "uri"
    },
    "Status": {
      "type": "string",
      "title": "Status"
    },
    "text_file": {
      "type": "string",
      "title": "Text File",
      "format": "uri"
    }
  }
}
```
