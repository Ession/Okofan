#!/usr/bin/env python
"""Gui application to analyze Ökofen log files."""

import sys
import csv
import os
import glob
import random
import datetime
import copy

import PyQt5.QtCore
from PyQt5.QtWidgets import (QApplication, QFileDialog, QTableWidgetItem,
                             QAbstractItemView, QMainWindow, QWidget,
                             QHBoxLayout, QTabWidget, QStatusBar, QAction,
                             QTableWidget, QVBoxLayout, QCalendarWidget,
                             QMessageBox, QProgressDialog)


class MainWindow(QMainWindow):

    """This class defines the main application Window."""

    # dictionary of log file paths with date as key (YYYY-MM-DD)
    logfiles = {}

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        # setting up the ui design
        self.resize(680, 500)
        self.setMinimumSize(PyQt5.QtCore.QSize(680, 500))

        # construct the main widget
        self.centralwidget = QWidget(self)
        self.centralwidgetlayout = QHBoxLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)

        # construct the menu bar items
        self.actionOpen = QAction('Open Directory', self)
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.setStatusTip('Open a log file directory')
        self.actionOpen.triggered.connect(self.open_action)
        self.actionExit = QAction('Exit', self)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setStatusTip('Exit the application')
        self.actionExit.triggered.connect(self.exit_action)
        self.actionAbout = QAction('About', self)
        self.actionAbout.setShortcut('Ctrl+A')
        self.actionAbout.setStatusTip('Open the About dialog')
        self.actionAbout.triggered.connect(self.about_action)

        # add menu bar items to menu bar
        self.menuFile = self.menuBar().addMenu('&File')
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp = self.menuBar().addMenu('&Help')
        self.menuHelp.addAction(self.actionAbout)

        # construct the status bar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # construct the main window tab
        self.maintabwidget = QTabWidget(self.centralwidget)

        # construct the overview tab
        self.taboverview = QWidget()
        self.taboverviewlayout = QHBoxLayout(self.taboverview)

        # layout to hold the calendar widget
        self.overviewcalendarlayout = QVBoxLayout(self.taboverview)

        # construct the calendar widget
        self.overviewcalendar = QCalendarWidget(self.taboverview)
        self.overviewcalendar.setMaximumSize(PyQt5.QtCore.QSize(260, 183))
        self.overviewcalendar.setVerticalHeaderFormat(QCalendarWidget
                                                      .NoVerticalHeader)
        self.overviewcalendar.setGridVisible(True)
        self.overviewcalendar.setNavigationBarVisible(True)
        self.overviewcalendar.clicked.connect(self.overview_cal_clicked)
        self.overviewcalendar.activated.connect(self.item_activated)
        self.overviewcalendarlayout.addWidget(self.overviewcalendar)
        self.overviewcalendarlayout.addStretch()
        self.taboverviewlayout.addLayout(self.overviewcalendarlayout)

        # construct the log list table
        self.loglist = QTableWidget(self.taboverview)
        self.loglist.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.loglist.setSelectionMode(QAbstractItemView.SingleSelection)
        self.loglist.itemSelectionChanged.connect(self.selection_changed)
        self.loglist.itemActivated.connect(self.item_activated)
        self.taboverviewlayout.addWidget(self.loglist)

        # construct the detail tab
        self.tabdetaillist = QWidget()
        self.logdetaillistlayout = QVBoxLayout(self.tabdetaillist)

        # construct the log detail table
        self.logdetaillist = QTableWidget(self.tabdetaillist)
        self.logdetaillist.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.logdetaillistlayout.addWidget(self.logdetaillist)

        # add the tabs to the main tab widget
        self.maintabwidget.addTab(self.taboverview, 'Overview')
        self.maintabwidget.addTab(self.tabdetaillist, 'Detail log')
        self.centralwidgetlayout.addWidget(self.maintabwidget)

    def open_action(self):
        """Open a file dialog to get the logfile location.

        :type self: MainWindow
        :return: empty

        """
        # opens directory chooser dialog
        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open Directory', '',
                                                     QFileDialog.ShowDirsOnly)

        # checks if the user canceled the dialog
        if not directory:
            return

        # open the log directory
        os.chdir(directory)

        # logfile name pattern: CM130513.CSV
        logdata = []
        filelist = glob.glob('CM[0-9][0-9][0-9][0-9][0-9][0-9].csv')

        # construct the progressbar dialog in case opening takes a while
        progress = QProgressDialog('Opening files...', 'Cancel', 0,
                                   len(filelist), self)
        progress.setWindowModality(PyQt5.QtCore.Qt.WindowModal)

        logfilescopy = copy.deepcopy(self.logfiles)

        for i, file in enumerate(filelist, start=1):
            path = directory + '/' + file

            # get date from the log file and convert it to YYYY-MM-DD
            filedate = self.getlogdate(path)
            date = datetime.datetime.strptime(filedate, '%d.%m.%Y')
            date = date.strftime('%Y-%m-%d')

            # save path and date for later use
            self.logfiles[date] = path

            # TODO Replace placeholder column with real data.
            logdata.append((date, random.randint(0, 100)))

            # increment the progress bar
            progress.setValue(i)
            if progress.wasCanceled():
                self.logfiles = logfilescopy
                return

        self.loglist.setRowCount(len(logdata))
        self.loglist.setColumnCount(len(logdata[0]))
        self.loglist.setHorizontalHeaderLabels(('Date', 'placeholder'))
        self.loglist.horizontalHeader().setStretchLastSection(True)

        for rowcount, rowdata in enumerate(logdata):
            for colcount, coldata in enumerate(rowdata):
                cellitem = QTableWidgetItem()
                cellitem.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable |
                                  PyQt5.QtCore.Qt.ItemIsEnabled)
                cellitem.setText(str(coldata))
                self.loglist.setItem(rowcount, colcount, cellitem)

    @staticmethod
    def exit_action():
        """Quit the application.

        :return: empty

        """
        QApplication.quit()

    @staticmethod
    def about_action(self):
        """Open the about dialog.

        :return: empty

        """
        # TODO Implement about_action: Opening about dialog.
        pass

    def overview_cal_clicked(self, date):
        """Select the selected day in the log table.

        :param date: Selected date.

        """
        items = self.loglist.findItems(date.toString('yyyy-MM-dd'),
                                       PyQt5.QtCore.Qt.MatchExactly)

        if items:
            for item in items:
                results = int(item.row())
                self.loglist.selectRow(results)

    def selection_changed(self):
        """Select the day in the calendar widget."""
        selected = self.loglist.selectedItems()[0].text()
        date = datetime.datetime.strptime(selected, '%Y-%m-%d')
        self.overviewcalendar.setSelectedDate(date)

    def item_activated(self, param):
        """Load the selected log in the detail table.

        :param param: QTableWidgetItem or QDate that was activated.

        """

        # Check if you got a WidgetItem from the table
        # or a QDate from the calendar.
        if isinstance(param, QTableWidgetItem):
            date = param.text()
        elif isinstance(param, PyQt5.QtCore.QDate):
            date = param.toString('yyyy-MM-dd')
        else:
            return

        # check if there is a log for the selected date
        if date not in self.logfiles:
            QMessageBox.warning(self, 'Error',
                                'No log for day \'' + date + '\' found.',
                                QMessageBox.Ok)
            return

        # open the csv file and save the data to a list
        logdata = []
        with open(self.logfiles[date], newline='') as logfile:
            logfile = (x.replace('\0', '') for x in logfile)
            reader = csv.reader(strip_lines(logfile), delimiter=';')

            # skip the header
            next(reader)

            # save the data to a list and omit the last column (it's empty)
            for logline in reader:
                logdata.append(logline[:-1])

        # setup the log detail table
        self.logdetaillist.setRowCount(len(logdata))
        self.logdetaillist.setColumnCount(len(logdata[0]))
        self.logdetaillist.setHorizontalHeaderLabels(('Date', 'Time',
                                                      'KF', 'RGF', 'SP_FRT',
                                                      'FRT', 'ES', 'PA', 'LL',
                                                      'SZ', 'SP_uP', 'uP',
                                                      'SM'))
        self.logdetaillist.horizontalHeader().setStretchLastSection(True)

        # insert data in to the table
        for rowcount, rowdata in enumerate(logdata):
            for colcount, coldata in enumerate(rowdata):
                cellitem = QTableWidgetItem()
                cellitem.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable |
                                  PyQt5.QtCore.Qt.ItemIsEnabled)
                cellitem.setText(str(coldata))
                self.logdetaillist.setItem(rowcount, colcount, cellitem)

        self.logdetaillist.resizeColumnsToContents()

        # switch to the details tab
        self.maintabwidget.setCurrentIndex(1)

    @staticmethod
    def getlogdate(filepath):
        """Open a log file and get the log files date.

        :param filepath: Path to the log file.
        :return: Date the log File was written in YYYY-MM-DD.

        """
        with open(filepath, newline='') as logfile:
            logfile = (x.replace('\0', '') for x in logfile)
            reader = csv.reader(strip_lines(logfile), delimiter=';')

            # skip the header
            next(reader)

            return str(next(reader)[0])


def strip_lines(iterable):
    """Strip empty lines from the iterator.

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
