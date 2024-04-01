import os
import sys
from functools import partial

import util.Util
from util.Util import unify_path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from util import Database
from service import handleuserinput
from pages.Page_Autoconfig import Ui_AutoConfig
from pages.Page_Home import Ui_Home
from pages.Page_Index import Ui_Index
from pages.Page_NewMainTask import Ui_NewMaintask
from pages.Page_SelfDefining import Ui_SelfDefining
from pages.Page_Setting import Ui_Setting
from pages.TaskWindow import TaskWindow
from util.Util import get_data_from_config
from pages.Page_Login import Ui_Dialog
from pages.Page_Regist import Ui_Regist


#原图名可以做成超链接查看原图 删除子数据
#删除主任务的时候其生成的子任务也要删除 且释放的序号需要还原
#算法设置页面介绍算法 管理员端配置
#指标选择页面 介绍指标 管理员端配置
# 把这两个页面的数据保存到数据库并展示
# 点击开始运行进行加载 实现多进程
#美化界面
#预览图片界面
# 分页
#进度条



class Login(QMainWindow,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
class Regist(QMainWindow,Ui_Regist):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
class MainWindow(QMainWindow,Ui_Home):
    def __init__(self,username):
        Ui_Home.username = username
        super().__init__()
        self.setupUi(self)
        #刚进页面都调用show_maintask,show_subtask
        super().show_maintask(1)
        super().show_subtask()
#新建任务页
class NewMainTask(QMainWindow,Ui_NewMaintask):
    def __init__(self,row):
        super().__init__()
        self.setupUi(self)
        #这个用法很重要！！！高级的页面给低级的传参
        self.row = row

class SelfDefining(QMainWindow,Ui_SelfDefining):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
class AutoConfig(QMainWindow,Ui_AutoConfig):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

class Setting(QMainWindow,Ui_Setting):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Index(QMainWindow,Ui_Index):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

class Controller:
    def __init__(self):
        pass
    # 以下函数只用于捕获信号后根据不同的信号做不同的跳转页面操作
    # 什么时候发出信号的逻辑在具体的页面内
    def show_Login(self):
        self.window_Login = Login()
        self.window_Login.show()
        self.window_Login.switch_window_to_login.connect(self.show_MainWindow)
        self.window_Login.switch_window_to_regist.connect(self.show_Regist)

    def show_Regist(self):
        self.window_Regist = Regist()
        self.window_Regist.show()
        self.window_Regist.switch_window_to_login.connect(self.show_Login)



    def show_MainWindow(self,username):
        self.window_Main = MainWindow(username)
        # 按钮对应的事件
        # 这里分析进入newmaintask的时候有两种情况 第一种是点击新建主任务 第二种是点击编辑 点击编辑/加号/删除/加号的时候均需要获取对应的行才能进行数据操作

        self.window_Main.switch_to_new_main_task_window.connect(self.show_window_NewMainTask) #点新建主任务
        self.window_Main.switch_to_SelfDefining_window.connect(self.show_window_SelfDefining)#点加号
        self.window_Main.switch_to_new_main_task_window_edit.connect(self.show_window_NewMainTask)#点编辑
        self.window_Login.close()
        self.window_Main.show()


    # python如何让row为空的时候也能执行 设置默认值为None 这里是动态的，点编辑进来的话有row这个参数新建的话没有
    def show_window_NewMainTask(self,row=None):
        self.window_NewMainTask = NewMainTask(row)
        # 如果是从编辑进入回显数据
        if not row is None:
            dt = Database.selectMaintaskByRow(row,Ui_Home.username)
            # print(dt['input'],dt['output'],dt['refer_folder'])
            self.window_NewMainTask.lineEdit.setText(dt['task_name'])
            if not dt['input'] == '选择文件':
                self.window_NewMainTask.pushButton.setFlat(True)
                self.window_NewMainTask.pushButton.setStyleSheet("background:transparent;")
            self.window_NewMainTask.pushButton.setText(dt['input'])
            if not dt['output'] == '选择文件':
                self.window_NewMainTask.pushButton_2.setFlat(True)
                self.window_NewMainTask.pushButton_2.setStyleSheet("background:transparent;")
            self.window_NewMainTask.pushButton_2.setText(dt['output'])
            if not dt['refer_folder'] == '选择文件':
                self.window_NewMainTask.pushButton_3.setFlat(True)
                self.window_NewMainTask.pushButton_3.setStyleSheet("background:transparent;")
            self.window_NewMainTask.pushButton_3.setText(dt['refer_folder'])

            self.window_NewMainTask.textEdit.setText(dt['desc'])
            index = self.window_NewMainTask.comboBox.findText(dt['mode'])
            self.window_NewMainTask.comboBox.setCurrentIndex(index)
        # 连续传递row
        self.window_NewMainTask.switch_window_to_home.connect(partial(self.back_to_MainWindow_fromNewMainTask,row))
        self.window_NewMainTask.show()

    def back_to_MainWindow_fromNewMainTask(self,row):
        self.window_NewMainTask.close()
        #判断是否从新建主任务点完成，是的话就直接添加 如果是点编辑就调用更新函数（区别在于更新函数没有insertrow） viewmodel操作
        if row is None:
            Ui_Home.add_task(self.window_Main)
        else:
            Ui_Home.update_task(self.window_Main,row)
        self.window_Main.show()





    def show_window_SelfDefining(self,row):
        self.window_SelfDefining = SelfDefining()
        input = Database.selectMaintaskByRow(Ui_Home.row_count,Ui_Home.username)["input"]
        output = Database.selectMaintaskByRow(Ui_Home.row_count,Ui_Home.username)["output"]
        Ui_SelfDefining.input_folder = input
        Ui_SelfDefining.input_folder = output





        self.window_SelfDefining.show()
        self.window_SelfDefining.switch_window.connect(partial(self.back_to_MainWindow_fromSelfDefining,row))

        self.window_SelfDefining.switch_window_2.connect(partial(self.show_window_Setting,row))
        self.window_SelfDefining.switch_window_3.connect(partial(self.show_window_Index,row))
        self.window_SelfDefining.switch_window_4.connect(self.back_to_NewMaintask_fromSelfDef)


    def show_window_Setting(self,row,a):

        self.window_Setting = Setting()
        #接受之前算法设置传来的参数名
        self.window_Setting.algo = a
        print("传来了"+a)
        if not(get_data_from_config(a)):
            QMessageBox.warning(self.window_SelfDefining,'警告', '联系管理员添加算法')
            return
        self.window_Setting.init_index_by_config()
        self.window_SelfDefining.hide()


        # 点击完成呴 这里使用了两种方法进行传递参数 switch_window和partial
        self.window_Setting.switch_window.connect(partial(self.back_to_SelfDef_fromSetting,row))

        self.window_Setting.show()

    def show_window_Index(self,row):
        self.window_Index = Index()

        self.window_Index.switch_window.connect(self.back_to_SelfDefining_fromIndex)

        self.window_Index.switch_window_2.connect(partial(self.back_to_MainWindow_fromIndex,row))

        self.window_Index.hide()

        self.window_Index.show()

    def back_to_MainWindow_fromIndex(self,row):
        self.window_Index.close()

        Ui_Home.add_task_2(self.window_Main,row)

        self.window_Main.show()


    def back_to_MainWindow_fromSelfDefining(self,row):
        self.window_SelfDefining.close()
        Ui_Home.add_task_2(self.window_Main,row)

        self.window_Main.show()


    def back_to_SelfDefining_fromIndex(self):
        self.window_Index.close()

        self.window_SelfDefining.show()
    # 点击完成后
    def back_to_SelfDef_fromSetting(self,row,para):
        self.window_Setting.close()
        #para[0] 是参数的取值字典
        for key,value in para[0].items():
            if value != "":
                para[0][key] = handleuserinput.handle(value)
            else:
                QMessageBox.warning(self.window_SelfDefining, '警告', '输入参数不能为空')
                break
        Ui_SelfDefining.add_task(self.window_SelfDefining, row, para[0], para[1])

        self.window_SelfDefining.show()

    def back_to_NewMaintask_fromSelfDef(self):
        self.window_SelfDefining.close()
        self.window_NewMainTask.show()


