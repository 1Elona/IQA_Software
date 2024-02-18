# -*- coding: utf-8 -*-

import os

import PyQt5.QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets

import Database
from Util import unify_path

class Ui_Dialog(object):
    # 定义两个信号用于窗口切换
    switch_window = QtCore.pyqtSignal()
    switch_windowto_regist = QtCore.pyqtSignal()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 600)
        Dialog.setMinimumSize(QtCore.QSize(700, 600))
        Dialog.setBaseSize(QtCore.QSize(700, 600))
        Dialog.setFixedSize(700, 600)
        # 根据运行环境设置路径
        exe_path = unify_path().user_path

        # 背景图片
        self.background_listView = QtWidgets.QListView(Dialog)
        self.background_listView.setGeometry(QtCore.QRect(10, 0, 671, 800))
        background_image_path = os.path.join(exe_path, 'img/OIP.jpeg')
        self.background_listView.setStyleSheet(f"border-image:url({background_image_path});")
        self.background_listView.setObjectName("background_listView")

        # 设置字体
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)

        # 用户标签
        self.User_label = QtWidgets.QLabel(Dialog)
        self.User_label.setGeometry(QtCore.QRect(190, 250, 61, 41))
        self.User_label.setFont(font)
        self.User_label.setObjectName("User_label")

        # 密码标签
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setGeometry(QtCore.QRect(190, 300, 61, 31))
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")

        # 登录按钮
        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setGeometry(QtCore.QRect(400, 370, 41, 41))
        button_path = os.path.join(exe_path, 'img/svg/login.svg')
        self.login_button.setStyleSheet(f"border-image:url({button_path});")
        self.login_button.setObjectName("login_button")

        # 注册按钮
        self.regist_button = QtWidgets.QPushButton(Dialog)
        self.regist_button.setGeometry(QtCore.QRect(230, 370, 41, 41))
        button_path = os.path.join(exe_path, 'img/svg/regist.svg')
        self.regist_button.setStyleSheet(f"border-image:url({button_path});")
        self.regist_button.setObjectName("regist_button")

        # 主标题标签
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(160, 80, 411, 161))
        self.label_3.setStyleSheet("""
            QLabel {
                color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 black, stop: 1 #333333
                );
                font-family: '楷体';
                font-size: 36pt;
                padding: 5px;
            }
        """)
        font.setFamily("楷体")
        font.setPointSize(36)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        # 设置输入框样式
        input_font = QtGui.QFont()
        input_font.setFamily("微软雅黑")
        input_font.setPointSize(12)
        style_sheet = """
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

        # 账户输入框
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(250, 300, 191, 31))
        self.lineEdit.setFont(input_font)
        self.lineEdit.setStyleSheet(style_sheet)
        self.lineEdit.setObjectName("lineEdit")

        # 密码输入框
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 250, 191, 31))
        self.lineEdit_2.setFont(input_font)
        self.lineEdit_2.setStyleSheet(style_sheet)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.login_button.clicked.connect(self.login)
        self.regist_button.clicked.connect(self.show_regist)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "图像处理"))
        self.User_label.setText(_translate("Dialog", "账户"))
        self.password_label.setText(_translate("Dialog", "密码"))
        self.label_3.setText(_translate("Dialog", "图像算法批量处理平台"))
    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if self.lineEdit.text() == "":
            PyQt5.QtWidgets.QMessageBox.warning(self, '警告', '密码不能为空，请输入！')
        if Database.login(username,password):
            self.switch_window.emit()
        else:
            PyQt5.QtWidgets.QMessageBox.critical(self, '错误', '密码错误！')
            self.lineEdit.clear()

        return Database.login(username,password)
    def show_regist(self):
        # 1打开新窗口
        self.switch_windowto_regist.emit()






