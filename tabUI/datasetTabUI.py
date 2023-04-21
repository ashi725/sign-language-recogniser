import threading
import time

import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import csv

from models.DataModelSingleton import DataModelSingleton, FingerDataset, FingerImage
from models.HyperParametersSingleton import HyperParametersSingleton
from tabUI.TabBaseAbstractClass import TabBaseAbstractClass


class DatasetTab(QWidget,TabBaseAbstractClass):
    def refreshWindowOnLoad(self):
        pass

    def __init__(self):

        # Init variables
        super().__init__()
        vbox = QVBoxLayout()
        self.dataModel = DataModelSingleton()
        self.hyperParameters = HyperParametersSingleton()
        self.downloadThreadInstance = None
        
        # Import Button
        importDatasetButton = QPushButton('Import dataset')
        importDatasetButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        importDatasetButton.setStyleSheet("font-size: 20px; padding: 10px;")
        importDatasetButton.clicked.connect(self.show_dialog)
        vbox.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(importDatasetButton)
        vbox.addStretch()
        self.setLayout(vbox)
    
    def show_dialog(self):
        dialog = QDialog(self)   
        dialog.setModal(True)
        dialog.setWindowTitle('Import dataset')
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        dialog.setFixedWidth(400)
        self.dropdown = QComboBox(dialog)
        self.dropdown.addItems(['Not selected', 'MNIST', 'Custom'])
        self.dropdown.currentIndexChanged.connect(self.dropdown_changed)

        # Error Label
        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet("color: red;")

        # Download/Stop Button
        self.downloadButton = QPushButton("Download")
        self.downloadButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton = QPushButton("Stop")
        self.stopButton.setDisabled(True)

        # Cancel Button
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cancelButton.clicked.connect(dialog.reject)

        # Progress Widgets
        self.progressBar = QProgressBar()
        self.progressPercentage = QLabel("")
        self.progressPercentage.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.progressPercentage.setStyleSheet("padding: 0px; margin: 0px;")
        self.downloadStatusLabel = QLabel("")

        # Layout settings
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignHCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(self.dropdown)
        hbox.addWidget(self.downloadButton)
        hbox.addWidget(self.stopButton)

        vbox.addLayout(hbox)
        vbox.addWidget(self.errorLabel)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.progressBar)
        hbox1.addWidget(self.progressPercentage)
        hbox1.addWidget(self.downloadStatusLabel)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(self.cancelButton)
        vbox.addLayout(hbox2)

        dialog.setLayout(vbox)

        # Event Binders
        self.downloadButton.clicked.connect(lambda: self.onDownloadDatabase(self.dropdown.currentText()))
        self.stopButton.clicked.connect(self.onStopDownloadButton)

        dialog.show()    

    def dropdown_changed(self):
        self.hyperParameters.dataset = self.dropdown.currentText() 
        print("drop down changed to " + self.dropdown.currentText() )
    
    def onDownloadDatabase(self, selectedDatabase):

        # Disable buttons
        self.downloadButton.setDisabled(True)
        self.stopButton.setDisabled(False)
        self.cancelButton.setDisabled(True)

        # Create new download thread.
        if (self.downloadThreadInstance != None):
            self.downloadThreadInstance.stop()
            self.downloadThreadInstance = None

        self.downloadThreadInstance = DownloadThread(selectedDatabase, self.dataModel)

        # Attach signal listeners
        self.downloadThreadInstance.progressBarChanged.connect(self.updateProgressBar)
        self.downloadThreadInstance.timerStringChanged.connect(self.updateTimerLabel)
        self.downloadThreadInstance.downloadStatusLabelChanged.connect(self.updateDownloadStatusLabel)
        self.downloadThreadInstance.errorLabelChanged.connect(self.updateErrorLabel)
        self.downloadThreadInstance.finishDownloadingFlag.connect(self.onDownloadFinish)

        self.downloadThreadInstance.start()

    def onStopDownloadButton(self):
        self.downloadThreadInstance.stop()

    # Component update methods 
    def updateProgressBar(self, progressBarValue):
        self.progressBar.setValue(progressBarValue)

    def updateTimerLabel(self, labelText):
        self.progressPercentage.setText(labelText)

    def updateDownloadStatusLabel(self, labelText):
        self.downloadStatusLabel.setText(labelText)

    def updateErrorLabel(self, labelText):
        self.errorLabel.setText(labelText)

    def onDownloadFinish(self, data):
        self.downloadButton.setDisabled(False)
        self.stopButton.setDisabled(True)
        self.cancelButton.setDisabled(False)

        # If data = 0 then download successful. Redirect to different tab
        if data == 0:
            self.redirectNextTab()

    def redirectNextTab(self):
        print("Redirect")
        # todo

class DownloadThread(QThread):
    progressBarChanged = pyqtSignal(int)
    timerStringChanged = pyqtSignal(str)
    downloadStatusLabelChanged = pyqtSignal(str)
    errorLabelChanged = pyqtSignal(str)
    finishDownloadingFlag = pyqtSignal(int) # Emit 0=Download successful. Else failed.

    def __init__(self, selectedDatabase, dataModelReference):
        super().__init__()
        self.selectedDatabase = selectedDatabase
        self.dataModelReference = dataModelReference
        self.stopFlag = threading.Event()
        self.noDatabaseSelectedEdgeCase = False

    def run(self):
        while not self.stopFlag.is_set():
            self.downloadDatabase()
            break

        # If no DB selected. Just return.
        if self.noDatabaseSelectedEdgeCase:
            self.finishDownloadingFlag.emit(2)
            return

        # Cleanup if stopped
        if self.stopFlag.is_set():
            self.stopCleanup()
            self.finishDownloadingFlag.emit(1)  # Signal download finish. So can enable widgets and allow cleanup.
        else:
            self.finishDownloadingFlag.emit(0)

    def stop(self):
        self.stopFlag.set()

    def stopCleanup(self):
        self.dataModelReference.testDataset = None
        self.dataModelReference.trainDataset = None
        self.progressBarChanged.emit(0)
        self.finishDownloadingFlag.emit(1)
        self.timerStringChanged.emit("Timer")
        self.downloadStatusLabelChanged.emit("Download Cancelled. Data cleared.")

    def downloadDatabase(self):
        if self.selectedDatabase == "MNIST":
            self.errorLabelChanged.emit("")

            self.downloadStatusLabelChanged.emit("Downloading Test Set (1/2)")
            mnistTest = self.loadCsv(r'resources\sign_mnist_test.csv')
            mnistTest.databaseName = "Test_MNIST"
            self.downloadStatusLabelChanged.emit("Downloading Train Set (2/2)")
            mnistTrain = self.loadCsv(r'resources\sign_mnist_train.csv')
            mnistTrain.databaseName = "Train_MNIST"
            self.downloadStatusLabelChanged.emit("Finished Downloading")

            # Store downloaded data into sharedData
            self.dataModelReference.testDataset = mnistTest
            self.dataModelReference.trainDataset = mnistTrain

        elif self.selectedDatabase == "Custom":
            testFilePath, tempVar = QFileDialog.getOpenFileName(None, "Select Test CSV file", "", "CSV (*.csv)")
            trainFilePath, tempVar = QFileDialog.getOpenFileName(None, "Select Train CSV file", "", "CSV (*.csv)")

            # Check invalid file paths
            if testFilePath == "" or trainFilePath=="":
                self.errorLabelChanged.emit("Please select valid test sets")
                self.noDatabaseSelectedEdgeCase = True
                return

            # Download datasets
            self.downloadStatusLabelChanged.emit("Downloading Test Set (1/2)")
            mnistTest = self.loadCsv(testFilePath)
            mnistTest.databaseName = "Test_Custom"
            self.downloadStatusLabelChanged.emit("Downloading Train Set (2/2)")
            mnistTrain = self.loadCsv(trainFilePath)
            mnistTrain.databaseName = "Train_Custom"
            self.downloadStatusLabelChanged.emit("Finished Downloading")

            # Store downloaded data into sharedData
            self.dataModelReference.testDataset = mnistTest
            self.dataModelReference.trainDataset = mnistTrain

        else:
            self.errorLabelChanged.emit("Please select a database")
            self.noDatabaseSelectedEdgeCase = True

    def loadCsv(self, csvLocation):
        dataset = FingerDataset() # Store loaded data into this data class

        # Check if stop flag set
        if self.stopFlag.is_set():
            return dataset

        # https://stackoverflow.com/questions/71175143/how-to-read-and-display-mnist-dataset
        with open(csvLocation, 'r') as csv_file:
            csvreader = csv.reader(csv_file)
            next(csvreader)

            # Get Total Rows
            self.timerStringChanged.emit("Calculating Time Remaining")
            totalRows = sum(1 for row in csvreader)
            csv_file.seek(0) # Move file pointer back to start of file
            next(csvreader)

            # Progress bar / Timer variables
            currentRowNumber = 0
            averageTime = 1
            totalTime = 0

            for data in csvreader:
                startTime = time.time()

                # Dissect columns
                label = data[0:1][0]  # Number classifying type of symbol
                pixels = data[1:]
                pixels = np.array(pixels, dtype='uint8')
                pixels = pixels.reshape((28, 28))

                # Generate image for PYQT
                pillowImage = Image.fromarray(np.uint8(pixels), 'L')
                pixMap = QPixmap.fromImage(ImageQt(pillowImage))

                # Save img information
                imageClass = FingerImage(label, pixels, pixMap, pillowImage)
                dataset.addFingerImage(label, imageClass)

                # Update progressbar
                currentRowNumber += 1
                totalTime += time.time() - startTime
                averageTime = totalTime / (currentRowNumber)
                timeLeftString = "Approx {} secs".format(self.calculateTimeLeft(currentRowNumber, totalRows, averageTime))

                self.progressBarChanged.emit(int((currentRowNumber/totalRows)*100))
                self.timerStringChanged.emit(timeLeftString)

                # Check if stop flag set
                if self.stopFlag.is_set():
                    break
        return dataset

    def calculateTimeLeft(self, currentRow, totalRows, averageTimePerRow):
            rowsLeft = totalRows-currentRow
            timeSeconds = rowsLeft * averageTimePerRow
            return int(timeSeconds)

