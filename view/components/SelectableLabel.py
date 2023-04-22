from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class SelectableLabel(QLabel):
    """
    This class is a custom label that can be selected
    """

    def __init__(self, imageDetails, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._selected = False
        self.imageDetails = imageDetails  # Stores everything about the image
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        """When user has pressed the widget"""
        if event.button() == Qt.LeftButton:
            self._selected = not self._selected

            # Toggle selected
            if (self.is_selected()):
                self.setStyleSheet("background-color: yellow; padding: 4px;")
            else:
                self.setStyleSheet("background-color: transparent; padding: 4px;")

    def is_selected(self):
        """
        Method to check if selected
        @return: bool
        """
        return self._selected
