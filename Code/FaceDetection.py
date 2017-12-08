import cv2
import numpy as np
import ImageLoader as il
from pprint import pprint

FACE_CASCADE = cv2.CascadeClassifier('haar_cascade.xml')
SIDE_CASCADE = cv2.CascadeClassifier('lbpcascade_sideface.xml')

def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (30,30),
        flags = 0
    )
    sides = SIDE_CASCADE.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (30,30),
        flags = 0
    )
    if len(sides) > 0 and len(faces) > 0:
        return np.concatenate((faces, sides), axis=0)
    elif len(sides) > 0:
        return sides
    else:
        return faces


def draw_boxes(img, facepositions, color):
    """
    color is a tuple containing three values for rgb-colors like (0, 255, 0)
    """
    for x, y, w, h in facepositions:
        cv2.rectangle(img, (x,y), (x+w, y+h), color)


def display_image(img):
    cv2.imshow("Webcam stream", frame)

    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        cv2.destroyAllWindows()



#test
"""
imgs = il.gen_load_imgs("Data/wider_face_train_bbx_gt.txt")

for i in imgs:
    img = i.get("img", None)
    faces = detect_faces(img)
    draw_boxes(img, faces, (255, 0, 0))

    cv2.imshow("Image", img)
    cv2.waitKey(1000)

    pprint(faces)
"""