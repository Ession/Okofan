#!/usr/bin/env python
"""Gui application to analyze Ökofen log files."""

import sys
import csv
from os import chdir
from glob import glob
from random import randint
from datetime import datetime
from operator import itemgetter

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QHeaderView
from PyQt5.uic import loadUiType

# load the ui MainWindow UI File
# returns the form class and the Qt base class of the MainWindow
MainWindowUI, MainWindowBase = loadUiType('ui\MainWindow.ui')


class MainWindow(MainWindowBase, MainWindowUI):

    """This class defines the main application Window."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setupUi(self)

        # connecting the signals of the menu bar
        self.actionOpen.triggered.connect(self.open_action)
        self.actionExit.triggered.connect(self.exit_action)
        self.actionAbout.triggered.connect(self.about_action)

    def open_action(self):
        """
        Open a file dialog to get the logfile location.

        :type self: MainWindow
        :return: empty
        """
        # opens directory chooser dialog
        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open Directory', '',
                                                     QFileDialog.ShowDirsOnly)

        # checks if the user canceled the dialog
        if directory:
            chdir(directory)

            # logfile name pattern: CM130513.CSV
            logdata = []
            for file in glob('CM[0-9][0-9][0-9][0-9][0-9][0-9].csv'):
                with open(directory + '/' + file, newline='') as logfile:
                    logfile = (x.replace('\0', '') for x in logfile)
                    reader = csv.DictReader(strip_lines(logfile),
                                            delimiter=';')

                    date = datetime.strptime((next(reader)['Date']),
                                             '%d.%m.%Y').strftime('%Y-%m-%d')

                    # TODO Replace placeholder column with real data.
                    logdata.append((date, randint(0, 100)))

            # populate the log list table with data
            log_list_header = ['Date', 'placeholder']
            table_view_log_list_model = TableModel(logdata,
                                                   log_list_header, self)
            self.tableViewLogList.setModel(table_view_log_list_model)
            self.tableViewLogList.horizontalHeader()\
                .setSectionResizeMode(0, QHeaderView.Stretch)
            self.tableViewLogList.setSortingEnabled(True)

    @staticmethod
    def exit_action(self):
        """
        Quit the application.

        :return: empty
        """
        QApplication.quit(self)

    @staticmethod
    def about_action(self):
        """
        Open the about dialog.

        :return: empty
        """
        # TODO Implement about_action: Opening about dialog.
        pass


class TableModel(QAbstractTableModel):

    """Table Model that defines the data for the logfile table view."""

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
        Return the data stored under the given role for the item at index.

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
        Return the given role and section in the header.

        :param section: In a horizontal header, the number of the column.
                        In a vertical header, the number of the row.
        :param orientation: The orientation of the header.
        :param role: The role of the datum.
        :return:
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_list[section])
        return QVariant()

    def sort(self, column, order):
        """
        Sort the table by given column.

        :param column: Column number to be sorted by.
        :param order: Order to sort by.
        :return:
        """
        self.layoutAboutToBeChanged.emit()
        self.data_list = sorted(self.data_list, key=itemgetter(column))
        if order == Qt.DescendingOrder:
            self.data_list.reverse()
        self.layoutChanged.emit()


def strip_lines(iterable):
    """
    Strip empty lines from the iterator.

    :param iterable: iterator to strip lines from
    :return: yields next iterator line
    """
    for line in iterable:
        if line.strip():
            yield line

app = QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
