# Smart A4 PDF Formatter

Turn uploaded images into compact A4 PDF batches using a local FastAPI application.

> **Development utility:** use locally with trusted images and one upload at a time. Output paths are currently shared between requests; this is not yet suitable for public multi-user deployment.

## What it does

| Stage | Current behavior |
| --- | --- |
| Input | Accepts multiple uploaded images through the web interface or `POST /upload` |
| Rotation | Calls the rotation-correction service |
| Enhancement | Calls the image-enhancement service |
| Cropping | Calls the content-cropping service |
| Layout | Groups processed images in batches of up to four and creates an A4 layout for each group |
| Export | Saves each layout as a separate PDF and returns `all_pdfs.zip` |

This is an image-to-PDF layout utility, not a general PDF editor or PDF merger. Results depend on image quality and the processing services.

## Quick start

Use Python 3.10+ with a virtual environment. Dependency compatibility must be checked on your platform; the pinned dependencies are in `requirements.txt`.

```bash
git clone https://github.com/b7662777-hash/smart-a4-pdf-formatter.git
cd smart-a4-pdf-formatter
python -m venv .venv
```

Activate the environment:

```bash
# Linux / macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Install and start from the repository root:

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open `http://127.0.0.1:8000`. Select images, submit the upload, and download the ZIP. Development reload is not a production deployment configuration.

## API example

```bash
curl --fail --show-error \
  -F "files=@scan-1.jpg" \
  -F "files=@scan-2.jpg" \
  http://127.0.0.1:8000/upload \
  --output all_pdfs.zip
```

Replace the sample paths with images you own or are authorized to process. The endpoint returns a ZIP containing PDFs, not a single merged document.

## Project structure

```text
main.py          FastAPI routes and batch orchestration
services/        Rotation, enhancement, cropping, and layout helpers
templates/       Web interface templates
static/          Frontend assets
requirements.txt Pinned application dependencies
```

Runtime processing uses `uploads/`, `processed/`, and `output/`. Run from the repository root so relative template, asset, and output paths resolve correctly.

## Known limitations and privacy

| Area | Limitation |
| --- | --- |
| Concurrent requests | Layouts, PDFs, and the ZIP use shared filenames; overlapping requests can overwrite results |
| Input validation | The upload route does not currently enforce explicit file-count, byte-size, or decoded-image limits |
| Error handling | Processing exceptions do not have a complete request-scoped recovery/cleanup path |
| Retention | Cropped images and generated outputs can remain on disk; do not assume automatic deletion |
| Input formats | General PDF input and merging are not implemented by the upload route |
| Verification | Build compatibility and runtime behavior must be tested locally; this README does not claim passing CI |

Do not expose the server publicly or process confidential documents until request isolation, validation, cleanup, and deployment controls have been reviewed. Local processing alone does not establish a privacy guarantee.

## Verification and development priorities

For a manual smoke test, process a single image and then five images in separate requests. Confirm that the first ZIP contains one PDF and the second contains two PDFs. Open the PDFs and inspect crop, rotation, readability, and layout. Manual checks do not replace automated tests.

| Priority | Next improvement |
| --- | --- |
| 1 | Add characterization tests for existing grouping and ZIP behavior |
| 2 | Introduce request-scoped work directories without changing the download contract |
| 3 | Add deterministic cleanup after response delivery and on processing failure |
| 4 | Add input limits and malformed-image tests |
| 5 | Add reproducible CI and documented deployment checks |

Keep changes focused and preserve the existing `POST /upload` ZIP-download contract unless a versioned API change is intentional.

## License

No repository-wide open-source license is currently declared. Public source availability does not grant unrestricted redistribution rights. An explicit license requires the maintainer's decision; this documentation update does not add one.
