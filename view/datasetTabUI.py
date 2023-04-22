from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont

from models.singletons.DataModelSingleton import DataModelSingleton
from models.singletons.HyperParametersSingleton import HyperParametersSingleton
from view.components.DownloadThread import DownloadThread
from view.TabBaseAbstractClass import TabBaseAbstractClass


class DatasetTab(QWidget,TabBaseAbstractClass):
    """
    This class contains the main tab for loading a dataset
    """
    def refreshWindowOnLoad(self):
        pass

    def __init__(self, disableTrainTabFunc):
        super().__init__()

        # Init variables
        self.dataModel = DataModelSingleton()
        self.hyperParameters = HyperParametersSingleton()
        self.downloadThreadInstance = None
        self.disableTrainTabFunc = disableTrainTabFunc

        # Logo
        self.imageLabel = QLabel(self)
        pixmap = QPixmap("resources/logo.png")
        scaled_pixmap = pixmap.scaled(300, 300)
        self.imageLabel.setPixmap(scaled_pixmap)

        # Title
        titleLabel = QLabel("Sign Language Recogniser")
        titleLabel.setStyleSheet("font-size: 30px; font-weight: bold; padding: 30px;")

        # Import Button
        importDatasetButton = QPushButton('Import dataset')
        importDatasetButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        importDatasetButton.setStyleSheet("font-size: 20px; padding: 10px;")
        importDatasetButton.clicked.connect(self.showImportDialog)

        # Vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.imageLabel, alignment=Qt.AlignCenter)
        vbox.addWidget(titleLabel, alignment=Qt.AlignCenter)
        vbox.addWidget(importDatasetButton, alignment=Qt.AlignCenter)
        vbox.addStretch()

        # Horizontal layout
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()

        # Set layout
        self.setLayout(hbox)

    
    def showImportDialog(self):
        """
        This method shows the import dialogue
        @return:
        """

        # Dialogue settings
        dialog = QDialog(self)   
        dialog.setModal(True)
        dialog.setWindowTitle('Import dataset')
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        dialog.setFixedSize(600, 200)

        # Dropdown for datatype
        self.dropdown = QComboBox(dialog)
        self.dropdown.setFixedWidth(200)
        self.dropdown.addItems(['Not selected', 'MNIST', 'Custom'])
        self.dropdown.currentIndexChanged.connect(self.dropdown_changed)

        # Error Label
        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet("color: red;")

        # Download/Stop Button
        self.downloadButton = QPushButton("Download")
        self.downloadButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton = QPushButton("Stop")
        self.stopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton.setDisabled(True)

        # Cancel Button
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cancelButton.clicked.connect(dialog.reject)

        # Progress Widgets
        self.progressBar = QProgressBar()
        self.progressBar.setFixedSize(200, 20)
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
        self.downloadButton.clicked.connect(lambda: self.onDownloadDatabaseButton(self.dropdown.currentText()))
        self.stopButton.clicked.connect(self.onStopDownloadButton)

        dialog.show()    

    def dropdown_changed(self):
        self.hyperParameters.dataset = self.dropdown.currentText()
        print("drop down changed to " + self.dropdown.currentText() )
    
    def onDownloadDatabaseButton(self, selectedDatabase):
        """
        This method is called when the download button is pressed.
        It starts downloading the dataset.
        @param selectedDatabase: Datatype to download
        """
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

    def updateProgressBar(self, progressBarValue):
        self.progressBar.setValue(progressBarValue)

    def updateTimerLabel(self, labelText):
        self.progressPercentage.setText(labelText)

    def updateDownloadStatusLabel(self, labelText):
        self.downloadStatusLabel.setText(labelText)

    def updateErrorLabel(self, labelText):
        self.errorLabel.setText(labelText)

    def onDownloadFinish(self, data):
        """
        This method is called once download is finished
        @param data: The download status. 0=Successful. Else fail
        @return:
        """
        self.downloadButton.setDisabled(False)
        self.stopButton.setDisabled(True)
        self.cancelButton.setDisabled(False)

        # If data = 0 then download successful. Redirect to different tab
        if data == 0:
            self.disableTrainTabFunc(True)


