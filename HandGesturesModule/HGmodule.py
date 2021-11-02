
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ReduceLROnPlateau
from time import perf_counter
import matplotlib.pyplot as plt
import os
import zipfile
import numpy as np
import cv2

class HGmodule():
    def __init__(self):
        self.model = Sequential([Conv2D(filters=32,  kernel_size=(3,3), activation="relu", input_shape=(40,40,1)),
                    MaxPool2D(2,2, padding='same'),
                    Conv2D(filters=64, kernel_size=(3, 3), activation="relu"),
                    MaxPool2D(2, 2, padding='same'),
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
        try:
            self.model.load_weights(r'.\HandGesturesModule\saveModule\HGR.h5')
        except:
            local_zip = r'.\HandGesturesModule\saveModule\HGR.zip'
            zip_ref = zipfile.ZipFile(local_zip, 'r')
            zip_ref.extractall(r'.\HandGesturesModule\saveModule')
            zip_ref.close()
            print('extract zipfile !')
            self.model.load_weights(r'.\HandGesturesModule\saveModule\HGR.h5')
        print("Load Weight sucsess !")

    # el.l
    def plot_image2(self,img):
        img_cvt = img.copy()
        # img_cvt =cv2.cvtColor(img_cvt,cv2.COLOR_GRAY2)
        print(img_cvt.shape)  # Prints the shape of the image just to check
        plt.imshow(img_cvt)  # Shows the image
        plt.xlabel("Width")
        plt.ylabel("Height")
        plt.show()

    def predictGesture(self, image):
        labelList = [ "nothing","move", "Left", "Right"]
        # image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        image=cv2.resize(image,(40,40),interpolation=cv2.INTER_AREA)
        image=np.array(image)
        images = image.reshape(1, 40, 40, 1)
        classes = self.model.predict(images)
        # print(np.argsort(classes))
        predicted_label = np.argmax(classes)
        return predicted_label