# ai ocr wrappers

## Long term vision.

`pdf_ocr_orchestrator` wrapper,
that will orchestrate whole pipeline
that uses variety of orchestrators and analyzers
in different ways and stages.

## Short term goal

Let's start by integrating: `nougat`, `marker`, and `pdftotext` and `pdftohtml`
tools and some LLM script combining outputs into one for better quality.

## Mid Term Goal

Utilized `pdftoimages in pipeline, combined with some vision models APIs
(like GPT-4V or similar)
for extracting information from images into text.

## PDF OCR data Extraction Intro.

PDF OCR is more complex then it looks like.

PDFs contain:
* tables
* formulas
* images
* charts

Understanding all of this and properly transcribing may require
big chunk of tooling.

Also different OCR analyzers or PDF extractors
may have different strenghts and weaknesses.

And later images/charts can be analyzed/transcribed
or textualised (e.g. using LaTeX, Marmaid, etc)
in many ways.

Therefore, let's keep

## Extractor Modules:

* `pdfextractors/` directory

Supported:

* None yet

To be supported:

* nougat - ML/AI OCR extractor specialised in Markdown+LaTeX formulas/tables
* marker - specialised for FAST extraction of simpler PDF documents
* `pdfimages` - images extractor
* `pdftotext`, `pdftohtml`

