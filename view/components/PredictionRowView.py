from PyQt5.QtWidgets import *

from models.singletons.PredictDataSingleton import convertLabelToClassName
from PyQt5.QtWidgets import *

from models.singletons.PredictDataSingleton import convertLabelToClassName


class PredictionRowView(QWidget ):
    def __init__(self, imagePixmap, predictionStr, accVal, actualPred=None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = QVBoxLayout(self)
        self.setLayout(vbox)

        imageLabel = QLabel()
        predictionLabel = QLabel()
        accuracyLabel = QLabel()
        actual = QLabel()

        # Convert classes into their correct label and not a num
        predictionStr = convertLabelToClassName(int(predictionStr))

        imageLabel.setPixmap(imagePixmap)
        predictionLabel.setText("Predicted: {}".format(predictionStr))
        accuracyLabel.setText("Confidence: {:.0f}%".format(accVal*100))
        vbox.addWidget(imageLabel)
        vbox.addWidget(predictionLabel)
        vbox.addWidget(accuracyLabel)
        vbox.setContentsMargins(0, 0, 0, 0)

        if (actualPred is not None):
            actualPred = convertLabelToClassName(int(actualPred.item()))
            actual.setText("Actual: {}".format(actualPred))
            vbox.addWidget(actual)
