import os
import sys
from PyQt5.QtWidgets import  QPushButton, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5 import QtGui

import Util


class TaskWindow_2(QWidget):

    def __init__(self, img_src1, status, img_src3, img_src4):
        super().__init__()
        status = 4 #测试
        # if status == 1:
        #     img_src2 = './need/play.png'
        # if status == 2:
        #     img_src2 = './need/stop.png'
        # if status == 3:
        #     img_src2 = './need/warning.png'
        # if status == 4:
        #     img_src2 = './need/success.png'

#创建四个按钮
        #编辑按钮
        if status == 1:
            #校准路径
            img_src2 = 'need/play.png'
            img_src2 = os.path.join(Util.unify_path().application_path, img_src2)

        if status == 2:
            img_src2 = 'need/stop.png'
            img_src2 = os.path.join(Util.unify_path().application_path, img_src2)
        if status == 3:
            img_src2 = 'need/warning.png'
            img_src2 = os.path.join(Util.unify_path().application_path, img_src2)
        if status == 4:
            img_src2 = 'need/success.png'
            img_src2 = os.path.join(Util.unify_path().application_path, img_src2)
        self.button_edit = QPushButton()
        self.pixmap = QPixmap(img_src1)
        self.button_edit.setIcon(QtGui.QIcon(self.pixmap))
        #按钮的大小
        self.button_edit.setIconSize(QSize(30, 30))
        self.button_edit.setMinimumSize(QSize(30, 30))
        self.button_edit.setMaximumSize(QSize(30, 30))
        #按钮透明
        self.button_edit.setFlat(True)
        self.button_edit.setStyleSheet("background:transparent;")
        # 点击按钮时连接到相应的槽
        self.button_edit.clicked.connect(self.button_clicked)

        #状态按钮
        self.button_status = QPushButton()
        self.pixmap = QPixmap(img_src2)
        self.button_status.setIcon(QtGui.QIcon(self.pixmap))
        #按钮的大小
        self.button_status.setIconSize(QSize(30, 30))
        self.button_status.setMinimumSize(QSize(30, 30))
        self.button_status.setMaximumSize(QSize(30, 30))
        #按钮透明
        self.button_status.setFlat(True)
        self.button_status.setStyleSheet("background:transparent;")
        # 点击按钮时连接到相应的槽
        self.button_status.clicked.connect(self.button_clicked)

        # 添加按钮 类变量初始化
        self.button_add = QPushButton()
        self.pixmap = QPixmap(img_src3)
        self.button_add.setIcon(QtGui.QIcon(self.pixmap))
        #按钮的大小
        self.button_add.setIconSize(QSize(30, 30))
        self.button_add.setMinimumSize(QSize(30, 30))
        self.button_add.setMaximumSize(QSize(30, 30))
        #按钮透明
        self.button_add.setFlat(True)
        self.button_add.setStyleSheet("background:transparent;")
        # 点击按钮时连接到相应的槽
        # self.button_add.clicked.connect(self.button_clicked)

        #删除按钮
        self.button_delete = QPushButton()
        self.pixmap = QPixmap(img_src4)
        self.button_delete.setIcon(QtGui.QIcon(self.pixmap))
        #按钮的大小
        self.button_delete.setIconSize(QSize(30, 30))
        self.button_delete.setMinimumSize(QSize(30, 30))
        self.button_delete.setMaximumSize(QSize(30, 30))
        #按钮透明
        self.button_delete.setFlat(True)
        self.button_delete.setStyleSheet("background:transparent;")




        # 创建一个水平布局，并将按钮添加到布局中
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button_edit)
        self.layout.addWidget(self.button_status)
        self.layout.addWidget(self.button_add)
        self.layout.addWidget(self.button_delete)

        # 设置该窗口的布局
        self.setLayout(self.layout)
    #
    def button_clicked(self):
        print("666")

