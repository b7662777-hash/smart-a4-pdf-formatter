from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import List

from services.rotation import fix_rotation
from services.enhancer import enhance_image
from services.cropper import crop_image
from services.layout import create_a4_layout

from PIL import Image

import shutil
import os
import uuid
import zipfile


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)



templates = Jinja2Templates(
    directory="templates"
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/upload")
def upload_images(
    files: List[UploadFile] = File(...)
):

    if len(files) < 1:

        return {
            "error": "Upload at least 1 image"
        }


    processed_images = []


    for file in files:

        unique_name = (
            str(uuid.uuid4()) + ".jpg"
        )

        temp_path = (
            f"uploads/temp_{unique_name}"
        )

        corrected_path = (
            f"processed/corrected_{unique_name}"
        )

        enhanced_path = (
            f"processed/enhanced_{unique_name}"
        )

        cropped_path = (
            f"processed/cropped_{unique_name}"
        )


        with open(temp_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        fix_rotation(
            temp_path,
            corrected_path
        )


        enhance_image(
            corrected_path,
            enhanced_path
        )


        crop_image(
            enhanced_path,
            cropped_path
        )

        processed_images.append(
            cropped_path
        )



        if os.path.exists(temp_path):
            os.remove(temp_path)

        if os.path.exists(corrected_path):
            os.remove(corrected_path)

        if os.path.exists(enhanced_path):
            os.remove(enhanced_path)


    groups = [

        processed_images[i:i+4]

        for i in range(
            0,
            len(processed_images),
            4
        )

    ]


    generated_pdfs = []


    for index, group in enumerate(groups):

        page_path = (
            f"output/page_{index + 1}.jpg"
        )

        create_a4_layout(
            group,
            page_path
        )


        pdf_path = (
            f"output/pdf_{index + 1}.pdf"
        )


        image = Image.open(
            page_path
        ).convert("RGB")


        image.save(
            pdf_path,
            "PDF",
            resolution=300.0
        )


        generated_pdfs.append(
            pdf_path
        )


    zip_path = (
        "output/all_pdfs.zip"
    )


    with zipfile.ZipFile(
        zip_path,
        "w"
    ) as zipf:

        for pdf in generated_pdfs:

            zipf.write(
                pdf,
                arcname=os.path.basename(pdf)
            )


    return FileResponse(

        path=zip_path,

        media_type="application/zip",

        filename="all_pdfs.zip"

    )