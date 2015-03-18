#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType

# load the ui MainWindow UI File
# returns the form class and the Qt base class of the MainWindow
MainWindowUI, MainWindowBase = loadUiType('ui\MainWindow.ui')


class MainWindow(MainWindowBase, MainWindowUI):
    """
    Main window docstring.
    """

    def __init__(self):
        """
        Initializes the main window.

        :return:
        """
        super().__init__()
        self.setupUi(self)


app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
