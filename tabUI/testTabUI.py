import threading
import time

import cv2
import numpy as np
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from PIL import Image
from models.DataModelSingleton import FingerDataset, FingerImage, DataModelSingleton
from models.PredictDataSingleton import PredictDataSingleton, convertLabelToClassName
from models.PredicterRunnerThread import PredicterRunnerThread
from models.save_mechanism.ModelSaver import SaveMechanism
from tabUI.ImageViewer import ImageViewer
from tabUI.TabBaseAbstractClass import TabBaseAbstractClass

class TestTab(QWidget, TabBaseAbstractClass):
    def refreshWindowOnLoad(self):
        self.updateTotalImagesLabel()
        # Check if should disable Dataset Image button.
        if self.dataModel.trainDataset is None or self.dataModel.testDataset is None:
            self.datasetImagesButton.setDisabled(True)
        else:
            self.datasetImagesButton.setDisabled(False)

    def __init__(self):
        super().__init__()
        self.predictionData = PredictDataSingleton()
        self.dataModel = DataModelSingleton()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        vboxHyperparameters = QVBoxLayout()

        self.modelPathLabel = QLabel("{}{}".format("Loaded Model:", "None"))
        self.valTrainRatio = QLabel("{}{}".format("Train/Val Ratio:", "None"))
        self.cnnLabel = QLabel("{}{}".format("Loaded CNN Name:", "None"))
        self.batchsizeLabel = QLabel("{}{}".format("Batch Size:", "None"))
        self.epochNumLabel = QLabel("{}{}".format("Epoch Number:", "None"))

        vboxHyperparameters.addWidget(self.modelPathLabel)
        vboxHyperparameters.addWidget(self.cnnLabel)
        vboxHyperparameters.addWidget(self.valTrainRatio)
        vboxHyperparameters.addWidget(self.batchsizeLabel)
        vboxHyperparameters.addWidget(self.epochNumLabel)

        loadModel = QPushButton("Load model from file")
        loadModel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loadModel.clicked.connect(self.on_load_model_button)

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
        self.datasetImagesButton = QPushButton("Dataset images")
        self.datasetImagesButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.datasetImagesButton.clicked.connect(self.on_show_dataset_Button)

        webcamButton = QPushButton("Webcam images")
        webcamButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        webcamButton.clicked.connect(self.on_camera_button)
        hboxButtons.addWidget(self.datasetImagesButton)
        hboxButtons.addWidget(webcamButton)

        self.totalImagesToPredictLabel = QLabel("Images Chosen: 0")
        clearImagesButton = QPushButton("Clear chosen Images")
        clearImagesButton.clicked.connect(self.onClearImagesButton)
        self.predictButton = QPushButton("Predict")
        self.predictButton.clicked.connect(self.onPredictButton)
        self.predictButton.setDisabled(True)

        vbox.addLayout(hboxButtons)
        self.setLayout(vbox)
        vbox.addWidget(self.totalImagesToPredictLabel)
        vbox.addWidget(clearImagesButton)
        vbox.addWidget(self.predictButton)

    def on_load_model_button(self):
        dialog = QDialog(self)
        dialog.setModal(True)
        dialog.show()

        vbox = QVBoxLayout()
        dialog.setLayout(vbox)

        infoLablel = QLabel("Select saved models")
        vbox.addWidget(infoLablel)

        saver = SaveMechanism()
        pyTorchSaves = saver._loadAll()

        pyTorchSaveRadios = [] # The position in this arr equals the save
        buttonGroup = QButtonGroup()

        # Display radio selection
        for index in range(0, len(pyTorchSaves)):
            rowWidget = QWidget()
            rowHbox = QHBoxLayout(rowWidget)

            # Show File
            radio = QRadioButton(pyTorchSaves[index].filePath) # Index is same as the pyTorchSaveRadios position
            pyTorchSaveRadios.append(radio)

            # Show stat
            statString = "Train/Val Ratio(%): {}|{}\tbatchSize: {}\tEpoch: {}\tDNN: {:<15s}".format(
                pyTorchSaves[index].trainRatio,
                pyTorchSaves[index].valRatio,
                pyTorchSaves[index].batchSize,
                pyTorchSaves[index].epochNumber,
                pyTorchSaves[index].dnnName,
            )
            statLabel = QLabel(statString)

            buttonGroup.addButton(radio, id=index)
            rowHbox.addWidget(statLabel)
            rowHbox.addWidget(radio)
            vbox.addWidget(rowWidget)

        # Choose button
        def onChooseModelButton():
            index = buttonGroup.checkedId()
            if (index != -1):
                saveLocation = pyTorchSaveRadios[index].text()
                pyTorchData = saver.loadTorchData(saveLocation)
                pyTorchModel = saver.loadTorchModel(saveLocation)

                # Load into sigleton memory
                self.predictionData.TrainedModel = pyTorchModel
                self.predictionData.latestTrainedModelTrain = pyTorchData.trainRatio
                self.predictionData.latestTrainedModelValidate = pyTorchData.valRatio
                self.predictionData.latestTrainedModelDnnName = pyTorchData.dnnName
                self.predictionData.latestTrainedModelBatchSize = pyTorchData.batchSize
                self.predictionData.latestTrainedModelEpoch = pyTorchData.epochNumber
                self.predictButton.setDisabled(False)

                # Update main tab stat
                self.modelPathLabel.setText("{}{}".format("Loaded Model: ", saveLocation))
                self.valTrainRatio.setText("{}{}|{}".format("Train/Val Ratio: ", pyTorchData.trainRatio,  pyTorchData.valRatio))
                self.cnnLabel.setText("{}{}".format("Loaded CNN Name: ",pyTorchData.dnnName ))
                self.batchsizeLabel.setText("{}{}".format("Batch Size: ", pyTorchData.batchSize))
                self.epochNumLabel.setText("{}{}".format("Epoch Number: ", pyTorchData.epochNumber))

            dialog.close()
        chooseModelButton = QPushButton("Select")
        chooseModelButton.clicked.connect(onChooseModelButton)
        vbox.addWidget(chooseModelButton)



    ####
    # Button handlers
    #####
    def on_show_dataset_Button(self):
        imageView = QDialog(self)
        imageView.resize(500, 500)
        imageView.setModal(True)

        vbox = QVBoxLayout()
        imageView.setLayout(vbox)

        imgViewer = ImageViewer()
        imgViewer.renderStats()
        vbox.addWidget(imgViewer)

        # Select Button
        chooseButton = QPushButton("Choose highlighted images for testing")
        vbox.addWidget(chooseButton)

        def onChooseButtonPress():
            selectedImages = imgViewer.getSelectedImages()

            for img in selectedImages:
                self.predictionData.predictionDataset.addFingerImage(str(img.label), img)
            self.updateTotalImagesLabel()
            imageView.close()



        chooseButton.clicked.connect(onChooseButtonPress)
        imageView.show()

    def on_camera_button(self):
        cameraDialog = QDialog(self)
        cameraDialog.resize(500, 500)
        cameraDialog.setModal(True)
        cameraDialog.rejected.connect(self.on_camera_dialog_close)
        hBox = QHBoxLayout(cameraDialog)
        self.cameraLabel = QLabel()
        hBox.addWidget(self.cameraLabel)
        self.cameraLabel.setText("Loading Camera")

        # Information label
        infoLabel = QLabel()
        self.totaImgsAddedCounter = 0
        infoLabel.setText("0 camera images added")
        hBox.addWidget(infoLabel)

        cameraDialog.show()

        self.cameraThread = CameraThread(self.predictionData)
        self.cameraThread.newFrameFlag.connect(self.render_latest_frame)
        self.cameraThread.start()

        snapButton = QPushButton("Capture")
        hBox.addWidget(snapButton)

        def saveImageHandler():
            self.cameraThread.saveImage()
            self.totaImgsAddedCounter += 1
            infoLabel.setText("{} camera images added".format(self.totaImgsAddedCounter))

        cameraDialog.finished.connect(lambda: self.updateTotalImagesLabel())

        snapButton.clicked.connect(lambda: saveImageHandler())

    def on_camera_dialog_close(self):
        self.cameraThread.stop()

    def render_latest_frame(self, image):
        pixelMap = QPixmap.fromImage(image)
        self.cameraLabel.setPixmap(pixelMap)
        self.cameraLabel.resize(pixelMap.width(), pixelMap.height())

    def updateTotalImagesLabel(self):
        self.totalImagesToPredictLabel.setText("Images Chosen: {}".format(self.predictionData.predictionDataset.totalImages))

    def onClearImagesButton(self):
        self.predictionData.predictionDataset = FingerDataset()
        self.updateTotalImagesLabel()

    def onPredictButton(self):
        print("Predict")
        predictThread = PredicterRunnerThread(self.predictionData)
        predictThread.start()

        predictDialogue = QDialog(self)
        predictDialogue.setModal(True)

        imageGridLayout = QGridLayout(predictDialogue)
        self.statusLabel = QLabel("Predicting. Please Wait")
        imageGridLayout.addWidget(self.statusLabel, 0, 0, 0, 10)

        def updateShowPredictions(status):
            self.statusLabel.setText("PREDICTIONS")

            MAX_COLUMNS = 10
            rowIndex = 1
            columnIndex = 0
            for prediction in self.predictionData.imagePredictionList:
                numpyImg = prediction.imageNumpy
                pilImg = Image.fromarray(numpyImg, mode='L')
                pixmap = QPixmap.fromImage(ImageQt(pilImg))
                predictedString = prediction.predictedClass

                predictionWidget = None
                if (prediction.actualClass is None):
                    predictionWidget = PredictionRowView(pixmap, predictedString, prediction.predictedClassProbability)
                else:
                    predictionWidget = PredictionRowView(pixmap, predictedString, prediction.predictedClassProbability, prediction.actualClass)

                imageGridLayout.addWidget(predictionWidget, rowIndex, columnIndex)
                # Grid pos algorithm
                columnIndex += 1
                if (columnIndex > MAX_COLUMNS):
                    columnIndex = 0
                    rowIndex += 1

        predictThread.predictionFinished.connect(updateShowPredictions)

        statusLabel = QLabel()

        predictDialogue.show()




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

class PredictionRowView(QWidget ):
    def __init__(self, imagePixmap, predictionStr, accVal, actualPred=None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = QVBoxLayout(self)
        self.setLayout(vbox)

        imageLabel = QLabel()
        predictionLabel = QLabel()
        accuracyLabel = QLabel()
        actual = QLabel()

        # Convert classes into their correct label and not a num
        predictionStr = convertLabelToClassName(int(predictionStr))

        imageLabel.setPixmap(imagePixmap)
        predictionLabel.setText("Predicted: {}".format(predictionStr))
        accuracyLabel.setText("Confidence: {:.0f}%".format(accVal*100))
        vbox.addWidget(imageLabel)
        vbox.addWidget(predictionLabel)
        vbox.addWidget(accuracyLabel)

        if (actualPred is not None):
            actualPred = convertLabelToClassName(int(actualPred.item()))
            actual.setText("Actual: {}".format(actualPred))
            vbox.addWidget(actual)





