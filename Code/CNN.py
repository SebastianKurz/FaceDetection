from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
import numpy as np
import cv2

import ImageLoader as il

row_size = 291
scale_size = 600

images = il.load_resized_imgs("Data/wider_face_train_bbx_gt.txt", 600)
train_samples = []
train_labels = []


#  <-----model----->

model = Sequential([
    # width x hight x dimension
    # 600x600x3
    Conv2D(10, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform", input_shape=(600, 600, 3)),
    # 596x596x10
    MaxPool2D((2,2), data_format="channels_last"),
    # 298x298x10
    Conv2D(20, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 294x294x20
    MaxPool2D((2,2), data_format="channels_last"),
    # 147x147x20
    Conv2D(20, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 143x143x20
    MaxPool2D((2,2), data_format="channels_last"),
    # 71x71x20
    Conv2D(20, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 67x67x20
    MaxPool2D((3,3), data_format="channels_last"),
    # 22x22x20
    Conv2D(9680, 22, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 1x1x9680
    Conv2D(9680, 1, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 1x1x9680
    Conv2D(84681, 1, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform", activation="softmax")
    # 1x1x84681 (Output --> 291x291; each Pixel equals one Bounding Box with fix sized shape of 20x20)
])

model.summary()


#  <-----utilities----->

def convert_to_trainingdata():
    for image in images:
        sfw = image.get("sfw", None)
        sfh = image.get("sfh", None)
        array = np.zeros(shape=(84681,))

        positions = image.get("positions", None)

        if(positions != None):
            for position in positions:
                x = position.get("x", None)
                y = position.get("y", None)
                w = position.get("width", None)
                h = position.get("height", None)

                array[convert_coordinates(x, y, w, h, sfw, sfh)] = 1
        
        train_samples.append(image_to_array(image))
        train_labels.append(array)


def convert_coordinates(x, y, w, h, sfw, sfh):
    x = int(x * sfw)
    y = int(y * sfh)
    w = int(w * sfw)
    h = int(h * sfh)

    # needs to be tested
    if(w > 20):
        x = x + int((w - 20) / 2)

    if(w < 20):
        x = x - int((20 - w) / 2)
    
    if(h > 20):
        y = y + int((h - 20) / 2)

    if(h < 20):
        y = y - int((20 - h) / 2)
        
    if(x > 580):
        x = 580

    if(y > 580):
        y = 580

    # interim result 
    index_x = int(x/2)
    index_y = int(y/2)

    # index for 1d-np-array
    index_array = int (row_size * index_y) + index_x

    # print("x: ", x)
    # print("y: ", y)
    # print("index_x: ", index_x)
    # print("index_y: ", index_y)
    # print("index_array: ", index_array)
    
    return index_array
    

def image_to_array(image):
    # TODO
    return image
