import cv2
import numpy as np


def crop_image(input_path, output_path):

    image = cv2.imread(input_path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )


    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )


   
    kernel = np.ones(
        (3, 3),
        np.uint8
    )

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )


  
    coords = cv2.findNonZero(
        thresh
    )


    if coords is not None:

        x, y, w, h = cv2.boundingRect(
            coords
        )


       
        padding = 8

        x = max(0, x - padding)
        y = max(0, y - padding)

        w = min(
            image.shape[1] - x,
            w + padding * 2
        )

        h = min(
            image.shape[0] - y,
            h + padding * 2
        )


        cropped = image[
            y:y+h,
            x:x+w
        ]


        cv2.imwrite(
            output_path,
            cropped
        )

    else:

        cv2.imwrite(
            output_path,
            image
        )