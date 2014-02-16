from otr_rename_gui_window import Ui_Form
import sys
from PyQt4 import QtCore, QtGui
import os
import re
import otr_rename
import move_tv_show

class OTRGUI(Ui_Form):
    def __init__(self, Form):
        self.setupUi(Form)

        files = [f for f in os.listdir(".") if f.endswith('.otrkey')]
        for filename in files:
            self.listWidget.addItem(filename)

        self.progressBar.setMaximum(len(files))
        self.pushButton.clicked.connect(self.selectFile)
        self.pushButton_2.clicked.connect(self.selectFolder)
        self.commandLinkButton.clicked.connect(self.getInfo)
        self.commandLinkButton_2.clicked.connect(self.move)
        self.commandLinkButton_3.clicked.connect(self.movebatch)

    def selectFile(self, Form):
        self.lineEdit.setText(QtGui.QFileDialog.getOpenFileName())

    def selectFolder(self):
        self.listWidget.clear()
        folder = QtGui.QFileDialog.getExistingDirectory()
        self.lineEdit_3.setText(folder)
        files = [f for f in os.listdir(folder) if f.endswith('.otrkey')]
        for filename in files:
            self.listWidget.addItem(filename)

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


def main():
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = OTRGUI(Form)
    #ui = Ui_Form()
    #ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()