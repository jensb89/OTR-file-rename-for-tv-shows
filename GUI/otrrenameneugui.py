# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'otrrenameguineu.ui'
#
# Created: Sat Oct 12 11:02:58 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os
import re
import otr_rename
import move_tv_show

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(550, 275)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineEdit_2 = QtGui.QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 0, 1, 1)
        self.commandLinkButton = QtGui.QCommandLinkButton(self.tab)
        self.commandLinkButton.setObjectName(_fromUtf8("commandLinkButton"))
        self.gridLayout_2.addWidget(self.commandLinkButton, 1, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_2.addWidget(self.pushButton, 0, 1, 1, 1)
        self.commandLinkButton_2 = QtGui.QCommandLinkButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLinkButton_2.sizePolicy().hasHeightForWidth())
        self.commandLinkButton_2.setSizePolicy(sizePolicy)
        self.commandLinkButton_2.setObjectName(_fromUtf8("commandLinkButton_2"))
        self.gridLayout_2.addWidget(self.commandLinkButton_2, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.listWidget = QtGui.QListWidget(self.tab_2)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout_3.addWidget(self.listWidget, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.commandLinkButton_3 = QtGui.QCommandLinkButton(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLinkButton_3.sizePolicy().hasHeightForWidth())
        self.commandLinkButton_3.setSizePolicy(sizePolicy)
        self.commandLinkButton_3.setObjectName(_fromUtf8("commandLinkButton_3"))
        self.verticalLayout.addWidget(self.commandLinkButton_3)
        self.progressBar = QtGui.QProgressBar(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

        files = [f for f in os.listdir(".") if f.endswith('.otrkey')]
        for filename in files:
            self.listWidget.addItem(filename)

        self.progressBar.setMaximum(len(files))
        self.pushButton.clicked.connect(self.selectFile)
        self.commandLinkButton.clicked.connect(self.getInfo)
        self.commandLinkButton_2.clicked.connect(self.move)
        self.commandLinkButton_3.clicked.connect(self.movebatch)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "OTR RENAMER", None))
        self.label.setText(_translate("Form", "OTR Renamer", None))
        self.commandLinkButton.setText(_translate("Form", "Get Episode Information", None))
        self.pushButton.setText(_translate("Form", "Load File", None))
        self.commandLinkButton_2.setText(_translate("Form", "Rename and Move File", None))
        self.label_2.setText(_translate("Form", "Episode information from www.fernsehserien.de", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "One File Rename", None))
        self.commandLinkButton_3.setText(_translate("Form", "Rename and Move", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Batch Rename", None))

    def selectFile(self, Form):
        self.lineEdit.setText(QtGui.QFileDialog.getOpenFileName())

    def getInfo(self, Form):
        a=self.lineEdit.text()
        filename=os.path.relpath(str(a))
        
        newfilename = otr_rename.buildNewFileName(filename)
        self.lineEdit_2.setText(newfilename)

    def move(self, Form):
        a=self.lineEdit.text()
        filename=os.path.relpath(str(a))
        move_tv_show.copysort(filename)

    def movebatch(self, Form):
        items = []
        for index in xrange(self.listWidget.count()):
            items.append(self.listWidget.item(index))
        labels = [i.text() for i in items]
        
        i=0
        for filename in labels:
            move_tv_show.copysort(str(filename))
            i+=1
            self.progressBar.setValue(i)
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

