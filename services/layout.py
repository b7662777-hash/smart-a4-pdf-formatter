from PIL import Image



A4_WIDTH = 3508
A4_HEIGHT = 4961



ROWS = 2
COLS = 2



PADDING = 6


def create_a4_layout(image_paths, output_path):

  
    canvas = Image.new(
        "RGB",
        (A4_WIDTH, A4_HEIGHT),
        "white"
    )


  
    box_width = (
        A4_WIDTH - (PADDING * (COLS + 1))
    ) // COLS

    box_height = (
        A4_HEIGHT - (PADDING * (ROWS + 1))
    ) // ROWS


    for index, path in enumerate(image_paths):

        if index >= 4:
            break


        img = Image.open(path)

        img = img.convert("RGB")


        img_width, img_height = img.size


    
        scale = min(
            box_width / img_width,
            box_height / img_height
        )


        scale *= 1.08


        new_width = int(
            img_width * scale
        )

        new_height = int(
            img_height * scale
        )


        img = img.resize(
            (new_width, new_height),
            Image.LANCZOS
        )


    
        if new_width > box_width:

            left = (
                new_width - box_width
            ) // 2

            img = img.crop((
                left,
                0,
                left + box_width,
                new_height
            ))


        if new_height > box_height:

            top = (
                new_height - box_height
            ) // 2

            img = img.crop((
                0,
                top,
                img.width,
                top + box_height
            ))


        
        final_width, final_height = img.size


        offset_x = (
            box_width - final_width
        ) // 2

        offset_y = (
            box_height - final_height
        ) // 2


        row = index // COLS

        col = index % COLS


        x = (
            PADDING +
            col * (box_width + PADDING) +
            offset_x
        )

        y = (
            PADDING +
            row * (box_height + PADDING) +
            offset_y
        )


        canvas.paste(
            img,
            (x, y)
        )


    canvas.save(
        output_path,
        quality=100
    )