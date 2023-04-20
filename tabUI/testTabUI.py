from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from tabUI.TabBaseAbstractClass import TabBaseAbstractClass

class TestTab(QWidget, TabBaseAbstractClass):
    def refreshWindowOnLoad(self):
        pass
    
    def __init__(self):
        super().__init__()

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
        hboxButtons.addWidget(datasetImagesButton)
        hboxButtons.addWidget(webcamButton)

        vbox.addLayout(hboxButtons)

        self.setLayout(vbox)

    def show_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')

    def show_dataset_dialog(self):
        print("dataset")
