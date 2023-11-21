# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from Util import unify_path

class Ui_Regist(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 600)
        Dialog.setMinimumSize(QtCore.QSize(700, 600))
        Dialog.setBaseSize(QtCore.QSize(700, 600))
        exe_path = unify_path().user_path  # 或 application_path

        # 设置字体
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        #设置背景
        self.background_listView = QtWidgets.QListView(Dialog)
        self.background_listView.setGeometry(QtCore.QRect(10, 0, 671, 800))
        self.background_listView.setMinimumSize(QtCore.QSize(0, 0))
        # self.background_listView.setStyleSheet("border-image:url(img/1111.png);")
        background_image_path = os.path.join(exe_path, 'img/OIP.jpeg')
        self.background_listView.setStyleSheet(f"border-image:url({background_image_path});")
        self.background_listView.setObjectName("background_listView")

        # 用户名标签
        self.username_label = QtWidgets.QLabel(Dialog)
        self.username_label.setGeometry(QtCore.QRect(190, 200, 61, 41))
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")

        # 密码标签
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setGeometry(QtCore.QRect(190, 250, 61, 41))
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")

        # 身份标签
        self.identity_label = QtWidgets.QLabel(Dialog)
        self.identity_label.setGeometry(QtCore.QRect(190, 300, 61, 41))
        self.identity_label.setFont(font)
        self.identity_label.setObjectName("identity_label")

        # 设置注册按钮
        self.register_button = QtWidgets.QPushButton(Dialog)
        self.register_button.setGeometry(QtCore.QRect(300, 370, 41, 41))
        button_path = os.path.join(exe_path, 'img/svg/acc.svg')
        self.register_button.setStyleSheet(f"border-image:url({button_path});")
        self.register_button.setObjectName("register_button")

        # 设置输入框样式
        input_font = QtGui.QFont()
        input_font.setFamily("微软雅黑")
        input_font.setPointSize(12)
        lineEdit_style = """
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 5px;
                font-size: 12pt;
                font-family: '微软雅黑';
                background-color: rgba(255, 255, 255, 200);
            }
            QLineEdit:focus {
                border-color: #0078D7;
            }
        """

        # 用户名输入框
        self.username_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.username_lineEdit.setGeometry(QtCore.QRect(260, 200, 191, 31))
        self.username_lineEdit.setFont(input_font)
        self.username_lineEdit.setStyleSheet(lineEdit_style)
        self.username_lineEdit.setObjectName("username_lineEdit")

        # 密码输入框
        self.password_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.password_lineEdit.setGeometry(QtCore.QRect(260, 250, 191, 31))
        self.password_lineEdit.setFont(input_font)
        self.password_lineEdit.setStyleSheet(lineEdit_style)
        self.password_lineEdit.setObjectName("password_lineEdit")

        # 身份输入框
        self.identity_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.identity_lineEdit.setGeometry(QtCore.QRect(260, 300, 191, 31))
        self.identity_lineEdit.setFont(input_font)
        self.identity_lineEdit.setStyleSheet(lineEdit_style)
        self.identity_lineEdit.setObjectName("identity_lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "注册"))
        self.username_label.setText(_translate("Dialog", "用户名"))
        self.password_label.setText(_translate("Dialog", "密码"))
        self.identity_label.setText(_translate("Dialog", "身份"))
