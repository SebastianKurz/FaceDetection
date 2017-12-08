import FaceDetection
import ImageLoader
import IntersectionOverUnion as IoU
import cv2
import numpy as np
from pprint import pprint


def evaluate():
    imgs = ImageLoader.gen_load_imgs("Data/wider_face_train_bbx_gt.txt")
    intersection_sum = 0
    union_sum = 0

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

            #IoU
            for face in faces:
                x, y, w, h = face
                calculated_position = {"x": x, "y": y, "width": w, "height": h}
                common_points = IoU.points_in_intersection_area(position, calculated_position)
                if (len(common_points) > 0):
                    intersection_sum += IoU.intersection_area_sum(position, calculated_position)
                    union_sum += IoU.union_area_sum(position, calculated_position)

        #intersection_over_union = intersection_sum / union_sum
        #print(intersection_over_union)
        cv2.imshow("pictures", img)
        cv2.waitKey(1000)

    intersection_over_union = intersection_sum / union_sum
    print(intersection_over_union)

evaluate()

#TODO: find a performant method for determining if the boxes overlap or not