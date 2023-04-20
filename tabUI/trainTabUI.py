import os
from subprocess import Popen
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from models.DataModelSingleton import DataModelSingleton
from models.HyperParametersSingleton import HyperParametersSingleton
from models.ModelRunnerThread import ModelTrainerThread
from tabUI.ImageViewer import ImageViewer
from tabUI.TabBaseAbstractClass import TabBaseAbstractClass



class TrainTab(QWidget, TabBaseAbstractClass):

    # Method called whenever this tab is viewed.
    def refreshWindowOnLoad(self):
        self.imgView.renderStats()

    def __init__(self):
        super().__init__()
        self.dataModel = DataModelSingleton()
        self.hyperParameters = HyperParametersSingleton()
        self.modelTrainerRunner = None

        gridLayout = QGridLayout()
        self.setLayout(gridLayout)

        # Image Viewer
        self.imgView = ImageViewer()
        gridLayout.addWidget(self.imgView, 0, 0)

        # Continue Button
        continueButton = QPushButton("Continue")
        continueButton.setStyleSheet("font-size: 16px")
        continueButton.clicked.connect(self.show_dialog)
        gridLayout.addWidget(continueButton, 1, 0)

    def show_dialog(self):
        self.dialog = QDialog(self)   
        self.dialog.setWindowTitle(self.hyperParameters.dataset + "[numimages" + "1" + "]")
        self.dialog.resize(400, 300)   

        # Model dropdown
        hboxModel = QHBoxLayout()
        modelLabel = QLabel("Model: ")
        self.modelDropdown = QComboBox()
        self.modelDropdown.addItems(["Not selected","lenet5", "resnet", "xxxx"])
        self.modelDropdown.currentTextChanged.connect(self.change_modelDropdown)
        hboxModel.addWidget(modelLabel)
        hboxModel.addWidget(self.modelDropdown)

        # Batchsize dropdown
        hboxBatchsize = QHBoxLayout()
        batchsizeLabel = QLabel("Batchsize: ")
        self.spinboxBatchsize = QSpinBox()
        self.spinboxBatchsize.setRange(0, 500)
        self.spinboxBatchsize.valueChanged.connect(self.change_spinboxBatchsize)
        hboxBatchsize.addWidget(batchsizeLabel)
        hboxBatchsize.addWidget(self.spinboxBatchsize)

        # Epoch number dropdown
        hboxEpochNum = QHBoxLayout()
        epochNumLabel = QLabel("Epoch Number: ")
        self.spinboxEpochNum = QSpinBox()
        self.spinboxEpochNum.setRange(0, 10)
        self.spinboxEpochNum.valueChanged.connect(self.change_spinboxEpochNum)
        hboxEpochNum.addWidget(epochNumLabel)
        hboxEpochNum.addWidget(self.spinboxEpochNum)

        # Test and validation splitter
        hboxSplitter = QHBoxLayout()
        vboxTrain = QVBoxLayout()
        vboxSlider = QVBoxLayout()
        vboxValidate = QVBoxLayout()

        trainLabel = QLabel("Train")
        self.spinboxTrain = QSpinBox()
        self.spinboxTrain.setRange(0, 100)
        
        sliderInfoLabel = QLabel("Both must be at least 10%")
        sliderInfoLabel.setAlignment(Qt.AlignCenter)
        sliderInfoLabel.setStyleSheet("font-size: 10px;")
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(50)
        
        validateLabel = QLabel("Validate")
        self.spinboxValidate = QSpinBox()
        self.spinboxValidate.setRange(0, 100)
        
        # Link values to each other
        self.slider.valueChanged.connect(lambda value: self.spinboxTrain.setValue(value))
        self.slider.valueChanged.connect(lambda value: self.spinboxValidate.setValue(100-value))
        self.spinboxTrain.valueChanged.connect(lambda value: self.slider.setValue(value))
        self.spinboxValidate.valueChanged.connect(lambda value: self.slider.setValue(100-value))

        # Update parameters in singleton
        self.slider.valueChanged.connect(self.change_slider)

        vboxTrain.addWidget(trainLabel)
        vboxTrain.addWidget(self.spinboxTrain)
        hboxSplitter.addLayout(vboxTrain)
        vboxSlider.addWidget(sliderInfoLabel)
        vboxSlider.addWidget(self.slider)
        hboxSplitter.addLayout(vboxSlider)
        vboxValidate.addWidget(validateLabel)
        vboxValidate.addWidget(self.spinboxValidate)
        hboxSplitter.addLayout(vboxValidate)

        # Train model button
        trainModelButton = QPushButton("Train model")
        trainModelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        trainModelButton.clicked.connect(self.on_train_model_button)
        trainModelButton.clicked.connect(self.dialog.reject)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hboxModel)
        vbox.addLayout(hboxBatchsize)
        vbox.addLayout(hboxEpochNum)
        vbox.addLayout(hboxSplitter)

        vboxButton = QVBoxLayout()
        vboxButton.setAlignment(Qt.AlignCenter)
        vboxButton.addWidget(trainModelButton)

        vboxAll = QVBoxLayout()
        vboxAll.addLayout(vbox)
        vboxAll.addLayout(vboxButton)

        self.dialog.setLayout(vboxAll)
        self.dialog.show()
        


    def show_train_dialog(self):

        print("training model...")
        self.modelTrainerRunner = ModelTrainerThread(self.hyperParameters)
        self.modelTrainerRunner.start()
        self.modelTrainerRunner.statusUpdate.connect(self.updateTrainingDataText)

        self.trainDialog = QDialog(self)
        self.trainDialog.setWindowTitle(self.hyperParameters.dataset + "[numimages" + "1" +"]")
        self.trainDialog.resize(400, 300)
        self.trainDialog.setModal(True)
        
        vbox = QVBoxLayout()
        hboxInfo = QHBoxLayout()
        vboxHyperparameters = QVBoxLayout()
        vboxHyperparameters.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        cnnLabel = QLabel("CNN Name: " + self.hyperParameters.modelName)
        batchsizeLabel = QLabel("Batch Size: " + str(self.hyperParameters.batchsize))
        epochNumLabel = QLabel("Epoch Number: " + str(self.hyperParameters.epochs))
        trainLabel = QLabel("Train Set Size: " + str(self.hyperParameters.train))
        validationLabel = QLabel("Validation Set Size: " + str(self.hyperParameters.validation))
        testLabel = QLabel("Test Set Size: " + str(self.hyperParameters.test))
        vboxHyperparameters.addWidget(cnnLabel)
        vboxHyperparameters.addWidget(batchsizeLabel)
        vboxHyperparameters.addWidget(epochNumLabel)
        vboxHyperparameters.addWidget(trainLabel)
        vboxHyperparameters.addWidget(validationLabel)
        vboxHyperparameters.addWidget(testLabel)

        # Training progress data
        self.trainingData = QTextEdit()
        self.trainingData.setReadOnly(True)
        self.trainingData.setText("Training progress data goes here")

        hboxInfo.addLayout(vboxHyperparameters)
        hboxInfo.addWidget(self.trainingData)

        # Progress bar
        progressBar = QProgressBar(self)
        progressBar.setRange(0, 100)
        progressBar.setValue(0)

        # Cancel Button
        hboxButtons = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hboxButtons.addWidget(self.cancelButton)
        #self.cancelButton.clicked.connect(self.trainDialog.reject)
        self.cancelButton.clicked.connect(self.showFinishedButtons) # just here for now to test the buttons

        # 3 different buttons after training finishes - train new model, save as, test model
        self.trainNewModelButton = QPushButton("Train new model")
        self.trainNewModelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.trainNewModelButton.clicked.connect(self.trainDialog.reject)

        self.saveAsButton = QPushButton("Save as")
        self.saveAsButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.saveAsButton.clicked.connect(self.showSaveAs)

        self.testModelButton = QPushButton("Test model")
        self.testModelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.trainNewModelButton.clicked.connect(self.trainDialog.reject) # Close dialog and open test tab

        hboxButtons.addWidget(self.trainNewModelButton)
        hboxButtons.addWidget(self.saveAsButton)
        hboxButtons.addWidget(self.testModelButton)
        self.trainNewModelButton.setVisible(False)
        self.saveAsButton.setVisible(False)
        self.testModelButton.setVisible(False)
        
        vbox.addLayout(hboxInfo)
        vbox.addWidget(progressBar)
        vbox.addLayout(hboxButtons)

        self.trainDialog.setLayout(vbox)
        self.trainDialog.show()

    def change_spinboxEpochNum(self):
        self.hyperParameters.epochs = self.spinboxEpochNum.value()

    def change_spinboxBatchsize(self):
        self.hyperParameters.batchsize = self.spinboxBatchsize.value()
    
    def change_modelDropdown(self):
        self.hyperParameters.modelName = self.modelDropdown.currentText()
    
    def change_slider(self):
        self.hyperParameters.train = self.slider.value()
        self.hyperParameters.validation = 100 - self.slider.value()
        self.hyperParameters.test = 0
        self.spinboxTrain.setValue(self.hyperParameters.train)
        self.spinboxValidate.setValue(self.hyperParameters.validation)

    # Call after training finished
    def showFinishedButtons(self):
        print("finished training")
        self.cancelButton.setVisible(False)
        self.trainNewModelButton.setVisible(True)
        self.saveAsButton.setVisible(True)
        self.testModelButton.setVisible(True)

        self.modelTrainerRunner.stop()

    # Dialog to save model
    def showSaveAs(self):
        print("save as")
        self.saveAsDialog = QDialog(self)
        self.saveAsDialog.setWindowTitle('Save as')

        self.modelName = QTextEdit()
        self.modelName.setFixedSize(200, 20)

        saveButton = QPushButton("Save")
        saveButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        saveButton.clicked.connect(self.saveAsDialog.reject)
        saveButton.clicked.connect(self.save)

        cancelButton = QPushButton("Cancel")
        cancelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cancelButton.clicked.connect(self.saveAsDialog.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(saveButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.modelName)
        vbox.addLayout(hbox)

        self.saveAsDialog.setLayout(vbox)
        self.saveAsDialog.show()

    # save the model
    def save(self):
        print("save")
        # code to save model somewhere?

    def onContinueButton(self):
        pass

    def on_train_model_button(self):
        self.show_train_dialog()

    def updateTrainingDataText(self, text):
        self.trainingData.setText(text)
