# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_image2text.ui'
#
# Created: Tue Apr  3 20:17:14 2018
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_image2textWidget(object):
    def setupUi(self, image2textWidget):
        image2textWidget.setObjectName("image2textWidget")
        image2textWidget.resize(611, 330)
        self.pushButtonOpen = QtWidgets.QPushButton(image2textWidget)
        self.pushButtonOpen.setGeometry(QtCore.QRect(190, 280, 201, 31))
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.textEdit = QtWidgets.QTextEdit(image2textWidget)
        self.textEdit.setGeometry(QtCore.QRect(7, 10, 591, 261))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(image2textWidget)
        QtCore.QMetaObject.connectSlotsByName(image2textWidget)

    def retranslateUi(self, image2textWidget):
        _translate = QtCore.QCoreApplication.translate
        image2textWidget.setWindowTitle(_translate("image2textWidget", "Form"))
        self.pushButtonOpen.setText(_translate("image2textWidget", "Open"))

