#!/usr/bin/python
#encoding: utf-8

from PyQt4 import QtCore, QtGui
import sys
import os
import GUI.otrrenameneugui


app = QtGui.QApplication(sys.argv)
Form = QtGui.QWidget()
ui = GUI.otrrenameneugui.Ui_Form()
ui.setupUi(Form)
Form.show()
sys.exit(app.exec_())