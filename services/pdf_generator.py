from PIL import Image


def generate_pdf(image_path, pdf_path):

    image = Image.open(image_path)

    rgb_image = image.convert("RGB")


    rgb_image.save(
        pdf_path,
        "PDF",
        resolution=450.0
    )