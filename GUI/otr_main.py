from otr_rename_gui_window import Ui_Form
import sys
from PyQt4 import QtCore, QtGui
import os
import re
from otr_rename import OTR_Rename

class OTRGUI(Ui_Form):
    def __init__(self, Form):
        self.setupUi(Form)

        files = [f for f in os.listdir(".") if f.endswith('.avi')]
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
        files = [f for f in os.listdir(folder) if f.endswith('.avi')]
        for filename in files:
            self.listWidget.addItem(filename)

    def getInfo(self, Form):
        a=self.lineEdit.text()
        filename=os.path.relpath(str(a))
        
        newfilename = OTR_Rename(filename).buildNewFilename()
        self.lineEdit_2.setText(newfilename)

    def move(self, Form):
        a=self.lineEdit.text()
        filename=os.path.relpath(str(a))
        OTR_Rename(filename).copy_and_sort()

    def movebatch(self, Form):
        items = []
        for index in xrange(self.listWidget.count()):
            items.append(self.listWidget.item(index))
        labels = [i.text() for i in items]
        
        i=0
        for filename in labels:
            OTR_Rename(str(filename)).copy_and_sort()
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