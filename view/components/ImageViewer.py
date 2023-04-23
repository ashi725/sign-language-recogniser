from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from models.singletons.DataModelSingleton import DataModelSingleton, convertIndexArrToAlphabetIndex
from models.singletons.HyperParametersSingleton import HyperParametersSingleton
from view.components.SelectableLabel import SelectableLabel


class ImageViewer(QWidget):
    """
    This class contains a widget to view images in the data singleton
    It also provides functionality to select imgs
    """
    def __init__(self):
        super().__init__()

        # Init vars
        self.dataModel = DataModelSingleton()
        self.hyperParameters = HyperParametersSingleton()
        self.imageLabelList = []

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
        imageScrollArea.setWidget(imageWidget)
        vboxRight.addWidget(imageScrollArea)

        # Main layout with letters and images
        hboxMain = QHBoxLayout()
        hboxMain.addLayout(hboxLeft)
        hboxMain.addLayout(vboxRight)
        vbox.addLayout(hboxMain)

        self.setLayout(vbox)

    def renderImages(self, datasetName, labelNumbersListArrForm):
        """
        Renders all images whose label is in the labelNumbersListArrForm arr.
        The images are taken from inside the datasetName [Train, Test]
        @param datasetName: [Train, test]
        @param labelNumbersListArrForm: Array form classes to dispaly
        @return:
        """
        MAX_COLUMNS = 10
        rowIndex = 0
        columnIndex = 0

        dataset = None
        # Get correct dataset
        if (datasetName == 'train'):
            dataset = self.dataModel.trainDataset
        else:
            dataset = self.dataModel.testDataset

        totalImagesCount = 0

        for labelArrFormNumber in labelNumbersListArrForm:
            # Check if label exist in dataset. If false skip
            if str(convertIndexArrToAlphabetIndex(labelArrFormNumber)) not in dataset.labeledSet:
                continue

            fingerImageList = dataset.labeledSet[str(convertIndexArrToAlphabetIndex(labelArrFormNumber))]

            for fingerImage in fingerImageList:
                # Load image details
                imageLabel = SelectableLabel(fingerImage)
                imageLabel.setPixmap(fingerImage.pixMap)
                totalImagesCount += 1

                # Render
                self.imageGridLayout.addWidget(imageLabel, rowIndex, columnIndex)
                self.imageLabelList.append(imageLabel)
                # Grid pos algorithm
                columnIndex += 1
                if (columnIndex > MAX_COLUMNS):
                    columnIndex = 0
                    rowIndex += 1

        # Update Stats
        self.numLettersLabel.setText("# Letters Displayed: {}".format(len(labelNumbersListArrForm)))
        self.numSelectedImagesLabel.setText("# Images Displayed: {}".format(totalImagesCount))


    def clearImages(self):
        """
        This method clears all image on the gridpane
        """
        self.imageLabelList = []
        while self.imageGridLayout.count():
            child = self.imageGridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def generateLabelNumberList(self):
        """
        This method returns a array containing the label class that are checked
        @return: Array indices in alphabet form
        """
        labelsToDisplay = [] # In alphabet index form
        counter = 0

        # Go through col1 checkboxes
        for chkBox in self.letterCol1CheckBoxes:
            if chkBox.isChecked():
                labelsToDisplay.append(counter)
            counter += 1

        # Go through col2 chkboxes
        for chkBox in self.letterCol2CheckBoxes:
            if chkBox.isChecked():
                labelsToDisplay.append(counter)
            counter += 1

        return labelsToDisplay

    def renderStats(self):
        """
        This method renders all the stats on the page
        @return:
        """

        # Grab which dataset [Train,test]
        dataset = None
        if (self.trainButton.isChecked()):
            dataset = self.dataModel.trainDataset
        else:
            dataset = self.dataModel.testDataset

        # Display header stats
        self.databaseNameLabel.setText("Database Name: {}".format(dataset.databaseName))
        self.numTotalImagesLabel.setText("Total # Images: {}".format(
        self.dataModel.testDataset.totalImages + self.dataModel.trainDataset.totalImages))

        totalImagesArrayNumber = dataset.totalImagesArray

        # Col1 stats
        tempArrIndexCounter = 0
        for statLabel in self.letterCol1Stats:
            statLabel.setText(str(totalImagesArrayNumber[tempArrIndexCounter]))
            tempArrIndexCounter += 1

        # Col2 Stats
        for statLabel in self.letterCol2Stats:
            statLabel.setText(str(totalImagesArrayNumber[tempArrIndexCounter]))
            tempArrIndexCounter += 1

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

        # Determine whether test/train dataset user wants to see
        if self.trainButton.isChecked() and not self.testButton.isChecked():
            datasetName = "train"
        elif not self.trainButton.isChecked() and self.testButton.isChecked():
            datasetName = "test"
        else:
            print("ERROR TRAIN/TEST RADIO NOT SELECTED")
            return
        # Render imgs
        self.renderImages(datasetName, self.generateLabelNumberList())

    def onRadioButtonPress(self):
        # Radio switching between test/train
        self.renderStats()

    def getSelectedImages(self):
        """
        Method that returns the selected images
        @return: Arr containing ImageDetail() objects
        """
        selectedImages = []
        for selectableLabel in self.imageLabelList:
            # If selected, append
            if selectableLabel.is_selected():
                selectedImages.append(selectableLabel.imageDetails)
        return selectedImages
