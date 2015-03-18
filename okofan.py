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

        # connecting the signals of the menu bar
        self.actionOpen.triggered.connect(self.open_action)
        self.actionExit.triggered.connect(self.exit_action)
        self.actionAbout.triggered.connect(self.about_action)

    def open_action(self):
        # TODO Implement open_action: Opening file open dialog.
        pass

    @staticmethod
    def exit_action():
        QApplication.quit()

    def about_action(self):
        # TODO Implement about_action: Opening about dialog.
        pass

app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
