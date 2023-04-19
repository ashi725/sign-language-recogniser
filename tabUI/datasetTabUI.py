from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  *

class DatasetTab(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        
        importDatasetButton = QPushButton('Import dataset')
        importDatasetButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        importDatasetButton.setStyleSheet("font-size: 20px; padding: 10px;")
        importDatasetButton.clicked.connect(self.show_dialog)
        vbox.setAlignment(Qt.AlignHCenter)
        vbox.setContentsMargins
        vbox.addWidget(importDatasetButton)
        vbox.addStretch()
        
        self.setLayout(vbox)
        
    def show_dialog(self):
        dialog = QDialog(self)   
        dialog.setWindowTitle('Import dataset')
        dialog.setFixedWidth(400)
        dropdown = QComboBox(dialog)
        dropdown.addItems(['Not selected', 'MNIST', 'xxxx'])

        self.errorLabel = QLabel("")
        self.errorLabel.setStyleSheet("color: red;")

        downloadButton = QPushButton("Download")
        downloadButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        stopButton = QPushButton("Stop")

        cancelButton = QPushButton("Cancel")
        cancelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cancelButton.clicked.connect(dialog.reject)

        self.progressBar = QProgressBar()
        self.progressPercentage = QLabel("0%")
        self.progressPercentage.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.progressPercentage.setStyleSheet("padding: 0px; margin: 0px;")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignHCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(dropdown)
        hbox.addWidget(downloadButton)

        vbox.addLayout(hbox)
        vbox.addWidget(self.errorLabel)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.progressBar)
        hbox1.addWidget(self.progressPercentage)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(cancelButton)
        vbox.addLayout(hbox2)

        dialog.setLayout(vbox)

        downloadButton.clicked.connect(lambda: self.selectDatabase(dropdown.currentText()))

        dialog.show()

    
    def selectDatabase(self, selectedDatabase):
        print("Clicked button to download dataset")

        if(selectedDatabase == "MNIST"):
            self.errorLabel = QLabel("")
            print('Downloading MNIST dataset...')
            self.downloadMNIST()
            print('MNIST dataset downloaded and saved to directory:')

        elif(selectedDatabase == "xxxx"):
            self.errorLabel = QLabel("")
            print("Selected xxxx")

        else:
            self.errorLabel.setText("Please select a database")
            print("Select a database")

    def downloadMNIST(self):
        print("download")
        # Add code to download MNIST
