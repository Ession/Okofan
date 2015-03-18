#!/usr/bin/env python

import sys
import os
from glob import glob

from PyQt5.QtWidgets import QApplication, QFileDialog
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
        """
        Opens a file dialog to get the logfile location

        :type self: MainWindow
        :return:
        """
        # opens directory chooser dialog
        directory_path = QFileDialog.getExistingDirectory(self, "Open Directory", "", QFileDialog.ShowDirsOnly)

        # checks if the user canceled the dialog
        if directory_path:
            os.chdir(directory_path)

            # only returns files that fit the logfile name pattern: CM130513.CSV
            logfilepaths = []
            for file in glob("CM[0-9][0-9][0-9][0-9][0-9][0-9].csv"):
                logfilepaths.append(directory_path + file)
            # TODO Open the files and add them to the table widget.

    @staticmethod
    def exit_action():
        """
        Quits the application

        :return:
        """
        QApplication.quit()

    def about_action(self):
        # TODO Implement about_action: Opening about dialog.
        pass

app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
