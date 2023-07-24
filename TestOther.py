#该文件用于测试部分代码块
#1.
# from PyQt5.QtSql import QSqlQuery, QSqlDatabase
#
# db = QSqlDatabase.addDatabase("QSQLITE")
# db.setDatabaseName("test.db")
# if not db.open():
#     t("无法连接数据库")
#
# query = QSqlQuery()
#
# columns_str = "p1,p2,p3,p4"
# placeholders = "?,?,?,?"
# query = QSqlQuery()
#
# query.prepare("INSERT INTO task (taskname,describe,{}) VALUES (?,?,{})".format(columns_str,placeholders))
# t("INSERT INTO task (taskname,describe,{}) VALUES (?,?,{})".format(columns_str,placeholders))
# for i,j in list(zip(range(6),['a','b',7,4,5,6])):
#     print(j)
#     query.addBindValue(j)
# query.exec_()
# print(query.boundValues())

#2.
# import sys
# from PyQt5 import QtCore, QtWidgets
#
# from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QStackedWidget
#
# from home import Ui_Home
# from newMaintask import Ui_NewMaintask




#一开始的这种跳转方式其实不合理
# class Page1(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.btn1 = QPushButton('跳转到 Page2', self)
#         self.btn1.clicked.connect(self.btn1_clicked)
#
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.btn1)
#
#     def btn1_clicked(self):
#
#         self.stacked_widget.setCurrentWidget(self.page2)
#
# class Page2(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.btn2 = QPushButton('跳转到 Page1', self)
#         self.btn2.clicked.connect(self.btn2_clicked)
#
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.btn2)
#
#     def btn2_clicked(self):
#         self.stacked_widget.setCurrentWidget(self.page1)
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.page1 = Page1()
#         self.page2 = Page2()
#
#         self.stacked_widget = QStackedWidget(self)
#         self.stacked_widget.addWidget(self.page1)
#         self.stacked_widget.addWidget(self.page2)
#         self.stacked_widget.setCurrentWidget(self.page1)
#         self.page1.stacked_widget = self.stacked_widget
#         self.page2.stacked_widget = self.stacked_widget
#         self.page1.page2 = self.page2
#         self.page2.page1 = self.page1
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

#3.
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5 import QtGui



class TaskWindow(QWidget):
    switch_window = pyqtSignal()

    def __init__(self, img_src1, status, img_src3, img_src4):
        super().__init__()
        status = 4 #测试
        if status == 1:
            img_src2 = './need/play.png'
        if status == 2:
            img_src2 = './need/stop.png'
        if status == 3:
            img_src2 = './need/warning.png'
        if status == 4:
            img_src2 = 'need/success.png'

#创建四个按钮
        #编辑按钮
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





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个按钮
        self.button = QPushButton('Add Task')
        self.button.clicked.connect(self.add_task)

        # 创建一个垂直布局
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)

        # 创建一个中心部件，并将布局设置为其布局
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        # 将中心部件设置为主窗口的中心部件
        self.setCentralWidget(self.central_widget)

    def add_task(self):
        status = 1#默认是play--1 stop--2 warning--3 success--4
        # 每次点击按钮，新建一个任务窗口
        task = TaskWindow('./need/edit.png',status,'./need/add-circle.png','./need/ashbin.png')
        self.layout.addWidget(task)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

