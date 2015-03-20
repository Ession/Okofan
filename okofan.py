#!/usr/bin/env python

import sys
import os
from glob import glob

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.uic import loadUiType

# load the ui MainWindow UI File
# returns the form class and the Qt base class of the MainWindow
MainWindowUI, MainWindowBase = loadUiType('ui\MainWindow.ui')


class MainWindow(MainWindowBase, MainWindowUI):
    """
    This class defines the main application Window.
    """
    def __init__(self):
        """
        Initialize the main window.

        :return: empty
        """
        super().__init__()
        self.setupUi(self)

        # connecting the signals of the menu bar
        self.actionOpen.triggered.connect(self.open_action)
        self.actionExit.triggered.connect(self.exit_action)
        self.actionAbout.triggered.connect(self.about_action)

        # setting the table model
        # TODO Display the real data instead of dummy values
        table_view_log_list_model = TableModel([('date 1', 2), ('date 2', 3), ('date 3', 4)],
                                               ['Date', 'Number'], self)
        self.tableViewLogList.setModel(table_view_log_list_model)

    def open_action(self):
        """
        Open a file dialog to get the logfile location.

        :type self: MainWindow
        :return: empty
        """
        # opens directory chooser dialog
        directory_path = QFileDialog.getExistingDirectory(self, 'Open Directory', '', QFileDialog.ShowDirsOnly)

        # checks if the user canceled the dialog
        if directory_path:
            os.chdir(directory_path)

            # only returns files that fit the logfile name pattern: CM130513.CSV
            logfilepaths = []
            for file in glob('CM[0-9][0-9][0-9][0-9][0-9][0-9].csv'):
                logfilepaths.append(directory_path + file)
            # TODO Open the files and add them to the table widget.

    @staticmethod
    def exit_action():
        """
        Quit the application.

        :return: empty
        """
        QApplication.quit()

    @staticmethod
    def about_action(self):
        """
        Open the about dialog.

        :return:empty
        """
        # TODO Implement about_action: Opening about dialog.
        pass


class TableModel(QAbstractTableModel):
    """
    Table Model that defines the data for the logfile table view
    """
    def __init__(self, data_list, header_list, parent=None):
        """
        Initialize the Table Model.

        :param data_list: List of data (2 dimensional list of tuples)
        :param header_list: List of header titles (strings)
        :return:
        """
        super().__init__(parent)
        self.data_list = data_list
        self.header_list = header_list

    def rowCount(self, parent):
        """
        Return the amount of rows in the table.

        :param parent: the table model
        :return: amount of rows in the table
        """
        return len(self.data_list)

    def columnCount(self, parent):
        """
        Return the amount of columns in the table.

        :param parent: The table model
        :return: Amount of columns in the table
        """
        return len(self.data_list[0])

    def data(self, index, role):
        """
        Return the data stored under the given role for the item referred to by the index.

        :param index: Index of the stored datum
        :param role: Role of the indexed datum
        :return: QVariant
        """
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.data_list[index.row()][index.column()])

    def headerData(self, section, orientation, role):
        """
        Return the given role and section in the header with the specific orientation.

        :param section: In a horizontal header, the number of the column.
                        In a vertical header, the number of the row.
        :param orientation: The orientation of the header (horizontal or vertical).
        :param role: The role of the datum.
        :return:
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_list[section])
        return QVariant()

    # TODO Implement table sorting.


app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
