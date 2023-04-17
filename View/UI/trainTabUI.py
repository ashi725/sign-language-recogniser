from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class TrainTab(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        self.databaseNameLabel = QLabel("Database Name: ")
        self.databaseNameLabel.setStyleSheet("font-size: 16px")
        vbox.addWidget(self.databaseNameLabel)

        self.numImagesLabel = QLabel("Number of images: ")
        self.numImagesLabel.setStyleSheet("font-size: 16px")
        vbox.addWidget(self.numImagesLabel)

        
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

        vboxCol1 = QVBoxLayout()
        vboxCol2 = QVBoxLayout()

        for letterCheckBox in letterCol1CheckBoxes:
            letterCheckBox.setStyleSheet("font-size: 16px")
            vboxCol1.addWidget(letterCheckBox)

        for letterCheckBox in letterCol2CheckBoxes:
            letterCheckBox.setStyleSheet("font-size: 16px")
            vboxCol2.addWidget(letterCheckBox)


        # Two columns
        hboxLetters = QHBoxLayout()
        hboxLetters.addLayout(vboxCol1)
        hboxLetters.addLayout(vboxCol2)

        vboxFilters = QVBoxLayout()
        vboxFilters.setAlignment(Qt.AlignTop)
        trainButton = QRadioButton("Train")
        trainButton.setStyleSheet("font-size: 16px")
        testButton = QRadioButton("Test")
        testButton.setStyleSheet("font-size: 16px")
        self.numLettersLabel = QLabel("Letters selected: ")
        self.numLettersLabel.setStyleSheet("font-size: 16px")
        self.numImagesLabel = QLabel("Total images: ")
        self.numImagesLabel.setStyleSheet("font-size: 16px")
        viewButton = QPushButton("View")
        viewButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        vboxFilters.addWidget(trainButton)
        vboxFilters.addWidget(testButton)
        vboxFilters.addWidget(self.numLettersLabel)
        vboxFilters.addWidget(self.numImagesLabel)
        vboxFilters.addWidget(viewButton)

        hboxFilters = QHBoxLayout()
        hboxFilters.addLayout(hboxLetters)
        hboxFilters.addLayout(vboxFilters)
        vbox.addLayout(hboxFilters)

        selectAllButton = QPushButton("Select all")
        selectAllButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        selectNoneButton = QPushButton("Clear")
        selectNoneButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        vboxCol1.addWidget(selectAllButton)
        vboxCol2.addWidget(selectNoneButton)

        self.setLayout(vbox)

