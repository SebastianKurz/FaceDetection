from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
import numpy as np

import ImageLoader as il


images = il.load_resized_imgs("Data/wider_face_train_bbx_gt.txt", 600)

model = Sequential([
    # width x hight x dimension
    # 600x600x3
    Conv2D(15, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform", input_shape=(600, 600, 3)),
    # 596x596x15
    MaxPool2D((2,2), data_format="channels_last"),
    # 298x298x15
    Conv2D(75, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 294x294x75
    MaxPool2D((2,2), data_format="channels_last"),
    # 147x147x75
    Conv2D(225, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 143x143x225
    MaxPool2D((3,3), data_format="channels_last"),
    # 47x47x225
    Conv2D(497025, 47, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 1x1x497025
    Conv2D(497025, 1, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 1x1x497025
    Conv2D(337561, 1, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform", activation="softmax")
    # 1x1x337561
])

model.summary()

def convertImagesToTrainigsdata():
    # TODO
    print('TODO')