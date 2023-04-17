from pathlib import Path
import sys
import cv2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QInputDialog
from PyQt5.QtGui import QPixmap


class TestTab(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("test!")

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        self.setLayout(vbox)