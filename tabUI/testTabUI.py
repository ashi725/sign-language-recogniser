import threading
import time

import cv2
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *

from models.PredictDataSingleton import PredictDataSingleton
from tabUI.ImageViewer import ImageViewer
from tabUI.TabBaseAbstractClass import TabBaseAbstractClass

class TestTab(QWidget, TabBaseAbstractClass):
    def refreshWindowOnLoad(self):
        pass
    
    def __init__(self):
        super().__init__()
        self.predictionData = PredictDataSingleton()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        vboxHyperparameters = QVBoxLayout()

        cnnLabel = QLabel("CNN Name: ")
        vboxHyperparameters.addWidget(cnnLabel)

        batchsizeLabel = QLabel("Batch Size: ")
        vboxHyperparameters.addWidget(batchsizeLabel)

        epochNumLabel = QLabel("Epoch Number: ")
        vboxHyperparameters.addWidget(epochNumLabel)

        loadModel = QPushButton("Load model from file")
        loadModel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loadModel.clicked.connect(self.show_file_dialog)

        hbox = QHBoxLayout()
        hbox.addLayout(vboxHyperparameters)
        hbox.addWidget(QLabel("                                     "))
        hbox.addWidget(loadModel)

        vbox.addLayout(hbox)

        testUsingLabel = QLabel("Test using: ")
        testUsingLabel.setStyleSheet("font-size: 16px; padding-top: 30px")
        hboxLabel = QHBoxLayout()
        hboxLabel.addWidget(testUsingLabel)
        hboxLabel.setAlignment(Qt.AlignCenter)
        vbox.addLayout(hboxLabel)

        hboxButtons = QHBoxLayout()
        datasetImagesButton = QPushButton("Dataset images")
        datasetImagesButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        datasetImagesButton.clicked.connect(self.show_dataset_dialog)

        webcamButton = QPushButton("Webcam images")
        webcamButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        webcamButton.clicked.connect(self.on_camera_button)
        hboxButtons.addWidget(datasetImagesButton)
        hboxButtons.addWidget(webcamButton)

        vbox.addLayout(hboxButtons)

        self.setLayout(vbox)

    def show_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')

    def show_dataset_dialog(self):
        imageView = QDialog(self)
        imageView.resize(500, 500)
        imageView.setModal(True)

        vbox = QVBoxLayout()
        imageView.setLayout(vbox)

        imgViewer = ImageViewer()
        vbox.addWidget(imgViewer)

        imageView.show()

    def on_camera_button(self):
        cameraDialog = QDialog(self)
        cameraDialog.resize(500, 500)
        cameraDialog.setModal(True)

        hBox = QHBoxLayout(cameraDialog)
        self.cameraLabel = QLabel()
        hBox.addWidget(self.cameraLabel)
        self.cameraLabel.setText("Loading Camera")
        cameraDialog.show()

        cameraThread = CameraThread(self.predictionData)
        cameraThread.newFrameFlag.connect(self.render_latest_frame)
        cameraThread.start()

        snapButton = QPushButton("Capture")
        hBox.addWidget(snapButton)
        snapButton.clicked.connect(lambda: cameraThread.saveImage())


    def render_latest_frame(self, image):
        pixelMap = QPixmap.fromImage(image)
        self.cameraLabel.setPixmap(pixelMap)
        self.cameraLabel.resize(pixelMap.width(), pixelMap.height())

class CameraThread(QThread):
    newFrameFlag = pyqtSignal(QImage)

    def __init__(self, dataSingleton):
        super().__init__()
        self.databaseSingleton = dataSingleton
        self.saveFlag = threading.Event()
    # https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv
    def run(self):
        cap = cv2.VideoCapture(0) # Remember to release when this ends

        while True:
            ret, frame = cap.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = gray_frame.shape
            q_image = QImage(gray_frame.data, width, height, width, QImage.Format_Grayscale8)
            self.newFrameFlag.emit(q_image)
            time.sleep(0.1)

            if (self.saveFlag.is_set()):
                print("Image saved")
                # todo Save image into correct format
                self.saveFlag.clear()

    def saveImage(self):
        self.saveFlag.set()


