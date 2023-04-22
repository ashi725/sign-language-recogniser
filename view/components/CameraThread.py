import threading
import time

import cv2
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap

from models.singletons.DataModelSingleton import FingerImage


class CameraThread(QThread):
    newFrameFlag = pyqtSignal(QImage)

    def __init__(self, predictionDataSingleton):
        super().__init__()
        self.predictSingleton = predictionDataSingleton
        self.saveFlag = threading.Event()
        self.stopFlag = threading.Event()

    # https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv
    def run(self):
        cap = cv2.VideoCapture(0) # Remember to release when this ends

        while not self.stopFlag.is_set():
            ret, frame = cap.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = gray_frame.shape
            q_image = QImage(gray_frame.data, width, height, width, QImage.Format_Grayscale8)
            self.newFrameFlag.emit(q_image)
            time.sleep(0.1)

            if (self.saveFlag.is_set()):
                print("Image saved")
                self.saveFrameIntoSingleton(gray_frame)
                self.saveFlag.clear()
        cap.release()

    def stop(self):
        self.stopFlag.set()

    def saveImage(self):
        self.saveFlag.set()

    def saveFrameIntoSingleton(self, grayFrame):
        # Create FingerImage class
        resized_image = cv2.resize(grayFrame, (28, 28)) # Resize into 28x28px
        pillowImg = Image.fromarray(np.uint8(resized_image), 'L')
        pixmapImg = QPixmap.fromImage(ImageQt(pillowImg))

        fingerImageObj = FingerImage(-1,resized_image, pixmapImg, pillowImg)
        self.predictSingleton.predictionDataset.addFingerImage(fingerImageObj.label, fingerImageObj)
        print("Finger image added")