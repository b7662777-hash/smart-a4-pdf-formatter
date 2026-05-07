import cv2
import numpy as np


def enhance_image(input_path, output_path):

    image = cv2.imread(input_path)


    
    image = cv2.resize(
        image,
        None,
        fx=1.35,
        fy=1.35,
        interpolation=cv2.INTER_CUBIC
    )



    lab = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB
    )

    l, a, b = cv2.split(lab)


   
    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    l = clahe.apply(l)


    enhanced_lab = cv2.merge(
        (l, a, b)
    )

    image = cv2.cvtColor(
        enhanced_lab,
        cv2.COLOR_LAB2BGR
    )



    kernel = np.array([
        [-1, -1, -1],
        [-1, 10, -1],
        [-1, -1, -1]
    ])

    image = cv2.filter2D(
        image,
        -1,
        kernel
    )


    image = cv2.convertScaleAbs(
        image,
        alpha=1.18,
        beta=8
    )


    cv2.imwrite(
        output_path,
        image
    )