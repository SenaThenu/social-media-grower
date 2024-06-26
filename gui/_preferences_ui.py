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
        Preferences.resize(443, 288)
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
        self.acceptedFollowRatio = QtWidgets.QHBoxLayout()
        self.acceptedFollowRatio.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.acceptedFollowRatio.setObjectName("acceptedFollowRatio")
        self.acceptedFollowRatioLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptedFollowRatioLabel.sizePolicy().hasHeightForWidth())
        self.acceptedFollowRatioLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.acceptedFollowRatioLabel.setFont(font)
        self.acceptedFollowRatioLabel.setObjectName("acceptedFollowRatioLabel")
        self.acceptedFollowRatio.addWidget(self.acceptedFollowRatioLabel)
        self.acceptedFollowRatioInfo = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.acceptedFollowRatioInfo.sizePolicy().hasHeightForWidth())
        self.acceptedFollowRatioInfo.setSizePolicy(sizePolicy)
        self.acceptedFollowRatioInfo.setMinimumSize(QtCore.QSize(2, 2))
        self.acceptedFollowRatioInfo.setMaximumSize(QtCore.QSize(15, 15))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.acceptedFollowRatioInfo.setFont(font)
        self.acceptedFollowRatioInfo.setToolTipDuration(-1)
        self.acceptedFollowRatioInfo.setText("")
        self.acceptedFollowRatioInfo.setPixmap(QtGui.QPixmap("C:/Users/Gayan/Downloads/info_FILL0_wght300_GRAD200_opsz24.png"))
        self.acceptedFollowRatioInfo.setScaledContents(True)
        self.acceptedFollowRatioInfo.setObjectName("acceptedFollowRatioInfo")
        self.acceptedFollowRatio.addWidget(self.acceptedFollowRatioInfo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.acceptedFollowRatio.addItem(spacerItem)
        self.acceptedFollowRatioInput = QtWidgets.QLineEdit(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.acceptedFollowRatioInput.setFont(font)
        self.acceptedFollowRatioInput.setObjectName("acceptedFollowRatioInput")
        self.acceptedFollowRatio.addWidget(self.acceptedFollowRatioInput)
        self.preferencesForm.addLayout(self.acceptedFollowRatio)
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
        font.setFamily("Segoe UI")
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
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.unfollowGapInfo.setFont(font)
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
        font.setFamily("Segoe UI")
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
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.unfollowGapUnit.setFont(font)
        self.unfollowGapUnit.setObjectName("unfollowGapUnit")
        self.unfollowGap.addWidget(self.unfollowGapUnit)
        self.preferencesForm.addLayout(self.unfollowGap)
        self.baseWaitingTime = QtWidgets.QHBoxLayout()
        self.baseWaitingTime.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.baseWaitingTime.setObjectName("baseWaitingTime")
        self.baseWaitingTimeLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseWaitingTimeLabel.sizePolicy().hasHeightForWidth())
        self.baseWaitingTimeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.baseWaitingTimeLabel.setFont(font)
        self.baseWaitingTimeLabel.setObjectName("baseWaitingTimeLabel")
        self.baseWaitingTime.addWidget(self.baseWaitingTimeLabel)
        self.baseWaitingTimeInfo = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.baseWaitingTimeInfo.sizePolicy().hasHeightForWidth())
        self.baseWaitingTimeInfo.setSizePolicy(sizePolicy)
        self.baseWaitingTimeInfo.setMinimumSize(QtCore.QSize(2, 2))
        self.baseWaitingTimeInfo.setMaximumSize(QtCore.QSize(15, 15))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.baseWaitingTimeInfo.setFont(font)
        self.baseWaitingTimeInfo.setToolTipDuration(-1)
        self.baseWaitingTimeInfo.setText("")
        self.baseWaitingTimeInfo.setPixmap(QtGui.QPixmap("C:/Users/Gayan/Downloads/info_FILL0_wght300_GRAD200_opsz24.png"))
        self.baseWaitingTimeInfo.setScaledContents(True)
        self.baseWaitingTimeInfo.setObjectName("baseWaitingTimeInfo")
        self.baseWaitingTime.addWidget(self.baseWaitingTimeInfo)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.baseWaitingTime.addItem(spacerItem2)
        self.baseWaitingTimeInput = QtWidgets.QLineEdit(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.baseWaitingTimeInput.setFont(font)
        self.baseWaitingTimeInput.setObjectName("baseWaitingTimeInput")
        self.baseWaitingTime.addWidget(self.baseWaitingTimeInput)
        self.baseWaitingTimeUnit = QtWidgets.QLabel(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.baseWaitingTimeUnit.setFont(font)
        self.baseWaitingTimeUnit.setObjectName("baseWaitingTimeUnit")
        self.baseWaitingTime.addWidget(self.baseWaitingTimeUnit)
        self.preferencesForm.addLayout(self.baseWaitingTime)
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
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.automaticMutingLabel.setFont(font)
        self.automaticMutingLabel.setObjectName("automaticMutingLabel")
        self.automaticMuting.addWidget(self.automaticMutingLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.automaticMuting.addItem(spacerItem3)
        self.automaticMutingCheckbox = QtWidgets.QCheckBox(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.automaticMutingCheckbox.setFont(font)
        self.automaticMutingCheckbox.setText("")
        self.automaticMutingCheckbox.setChecked(False)
        self.automaticMutingCheckbox.setObjectName("automaticMutingCheckbox")
        self.automaticMuting.addWidget(self.automaticMutingCheckbox)
        self.preferencesForm.addLayout(self.automaticMuting)
        self.followPrivateAccounts = QtWidgets.QHBoxLayout()
        self.followPrivateAccounts.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.followPrivateAccounts.setObjectName("followPrivateAccounts")
        self.followPrivateAccountsLabel = QtWidgets.QLabel(parent=Preferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.followPrivateAccountsLabel.sizePolicy().hasHeightForWidth())
        self.followPrivateAccountsLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.followPrivateAccountsLabel.setFont(font)
        self.followPrivateAccountsLabel.setObjectName("followPrivateAccountsLabel")
        self.followPrivateAccounts.addWidget(self.followPrivateAccountsLabel)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.followPrivateAccounts.addItem(spacerItem4)
        self.followPrivateAccountsCheckbox = QtWidgets.QCheckBox(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.followPrivateAccountsCheckbox.setFont(font)
        self.followPrivateAccountsCheckbox.setText("")
        self.followPrivateAccountsCheckbox.setObjectName("followPrivateAccountsCheckbox")
        self.followPrivateAccounts.addWidget(self.followPrivateAccountsCheckbox)
        self.preferencesForm.addLayout(self.followPrivateAccounts)
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
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.onlyFollowLabel.setFont(font)
        self.onlyFollowLabel.setObjectName("onlyFollowLabel")
        self.onlyFollow.addWidget(self.onlyFollowLabel)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.onlyFollow.addItem(spacerItem5)
        self.onlyFollowCheckbox = QtWidgets.QCheckBox(parent=Preferences)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
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
        font.setFamily("Segoe UI")
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
        font.setFamily("Segoe UI")
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
        self.acceptedFollowRatioLabel.setText(_translate("Preferences", "Accepted Follow Ratio"))
        self.acceptedFollowRatioInfo.setToolTip(_translate("Preferences", "<html><head/><body><p>Only follows/likes if n(following)/n(followers) is greater than the specified value!</p><p>(Greater this is, more likely they would follow back!)</p></body></html>"))
        self.unfollowGapLabel.setText(_translate("Preferences", "Unfollow Gap"))
        self.unfollowGapInfo.setToolTip(_translate("Preferences", "Time to wait before unfollowing a user if they don\'t follow you back!"))
        self.unfollowGapUnit.setText(_translate("Preferences", "(in days)"))
        self.baseWaitingTimeLabel.setText(_translate("Preferences", "Base Waiting Time"))
        self.baseWaitingTimeInfo.setToolTip(_translate("Preferences", "<html><head/><body><p>Approximate waiting time period till an element appears!</p><p>(find a sweet spot that suits your connection speed)</p></body></html>"))
        self.baseWaitingTimeUnit.setText(_translate("Preferences", "(in seconds)"))
        self.automaticMutingLabel.setText(_translate("Preferences", "Automatic Muting"))
        self.followPrivateAccountsLabel.setText(_translate("Preferences", "Follow Private Accounts"))
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
