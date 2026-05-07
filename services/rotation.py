from PIL import Image
from PIL import ImageOps


def fix_rotation(input_path, output_path):

    image = Image.open(input_path)


    image = ImageOps.exif_transpose(image)


    width, height = image.size


  
    if width > height:

        image = image.rotate(
            90,
            expand=True
        )


    image.save(output_path)