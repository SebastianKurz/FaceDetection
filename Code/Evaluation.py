import FaceDetection
import ImageLoader
import IntersectionOverUnion as IOU
import cv2
import numpy as np
from pprint import pprint


def evaluate():
    imgs = ImageLoader.gen_load_imgs("Data/wider_face_train_bbx_gt.txt")
    union_area_list = []

    for i in imgs:
        img = i.get("img", None)
        positions = i.get("positions", None)

        faces = FaceDetection.detect_faces(img)
        FaceDetection.draw_boxes(img, faces, (255, 0, 0))
        
        for position in positions:
            x_actual = position.get("x", None)
            y_actual = position.get("y", None)
            w_actual = position.get("width", None)
            h_actual = position.get("height", None)

            cv2.rectangle(
                img,
                (x_actual, y_actual),
                (x_actual + w_actual, y_actual + h_actual),
                (0,255,0)
            )
        cv2.imshow("pictures", img)
        cv2.waitKey(1000)


evaluate()