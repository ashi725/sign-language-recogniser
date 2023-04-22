import csv
import threading
import time

import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from models.singletons.DataModelSingleton import FingerDataset, FingerImage


class DownloadThread(QThread):
    """
    This contains a thread to download a CSV file and load it into memory.
    It also sends data back to parent via signals
    """
    # Signals
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
        # Download database
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
        """
        This method is automatically called when the download is stopped.
        It allows cleanup of half loaded data
        """
        self.dataModelReference.testDataset = None
        self.dataModelReference.trainDataset = None
        self.progressBarChanged.emit(0)
        self.finishDownloadingFlag.emit(1)
        self.timerStringChanged.emit("Timer")
        self.downloadStatusLabelChanged.emit("Download Cancelled. Data cleared.")

    def downloadDatabase(self):
        """
        This method downloads the database and loads into memory
        """
        if self.selectedDatabase == "MNIST":
            # MNIST CSV file
            self.errorLabelChanged.emit("")

            # Download Train
            self.downloadStatusLabelChanged.emit("Downloading Test Set (1/2)")
            mnistTest = self.loadCsv(r'resources\sign_mnist_test.csv')
            mnistTest.databaseName = "Test_MNIST"

            # Download Test
            self.downloadStatusLabelChanged.emit("Downloading Train Set (2/2)")
            mnistTrain = self.loadCsv(r'resources\sign_mnist_train.csv')
            mnistTrain.databaseName = "Train_MNIST"
            self.downloadStatusLabelChanged.emit("Finished Downloading")

            # Store downloaded data into sharedData
            self.dataModelReference.testDataset = mnistTest
            self.dataModelReference.trainDataset = mnistTrain

        elif self.selectedDatabase == "Custom":
            # Custom CSV file. Get users file paths
            testFilePath, tempVar = QFileDialog.getOpenFileName(None, "Select Test CSV file", "", "CSV (*.csv)")
            trainFilePath, tempVar = QFileDialog.getOpenFileName(None, "Select Train CSV file", "", "CSV (*.csv)")

            # Check invalid file paths
            if testFilePath == "" or trainFilePath=="":
                self.errorLabelChanged.emit("Please select valid test sets")
                self.noDatabaseSelectedEdgeCase = True
                return

            # Download test csv set
            self.downloadStatusLabelChanged.emit("Downloading Test Set (1/2)")
            mnistTest = self.loadCsv(testFilePath)
            mnistTest.databaseName = "Test_Custom"

            # Download train csv set
            self.downloadStatusLabelChanged.emit("Downloading Train Set (2/2)")
            mnistTrain = self.loadCsv(trainFilePath)
            mnistTrain.databaseName = "Train_Custom"
            self.downloadStatusLabelChanged.emit("Finished Downloading")

            # Store downloaded data into sharedData
            self.dataModelReference.testDataset = mnistTest
            self.dataModelReference.trainDataset = mnistTrain

        else:
            # No db set
            self.errorLabelChanged.emit("Please select a database")
            self.noDatabaseSelectedEdgeCase = True

    def loadCsv(self, csvLocation):
        """
        This method loads the CSV and puts it into memory (Singleton)
        @param csvLocation: File path
        """
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
        """
        Algorithm to determine how much time left.
        @return: Seconds left
        """
        rowsLeft = totalRows-currentRow
        timeSeconds = rowsLeft * averageTimePerRow
        return int(timeSeconds)

