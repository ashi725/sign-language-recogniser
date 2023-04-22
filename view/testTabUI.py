from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from models.PredicterRunnerThread import PredicterRunnerThread
from models.save_mechanism.ModelSaver import SaveMechanism
from models.singletons.DataModelSingleton import FingerDataset, DataModelSingleton
from models.singletons.PredictDataSingleton import PredictDataSingleton
from view.TabBaseAbstractClass import TabBaseAbstractClass
from view.components.CameraThread import CameraThread
from view.components.ImageViewer import ImageViewer
from view.components.PredictionRowView import PredictionRowView


class TestTab(QWidget, TabBaseAbstractClass):
    """
    This is the main tab for predictions
    It contains func to
    - Load a saved model
    - Use webcam to add to prediction list
    - Select imgs from dataset to predict
    """
    def refreshWindowOnLoad(self):
        """
        This method is called once the tab pressed.
        """
        self.updateTotalImagesLabel() # update total images to predict
        # Check if should disable Dataset Image button.
        if self.dataModel.trainDataset is None or self.dataModel.testDataset is None:
            self.datasetImagesButton.setDisabled(True)
        else:
            self.datasetImagesButton.setDisabled(False)

    def __init__(self):
        # Init vars
        super().__init__()
        self.predictionData = PredictDataSingleton()
        self.dataModel = DataModelSingleton()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        vboxHyperparameters = QVBoxLayout()

        # Current model labels
        self.modelPathLabel = QLabel("{}{}".format("Loaded Model:", "None"))
        self.valTrainRatio = QLabel("{}{}".format("Train/Val Ratio:", "None"))
        self.cnnLabel = QLabel("{}{}".format("Loaded CNN Name:", "None"))
        self.batchsizeLabel = QLabel("{}{}".format("Batch Size:", "None"))
        self.epochNumLabel = QLabel("{}{}".format("Epoch Number:", "None"))

        # Layout settings
        vboxHyperparameters.addWidget(self.modelPathLabel)
        vboxHyperparameters.addWidget(self.cnnLabel)
        vboxHyperparameters.addWidget(self.valTrainRatio)
        vboxHyperparameters.addWidget(self.batchsizeLabel)
        vboxHyperparameters.addWidget(self.epochNumLabel)

        # Load model button
        loadModel = QPushButton("Load model from file")
        loadModel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loadModel.clicked.connect(self.on_load_model_button)

        # Layout settings
        hbox = QHBoxLayout()
        hbox.addLayout(vboxHyperparameters)
        hbox.addWidget(QLabel("                                     "))
        hbox.addWidget(loadModel)
        vbox.addLayout(hbox)

        # Labels
        testUsingLabel = QLabel("Test using: ")
        testUsingLabel.setStyleSheet("font-size: 16px; padding-top: 30px")
        hboxLabel = QHBoxLayout()
        hboxLabel.addWidget(testUsingLabel)
        hboxLabel.setAlignment(Qt.AlignCenter)
        vbox.addLayout(hboxLabel)

        # Load dataset button
        hboxButtons = QHBoxLayout()
        self.datasetImagesButton = QPushButton("Dataset images")
        self.datasetImagesButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.datasetImagesButton.clicked.connect(self.on_show_dataset_Button)

        # WEbcam button
        webcamButton = QPushButton("Webcam images")
        webcamButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        webcamButton.clicked.connect(self.on_camera_button)
        hboxButtons.addWidget(self.datasetImagesButton)
        hboxButtons.addWidget(webcamButton)

        # Clear and predict button
        self.totalImagesToPredictLabel = QLabel("Images Chosen: 0")
        clearImagesButton = QPushButton("Clear chosen Images")
        clearImagesButton.clicked.connect(self.onClearImagesButton)
        self.predictButton = QPushButton("Predict")
        self.predictButton.clicked.connect(self.onPredictButton)
        self.predictButton.setDisabled(True)

        # Layout settings
        vbox.addLayout(hboxButtons)
        self.setLayout(vbox)
        vbox.addWidget(self.totalImagesToPredictLabel)
        vbox.addWidget(clearImagesButton)
        vbox.addWidget(self.predictButton)

    def on_load_model_button(self):
        """
        This method is called on a load model button pressed.
        It shows all models saved in disc and allows user to choose which to load
        @return:
        """
        # Dialogue sett
        dialog = QDialog(self)
        dialog.setWindowTitle('Choose ML Model')
        dialog.setModal(True)
        dialog.setMinimumSize(900, 250)
        dialog.setMaximumSize(900, 600)
        dialog.show()

        # Layout
        vbox = QVBoxLayout(dialog)
        vbox.setContentsMargins(20, 20, 20, 20)

        # Header
        infoLablel = QLabel("Choose a saved model")
        vbox.addWidget(infoLablel)

        # Load saved models
        saver = SaveMechanism()
        pyTorchSaves = saver.loadAllMetadata()
        pyTorchSaveRadios = [] # The position in this arr equals the save
        buttonGroup = QButtonGroup()

        # Display saved models
        for index in range(0, len(pyTorchSaves)):
            rowWidget = QWidget()
            rowHbox = QHBoxLayout(rowWidget)

            # Show File
            radio = QRadioButton(pyTorchSaves[index].filePath) # Index is same as the pyTorchSaveRadios position
            pyTorchSaveRadios.append(radio)

            # Show stat
            statString = "[CNN: {}]\t[Batch Size: {}]\t[Epoch: {}]\t[Train/Val Ratio(%): {}|{}]".format(
                pyTorchSaves[index].cnnName,
                pyTorchSaves[index].batchSize,
                pyTorchSaves[index].epochNumber,
                pyTorchSaves[index].trainRatio,
                pyTorchSaves[index].valRatio,
            )

            # Layout
            statLabel = QLabel(statString)
            buttonGroup.addButton(radio, id=index)
            rowHbox.addWidget(statLabel)
            rowHbox.addWidget(radio)
            vbox.addWidget(rowWidget)

        # Choose model handler
        def onChooseModelButton():
            index = buttonGroup.checkedId()
            if (index != -1): # -1 indicates no model chosen
                # Get saved model settings
                saveLocation = pyTorchSaveRadios[index].text()
                pyTorchData = saver.loadTorchData(saveLocation)
                pyTorchModel = saver.loadTorchModel(saveLocation)

                # Load into singleton memory
                self.predictionData.TrainedModel = pyTorchModel
                self.predictionData.latestTrainedModelTrain = pyTorchData.trainRatio
                self.predictionData.latestTrainedModelValidate = pyTorchData.valRatio
                self.predictionData.latestTrainedModelCnnName = pyTorchData.cnnName
                self.predictionData.latestTrainedModelBatchSize = pyTorchData.batchSize
                self.predictionData.latestTrainedModelEpoch = pyTorchData.epochNumber
                self.predictButton.setDisabled(False)

                # Update main tab stat
                self.modelPathLabel.setText("{}{}".format("Loaded Model: ", saveLocation))
                self.valTrainRatio.setText("{}{}|{}".format("Train/Val Ratio: ", pyTorchData.trainRatio,  pyTorchData.valRatio))
                self.cnnLabel.setText("{}{}".format("Loaded CNN Name: ",pyTorchData.cnnName ))
                self.batchsizeLabel.setText("{}{}".format("Batch Size: ", pyTorchData.batchSize))
                self.epochNumLabel.setText("{}{}".format("Epoch Number: ", pyTorchData.epochNumber))

            dialog.close()

        # Layout settings
        chooseModelButton = QPushButton("Select")
        chooseModelButton.setFixedWidth(100)
        chooseModelButton.clicked.connect(onChooseModelButton)
        vbox.addWidget(chooseModelButton)



    def on_show_dataset_Button(self):
        """
        This method is called when button to select images to predict is pressed
        @return:
        """

        # Dialogue settings
        imageView = QDialog(self)
        imageView.setWindowTitle("Choose images to predict")
        imageView.resize(800, 800)
        imageView.setModal(True)

        # Layout settings
        vbox = QVBoxLayout()
        imageView.setLayout(vbox)

        # Image viewer widget
        imgViewer = ImageViewer()
        imgViewer.renderStats()
        vbox.addWidget(imgViewer)

        # Select Button
        chooseButton = QPushButton("Choose highlighted images for testing")
        vbox.addWidget(chooseButton)

        def onChooseButtonPress():
            # This method is called when choose button pressed
            # Get selected images
            selectedImages = imgViewer.getSelectedImages()

            # Saves all selected images into memroy
            for img in selectedImages:
                self.predictionData.predictionDataset.addFingerImage(str(img.label), img)
            self.updateTotalImagesLabel()
            imageView.close()



        chooseButton.clicked.connect(onChooseButtonPress)
        imageView.show()

    def on_camera_button(self):
        cameraDialog = QDialog(self)
        cameraDialog.setWindowTitle("Predict webcam pictures")
        cameraDialog.resize(500, 500)
        cameraDialog.setModal(True)
        cameraDialog.rejected.connect(self.on_camera_dialog_close)

        gridLayout = QGridLayout(cameraDialog)
        gridLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.cameraLabel = QLabel()
        self.cameraLabel.resize(200, 200)
        gridLayout.addWidget(self.cameraLabel, 0, 0, 1, 2)
        self.cameraLabel.setText("Loading Camera")

        # Information label
        infoLabel = QLabel()
        self.totaImgsAddedCounter = 0
        infoLabel.setText("0 camera images added")
        gridLayout.addWidget(infoLabel, 1, 1)

        cameraDialog.show()

        self.cameraThread = CameraThread(self.predictionData)
        self.cameraThread.newFrameFlag.connect(self.render_latest_frame)
        self.cameraThread.start()

        self.snapButton = QPushButton("Capture")
        self.snapButton.setDisabled(True)
        gridLayout.addWidget(self.snapButton, 1,0)

        def saveImageHandler():
            self.cameraThread.saveImage()
            self.totaImgsAddedCounter += 1
            infoLabel.setText("{} camera images added".format(self.totaImgsAddedCounter))

        cameraDialog.finished.connect(lambda: self.updateTotalImagesLabel())

        self.snapButton.clicked.connect(lambda: saveImageHandler())

    def on_camera_dialog_close(self):
        self.cameraThread.stop()

    def render_latest_frame(self, image):
        pixelMap = QPixmap.fromImage(image)
        self.cameraLabel.setPixmap(pixelMap)
        self.snapButton.setDisabled(False)
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
        predictDialogue.setWindowTitle("Predictions")
        predictDialogue.setModal(True)

        imageGridLayout = QGridLayout(predictDialogue)
        imageGridLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.statusLabel = QLabel("Predicting. Please Wait")
        imageGridLayout.addWidget(self.statusLabel, 0, 0, 1, 10, alignment=Qt.AlignHCenter)
        self.statusLabel.setStyleSheet('padding: 5px; font-size: 16px; font-weight: bold;')

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











