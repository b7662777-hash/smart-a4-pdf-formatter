# Smart A4 PDF Formatter

A FastAPI-based document processing tool that:
- Enhances scanned images
- Removes whitespace
- Auto-crops pages
- Fixes rotation
- Combines 4 pages into printable A4 PDFs
- Generates batch PDFs automatically

## Tech Stack

- FastAPI
- OpenCV
- Pillow
- NumPy
- HTML/CSS/JavaScript

## Features

- Smart image enhancement
- Adaptive cropping
- Multi-page batching
- ZIP export
- High-quality PDF generation

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload