from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class TrainTab(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        vboxDetails1 = QVBoxLayout()
        self.databaseNameLabel = QLabel("Database Name: ")
        self.databaseNameLabel.setStyleSheet("font-size: 16px")
        self.numImagesLabel = QLabel("Number of images: ")
        self.numImagesLabel.setStyleSheet("font-size: 16px")
        vboxDetails1.addWidget(self.databaseNameLabel)
        vboxDetails1.addWidget(self.numImagesLabel)

        vboxDetails2 = QVBoxLayout()
        self.numLettersLabel = QLabel("Letters selected: ")
        self.numLettersLabel.setStyleSheet("font-size: 16px")
        self.numImagesLabel = QLabel("Total images: ")
        self.numImagesLabel.setStyleSheet("font-size: 16px")
        vboxDetails2.addWidget(self.numLettersLabel)
        vboxDetails2.addWidget(self.numImagesLabel)

        hboxDetails = QHBoxLayout()
        hboxDetails.addLayout(vboxDetails1)
        hboxDetails.addLayout(vboxDetails2)
        vbox.addLayout(hboxDetails)
        
        cbA = QCheckBox('A: ', self)
        cbB = QCheckBox('B: ', self)
        cbC = QCheckBox('C: ', self)
        cbD = QCheckBox('D: ', self)
        cbE = QCheckBox('E: ', self)
        cbF = QCheckBox('F: ', self)
        cbG = QCheckBox('G: ', self)
        cbH = QCheckBox('H: ', self)
        cbI = QCheckBox('I: ', self)
        cbK = QCheckBox('K: ', self)
        cbL = QCheckBox('L: ', self)
        cbM = QCheckBox('M: ', self)
        cbN = QCheckBox('N: ', self)
        cbO = QCheckBox('O: ', self)
        cbP = QCheckBox('P: ', self)
        cbQ = QCheckBox('Q: ', self)
        cbR = QCheckBox('R: ', self)
        cbS = QCheckBox('S: ', self)
        cbT = QCheckBox('T: ', self)
        cbU = QCheckBox('U: ', self)
        cbV = QCheckBox('V: ', self)
        cbW = QCheckBox('W: ', self)
        cbX = QCheckBox('X: ', self)
        cbY = QCheckBox('Y: ', self)

        letterCol1CheckBoxes = [cbA, cbB, cbC, cbD, cbE, cbF, cbG, cbH, cbI, cbK, cbL, cbM]
        letterCol2CheckBoxes = [cbN, cbO, cbP, cbQ, cbR, cbS, cbT, cbU, cbV, cbW, cbX, cbY]
        
        # A-M and select all button
        vboxLetters1 = QVBoxLayout()
        for letterCheckBox in letterCol1CheckBoxes:
            letterCheckBox.setStyleSheet("font-size: 16px")
            vboxLetters1.addWidget(letterCheckBox)
        
        selectAllButton = QPushButton("Select all")
        selectAllButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        vboxLetters1.addWidget(selectAllButton)

        # N-Y and clear button
        vboxLetters2 = QVBoxLayout()
        for letterCheckBox in letterCol2CheckBoxes:
            letterCheckBox.setStyleSheet("font-size: 16px")
            vboxLetters2.addWidget(letterCheckBox)
        
        selectNoneButton = QPushButton("Clear")
        selectNoneButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        vboxLetters2.addWidget(selectNoneButton)

        # Left side of main layout - letters and select/clear buttons
        hboxLeft = QHBoxLayout()
        hboxLeft.addLayout(vboxLetters1)
        hboxLeft.addLayout(vboxLetters2)


        # Train, test and view 
        trainButton = QRadioButton("Train")
        trainButton.setStyleSheet("font-size: 16px")
        testButton = QRadioButton("Test")
        testButton.setStyleSheet("font-size: 16px")
        viewButton = QPushButton("View")
        viewButton.setStyleSheet("font-size: 16px")
        viewButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hboxFilters = QHBoxLayout()
        hboxFilters.setAlignment(Qt.AlignCenter)
        hboxFilters.addWidget(trainButton)
        hboxFilters.addWidget(testButton)
        hboxFilters.addWidget(viewButton)

        # Continue button
        hboxContinueButton = QHBoxLayout()
        hboxContinueButton.setAlignment(Qt.AlignRight)
        continueButton = QPushButton("Continue")
        continueButton.setStyleSheet("font-size: 16px")
        continueButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        continueButton.clicked.connect(self.show_dialog)
        hboxContinueButton.addWidget(continueButton)

        # Right side of main layout - train, test, view, images, and continue button
        vboxRight = QVBoxLayout()
        vboxRight.setAlignment(Qt.AlignCenter)
        vboxRight.addLayout(hboxFilters)
        spacer = QLabel("images go here")
        spacer.setStyleSheet("font-size: 30px; padding: 200px 100px 200px 100px")
        vboxRight.addWidget(spacer)
        vboxRight.addLayout(hboxContinueButton)

        # Main layout with letters and images
        hboxMain = QHBoxLayout()
        hboxMain.addLayout(hboxLeft)
        hboxMain.addLayout(vboxRight)
        vbox.addLayout(hboxMain)

        self.setLayout(vbox)

    def show_dialog(self):
        self.dialog = QDialog(self)   
        self.dialog.setWindowTitle('\"Database Name\" [\"Num images\"]')
        self.dialog.resize(400, 300)   

        # Model dropdown
        hboxModel = QHBoxLayout()
        modelLabel = QLabel("Model: ")
        self.modelDropdown = QComboBox()
        self.modelDropdown.addItems(["Not selected","LeNet-5", "ResNet", "xxxx"])
        hboxModel.addWidget(modelLabel)
        hboxModel.addWidget(self.modelDropdown)

        # Batchsize dropdown
        hboxBatchsize = QHBoxLayout()
        batchsizeLabel = QLabel("Batchsize: ")
        self.spinboxBatchsize = QSpinBox()
        self.spinboxBatchsize.setRange(0, 500)
        hboxBatchsize.addWidget(batchsizeLabel)
        hboxBatchsize.addWidget(self.spinboxBatchsize)

        # Epoch number dropdown
        hboxEpochNum = QHBoxLayout()
        epochNumLabel = QLabel("Epoch Number: ")
        self.spinboxEpochNum = QSpinBox()
        self.spinboxEpochNum.setRange(0, 10)
        hboxEpochNum.addWidget(epochNumLabel)
        hboxEpochNum.addWidget(self.spinboxEpochNum)

        # Test and validation splitter
        hboxSplitter = QHBoxLayout()
        vboxTrain = QVBoxLayout()
        trainLabel = QLabel("Train")
        vboxTrain.addWidget(trainLabel)
        self.spinboxTrain = QSpinBox()
        self.spinboxTrain.setRange(0, 100)
        vboxTrain.addWidget(self.spinboxTrain)
        hboxSplitter.addLayout(vboxTrain)
        vboxSlider = QVBoxLayout()
        sliderInfoLabel = QLabel("Both must be at least 10%")
        sliderInfoLabel.setAlignment(Qt.AlignCenter)
        sliderInfoLabel.setStyleSheet("font-size: 10px;")
        vboxSlider.addWidget(sliderInfoLabel)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(50)
        vboxSlider.addWidget(self.slider)
        hboxSplitter.addLayout(vboxSlider)
        vboxValidate = QVBoxLayout()
        validateLabel = QLabel("Validate")
        vboxValidate.addWidget(validateLabel)
        self.spinboxValidate = QSpinBox()
        self.spinboxValidate.setRange(0, 100)
        vboxValidate.addWidget(self.spinboxValidate)
        hboxSplitter.addLayout(vboxValidate)

        # Train model button
        trainModelButton = QPushButton("Train model")
        trainModelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        trainModelButton.clicked.connect(self.train_model)
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
        
    def train_model(self):
        print("train model")
        
        self.show_train_dialog()

    def show_train_dialog(self):
        print("training model...")
        self.trainDialog = QDialog(self)
        self.trainDialog.setWindowTitle('\"Database Name\" [\"Num images\"]')
        self.trainDialog.resize(400, 300)
        
        vbox = QVBoxLayout()
        hboxInfo = QHBoxLayout()
        vboxHyperparameters = QVBoxLayout()
        vboxHyperparameters.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        cnnLabel = QLabel("CNN Name: ")
        batchsizeLabel = QLabel("Batch Size: ")
        epochNumLabel = QLabel("Epoch Number: ")
        trainLabel = QLabel("Train Set Size: ")
        validationLabel = QLabel("Validation Set Size: ")
        testLabel = QLabel("Test Set Size: ")
        vboxHyperparameters.addWidget(cnnLabel)
        vboxHyperparameters.addWidget(batchsizeLabel)
        vboxHyperparameters.addWidget(epochNumLabel)
        vboxHyperparameters.addWidget(trainLabel)
        vboxHyperparameters.addWidget(validationLabel)
        vboxHyperparameters.addWidget(testLabel)

        # Training progress data
        trainingData = QTextEdit()
        trainingData.setReadOnly(True)
        trainingData.setText("Training progress data goes here")

        hboxInfo.addLayout(vboxHyperparameters)
        hboxInfo.addWidget(trainingData)

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

    # Call after training finished
    def showFinishedButtons(self):
        print("finished training")
        self.cancelButton.setVisible(False)
        self.trainNewModelButton.setVisible(True)
        self.saveAsButton.setVisible(True)
        self.testModelButton.setVisible(True)
    
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
        print("saved")
        # code to save model somewhere?


