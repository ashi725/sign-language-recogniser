import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from view.DatasetTabUI import DatasetTab
from view.TrainTabUI import TrainTab
from view.TestTabUI import TestTab
from models.singletons.DataModelSingleton import DataModelSingleton


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dataModel = DataModelSingleton()


    def initUI(self):

        self.tabWidget = QTabWidget()
        self.tabWidget.currentChanged.connect(self.onTabChanged)

        datasetTab = DatasetTab(self.disableTrainTab)
        trainTab = TrainTab()
        testTab = TestTab()
        

        self.tabWidget.addTab(datasetTab, 'Dataset')
        self.tabWidget.addTab(trainTab, 'Train')
        self.tabWidget.addTab(testTab, 'Test')
        self.disableTrainTab(False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabWidget)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        self.setWindowTitle('Sign language recognition')
        self.setWindowIcon(QIcon("resources/thumbsup.png"))
        self.move(800, -800)
        self.resize(800, 600)        
        self.show()

    def onTabChanged(self):
        currentTab = self.tabWidget.currentWidget()
        currentTab.refreshWindowOnLoad()

    def disableTrainTab(self, shouldDisable):
        self.tabWidget.setTabEnabled(1, shouldDisable)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MyApp()
    sys.exit(app.exec_())
