import os
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from PyQt5 import QtGui

import service.Optimize_ImageEhancement
from util import Database
from pages import Page_Home
from service import Quanti
from util import Util
from service.ImageEhancement import ImageEnhancement


class TaskWindow(QWidget):
    status = 1

    def __init__(self, img_src1, status, img_src3, img_src4,i):
        super().__init__()
        self.row = i
        # status = 1 #测试
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
        # self.button_edit.clicked.connect(self.button_clicked)

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
        # 点击按钮时连接到相应的槽（动态生成的时候会指定这里不用 后面同理）
        # self.button_status.clicked.connect(self.status_change)

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
        # 点击按钮时连接到相应的槽
        # self.button_add.clicked.connect(self.button_clicked)



        # 创建一个水平布局，并将按钮添加到布局中
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button_edit)
        self.layout.addWidget(self.button_status)
        self.layout.addWidget(self.button_add)
        self.layout.addWidget(self.button_delete)

        # 设置该窗口的布局
        self.setLayout(self.layout)


    # def status_change(self):
    #     if self.status ==1:
    #         img_src2 = os.path.join(Util.unify_path().application_path, 'need/stop.png')
    #         self.pixmap = QPixmap(img_src2)
    #         self.button_status.setIcon(QtGui.QIcon(self.pixmap))
    #         self.status =2
    #     else:
    #         img_src2 = os.path.join(Util.unify_path().application_path, 'need/play.png')
    #         self.pixmap = QPixmap(img_src2)
    #         self.button_status.setIcon(QtGui.QIcon(self.pixmap))
    #         self.status = 1
    #     #获取某一行后调用某个算法
    #     # 1. 先从数据库获取输入输出文件夹的路径然后遍历
    #     print("状态变化",self.row)
    #     input_folder = Database.selectMaintaskByRow(self.row)["input"]
    #     output_folder = Database.selectMaintaskByRow(self.row)["output"]
    #     # 判断是否已针对主任务创建子任务
    #     subtask_data = Database.selectall_subdataById(self.row,False,False,False)
    #     if not subtask_data:
    #         QMessageBox.warning(self, '提示', '未选择算法')
    #         return
    #     # 找到当前执行任务的用户选的算法名 参数值 和参数名
    #     alg_name = Database.selectall_subdataById(self.row,True,False,None)[0]['Alg_Name']
    #     for subtask in subtask_data:
    #         dict = {paramname: subtask[paramname] for paramname in list(Util.get_data_from_config(alg_name))}
    #         # 使用示例
    #         executor = service.Optimize_ImageEhancement.AlgorithmExecutor(input_folder,output_folder)
    #         # **解包成key--alpha value--0.3关键字参数传入
    #         executor.add_algorithm(alg_name, **dict)
    #         print("=========正在执行增强算法代码==========")
    #         # 执行算法
    #         result = executor.apply_image_enhancement()
    #     print("=========正在执行生成指标csv算法代码==========")
    #     Quanti.quant(self.progress_signal,len(Util.get_data_from_config(alg_name)), self.row,inputf = input_folder, outputf = output_folder)
    #     QMessageBox.warning(self, '提示', '执行成功')









