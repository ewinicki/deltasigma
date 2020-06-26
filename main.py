#!/usr/bin/python

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
        QAction, QLineEdit, QMessageBox, QTextEdit, QLabel, QGridLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from MainGrid import MainGrid

from deltasigma import deltasigma

RUN_ICON = 'icons/run.png'
RESET_ICON = 'icons/reset.png'
EXIT_ICON = 'icons/exit.png'
 
class SigmaDelta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Delta Sigma Simulator'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.grid = MainGrid()
        self.runAct = self.initRunAct()
        self.resetAct = self.initResetAct()
        self.exitAct = self.initExitAct()
        self.initUI()
 
    def initUI(self):
        menubar = self.initMenuBar()
        toolbar = self.initToolBar()
 
        self.statusBar().showMessage('Ready')
        self.setCentralWidget(self.grid)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def initMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.runAct)
        fileMenu.addAction(self.resetAct)
        fileMenu.addAction(self.exitAct)

        return menubar

    def initToolBar(self):
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.exitAct)
        toolbar.addAction(self.resetAct)
        toolbar.addAction(self.runAct)

    def initExitAct(self):
        exitAct = QAction(QIcon(EXIT_ICON), 'Exit', self)
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        return exitAct

    def initRunAct(self):
        runAct = QAction(QIcon(RUN_ICON), 'Run Delta Sigma', self)
        runAct.setStatusTip('Run Delta Sigma')
        runAct.triggered.connect(self.run)

        return runAct

    def initResetAct(self):
        resetAct = QAction(QIcon(RESET_ICON), 'Default Settings', self)
        resetAct.setStatusTip('Default Settings')
        resetAct.triggered.connect(self.grid.reset)

        return resetAct

    def run(self):
        self.statusBar().showMessage('Running...')

        deltasigma(
                self.grid.frequency,
                self.grid.amplitude,
                self.grid.waveform,
                self.grid.samples,
                self.grid.dc,
                self.grid.noise,
                self.grid.sampling_frequency,
                self.grid.oversampling_rate,
                self.grid.vref,
                self.grid.periods,
                self.grid.order
                )

        self.statusBar().showMessage('Done')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SigmaDelta()
    sys.exit(app.exec_())
