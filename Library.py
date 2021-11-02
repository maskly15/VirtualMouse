# Open package
from HandGesturesModule.HSVmodule import *
from HandGesturesModule.HGmodule import *
from MouseEmulateModule import cordinateTracker as ct
#############################################################
# Main Lib
import cv2
import time
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#HandGestures

# import tensorflow as tf

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
# from tensorflow.keras.callbacks import ReduceLROnPlateau
# from time import perf_counter
# import matplotlib.pyplot as plt


import zipfile

import imutils
import math
###########
#Mouse Emulate
import autopy
##############