# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import Util
from ImageEhancement import ImageEnhancement


class Ui_Setting(object):
    switch_window = QtCore.pyqtSignal(tuple)
    algo = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1268, 911)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 10, 1016, 489))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.horLayout_general = QtWidgets.QHBoxLayout()
        self.horLayout_general.setContentsMargins(-1, -1, -1, 20)
        self.horLayout_general.setObjectName("horLayout_general")

        self.radioButton_general = QtWidgets.QRadioButton(self.frame)
        self.radioButton_general.setObjectName("radioButton_general")
        self.horLayout_general.addWidget(self.radioButton_general)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horLayout_general.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horLayout_general)
        self.horSetvalue = QtWidgets.QHBoxLayout()
        self.horSetvalue.setContentsMargins(0, -1, 126, -1)
        self.horSetvalue.setObjectName("horSetvalue")
        self.label_setSingleval = QtWidgets.QLabel(self.frame)
        self.label_setSingleval.setObjectName("label_setSingleval")
        self.horSetvalue.addWidget(self.label_setSingleval)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horSetvalue.addItem(spacerItem2)
        self.label_setMultival = QtWidgets.QLabel(self.frame)
        self.label_setMultival.setObjectName("label_setMultival")
        self.horSetvalue.addWidget(self.label_setMultival)
        spacerItem3 = QtWidgets.QSpacerItem(126, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horSetvalue.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horSetvalue)
        self.horlLayout_generalfather = QtWidgets.QHBoxLayout()
        self.horlLayout_generalfather.setObjectName("horlLayout_generalfather")
        self.hori_generalmodel = QtWidgets.QHBoxLayout()
        self.hori_generalmodel.setObjectName("hori_generalmodel")
        self.radioButton_8 = QtWidgets.QRadioButton(self.frame)
        self.radioButton_8.setObjectName("radioButton_8")
        self.hori_generalmodel.addWidget(self.radioButton_8)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.hori_generalmodel.addWidget(self.lineEdit_13)
        self.label_18 = QtWidgets.QLabel(self.frame)
        self.label_18.setObjectName("label_18")
        self.hori_generalmodel.addWidget(self.label_18)
        self.radioButton_9 = QtWidgets.QRadioButton(self.frame)
        self.radioButton_9.setText("")
        self.radioButton_9.setObjectName("radioButton_9")
        self.hori_generalmodel.addWidget(self.radioButton_9)
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setObjectName("label_12")
        self.hori_generalmodel.addWidget(self.label_12)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.hori_generalmodel.addWidget(self.lineEdit_14)
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setObjectName("label_13")
        self.hori_generalmodel.addWidget(self.label_13)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.hori_generalmodel.addWidget(self.lineEdit_15)
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setObjectName("label_14")
        self.hori_generalmodel.addWidget(self.label_14)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.hori_generalmodel.addWidget(self.lineEdit_16)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hori_generalmodel.addItem(spacerItem4)
        self.hori_generalmodel.setStretch(2, 1)
        self.horlLayout_generalfather.addLayout(self.hori_generalmodel)
        self.verticalLayout.addLayout(self.horlLayout_generalfather)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horLayout_profession = QtWidgets.QHBoxLayout()
        self.horLayout_profession.setObjectName("horLayout_profession")
        self.radioButton_profession = QtWidgets.QRadioButton(self.frame)
        self.radioButton_profession.setObjectName("radioButton_profession")
        self.horLayout_profession.addWidget(self.radioButton_profession)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horLayout_profession.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horLayout_profession)
        self.vertiLayout_professionfather = QtWidgets.QVBoxLayout()
        self.vertiLayout_professionfather.setObjectName("vertiLayout_professionfather")
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++
        # self.horLayout_profession_1 = QtWidgets.QHBoxLayout()
        # self.horLayout_profession_1.setObjectName("horLayout_profession_1")
        # #+++++++++++++++++++++++++++++++++++++++++++++++++++++
        # self.label = QtWidgets.QLabel(self.frame)
        # self.label.setObjectName("label")
        # self.horLayout_profession_1.addWidget(self.label)
        # #+++++++++++++++++++++++++++++++++++++++++++++++++++++
        # self.lineEdit = QtWidgets.QLineEdit(self.frame)
        # self.lineEdit.setObjectName("lineEdit")
        # #+++++++++++++++++++++++++++++++++++++++++++++++++++++
        # self.horLayout_profession_1.addWidget(self.lineEdit)
        # spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horLayout_profession_1.addItem(spacerItem7)
        # self.vertiLayout_professionfather.addLayout(self.horLayout_profession_1)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++



        self.verticalLayout.addLayout(self.vertiLayout_professionfather)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout_note = QtWidgets.QHBoxLayout()
        self.horizontalLayout_note.setObjectName("horizontalLayout_note")
        self.label_19 = QtWidgets.QLabel(self.frame)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_note.addWidget(self.label_19)
        self.verticalLayout.addLayout(self.horizontalLayout_note)
        self.horizontalLayout_finish = QtWidgets.QHBoxLayout()
        self.horizontalLayout_finish.setObjectName("horizontalLayout_finish")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_finish.addItem(spacerItem9)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.SettingToHome)

        self.horizontalLayout_finish.addWidget(self.pushButton)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_finish.addItem(spacerItem10)
        self.horizontalLayout_finish.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_finish)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1268, 42))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton_general.setText(_translate("MainWindow", "一般模式"))
        self.label_setSingleval.setText(_translate("MainWindow", "单值设置"))
        self.label_setMultival.setText(_translate("MainWindow", "多值设置"))
        self.radioButton_8.setText(_translate("MainWindow", " δ 德尔塔   "))
        self.label_18.setText(_translate("MainWindow", "参数提示范围：1～5"))
        self.label_12.setText(_translate("MainWindow", "最小值"))
        self.label_13.setText(_translate("MainWindow", "最大值"))
        self.label_14.setText(_translate("MainWindow", "步长间隔"))
        self.radioButton_profession.setText(_translate("MainWindow", "专业模式"))
        self.label_19.setText(_translate("MainWindow", "备注：\n"
                                                       "井号后面为步长，可以用逗号分隔多组不同参数实验组\n"
                                                       "如图中表示阿尔法取值为1，2，3，5，5.2,5.4...6贝塔取2伽马取4，4.5 ...,9\n"
                                                       "德尔塔为4，则图中共产生3*5*1*10*1种不同的实验组"))
        self.pushButton.setText(_translate("MainWindow", "完成"))


    def SettingToHome(self):
        dic = {}
        #获取用户的输入值
        for i, (key_dict, value_dict) in zip(range(1, 1 + self.index_num), self.index_name.items()):
            lineedit = self.findChild(QtWidgets.QLineEdit, f"lineEdit_{i}")
            input = lineedit.text()
            dic[key_dict] = input
        self.switch_window.emit((dic,self.algo))

#从config中解析数据
    def init_index_by_config(self):
        data= Util.get_data_from_config(self.algo)
        info = Util.get_algorithm_params_info(data,self.algo)
        #某种算法的参数个数：
        self.index_num = info.length
        self.index_name = info.params #dict
        # 循环创建label和lineEdit
        # zip方法一次可以同时遍历一个列表和数组
        for i, (key_dict, value_dict) in zip(range(1,1+self.index_num), self.index_name.items()):
            layout = QtWidgets.QHBoxLayout()
            layout.setObjectName("horLayout_profession_"+str(i))
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++
            labelnew = QtWidgets.QLabel(key_dict)
            labelnew.setObjectName("label_"+str(i))
            #拿到这个新建的layout

            layout.addWidget(labelnew)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++
            lineEdit = QtWidgets.QLineEdit()
            lineEdit.setObjectName("lineEdit_"+str(i))
            lineEdit.setPlaceholderText("取值范围:"+value_dict)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++
            layout.addWidget(lineEdit)
            spacerItem7 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            layout.addItem(spacerItem7)
            self.vertiLayout_professionfather.addLayout(layout)










