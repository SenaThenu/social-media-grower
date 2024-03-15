# Form implementation generated from reading ui file 'preferences.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(441, 288)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Preferences.sizePolicy().hasHeightForWidth())
        Preferences.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Preferences)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.preferencesForm = QtWidgets.QVBoxLayout()
        self.preferencesForm.setObjectName("preferencesForm")
        self.acceptedRatio = QtWidgets.QHBoxLayout()
        self.acceptedRatio.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.acceptedRatio.setObjectName("acceptedRatio")
        self.acceptedRatioLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptedRatioLabel.sizePolicy().hasHeightForWidth())
        self.acceptedRatioLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.acceptedRatioLabel.setFont(font)
        self.acceptedRatioLabel.setObjectName("acceptedRatioLabel")
        self.acceptedRatio.addWidget(self.acceptedRatioLabel)
        self.acceptedRatioInfo = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.acceptedRatioInfo.sizePolicy().hasHeightForWidth())
        self.acceptedRatioInfo.setSizePolicy(sizePolicy)
        self.acceptedRatioInfo.setMinimumSize(QtCore.QSize(2, 2))
        self.acceptedRatioInfo.setMaximumSize(QtCore.QSize(15, 15))
        self.acceptedRatioInfo.setToolTipDuration(-1)
        self.acceptedRatioInfo.setText("")
        self.acceptedRatioInfo.setPixmap(QtGui.QPixmap("C:/Users/Gayan/Downloads/info_FILL0_wght300_GRAD200_opsz24.png"))
        self.acceptedRatioInfo.setScaledContents(True)
        self.acceptedRatioInfo.setObjectName("acceptedRatioInfo")
        self.acceptedRatio.addWidget(self.acceptedRatioInfo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.acceptedRatio.addItem(spacerItem)
        self.acceptedRatioInput = QtWidgets.QLineEdit(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.acceptedRatioInput.setFont(font)
        self.acceptedRatioInput.setObjectName("acceptedRatioInput")
        self.acceptedRatio.addWidget(self.acceptedRatioInput)
        self.preferencesForm.addLayout(self.acceptedRatio)
        self.unfollowGap = QtWidgets.QHBoxLayout()
        self.unfollowGap.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.unfollowGap.setObjectName("unfollowGap")
        self.unfollowGapLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unfollowGapLabel.sizePolicy().hasHeightForWidth())
        self.unfollowGapLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.unfollowGapLabel.setFont(font)
        self.unfollowGapLabel.setObjectName("unfollowGapLabel")
        self.unfollowGap.addWidget(self.unfollowGapLabel)
        self.unfollowGapInfo = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.unfollowGapInfo.sizePolicy().hasHeightForWidth())
        self.unfollowGapInfo.setSizePolicy(sizePolicy)
        self.unfollowGapInfo.setMinimumSize(QtCore.QSize(2, 2))
        self.unfollowGapInfo.setMaximumSize(QtCore.QSize(15, 15))
        self.unfollowGapInfo.setToolTipDuration(-1)
        self.unfollowGapInfo.setText("")
        self.unfollowGapInfo.setPixmap(QtGui.QPixmap("C:/Users/Gayan/Downloads/info_FILL0_wght300_GRAD200_opsz24.png"))
        self.unfollowGapInfo.setScaledContents(True)
        self.unfollowGapInfo.setObjectName("unfollowGapInfo")
        self.unfollowGap.addWidget(self.unfollowGapInfo)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.unfollowGap.addItem(spacerItem1)
        self.unfollowGapInput = QtWidgets.QLineEdit(parent=Preferences)
        self.unfollowGapInput.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.unfollowGapInput.setFont(font)
        self.unfollowGapInput.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.unfollowGapInput.setInputMask("")
        self.unfollowGapInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.unfollowGapInput.setPlaceholderText("")
        self.unfollowGapInput.setObjectName("unfollowGapInput")
        self.unfollowGap.addWidget(self.unfollowGapInput)
        self.unfollowGapUnit = QtWidgets.QLabel(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.unfollowGapUnit.setFont(font)
        self.unfollowGapUnit.setObjectName("unfollowGapUnit")
        self.unfollowGap.addWidget(self.unfollowGapUnit)
        self.preferencesForm.addLayout(self.unfollowGap)
        self.baseWaiting = QtWidgets.QHBoxLayout()
        self.baseWaiting.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.baseWaiting.setObjectName("baseWaiting")
        self.baseWaitingLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseWaitingLabel.sizePolicy().hasHeightForWidth())
        self.baseWaitingLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.baseWaitingLabel.setFont(font)
        self.baseWaitingLabel.setObjectName("baseWaitingLabel")
        self.baseWaiting.addWidget(self.baseWaitingLabel)
        self.baseWaitingInfo = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.baseWaitingInfo.sizePolicy().hasHeightForWidth())
        self.baseWaitingInfo.setSizePolicy(sizePolicy)
        self.baseWaitingInfo.setMinimumSize(QtCore.QSize(2, 2))
        self.baseWaitingInfo.setMaximumSize(QtCore.QSize(15, 15))
        self.baseWaitingInfo.setToolTipDuration(-1)
        self.baseWaitingInfo.setText("")
        self.baseWaitingInfo.setPixmap(QtGui.QPixmap("C:/Users/Gayan/Downloads/info_FILL0_wght300_GRAD200_opsz24.png"))
        self.baseWaitingInfo.setScaledContents(True)
        self.baseWaitingInfo.setObjectName("baseWaitingInfo")
        self.baseWaiting.addWidget(self.baseWaitingInfo)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.baseWaiting.addItem(spacerItem2)
        self.baseWaitingInput = QtWidgets.QLineEdit(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.baseWaitingInput.setFont(font)
        self.baseWaitingInput.setObjectName("baseWaitingInput")
        self.baseWaiting.addWidget(self.baseWaitingInput)
        self.baseWaitingUnit = QtWidgets.QLabel(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.baseWaitingUnit.setFont(font)
        self.baseWaitingUnit.setObjectName("baseWaitingUnit")
        self.baseWaiting.addWidget(self.baseWaitingUnit)
        self.preferencesForm.addLayout(self.baseWaiting)
        self.automaticMuting = QtWidgets.QHBoxLayout()
        self.automaticMuting.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.automaticMuting.setObjectName("automaticMuting")
        self.automaticMutingLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.automaticMutingLabel.sizePolicy().hasHeightForWidth())
        self.automaticMutingLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.automaticMutingLabel.setFont(font)
        self.automaticMutingLabel.setObjectName("automaticMutingLabel")
        self.automaticMuting.addWidget(self.automaticMutingLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.automaticMuting.addItem(spacerItem3)
        self.automaticMutingCheckbox = QtWidgets.QCheckBox(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.automaticMutingCheckbox.setFont(font)
        self.automaticMutingCheckbox.setText("")
        self.automaticMutingCheckbox.setObjectName("automaticMutingCheckbox")
        self.automaticMuting.addWidget(self.automaticMutingCheckbox)
        self.preferencesForm.addLayout(self.automaticMuting)
        self.followPrivate = QtWidgets.QHBoxLayout()
        self.followPrivate.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.followPrivate.setObjectName("followPrivate")
        self.followPrivateLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.followPrivateLabel.sizePolicy().hasHeightForWidth())
        self.followPrivateLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.followPrivateLabel.setFont(font)
        self.followPrivateLabel.setObjectName("followPrivateLabel")
        self.followPrivate.addWidget(self.followPrivateLabel)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.followPrivate.addItem(spacerItem4)
        self.followPrivateCheckbox = QtWidgets.QCheckBox(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.followPrivateCheckbox.setFont(font)
        self.followPrivateCheckbox.setText("")
        self.followPrivateCheckbox.setObjectName("followPrivateCheckbox")
        self.followPrivate.addWidget(self.followPrivateCheckbox)
        self.preferencesForm.addLayout(self.followPrivate)
        self.onlyFollow = QtWidgets.QHBoxLayout()
        self.onlyFollow.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.onlyFollow.setObjectName("onlyFollow")
        self.onlyFollowLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.onlyFollowLabel.sizePolicy().hasHeightForWidth())
        self.onlyFollowLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.onlyFollowLabel.setFont(font)
        self.onlyFollowLabel.setObjectName("onlyFollowLabel")
        self.onlyFollow.addWidget(self.onlyFollowLabel)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.onlyFollow.addItem(spacerItem5)
        self.onlyFollowCheckbox = QtWidgets.QCheckBox(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.onlyFollowCheckbox.setFont(font)
        self.onlyFollowCheckbox.setText("")
        self.onlyFollowCheckbox.setObjectName("onlyFollowCheckbox")
        self.onlyFollow.addWidget(self.onlyFollowCheckbox)
        self.preferencesForm.addLayout(self.onlyFollow)
        self.verticalLayout_2.addLayout(self.preferencesForm)
        self.saveBtn = QtWidgets.QPushButton(parent=Preferences)
        self.saveBtn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.saveBtn.setFont(font)
        self.saveBtn.setObjectName("saveBtn")
        self.verticalLayout_2.addWidget(self.saveBtn)
        self.savedMessageLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savedMessageLabel.sizePolicy().hasHeightForWidth())
        self.savedMessageLabel.setSizePolicy(sizePolicy)
        self.savedMessageLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.savedMessageLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Titillium Web")
        font.setPointSize(11)
        self.savedMessageLabel.setFont(font)
        self.savedMessageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.savedMessageLabel.setObjectName("savedMessageLabel")
        self.verticalLayout_2.addWidget(self.savedMessageLabel)

        self.retranslateUi(Preferences)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        _translate = QtCore.QCoreApplication.translate
        Preferences.setWindowTitle(_translate("Preferences", "Preferences"))
        self.acceptedRatioLabel.setText(_translate("Preferences", "Accepted Follow Ratio"))
        self.acceptedRatioInfo.setToolTip(_translate("Preferences", "<html><head/><body><p>Only follows/likes if n(following)/n(followers) is greater than the specified value!</p><p>(Greater this is, more likely they would follow back!)</p></body></html>"))
        self.unfollowGapLabel.setText(_translate("Preferences", "Unfollow Gap"))
        self.unfollowGapInfo.setToolTip(_translate("Preferences", "Time to wait before unfollowing a user if they don\'t follow you back!"))
        self.unfollowGapUnit.setText(_translate("Preferences", "(in days)"))
        self.baseWaitingLabel.setText(_translate("Preferences", "Base Waiting Time"))
        self.baseWaitingInfo.setToolTip(_translate("Preferences", "<html><head/><body><p>Approximate waiting time period till an element appears!</p><p>(find a sweet spot that suits your connection speed)</p></body></html>"))
        self.baseWaitingUnit.setText(_translate("Preferences", "(in seconds)"))
        self.automaticMutingLabel.setText(_translate("Preferences", "Automatic Muting"))
        self.followPrivateLabel.setText(_translate("Preferences", "Follow Private Accounts"))
        self.onlyFollowLabel.setText(_translate("Preferences", "Only Follow"))
        self.saveBtn.setText(_translate("Preferences", "Save"))
        self.savedMessageLabel.setText(_translate("Preferences", "Saved!👍"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Preferences = QtWidgets.QDialog()
    ui = Ui_Preferences()
    ui.setupUi(Preferences)
    Preferences.show()
    sys.exit(app.exec())
