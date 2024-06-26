# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import re
import subprocess
import sys
import traceback
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QPushButton, QProgressBar, QMessageBox, QHBoxLayout, QWidget
import time

from threaddemo.Async import WorkerThread
from util import Database
from util import Util
from pages.TaskWindow import TaskWindow

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPalette

from PyQt5.QtWidgets import QProgressBar, QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPalette


class CustomProgressBar(QProgressBar):
    def __init__(self, parent=None, isRainBow=False):
        super().__init__(parent)
        self.isRainBow = isRainBow  # Add an attribute to track whether it's rainbow or not
        self.setTextVisible(False)

    def setIsRainBow(self, isRainBow):
        self.isRainBow = isRainBow
        self.update()  # Request a repaint when the attribute changes

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        # Calculate the progress value as a percentage
        progress = (self.value() - self.minimum()) * 100 / (self.maximum() - self.minimum())
        # Define the text to be displayed on the progress bar
        text = '{}已完成{:d}%'.format("计算算法" if not self.isRainBow else "计算指标", int(progress))
        # Set the color depending on the widget state
        palette = self.palette()
        color = palette.color(QPalette.Text) if self.isEnabled() else palette.color(QPalette.Disabled, QPalette.Text)
        painter.setPen(color)
        # Draw the text in the center of the progress bar
        painter.drawText(self.rect(), Qt.AlignCenter, text)
        painter.end()


class Ui_Home(object):
    # 新建主任务后发出信号
    switch_to_new_main_task_window = QtCore.pyqtSignal()
    # 点击加号后发出信号
    switch_to_SelfDefining_window = QtCore.pyqtSignal(int)
    # 点击编辑发出信号
    switch_to_new_main_task_window_edit = QtCore.pyqtSignal(int)

    # 当前有多少行
    row_count = 0
    # 新建的任务
    tasklist = []
    task_index = 0

    # 后端返回的参数个数
    num_columns = 3

    # 当前有多少子表行
    row_count_sub = 0

    # 初始化展示出来的数据供子任务查询
    my_dict = {'mainId': [], 'inputfolderPath': [], 'outputfolderPath': []}
    my_progress_list = []
    username = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # 锁死MainWindow不让用户缩放
        MainWindow.resize(1256, 768)
        MainWindow.resize(1256, 768)
        MainWindow.setMinimumSize(QtCore.QSize(1256, 768))
        MainWindow.setBaseSize(QtCore.QSize(1256, 768))
        MainWindow.setFixedSize(1256, 768)
        image_path = "/Users/elona/Desktop/pythonProject/IQA_Software2/IQA_Software/img/47821712483767_.pic.jpg"  # 替换为你的图片路径
        gradient_style = f"""
        QMainWindow {{
            background-image: url({image_path});
            background-repeat: no-repeat;
            background-position: center;
            border: none
        }}
        """
        MainWindow.setStyleSheet(gradient_style)

        self.edit = os.path.join(Util.unify_path().application_path, 'need/edit.png')
        self.add = os.path.join(Util.unify_path().application_path, 'need/add-circle.png')
        self.ashbin = os.path.join(Util.unify_path().application_path, 'need/ashbin.png')

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("QFrame, .QWidget { border: none; }")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")

        self.frame_2 = QtWidgets.QFrame(self.widget_2)
        self.frame_2.setStyleSheet("QFrame#frame_2{\n"
                                   "    background-color: rgba(255, 255, 255, 255);\n"
                                   "    border-radius:20px;\n"
                                   "}")


        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.Button_Create = QtWidgets.QPushButton(self.widget_4)
        self.Button_Create.setObjectName("Button_Create")
        self.horizontalLayout_4.addWidget(self.Button_Create)
        self.Button_Delete = QtWidgets.QPushButton(self.widget_4)
        self.Button_Delete.setStyleSheet("#Button_Delete{\n"
                                         "color:rgb(255, 0, 0);\n"
                                         "}")
        self.Button_Delete.setObjectName("Button_Delete")
        self.horizontalLayout_4.addWidget(self.Button_Delete)
        spacerItem = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.widget_4)
        self.tableWidget_2.setObjectName("tableWidget_2")

        # tableWidget_2是上表格
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setHorizontalHeaderLabels(
            ['序号', '任务名', '执行进度', '输入文件夹', '输出文件夹', '操作', '创建时间'])

        self.horizontalLayout_5.addWidget(self.tableWidget_2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.Button_up_1 = QtWidgets.QPushButton(self.widget_4)
        self.Button_up_1.setObjectName("Button_up_1")
        self.horizontalLayout.addWidget(self.Button_up_1)
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        self.label_2.setEnabled(True)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.Button_down_1 = QtWidgets.QPushButton(self.widget_4)
        self.Button_down_1.setObjectName("Button_down_1")
        self.horizontalLayout.addWidget(self.Button_down_1)
        spacerItem2 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.widget_4)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        # 横向框
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # 任务下拉框
        self.comboBox = QtWidgets.QComboBox(self.widget_4)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox)
        # 执行总时间
        self.zxzsj = QtWidgets.QLabel(self.widget_4)
        self.zxzsj.setObjectName("zxzsj")
        self.horizontalLayout_3.addWidget(self.zxzsj)

        spacerItem_108_23 = QtWidgets.QSpacerItem(108, 20, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem_108_23)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        # 横向框 筛选条件
        self.horizontalLayout_combox = QtWidgets.QHBoxLayout()
        self.horizontalLayout_combox.setObjectName("horizontalLayout_combox")
        # 原图筛选条件
        self.comboBox_oripicname = QtWidgets.QComboBox(self.widget_4)
        self.comboBox_oripicname.setObjectName("comboBox_oripicname")
        self.comboBox_oripicname.addItem("无")
        # 指标筛选条件 默认无
        # self.comboBox_indexname = QtWidgets.QComboBox(self.widget_4)
        # self.comboBox_indexname.setObjectName("comboBox_indexname")
        # self.comboBox_indexname.addItem("无")

        # 针对每一列制造一个筛选下拉框（类似excel）动态根据算法参数个数
        # self.comboBox_col2 = QtWidgets.QComboBox(self.widget_4)
        # self.comboBox_col2.setObjectName("comboBox_col2")
        # self.comboBox_col2.addItem("col2")
        # 参数值筛选条件
        self.cszsxtj = QtWidgets.QLabel(self.widget_4)
        self.cszsxtj.setObjectName("cszsxtj")

        # 用上一个弹簧
        spacerItem_200_20 = QtWidgets.QSpacerItem(380, 20, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)
        spacerItem_300_20 = QtWidgets.QSpacerItem(370, 20, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_combox.addItem(spacerItem_200_20)
        spacerItem_400_20 = QtWidgets.QSpacerItem(320, 20, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)
        spacerItem_700_20 = QtWidgets.QSpacerItem(700, 20, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_combox.addWidget(self.comboBox_oripicname)
        self.horizontalLayout_combox.addItem(spacerItem_300_20)

        self.horizontalLayout_combox.addItem(spacerItem_300_20)

        self.horizontalLayout_combox.addWidget(self.cszsxtj)
        # self.horizontalLayout_combox.addWidget(self.comboBox_col2)
        self.horizontalLayout_combox.addItem(spacerItem_700_20)

        self.verticalLayout.addLayout(self.horizontalLayout_combox)

        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        # tableWidget_4是下面的表格
        self.tableWidget_4 = QtWidgets.QTableWidget(self.widget_4)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(6)
        self.tableWidget_4.setHorizontalHeaderLabels(['任务名', '原图名', '算法名', '执行时间', '增强效果', '操作'])

        self.horizontalLayout_8.addWidget(self.tableWidget_4)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.Button_up_2 = QtWidgets.QPushButton(self.widget_4)
        self.Button_up_2.setObjectName("Button_up_2")
        self.horizontalLayout_6.addWidget(self.Button_up_2)
        self.label_9 = QtWidgets.QLabel(self.widget_4)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.Button_down_2 = QtWidgets.QPushButton(self.widget_4)
        self.Button_down_2.setObjectName("Button_down_2")
        self.horizontalLayout_6.addWidget(self.Button_down_2)
        spacerItem5 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_12.addWidget(self.widget_4)
        self.horizontalLayout_10.addWidget(self.widget_2)
        self.horizontalLayout_11.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1256, 42))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)





        self.Button_Create.clicked.connect(self.HomeToNewMainTask)
        self.Button_Delete.clicked.connect(self.delete_all)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # self.label88.setText(_translate("MainWindow", "Erduo"))
        # self.label_82.setText(_translate("MainWindow", "Pro Member"))
        # __sortingEnabled = self.listWidget88.isSortingEnabled()
        # self.listWidget88.setSortingEnabled(False)
        # item = self.listWidget88.item(0)
        # item.setText(_translate("MainWindow", "Streams"))
        # item = self.listWidget88.item(1)
        # item.setText(_translate("MainWindow", "Games"))
        # item = self.listWidget88.item(2)
        # item.setText(_translate("MainWindow", "New"))
        # item = self.listWidget88.item(3)
        # item.setText(_translate("MainWindow", "Librory"))
        # self.listWidget88.setSortingEnabled(__sortingEnabled)
        # self.label_83.setText(_translate("MainWindow", "Join pro"))
        # self.label_84.setText(_translate("MainWindow", "for free"))
        # self.label_85.setText(_translate("MainWindow", "games."))

        self.label_4.setText(_translate("MainWindow", "主任务列表"))
        self.Button_Create.setText(_translate("MainWindow", "新建主任务"))
        self.Button_Delete.setText(_translate("MainWindow", "删除所有任务"))
        # self.Button_up_1.setText(_translate("MainWindow", "上一页"))
        # self.label_2.setText(_translate("MainWindow", "1/5"))
        # self.Button_down_1.setText(_translate("MainWindow", "下一页"))
        self.label_3.setText(_translate("MainWindow", "子任务列表"))
        self.comboBox.setItemText(0, _translate("MainWindow", ""))
        self.zxzsj.setText(_translate("MainWindow", "执行总时间：无（单位ms）"))
        self.cszsxtj.setText(_translate("MainWindow", "                                               "))
        # self.Button_up_2.setText(_translate("MainWindow", "上一页"))
        # self.label_9.setText(_translate("MainWindow", "1/5"))
        # self.Button_down_2.setText(_translate("MainWindow", "下一页"))

        self.Button_up_2.setFixedSize(100, 30)
        self.Button_up_2.setStyleSheet("background:transparent;")

        self.Button_down_2.setFixedSize(100, 30)
        self.Button_down_2.setStyleSheet("background:transparent;")

        self.Button_up_1.setFixedSize(100, 30)
        self.Button_up_1.setStyleSheet("background:transparent;")

        self.Button_down_1.setFixedSize(100, 30)
        self.Button_down_1.setStyleSheet("background:transparent;")

    def HomeToNewMainTask(self):
        self.switch_to_new_main_task_window.emit()

    # 从新建主任务点击完成（数据库已添加）后调用
    def add_task(self):
        self.show_maintask()


    # 从编辑点击完成后调用这个
    def update_task(self, row):
        task_dict = Database.selectMaintaskByRow(row, self.username)
        print("更新后任务", task_dict)
        self.show_maintask()
    def openImage(self, path):
        if sys.platform == 'win32':
            os.startfile(path)  # Windows
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])  # macOS
        else:
            subprocess.Popen(['xdg-open', path])  # Linux

    def set_table_item(self, table, row, column, text, align_center=False):
        item = QTableWidgetItem(str(text))
        if align_center:
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        table.setItem(row, column, item)
    def draw_one_maintask_record(self, i, j, isinsert, isInit=False):
        if isinsert:
            self.tableWidget_2.insertRow(i)
            progressbar = CustomProgressBar()
            self.my_progress_list.append({str(i): progressbar})
            buttonList = TaskWindow(self.edit, 1, self.add, self.ashbin, i + 1)
            buttonList.button_add.clicked.connect(partial(self.addbutton_clicked, buttonList))

            buttonList.button_status.clicked.connect(partial(self.start_task, progressbar, buttonList))

            buttonList.button_edit.clicked.connect(partial(self.editbutton_clicked, buttonList))
            buttonList.button_delete.clicked.connect(partial(self.delete_tab2row, buttonList))

            self.set_table_item(self.tableWidget_2, i, 0, j["Id"], align_center=True)
            self.set_table_item(self.tableWidget_2, i, 1, j["task_name"], align_center=True)
            self.tableWidget_2.setCellWidget(i, 2, progressbar)
            self.set_table_item(self.tableWidget_2, i, 3, j["input"])
            self.set_table_item(self.tableWidget_2, i, 4, j["output"])
            self.tableWidget_2.setCellWidget(i, 5, buttonList)
            self.set_table_item(self.tableWidget_2, i, 6, j["create_time"], align_center=True)
        else:
            self.tableWidget_2.removeRow(i)

    def show_maintask(self, isInit=False):
        try:
            self.my_dict = {'mainId': [], 'inputfolderPath': [], 'outputfolderPath': []}
            self.tableWidget_2.setColumnWidth(5, 180)
            self.tableWidget_2.setColumnWidth(2, 280)
            self.tableWidget_2.verticalHeader().setDefaultSectionSize(50)  # 使表高固定
            maintask_list = Database.selectAll(Ui_Home.username)
            if not maintask_list is None:
                Ui_Home.row_count = len(maintask_list)
                current_row_count = self.tableWidget_2.rowCount()
                for i in range(current_row_count, len(maintask_list)):
                    self.draw_one_maintask_record(i, maintask_list[i], True, isInit)
                # 如果数据库中的任务数量小于当前表格的行数，则删除多余的行
                for i in range(len(maintask_list), current_row_count):
                    self.draw_one_maintask_record(i, None, False, isInit)
                # 更新已有的数据
                for i, j in enumerate(maintask_list):
                    self.my_dict['mainId'].append(j["Id"])
                    self.my_dict['inputfolderPath'].append(j["input"])
                    self.my_dict['outputfolderPath'].append(j["output"])
                    self.set_table_item(self.tableWidget_2, i, 0, j["Id"], align_center=True)
                    self.set_table_item(self.tableWidget_2, i, 1, j["task_name"], align_center=True)
                    self.set_table_item(self.tableWidget_2, i, 3, j["input"])
                    self.set_table_item(self.tableWidget_2, i, 4, j["output"])
                    self.set_table_item(self.tableWidget_2, i, 6, j["create_time"], align_center=True)
            else:
                pass
        except Exception as e:
            traceback.print_exc()

    def show_subtask(self):
        # 凑出已有的任务（初始化subtask）
        self.tableWidget_4.setRowCount(0)
        self.comboBox.clear()
        yiyoutaskList = []
        for i in self.my_dict['mainId']:
            for j in range(0, Database.count_table(self.username, i)):
                yiyoutaskList.append("任务{}_{}".format(i, j + 1))
        # yiyoutask = ["任务{}".format(i) for i in self.my_dict['mainId']]
        # 查数据库有多少个Subtask+self.my_dict['mainId']+username的开头的表
        self.comboBox.addItems(yiyoutaskList)
        self.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.comboBox_oripicname.currentIndexChanged.connect(self.selectByOriPicName)
        if yiyoutaskList is not None:
            self.comboBox.setCurrentIndex(1)
        self.tableWidget_4.verticalHeader().setDefaultSectionSize(50)

    def updateOneRecord(self, i, executetime):
        self.set_table_item(self.tableWidget_4, i, 3, executetime, True)

    def selectionchange(self):
        self.tableWidget_4.setRowCount(0)
        # 提取数字
        try:
            if self.comboBox.currentText():
                d = re.findall(r'\d+', self.comboBox.currentText().split("_")[0])
                d2 = re.findall(r'\d+', self.comboBox.currentText().split("_")[1])
                # 先获取当前选择的任务
                result = Database.select_stastic(d[0], d2[0], self.username)
                if result:
                    self.zxzsj.setText("算法执行总时间：{}ms   指标生成总时间：{}ms".format(result['total_algtime'],
                                                                                          result['total_indextime']))
                self.initSubFormUi(d[0], False, d2[0])
        except Exception as e:
            traceback.print_exc()
            return

    def selectByOriPicName(self):
        self.tableWidget_4.setRowCount(0)
        # 提取数字
        try:
            d = re.findall(r'\d+', self.comboBox.currentText().split("_")[0])
            d2 = re.findall(r'\d+', self.comboBox.currentText().split("_")[1])
            self.initSubFormUi(d[0], True, d2[0])
        except Exception as e:
            traceback.print_exc()
            return

    def add_task_2(self, row):
        self.show_subtask()
    def addbutton_clicked(self, task):
        self.switch_to_SelfDefining_window.emit(task.row)

    def editbutton_clicked(self, task):

        print('编辑mainid', task.row)
        self.switch_to_new_main_task_window_edit.emit(task.row)

    # 这个场景也实现了在不知道有多少个删除按钮的情况下实现了对按钮的移除self.sender()会自动解析传递过来对信号找到对应对按钮
    # 注意只有一个按钮的时候可以用这种方法获取，封装成一个task到时候需要在task中定义row editbutton_clicked同理
    def delete_tab4row(self):
        button = self.sender()
        row = self.tableWidget_4.indexAt(button.pos()).row()
        print("delete", row)
        self.tableWidget_4.removeRow(row)
        d = re.findall(r'\d+', self.comboBox.currentText())
        Database.delete_subdataByrow(row + 1, d[0])

    # 以下是多线程执行任务的逻辑
    def start_task(self, progress, task):
        # 获取当前选择的行（任务）
        self.row = task.row
        print("正在执行", task.row)
        # 创建工作线程 获取d2
        # d2 = re.findall(r'\d+', self.comboBox.currentText().split("_")[1])
        self.worker_thread = WorkerThread(task.row, self.username)

        self.worker_thread.progress_signal.connect(self.update_progress_bar)
        self.worker_thread.finished_signal.connect(self.onTaskFinished)
        self.worker_thread.start()

    def update_progress_bar(self, value, color, isRainBow, row, excuteTime, i):
        # 更新进度条的值和颜色
        print("更新进度条的值和颜色", value, color)
        # 获取第i个progress_bar
        progress_bar_i = self.my_progress_list[row - 1][str(row - 1)]
        progress_bar_i.setValue(value)
        progress_bar_i.setIsRainBow(isRainBow)
        if isRainBow == 1:
            # 设置一种渐变背景色
            zhibiaoorsuanfa = '计算指标'
            gradient_style = """
                QProgressBar::chunk {
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                                      stop: 0 #FF0000,    /* Red */
                                                      stop: 0.14 #FF7F00, /* Orange */
                                                      stop: 0.28 #FFFF00, /* Yellow */
                                                      stop: 0.42 #00FF00, /* Green */
                                                      stop: 0.57 #0000FF, /* Blue */
                                                      stop: 0.71 #4B0082, /* Indigo */
                                                      stop: 0.85 #9400D3); /* Violet */
                }
                """
        else:
            # 设置蓝绿背景色
            zhibiaoorsuanfa = '计算算法'
            gradient_style = """
            QProgressBar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                                  stop: 0 #62E4FF, stop: 0.5 #23A6D5, stop: 1 #23D5AB);
            }
            """
        progress_bar_i.setStyleSheet(f"""
        QProgressBar {{
            border: 2px solid grey;
            border-radius: 5px;
            background-color: #FFFFFF;
            text-align: center;
            height: 15px;
        }}
        {gradient_style}
        """)
        # 更新执行时间
        if not excuteTime is 0.0 and i is not 9999999:
            self.updateOneRecord(i, excuteTime)

    def onTaskFinished(self, total_time, index_time):
        # 所有任务完成后的操作
        QMessageBox.information(self, "完成", "所有任务执行成功。")
        # 在这里可以更新UI，例如按钮状态等

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "是否退出?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 停止线程
            if self.worker_thread is not None:
                self.worker_thread.stop()  # 优雅地停止线程
                self.worker_thread.wait()  # 等待线程真正停止
            event.accept()  # 确认关闭
        else:
            event.ignore()  # 忽略关闭事件

    def delete_all(self):
        Database.deleteSth(self.username, None)
        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)
        Ui_Home.row_count = 0

    def delete_tab2row(self, task):
        print(task.row)
        self.tableWidget_2.removeRow(task.row - 1)
        Database.deleteSth(self.username, task.row)
        Ui_Home.row_count = Ui_Home.row_count - 1
        # 先把删除的那一行后面的所有的行数都需要重制row索引
        for i in range(task.row, len(Ui_Home.tasklist)):
            print(Ui_Home.tasklist[i].row, '6', i)
            Ui_Home.tasklist[i].row = i
        # del Ui_Home.tasklist[task.row-1]
        # 可用的索引-1
        Ui_Home.task_index = Ui_Home.task_index - 1

        print("删除一行后row_count", Ui_Home.row_count)

    def initIcon(self, widget, icon):
        self.pixmap = QPixmap(icon)
        widget.setIcon(QtGui.QIcon(self.pixmap))
        # 按钮的大小
        widget.setIconSize(QSize(30, 30))
        widget.setMinimumSize(QSize(30, 30))
        widget.setMaximumSize(QSize(30, 30))
        # 按钮透明
        widget.setFlat(True)
        widget.setStyleSheet("background:transparent;")
        return widget

    def center_button_in_table(self, table, row, column, button):
        # 创建一个QWidget作为容器
        widget = QWidget()
        # 创建水平布局
        layout = QHBoxLayout(widget)
        # 设置布局的边距为0，这样按钮可以填满整个单元格
        layout.setContentsMargins(0, 0, 0, 0)
        # 添加伸缩因子在按钮前后，这样会推动按钮到中间
        layout.addStretch()
        layout.addWidget(button)
        layout.addStretch()
        # 设置QWidget的布局
        widget.setLayout(layout)
        # 把这个QWidget设置为表格的单元格小部件
        table.setCellWidget(row, column, widget)

    # 传入主任务id来初始化子表
    def initSubFormUi(self, id, isClickOriPicCombox, subtable_id):
        try:
            # 如果点下拉框筛选原图的记录
            if isClickOriPicCombox:
                if self.comboBox_oripicname.currentText() == "无":
                    kk = Database.selectall_subdataById(id, False, None, None, Ui_Home.username, subtable_id)
                else:
                    kk = Database.selectall_subdataById(id, False, True, self.comboBox_oripicname.currentText(),
                                                        Ui_Home.username, subtable_id)
            # 每次都得从数据库拿默认查某个子任务所有数据
            else:
                self.comboBox_oripicname.clear()
                self.comboBox_oripicname.addItem("无")
                list_pic = Database.selectDistinctOriPicName(id, self.username, subtable_id)
                for pic in list_pic:
                    index = self.comboBox_oripicname.findText(pic)
                    # 检查返回的索引，如果索引不是 -1，则表示已经存在该项
                    if index != -1:
                        print("已有下拉框值")
                    else:
                        # 如果不存在，则可以添加该项
                        self.comboBox_oripicname.addItem(pic)
                        # self.comboBox_oripicname.addItem(pic)
                        self.comboBox_oripicname.setFixedSize(100, 20)
                kk = Database.selectall_subdataById(id, False, None, None, Ui_Home.username, subtable_id)
            self.tableWidget_4.setColumnWidth(4, 380)
            output_folder = Database.selectMaintaskByRow(id, Ui_Home.username)["output"]
            if not kk is None:
                for i, j in enumerate(kk):
                    # 删除按钮
                    self.button_delete = QPushButton()
                    self.initIcon(self.button_delete, "./iconfont/error.png")
                    self.tableWidget_4.insertRow(i)

                    self.button_seePic = QPushButton()
                    self.button_seePic.setText(j["Ori_Imgname"])
                    self.button_seePic.setStyleSheet("background:transparent;")

                    self.button_seeEnhancedPic = QPushButton()

                    oriimage_name = str(j["Ori_Imgname"]).split(".")[0]
                    suffix = str(j["Ori_Imgname"]).split(".")[1]

                    # 读取json判断该条记录的参数个数拼接
                    paramList = [paramname for paramname in
                                 list(Util.get_data_from_config(j["Alg_Name"]))]

                    joinedPicName = oriimage_name + "%%" + j["Alg_Name"]
                    # 遍历并打印字典的值
                    for param_name in paramList:
                        joinedPicName = joinedPicName + "%%" + str(j[param_name])

                    enhancedPicName = joinedPicName + "." + suffix

                    # enhancedPicName = oriimage_name + "%%" + str(j["Alg_Name"]) + "%%" + str(j["alpha"]) + "%%" + str(
                    #     j["iterations"] + "%%" + str(j["kernel_size"])) + "." + suffix
                    self.button_seeEnhancedPic.setText(enhancedPicName)
                    self.button_seeEnhancedPic.setStyleSheet("QPushButton {background: transparent;}")

                    self.set_table_item(self.tableWidget_4, i, 0, ((j["Taskname"])), True)
                    self.tableWidget_4.setCellWidget(i, 1, self.button_seePic)

                    self.set_table_item(self.tableWidget_4, i, 2, (j["Alg_Name"]), True)
                    self.set_table_item(self.tableWidget_4, i, 3, (j["Execute_Time"]), True)
                    self.tableWidget_4.setCellWidget(i, 4, self.button_seeEnhancedPic)
                    self.center_button_in_table(self.tableWidget_4, i, 5, self.button_delete)
                    # self.tableWidget_4.setCellWidget(i, 7, self.button_delete)
                    self.button_delete.clicked.connect(self.delete_tab4row)
                    self.button_seePic.clicked.connect(
                        partial(self.openImage, self.my_dict['inputfolderPath'][int(id) - 1] + '/' + j["Ori_Imgname"]))
                    self.button_seeEnhancedPic.clicked.connect(
                        partial(self.openImage, self.my_dict['outputfolderPath'][int(id) - 1] + '/' + enhancedPicName))

        except Exception as e:
            traceback.print_exc()
            print(e)
