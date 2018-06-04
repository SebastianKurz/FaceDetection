from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.optimizers import SGD
import numpy as np
import cv2

import ImageLoader as il


scale_size = 600

sliding_window_size = 20 # windows don't overlapp
row_size = int(scale_size / sliding_window_size) # 30

btch_size = 50
epoch_amount = 140

images = il.load_cropped_imgs("Data/wider_face_train_bbx_gt.txt", 600)
samples = []
labels = []

# -----utilities-----
def convert_coordinate_to_label(x, y, w, h, sfw, sfh):
    x = int(x * sfw)
    y = int(y * sfh)
    w = int(w * sfw)
    h = int(h * sfh)

    x_realtive = x % sliding_window_size
    y_relative = y % sliding_window_size

    index_x = int(x / sliding_window_size)
    index_y = int(y / sliding_window_size)

    # print("x_relative: ", x_realtive)
    # print("y_relative: ", y_relative)
    # print("index_x: ", index_x)
    # print("index_y: ", index_y)

    return {"i_x": index_x, "i_y": index_y, "x_rel": x_realtive, "y_rel": y_relative, "w": w, "h": h}

def convert_to_trainingsdata():
    for img in images:
        sfw = img.get("sfw", None)
        sfh = img.get("sfh", None)
        array = np.zeros(shape=(row_size, row_size, 4))

        positions = img.get("positions", None)
        for position in positions:
            x = position.get("x", None)
            y = position.get("y", None)
            w = position.get("width", None)
            h = position.get("height", None)

            label_position = convert_coordinate_to_label(x, y ,w, h, sfw, sfh)
            array[label_position.get("i_x"), label_position.get("i_y"), 0] = label_position.get("x_rel")
            array[label_position.get("i_x"), label_position.get("i_y"), 1] = label_position.get("y_rel")
            array[label_position.get("i_x"), label_position.get("i_y"), 2] = label_position.get("w")
            array[label_position.get("i_x"), label_position.get("i_y"), 3] = label_position.get("h")
            
        samples.append(img.get("img"))
        labels.append(array)


convert_to_trainingsdata()

x_train = np.array(samples[:int(len(samples) / 2)])
del samples[:int(len(samples) / 2)]
x_test = np.array(samples)

del samples[:]

y_train = np.array(labels[:int(len(labels) / 2)])
del labels[:int(len(labels) / 2)]
y_test = np.array(labels)

del labels[:]


model = Sequential([
    # width x hight x dimension
    # 600x600x3
    Conv2D(10, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform", input_shape=(600, 600, 3)),
    # 596x596x10
    MaxPool2D((2,2)),
    # 298x298x10
    Conv2D(20, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 294x294x20
    Conv2D(20, 5, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 290x290x20
    MaxPool2D((3,3)),
    # 96x96x20
    Conv2D(40, 3, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 94x94x40
    MaxPool2D((2,2)),
    # 47x47x40
    Conv2D(80, 3, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform"),
    # 45x45x80
    Conv2D(4, 16, strides=(1, 1), data_format="channels_last", kernel_initializer="glorot_uniform", activation="softmax"),
    # 30x30x4 --> Output
])

model.summary()

model.compile(
    #SGD(lr=0.001),
    #SGD(lr=0.01),
    SGD(lr=0.01),
    loss="mean_squared_error",  
    metrics=[
        "accuracy"
    ]
)

model.fit(
    x_train,
    y_train,
    batch_size=btch_size,
    epochs=epoch_amount,
    verbose=2
)

score = model.evaluate(
    x_test,
    y_test,
    batch_size=btch_size,
    verbose=1
)

predictions = model.predict(x_test)
print(predictions)

exit()