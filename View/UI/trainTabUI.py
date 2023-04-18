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

