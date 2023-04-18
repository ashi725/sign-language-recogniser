import sys
from PyQt5.QtWidgets import *
from datasetTabUI import DatasetTab
from trainTabUI import TrainTab
from testTabUI import TestTab

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        tabWidget = QTabWidget()
        
        datasetTab = DatasetTab()
        trainTab = TrainTab()
        testTab = TestTab()
        
        tabWidget.addTab(datasetTab, 'Dataset')
        tabWidget.addTab(trainTab, 'Train')
        tabWidget.addTab(testTab, 'Test')

        vbox = QVBoxLayout()
        vbox.addWidget(tabWidget)
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
