#!/usr/bin/env python
"""Gui application to analyze Ökofen log files."""

import sys
import csv
from os import chdir
from glob import glob
from random import randint
from datetime import datetime

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import (QApplication, QFileDialog, QTableWidgetItem,
                             QAbstractItemView, QMainWindow, QWidget,
                             QHBoxLayout, QTabWidget, QMenuBar, QMenu,
                             QStatusBar, QAction, QTableWidget, QFrame,
                             QSizePolicy, QVBoxLayout, QCalendarWidget,
                             QFormLayout, QSpacerItem)


class MainWindow(QMainWindow):

    """This class defines the main application Window."""

    # dictionary of log file paths with date as key (YYYY-MM-DD)
    logfiles = {}

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        # setting up the ui design
        self.resize(680, 500)
        self.setMinimumSize(QSize(680, 500))

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
        self.frame = QFrame(self.taboverview)
        self.framelayout = QVBoxLayout(self.frame)
        self.framelayout.setContentsMargins(0, 0, 0, 0)

        # construct the calendar widget
        self.overview_cal = QCalendarWidget(self.frame)
        sizepolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizepolicy.setHeightForWidth(self.overview_cal.sizePolicy()
                                     .hasHeightForWidth())
        self.overview_cal.setSizePolicy(sizepolicy)
        self.overview_cal.setMinimumSize(QSize(260, 183))
        self.overview_cal.setMaximumSize(QSize(260, 183))
        self.overview_cal.setGridVisible(True)
        self.overview_cal.setHorizontalHeaderFormat(QCalendarWidget
                                                    .SingleLetterDayNames)
        self.overview_cal.setVerticalHeaderFormat(QCalendarWidget
                                                  .NoVerticalHeader)
        self.overview_cal.setNavigationBarVisible(True)
        self.overview_cal.setDateEditEnabled(True)

        self.framelayout.addWidget(self.overview_cal)

        self.formlayout = QFormLayout(self.frame)
        spaceritem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        self.formlayout.setItem(0, QFormLayout.LabelRole, spaceritem)
        self.framelayout.addLayout(self.formlayout)

        self.taboverviewlayout.addWidget(self.frame)

        # construct the log list table
        self.loglist = QTableWidget(self.taboverview)
        self.taboverviewlayout.addWidget(self.loglist)

        # add the tab to the main tab widget
        self.maintabwidget.addTab(self.taboverview, 'Overview')
        self.tabdetail = QWidget()
        self.maintabwidget.addTab(self.tabdetail, 'Detail')
        self.centralwidgetlayout.addWidget(self.maintabwidget)

        # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(
        # self.frame.sizePolicy().hasHeightForWidth())
        # self.frame.setSizePolicy(sizePolicy)
        # self.frame.setFrameShape(QFrame.StyledPanel)
        # self.frame.setFrameShadow(QFrame.Raised)
        # self.verticalLayout = QVBoxLayout(self.frame)
        # self.overview_cal = QCalendarWidget(self.frame)
        #
        # self.verticalLayout.addWidget(self.overview_cal)
        #
        # self.taboverviewlayout.addWidget(self.frame)
        #
        # self.loglist = QTableWidget(self.taboverview)
        # self.taboverviewlayout.addWidget(self.loglist)

        # connecting the signals of the menu bar
        # self.overview_cal.clicked.connect(self.overview_cal_clicked)
        # self.loglist.itemSelectionChanged.connect(self.selection_changed)
        # self.loglist.itemActivated.connect(self.item_activated)
        #
        # self.loglist.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.loglist.setSelectionMode(QAbstractItemView.SingleSelection)
        #
        # self.logdetail.setSelectionBehavior(QAbstractItemView.SelectRows)

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
        if directory:
            chdir(directory)

            # logfile name pattern: CM130513.CSV
            logdata = []
            for file in glob('CM[0-9][0-9][0-9][0-9][0-9][0-9].csv'):
                path = directory + '/' + file

                # get date from the log file and convert it to YYYY-MM-DD
                date = datetime.strptime(self.getlogdate(path),
                                         '%d.%m.%Y').strftime('%Y-%m-%d')

                # save path and date for later use
                self.logfiles[date] = path

                # TODO Replace placeholder column with real data.
                logdata.append((date, randint(0, 100)))

            self.loglist.setRowCount(len(logdata))
            self.loglist.setColumnCount(len(logdata[0]))
            self.loglist.setHorizontalHeaderLabels(('Date', 'placeholder'))
            self.loglist.horizontalHeader().setStretchLastSection(True)

            for rowcount, rowdata in enumerate(logdata):
                for colcount, coldata in enumerate(rowdata):
                    cellitem = QTableWidgetItem()
                    cellitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
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
                                       Qt.MatchExactly)

        if items:
            for item in items:
                results = int(item.row())
                self.loglist.selectRow(results)

    def selection_changed(self):
        """Select the day in the calendar widget."""
        selected = self.loglist.selectedItems()[0].text()
        date = datetime.strptime(selected, '%Y-%m-%d')
        self.overview_cal.setSelectedDate(date)

    def item_activated(self, item):
        """Load the selected log in the detail table.

        :param item: Item that way activated in the table.

        """
        # switch to the details tab
        self.maintab.setCurrentIndex(1)

        # open the csv file and save the data to a list
        logdata = []
        with open(self.logfiles[item.text()], newline='') as logfile:
            logfile = (x.replace('\0', '') for x in logfile)
            reader = csv.reader(strip_lines(logfile), delimiter=';')

            # skip the header
            next(reader)

            # save the data to a list and omit the last column (it's empty)
            for logline in reader:
                logdata.append(logline[:-1])

        # setup the log detail table
        self.logdetail.setRowCount(len(logdata))
        self.logdetail.setColumnCount(len(logdata[0]))
        self.logdetail.setHorizontalHeaderLabels(('Date', 'Time', 'KF', 'RGF',
                                                  'SP_FRT', 'FRT', 'ES', 'PA',
                                                  'LL', 'SZ', 'SP_uP', 'uP',
                                                  'SM'))
        self.logdetail.horizontalHeader().setStretchLastSection(True)

        # insert data in to the table
        for rowcount, rowdata in enumerate(logdata):
            for colcount, coldata in enumerate(rowdata):
                cellitem = QTableWidgetItem()
                cellitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                cellitem.setText(str(coldata))
                self.logdetail.setItem(rowcount, colcount, cellitem)

        self.logdetail.resizeColumnsToContents()

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
