import numpy as np
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Dense, Flatten
from keras.layers import Dense, Dropout, Flatten, BatchNormalization
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ReduceLROnPlateau
from time import perf_counter
import cv2
import matplotlib.pyplot as plt


class HGmodule():
    def __init__(self):
        self.model = Sequential([Conv2D(filters=32,  kernel_size=(3,3), activation="relu", input_shape=(40,40,1)),
                    MaxPool2D(2,2, padding='same'),

                    Conv2D(filters=128,  kernel_size=(3,3), activation="relu"),
                    MaxPool2D(2,2, padding='same'),

                    Conv2D(filters=512, kernel_size=(3,3), activation="relu"),
                    MaxPool2D(2,2, padding='same'),

                    Flatten(),

                    Dense(units=1024, activation="relu"),
                    Dense(units=256, activation="relu"),
                    Dense(units= 32,activation="relu"),
                    Dropout(0.5),
                    Dense(units=4, activation="softmax")
])

        self.model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        self.model.load_weights(r'D:\FPT\Project\saveModule\HGR_test_12.h5')

    def plot_image2(self,img):
        img_cvt = img.copy()
        # img_cvt =cv2.cvtColor(img_cvt,cv2.COLOR_GRAY2)
        print(img_cvt.shape)  # Prints the shape of the image just to check
        plt.imshow(img_cvt)  # Shows the image
        plt.xlabel("Width")
        plt.ylabel("Height")
        plt.show()
    def predictGesture(self, image):
        labelList = [ "Right Click","", "left click", ""]
        # image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        image=cv2.resize(image,(40,40),interpolation=cv2.INTER_AREA)
        cv2.imshow("predict image",image)
        image=np.array(image)
        images = image.reshape(1, 40, 40, 1)
        classes = self.model.predict(images)
        # print(np.argsort(classes))
        predicted_label = np.argmax(classes)
        return labelList[predicted_label]