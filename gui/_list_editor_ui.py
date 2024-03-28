# Form implementation generated from reading ui file 'list_editor.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_listEdit(object):
    def setupUi(self, listEdit):
        listEdit.setObjectName("listEdit")
        listEdit.resize(400, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(listEdit.sizePolicy().hasHeightForWidth())
        listEdit.setSizePolicy(sizePolicy)
        listEdit.setMaximumSize(QtCore.QSize(500, 600))
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        listEdit.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(listEdit)
        self.verticalLayout.setContentsMargins(15, 10, 15, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.itemInputPrompt = QtWidgets.QLabel(parent=listEdit)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.itemInputPrompt.setFont(font)
        self.itemInputPrompt.setObjectName("itemInputPrompt")
        self.verticalLayout.addWidget(self.itemInputPrompt)
        self.itemInputField = QtWidgets.QLineEdit(parent=listEdit)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.itemInputField.setFont(font)
        self.itemInputField.setObjectName("itemInputField")
        self.verticalLayout.addWidget(self.itemInputField)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deleteBtn = QtWidgets.QPushButton(parent=listEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteBtn.sizePolicy().hasHeightForWidth())
        self.deleteBtn.setSizePolicy(sizePolicy)
        self.deleteBtn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.deleteBtn.setFont(font)
        self.deleteBtn.setObjectName("deleteBtn")
        self.horizontalLayout.addWidget(self.deleteBtn)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addBtn = QtWidgets.QPushButton(parent=listEdit)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.addBtn.setFont(font)
        self.addBtn.setObjectName("addBtn")
        self.horizontalLayout.addWidget(self.addBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.itemsList = QtWidgets.QListWidget(parent=listEdit)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.itemsList.setFont(font)
        self.itemsList.setObjectName("itemsList")
        self.verticalLayout.addWidget(self.itemsList)

        self.retranslateUi(listEdit)
        QtCore.QMetaObject.connectSlotsByName(listEdit)

    def retranslateUi(self, listEdit):
        _translate = QtCore.QCoreApplication.translate
        listEdit.setWindowTitle(_translate("listEdit", "List Edit"))
        self.itemInputPrompt.setText(_translate("listEdit", "Enter:"))
        self.deleteBtn.setText(_translate("listEdit", "Delete"))
        self.addBtn.setText(_translate("listEdit", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    listEdit = QtWidgets.QDialog()
    ui = Ui_listEdit()
    ui.setupUi(listEdit)
    listEdit.show()
    sys.exit(app.exec())
