import sys
from PyQt5.QtWidgets import *
from tabUI.datasetTabUI import DatasetTab
from tabUI.trainTabUI import TrainTab
from tabUI.testTabUI import TestTab
from models.DataModelSingleton import DataModelSingleton


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dataModel = DataModelSingleton()


    def initUI(self):

        self.tabWidget = QTabWidget()
        
        datasetTab = DatasetTab()
        trainTab = TrainTab()
        testTab = TestTab()
        

        self.tabWidget.addTab(datasetTab, 'Dataset')
        self.tabWidget.addTab(trainTab, 'Train')
        self.tabWidget.addTab(testTab, 'Test')

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabWidget)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        self.setWindowTitle('Test Application')
        self.move(900, -800)
        self.resize(800, 600)        
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MyApp()
    sys.exit(app.exec_())
