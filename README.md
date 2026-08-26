# Smart A4 PDF Formatter

A lightweight document-processing utility that turns scanned or image-based pages into cleaner, print-ready A4 PDF batches.

## What It Does

- Enhances scanned images
- Removes excess whitespace
- Automatically crops page content
- Corrects page rotation
- Combines multiple pages into printable A4 layouts
- Generates batch PDF output
- Supports ZIP export

## Technology

- FastAPI
- OpenCV
- Pillow
- NumPy
- HTML/CSS/JavaScript

## Run Locally

### Requirements

- Python 3.10+
- `pip`

### Install

```bash
pip install -r requirements.txt
```

### Start

```bash
uvicorn main:app --reload
```

Open the local URL printed by Uvicorn in your browser.

## Processing Flow

1. Provide the source pages or images.
2. Enhance and normalize the input.
3. Detect and crop page content.
4. Correct rotation where required.
5. Compose the pages into A4 output.
6. Export the resulting PDF or batch archive.

## Project Status

Active utility project. Processing behavior depends on the input document quality and image characteristics.

## License

No repository-wide open-source license is currently declared. Add an explicit license before redistributing the project as open source.
