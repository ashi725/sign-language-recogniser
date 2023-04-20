from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from models.DataModelSingleton import DataModelSingleton
from models.HyperParametersSingleton import HyperParametersSingleton
from tabUI.TabBaseAbstractClass import TabBaseAbstractClass



class TrainTab(QWidget, TabBaseAbstractClass):

    # Method called whenever this tab is viewed.
    def refreshWindowOnLoad(self):
        self.renderStats()

    def __init__(self):
        super().__init__()
        self.dataModel = DataModelSingleton()
        self.hyperParameters = HyperParametersSingleton()

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        # Database name and number of images
        vboxDetails1 = QVBoxLayout()
        self.databaseNameLabel = QLabel("Database Name: ")
        self.databaseNameLabel.setStyleSheet("font-size: 16px")
        self.numTotalImagesLabel = QLabel("Total # of images: ")
        self.numTotalImagesLabel.setStyleSheet("font-size: 16px")
        vboxDetails1.addWidget(self.databaseNameLabel)
        vboxDetails1.addWidget(self.numTotalImagesLabel)

        # Letters selected and number of images selected
        vboxDetails2 = QVBoxLayout()
        self.numLettersLabel = QLabel("# Letters Displayed: 0")
        self.numLettersLabel.setStyleSheet("font-size: 16px")
        self.numSelectedImagesLabel = QLabel("# Images Displayed: 0")
        self.numSelectedImagesLabel.setStyleSheet("font-size: 16px")
        vboxDetails2.addWidget(self.numLettersLabel)
        vboxDetails2.addWidget(self.numSelectedImagesLabel)

        hboxDetails = QHBoxLayout()
        hboxDetails.addLayout(vboxDetails1)
        hboxDetails.addLayout(vboxDetails2)
        vbox.addLayout(hboxDetails)
        
        # Checkboxes for letters
        cbA = QCheckBox('A:')
        cbB = QCheckBox('B:')
        cbC = QCheckBox('C:')
        cbD = QCheckBox('D:')
        cbE = QCheckBox('E:')
        cbF = QCheckBox('F:')
        cbG = QCheckBox('G:')
        cbH = QCheckBox('H:')
        cbI = QCheckBox('I:')
        cbK = QCheckBox('K:')
        cbL = QCheckBox('L:')
        cbM = QCheckBox('M:')
        cbN = QCheckBox('N:')
        cbO = QCheckBox('O:')
        cbP = QCheckBox('P:')
        cbQ = QCheckBox('Q:')
        cbR = QCheckBox('R:')
        cbS = QCheckBox('S:')
        cbT = QCheckBox('T:')
        cbU = QCheckBox('U:')
        cbV = QCheckBox('V:')
        cbW = QCheckBox('W:')
        cbX = QCheckBox('X:')
        cbY = QCheckBox('Y:')
        aStat = QLabel('0')
        cStat = QLabel('0')
        bStat = QLabel('0')
        dStat = QLabel('0')
        eStat = QLabel('0')
        fStat = QLabel('0')
        gStat = QLabel('0')
        hStat = QLabel('0')
        iStat = QLabel('0')
        kStat = QLabel('0')
        lStat = QLabel('0')
        mStat = QLabel('0')
        nStat = QLabel('0')
        oStat = QLabel('0')
        pStat = QLabel('0')
        qStat = QLabel('0')
        rStat = QLabel('0')
        sStat = QLabel('0')
        tStat = QLabel('0')
        uStat = QLabel('0')
        vStat = QLabel('0')
        wStat = QLabel('0')
        xStat = QLabel('0')
        yStat = QLabel('0')

        self.letterCol1CheckBoxes = [cbA, cbB, cbC, cbD, cbE, cbF, cbG, cbH, cbI, cbK, cbL, cbM]
        self.letterCol1Stats = [aStat, bStat, cStat, dStat, eStat, fStat, gStat, hStat, iStat, kStat, lStat, mStat]
        self.letterCol2CheckBoxes = [cbN, cbO, cbP, cbQ, cbR, cbS, cbT, cbU, cbV, cbW, cbX, cbY]
        self.letterCol2Stats = [nStat, oStat, pStat, qStat, rStat, sStat, tStat, uStat, vStat, wStat, xStat, yStat]

        # Left side Display checkboxes
        hboxLeft = QHBoxLayout()
        checkBoxGrid = QGridLayout()
        hboxLeft.addLayout(checkBoxGrid)

        # # A-M and select all button
        checkBoxGrid.addWidget(self.letterCol2Stats[0], 0, 0)
        checkBoxGrid.addWidget(self.letterCol1CheckBoxes[0], 0, 1)

        tempCounter = 0
        for letterCheckBox in self.letterCol1CheckBoxes:
            checkBoxGrid.addWidget(self.letterCol1CheckBoxes[tempCounter], tempCounter, 0)
            checkBoxGrid.addWidget(self.letterCol1Stats[tempCounter], tempCounter, 1)
            tempCounter += 1
        selectAllButton = QPushButton("Select all")
        selectAllButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        selectAllButton.clicked.connect(self.onSelectAllCheckboxes)
        checkBoxGrid.addWidget(selectAllButton, tempCounter, 0, 1, 2)

        # # N-Y and clear button
        tempCounter = 0
        for letterCheckBox in self.letterCol1CheckBoxes:
            checkBoxGrid.addWidget(self.letterCol2CheckBoxes[tempCounter], tempCounter, 2)
            checkBoxGrid.addWidget(self.letterCol2Stats[tempCounter], tempCounter, 3)
            tempCounter += 1
        selectNoneButton = QPushButton("Clear")
        selectNoneButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        selectNoneButton.clicked.connect(self.onClearButtonCheckboxes)
        checkBoxGrid.addWidget(selectNoneButton, tempCounter, 2, 1, 2)

        # Train, test and view 
        self.trainButton = QRadioButton("Train")
        self.trainButton.setStyleSheet("font-size: 16px")
        self.testButton = QRadioButton("Test")
        self.testButton.setStyleSheet("font-size: 16px")
        self.trainButton.setChecked(True)
        self.trainButton.clicked.connect(self.onRadioButtonPress)
        self.testButton.clicked.connect(self.onRadioButtonPress)
        viewButton = QPushButton("View")
        viewButton.setStyleSheet("font-size: 16px")
        viewButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        viewButton.clicked.connect(self.onViewImagesButton)
        hboxFilters = QHBoxLayout()
        hboxFilters.setAlignment(Qt.AlignCenter)
        hboxFilters.addWidget(self.trainButton)
        hboxFilters.addWidget(self.testButton)
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

        # Images
        imageScrollArea = QScrollArea()
        imageWidget = QWidget()
        self.imageGridLayout = QGridLayout(imageWidget)
        imageScrollArea.setWidgetResizable(True)
        imageScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        imageScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        imageScrollArea.setWidget(imageWidget)
        vboxRight.addWidget(imageScrollArea)

        vboxRight.addLayout(hboxContinueButton)

        # Main layout with letters and images
        hboxMain = QHBoxLayout()
        hboxMain.addLayout(hboxLeft)
        hboxMain.addLayout(vboxRight)
        vbox.addLayout(hboxMain)

        self.setLayout(vbox)

    def renderImages(self, datasetName, labelNumbersList):
        MAX_COLUMNS = 10
        rowIndex = 0
        columnIndex = 0

        dataset = None
        # Get correct dataset
        if (datasetName == 'train'):
            dataset = self.dataModel.trainDataset
        else:
            dataset = self.dataModel.testDataSet

        totalImagesCount = 0

        for labelNumber in labelNumbersList:
            # Check if label exist in dataset. If false skip
            if str(labelNumber) not in dataset.labeledSet:
                continue

            fingerImageList = dataset.labeledSet[str(labelNumber)]

            for fingerImage in fingerImageList:
                imageLabel = QLabel()
                imageLabel.setPixmap(fingerImage.pixMap)
                totalImagesCount += 1
                self.imageGridLayout.addWidget(imageLabel, rowIndex, columnIndex)

                # Grid pos algorithm
                columnIndex += 1
                if (columnIndex > MAX_COLUMNS):
                    columnIndex = 0
                    rowIndex += 1

        # Update Stats
        self.numLettersLabel.setText("# Letters Displayed: {}".format(len(labelNumbersList)))
        self.numSelectedImagesLabel.setText("# Images Displayed: {}".format(totalImagesCount))

    def clearImages(self):
        while self.imageGridLayout.count():
            child = self.imageGridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # This method generates a list of numbers according to labels of the checkbox
    def generateLabelNumberList(self):
        labelsToDisplay = []
        counter= 1
        for chkBox in self.letterCol1CheckBoxes:
            if chkBox.isChecked():
                labelsToDisplay.append(counter)
            counter+=1
        for chkBox in self.letterCol2CheckBoxes:
            if chkBox.isChecked():
                labelsToDisplay.append(counter)
            counter += 1
        return labelsToDisplay

    def renderStats(self):
        dataSet = None
        if (self.trainButton.isChecked()):
            dataSet = self.dataModel.trainDataset
        else:
            dataSet = self.dataModel.testDataSet

        self.databaseNameLabel.setText("Database Name: {}".format(dataSet.databaseName))
        self.numTotalImagesLabel.setText("Total # Images: {}".format(self.dataModel.testDataSet.totalImages + self.dataModel.trainDataset.totalImages))

        totalImagesArrayNumber = dataSet.totalImagesArray

        # Col1 stats
        tempCounter = 0
        for statLabel in self.letterCol1Stats:
            statLabel.setText(str(totalImagesArrayNumber[tempCounter]))
            tempCounter += 1
        # Col2 Stats
        for statLabel in self.letterCol2Stats:
            statLabel.setText(str(totalImagesArrayNumber[tempCounter]))
            tempCounter += 1

    def show_dialog(self):
        self.dialog = QDialog(self)   
        self.dialog.setWindowTitle(self.hyperParameters.dataset + "[numimages" + "1" + "]")
        self.dialog.resize(400, 300)   

        # Model dropdown
        hboxModel = QHBoxLayout()
        modelLabel = QLabel("Model: ")
        self.modelDropdown = QComboBox()
        self.modelDropdown.addItems(["Not selected","LeNet-5", "ResNet", "xxxx"])
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
        self.trainDialog.setWindowTitle(self.hyperParameters.dataset + "[numimages" + "1" +"]")
        self.trainDialog.resize(400, 300)
        
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

    def onSelectAllCheckboxes(self):
        for chkBox in self.letterCol1CheckBoxes:
            chkBox.setChecked(True)
        for chkBox in self.letterCol2CheckBoxes:
            chkBox.setChecked(True)

    def onClearButtonCheckboxes(self):
        for chkBox in self.letterCol1CheckBoxes:
            chkBox.setChecked(False)
        for chkBox in self.letterCol2CheckBoxes:
            chkBox.setChecked(False)

    def onViewImagesButton(self):
        self.clearImages()
        datasetName = None
        if self.trainButton.isChecked() and not self.testButton.isChecked():
            datasetName = "train"
        elif not self.trainButton.isChecked() and self.testButton.isChecked():
            datasetName = "test"
        else:
            print("ERROR TRAIN/TEST RADIO NOT SELECTED")
            return
        self.renderImages(datasetName, self.generateLabelNumberList())

    def onContinueButton(self):
        pass

    def onRadioButtonPress(self):
        self.renderStats()




