#!/usr/bin/python


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow
import sys
from ui import *
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.Qt import QGraphicsScene, QRectF
import numpy as np



if __name__ == '__main__':
    arg = sys.argv
    app = QApplication(arg)
    name = None if len(sys.argv) == 1 else sys.argv[1]
    w = Ui_MainWindow(name)
    w.show()
    w.raise_()
    
    
    sys.exit(app.exec_())
