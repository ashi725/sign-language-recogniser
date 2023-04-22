from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from models.singletons.DataModelSingleton import DataModelSingleton
from models.singletons.HyperParametersSingleton import HyperParametersSingleton
from models.PyModelTrainThread import PyModelTrainThread
from models.save_mechanism.ModelSaver import SaveMechanism
from view.components.ImageViewer import ImageViewer
from view.TabBaseAbstractClass import TabBaseAbstractClass



class TrainTab(QWidget, TabBaseAbstractClass):
    """
    This is the main tab for training a model
    """
    # Method called whenever this tab is viewed.
    def refreshWindowOnLoad(self):
        # Render the stats for image dispaly
        self.imgView.renderStats()

    def __init__(self):
        # init vars
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
        continueButton.clicked.connect(self.show_train_dialogue_settings)
        gridLayout.addWidget(continueButton, 1, 0)

    def show_train_dialogue_settings(self):
        """
        This method is called on train button. It opens a dialgoue for training
        @return:
        """
        # Dialogue settings
        self.dialog = QDialog(self)   
        self.dialog.setWindowTitle("Training Model")
        self.dialog.resize(400, 300)   

        # Model dropdown
        hboxModel = QHBoxLayout()
        modelLabel = QLabel("Model: ")
        self.modelDropdown = QComboBox()
        self.modelDropdown.addItems(["lenet5", "resnet"])
        self.modelDropdown.setCurrentIndex(0)
        self.modelDropdown.currentTextChanged.connect(self.change_modelDropdown)
        hboxModel.addWidget(modelLabel)
        hboxModel.addWidget(self.modelDropdown)

        # Batchsize dropdown
        hboxBatchsize = QHBoxLayout()
        batchsizeLabel = QLabel("Batchsize: ")
        self.spinboxBatchsize = QSpinBox()
        self.spinboxBatchsize.setRange(1, 500)
        self.spinboxBatchsize.setValue(100)
        self.spinboxBatchsize.valueChanged.connect(self.change_spinboxBatchsize)
        hboxBatchsize.addWidget(batchsizeLabel)
        hboxBatchsize.addWidget(self.spinboxBatchsize)

        # Epoch number dropdown
        hboxEpochNum = QHBoxLayout()
        epochNumLabel = QLabel("Epoch Number: ")
        self.spinboxEpochNum = QSpinBox()
        self.spinboxEpochNum.setRange(1, 10)
        self.spinboxEpochNum.setValue(2)
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
        self.spinboxTrain.setRange(10, 90)
        self.spinboxTrain.setValue(50)

        sliderInfoLabel = QLabel("Both must be at least 10%")
        sliderInfoLabel.setAlignment(Qt.AlignCenter)
        sliderInfoLabel.setStyleSheet("font-size: 10px;")
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(10, 90)
        self.slider.setValue(50)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(50)
        
        validateLabel = QLabel("Validate")
        self.spinboxValidate = QSpinBox()
        self.spinboxValidate.setValue(50)
        self.spinboxValidate.setRange(10, 90)
        
        # Link values to each other
        self.slider.valueChanged.connect(lambda value: self.spinboxTrain.setValue(value))
        self.slider.valueChanged.connect(lambda value: self.spinboxValidate.setValue(100-value))
        self.spinboxTrain.valueChanged.connect(lambda value: self.slider.setValue(value))
        self.spinboxValidate.valueChanged.connect(lambda value: self.slider.setValue(100-value))

        # Update parameters in singleton
        self.slider.valueChanged.connect(self.change_slider)

        # Layout settings
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

        # Layout settings
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

        # Refresh the singleton values
        self.change_modelDropdown()
        self.change_spinboxBatchsize()
        self.change_spinboxEpochNum()
        self.change_slider()

        # Layout settings
        self.dialog.setLayout(vboxAll)
        self.dialog.show()


    def show_train_dialog(self):
        """
        This method is the training process dialogue
        """

        # Attach signal listeners
        print("training model...")
        self.modelTrainerRunner = PyModelTrainThread(self.hyperParameters, self.dataModel)
        self.modelTrainerRunner.start()
        self.modelTrainerRunner.statusUpdate.connect(self.updateTrainingDataText)
        self.modelTrainerRunner.progressBarChanged.connect(self.updateProgressBar)
        self.modelTrainerRunner.finishStatus.connect(self.onTrainingFInish)

        # Dialogue settings
        self.trainDialog = QDialog(self)
        self.trainDialog.setWindowTitle("Training model")
        self.trainDialog.resize(400, 300)
        self.trainDialog.setModal(True)

        # Layout settings
        vbox = QVBoxLayout()
        hboxInfo = QHBoxLayout()
        vboxHyperparameters = QVBoxLayout()
        vboxHyperparameters.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Labels
        cnnLabel = QLabel("CNN Name: " + self.hyperParameters.modelName)
        batchsizeLabel = QLabel("Batch Size: " + str(self.hyperParameters.batchsize))
        epochNumLabel = QLabel("Epoch Number: " + str(self.hyperParameters.epochs))
        trainLabel = QLabel("Train Set Size: " + str(self.hyperParameters.train))
        validationLabel = QLabel("Validation Set Size: " + str(self.hyperParameters.validation))

        # Dialogue
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
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

        # Cancel Button
        hboxButtons = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hboxButtons.addWidget(self.cancelButton)
        #self.cancelButton.clicked.connect(self.trainDialog.reject)
        self.cancelButton.clicked.connect(self.onCancelButton) # just here for now to test the buttons

        # 3 different buttons after training finishes - train new model, save as, test model
        self.trainNewModelButton = QPushButton("Train new model")
        self.trainNewModelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.trainNewModelButton.clicked.connect(self.trainDialog.reject)

        self.saveAsButton = QPushButton("Save as")
        self.saveAsButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.saveAsButton.clicked.connect(self.onSaveButton)

        self.trainNewModelButton.clicked.connect(self.trainDialog.reject) # Close dialog and open test tab

        hboxButtons.addWidget(self.trainNewModelButton)
        hboxButtons.addWidget(self.saveAsButton)
        self.trainNewModelButton.setVisible(False)
        self.saveAsButton.setVisible(False)

        vbox.addLayout(hboxInfo)
        vbox.addWidget(self.progressBar)
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
        self.saveAsButton.setDisabled(False)
        self.cancelButton.setVisible(False)
        self.trainNewModelButton.setVisible(True)
        self.saveAsButton.setVisible(True)
        self.modelTrainerRunner.stop()
    
    # Dialog to save model
    def onSaveButton(self):
        """
        This method is called on save.
        It allows saving of the model
        @return:
        """
        # Show the save dialog
        file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Pytorch Model (*.pt);;All Files (*)")
        saver = SaveMechanism()

        hyperParamsSingleton = HyperParametersSingleton()

        # Check if a file name was selected
        if file_name:
            # save model into disc
            saver.saveTorch(
                file_name,
                file_name,
                hyperParamsSingleton.latestTrainedModelTrain,
                hyperParamsSingleton.latestTrainedModelValidate,
                hyperParamsSingleton.latestTrainedModelDnnName,
                hyperParamsSingleton.latestTrainedModelBatchSize,
                hyperParamsSingleton.latestTrainedModelEpoch,
                hyperParamsSingleton.latestTrainedModel
            )
            print("Saved")

    def on_train_model_button(self):
        self.show_train_dialog()

    def updateTrainingDataText(self, text):
        self.trainingData.setText(text)

    def updateProgressBar(self, value):
        print(value)
        self.progressBar.setValue(value)

    def onTrainingFInish(self, status):
        print("TrainUI finin")
        self.showFinishedButtons()

    def onCancelButton(self):
        self.showFinishedButtons()
        self.saveAsButton.setDisabled(True)
        self.testModelButton.setDisabled(True)







