#测试
# import sys
# from PyQt5 import QtWidgets, QtGui
#
# app = QtWidgets.QApplication(sys.argv)
#
# table = QtWidgets.QTableWidget(5, 4)
#
# # 设置表格标题
# table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3", "Column 4"])
#
# # 设置行高
# table.verticalHeader().setDefaultSectionSize(50)
#
# # 调整列宽
# table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
#
# # 设置元素内容
# for row in range(5):
#     for col in range(4):
#         item = QtWidgets.QTableWidgetItem("Item ({}, {})".format(row, col))
#         table.setItem(row, col, item)
#
# table.show()
#
# sys.exit(app.exec_())


#列表
# import sys
# from PyQt5 import QtWidgets, QtGui
#
# app = QtWidgets.QApplication(sys.argv)
#
# window = QtWidgets.QWidget()
# layout = QtWidgets.QVBoxLayout(window)
#
# list_view = QtWidgets.QListView()
# model = QtGui.QStandardItemModel(list_view)
# list_view.setModel(model)
# layout.addWidget(list_view)
#
# add_row_button = QtWidgets.QPushButton("Add Row")
# layout.addWidget(add_row_button)
#
# def add_row():
#     item = QtGui.QStandardItem("Row {}".format(model.rowCount() + 1))
#     model.appendRow(item)
#
# add_row_button.clicked.connect(add_row)
#
# window.show()
# sys.exit(app.exec_())




#


# import sys
# from PyQt5 import QtWidgets, QtGui
#
# app = QtWidgets.QApplication(sys.argv)
#
# window = QtWidgets.QWidget()
# layout = QtWidgets.QVBoxLayout(window)
#
# table = QtWidgets.QTableWidget(0, 4)
# layout.addWidget(table)
#
# # 设置表格标题
# table.setHorizontalHeaderLabels(["序号","任务名","执行进度","输入文件夹","输出文件夹","操作","创建时间"])
#
# # 设置行高
# table.verticalHeader().setDefaultSectionSize(50)
#
# # 调整列宽
# table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
#
# add_row_button = QtWidgets.QPushButton("Add Row")
# layout.addWidget(add_row_button)
#
# def add_row():
#     row_count = table.rowCount()
#     table.insertRow(row_count)
#     for col in range(4):
#         item = QtWidgets.QTableWidgetItem("")
#         table.setItem(row_count, col, item)
#
# add_row_button.clicked.connect(add_row)
#
# window.show()
# sys.exit(app.exec_())
#

# import os
# import sys
#
# from PyQt5.QtGui import QStandardItem, QPixmap, QIcon
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, \
#     QWidget, QHBoxLayout, QHeaderView, QDesktopWidget
# from PyQt5.QtCore import Qt, QSize
#
# from TestOther import TaskWindow
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # 初始化任务列表
#
#         # 设置布局
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout(self.central_widget)
#         self.setGeometry(1000, 1000, 1200, 700)
#
#         # 创建表格
#         self.table = QTableWidget()
#         self.table.setColumnCount(7)
#         self.table.setHorizontalHeaderLabels(['序号', '任务名', '执行进度', '输入文件夹', '输出文件夹', '操作', '创建时间'])
#         self.layout.addWidget(self.table)
#
#         # 创建添加任务按钮
#         self.add_task_button = QPushButton("添加任务")
#         self.add_task_button.clicked.connect(self.add_task)
#         self.layout.addWidget(self.add_task_button)
#
#
#
#     def add_task(self):
#         # 创建任务对象
#         task = TaskWindow('./need/edit.png', 1, './need/add-circle.png', './need/ashbin.png')
#         self.table.setColumnWidth(3, 330)
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使表宽度自适应
#         self.table.verticalHeader().setDefaultSectionSize(50) #使表高固定
#
#
#         # 创建任务字典
#         task_dict = {"name": "任务1", "description": "描述1", "created_at": "2022-01-01", "status": task}
#
#         # 更新表格
#         row_count = self.table.rowCount()
#         self.table.insertRow(row_count)
#         self.table.setItem(row_count, 0, QTableWidgetItem(task_dict["name"]))
#         self.table.setItem(row_count, 1, QTableWidgetItem(task_dict["description"]))
#         self.table.setItem(row_count, 2, QTableWidgetItem(task_dict["created_at"]))
#         self.table.setCellWidget(row_count, 5, task_dict["status"])
#
#     def center(self):
#         screen = QDesktopWidget().screenGeometry()
#         size = self.geometry()
#         self.move((screen.width() - size.width()) / 2,
#                   (screen.height() - size.height()) / 2)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     window.center()
#     sys.exit(app.exec_())


#sender的作用
# from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         button1 = QPushButton("Button 1", self)
#         button1.clicked.connect(self.handle_button_click)
#
#         button2 = QPushButton("Button 2", self)
#         button2.move(30, 30)
#         button2.clicked.connect(self.handle_button_click)
#
#     def handle_button_click(self):
#         sender = self.sender()
#         print("Button '{}' was clicked".format(sender.text()))
#
#
# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec_()



# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.table = QTableWidget(self)
#         self.table.setRowCount(3)
#         self.table.setColumnCount(3)
#         self.table.setHorizontalHeaderLabels(["Column 1", "Column 2"])
#         self.table.setItem(0, 0, QTableWidgetItem("Row 1, Column 1"))
#         self.table.setItem(0, 1, QTableWidgetItem("Row 1, Column 2"))
#         self.table.setItem(1, 0, QTableWidgetItem("Row 2, Column 1"))
#         self.table.setItem(1, 1, QTableWidgetItem("Row 2, Column 2"))
#         self.table.setItem(2, 0, QTableWidgetItem("Row 3, Column 1"))
#         self.table.setItem(2, 1, QTableWidgetItem("Row 3, Column 2"))
#
#         for i in range(self.table.rowCount()):
#             button = QPushButton("Delete")
#             button.clicked.connect(self.delete_row)
#             button.row = i
#             self.table.setCellWidget(i, 2, button)
#
#         self.setCentralWidget(self.table)
#
#     def delete_row(self):
#         button = self.sender()
#         row = button.row
#         self.table.removeRow(row)
#
# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# sys.exit(app.exec_())




# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar
# from PyQt5.QtCore import QThread, pyqtSignal
# import time
#
# class MyThread(QThread):
#     # 定义信号，更新进度条的进度
#     progress_signal = pyqtSignal(int)
#
#     def __init__(self):
#         super().__init__()
#
#     def run(self):
#         for i in range(101):
#             #收到完成的信号后到时候这里自己改
#             self.progress_signal.emit(i)
#             time.sleep(0.1)
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(100, 100, 300, 300)
#
#         # 创建按钮
#         self.button = QPushButton('开始任务', self)
#         self.button.move(100, 100)
#         self.button.clicked.connect(self.start_task)
#
#         # 创建进度条
#         self.progress = QProgressBar(self)
#         self.progress.setGeometry(100, 150, 150, 20)
#
#     def start_task(self):
#         # 创建线程，并开始执行任务
#         self.thread = MyThread()
#         self.thread.progress_signal.connect(self.update_progress)
#         self.thread.start()
#
#     def update_progress(self, value):
#         # 更新进度条的进度
#         self.progress.setValue(value)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())


#
#
#
#
#
#
#
#
#





# import sys
# import pickle
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction
# from PyQt5.QtCore import QFile, QTextStream
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(100, 100, 300, 300)
#         self.text_edit = QTextEdit(self)
#         self.setCentralWidget(self.text_edit)
#         self.create_actions()
#         self.create_buttons()
#
#     def create_actions(self):
#         self.save_action = QAction("Save", self)
#         self.save_action.triggered.connect(self.save)
#         self.menuBar().addAction(self.save_action)
#
#         self.load_action = QAction("Load", self)
#         self.load_action.triggered.connect(self.load)
#         self.menuBar().addAction(self.load_action)
#
#     def create_buttons(self):
#         save_button = QPushButton("Save", self)
#         save_button.clicked.connect(self.save)
#         save_button.move(100, 250)
#
#         load_button = QPushButton("Load", self)
#         load_button.clicked.connect(self.load)
#         load_button.move(200, 250)
#
#     def save(self):
#         data = {"text": self.text_edit.toPlainText()}
#         with open("data.pickle", "wb") as f:
#             pickle.dump(data, f)
#         print(os.path.abspath('data.pickle'))
#
#     def load(self):
#         try:
#             with open("data.pickle", "rb") as f:
#                 data = pickle.load(f)
#                 self.text_edit.setPlainText(data["text"])
#         except FileNotFoundError:
#             pass
#
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# sys.exit(app.exec_())


#tableview
# import sys
# from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget
#
#
# class PageModel(QAbstractTableModel):
#     def __init__(self, data, parent=None):
#         super().__init__(parent)
#         self._data = data
#         self._page_size = 5
#         self._current_page = 0
#
#     def rowCount(self, parent=None):
#         return min(self._page_size, len(self._data) - self._current_page * self._page_size)
#
#     def columnCount(self, parent=None):
#         return 1
#
#     def data(self, index, role=Qt.DisplayRole):
#         if role == Qt.DisplayRole:
#             return self._data[index.row() + self._current_page * self._page_size]
#         return QVariant()
#
#     def set_page_size(self, page_size):
#         self._page_size = page_size
#
#     def set_current_page(self, page):
#         self._current_page = page
#         self.layoutChanged.emit()
#
#     @property
#     def current_page(self):
#         return self._current_page
#
#
# class PageWindow(QMainWindow):
#     def __init__(self, data):
#         super().__init__()
#         self._model = PageModel(data)
#         self._table_view = QTableView()
#         self._table_view.setModel(self._model)
#         self._previous_button = QPushButton("Previous")
#         self._previous_button.clicked.connect(self._on_previous)
#         self._next_button = QPushButton("Next")
#         self._next_button.clicked.connect(self._on_next)
#         layout = QVBoxLayout()
#         layout.addWidget(self._table_view)
#         layout.addWidget(self._previous_button)
#         layout.addWidget(self._next_button)
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#     def _on_previous(self):
#         current_page = self._model.current_page
#         if current_page > 0:
#             self._model.set_current_page(current_page - 1)
#
#     def _on_next(self):
#         current_page = self._model.current_page
#         if current_page < (len(self._model._data) - 1) // self._model._page_size:
#             self._model.set_current_page(current_page + 1)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = PageWindow(list(range(100)))
#     window.show()
#     sys.exit(app.exec_())
# QTableWidget
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QPushButton, QTableWidgetItem, QWidget
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, data, items_per_page=10, parent=None):
#         super().__init__(parent)
#         self.data = data
#         self.items_per_page = items_per_page
#         self.current_page = 0
#         self.table = QTableWidget(0, len(self.data[0]))
#         self.table.setHorizontalHeaderLabels(self.data[0].keys())
#         self.update_table()
#         prev_button = QPushButton("Prev")
#         prev_button.clicked.connect(self.prev_page)
#         next_button = QPushButton("Next")
#         next_button.clicked.connect(self.next_page)
#         layout = QVBoxLayout()
#         layout.addWidget(self.table)
#         layout.addWidget(prev_button)
#         layout.addWidget(next_button)
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#     def update_table(self):
#         self.table.clear()
#         self.table.setRowCount(self.items_per_page)
#         self.table.setHorizontalHeaderLabels(self.data[0].keys())
#         for i, item in enumerate(self.data[self.current_page * self.items_per_page : (self.current_page + 1) * self.items_per_page]):
#             for j, (key, value) in enumerate(item.items()):
#                 self.table.setItem(i, j, QTableWidgetItem(str(value)))
#
#     def prev_page(self):
#         if self.current_page > 0:
#             self.current_page -= 1
#             self.update_table()
#
#     def next_page(self):
#         if self.current_page < len(self.data) // self.items_per_page:
#             self.current_page += 1
#             self.update_table()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow([{"col1": 1, "col2": 2, "col3": 3} for i in range(100)])
#     window.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QPushButton, QHeaderView, QWidget
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
#
# class PageModel(QStandardItemModel):
#     def __init__(self, data, items_per_page=10, parent=None):
#         super().__init__(parent)
#         self.data = data
#         self.items_per_page = items_per_page
#         self.current_page = 0
#         self.update_model()
#
#     def update_model(self):
#         self.clear()
#         for key in self.data[0].keys():
#             self.setHorizontalHeaderItem(len(self.data[0].keys()), QStandardItem(key))
#         for i, item in enumerate(self.data[self.current_page * self.items_per_page : (self.current_page + 1) * self.items_per_page]):
#             for j, (key, value) in enumerate(item.items()):
#                 self.setItem(i, j, QStandardItem(str(value)))
#
# class MainWindow(QMainWindow):
#     def __init__(self, data, items_per_page=10, parent=None):
#         super().__init__(parent)
#         self.data = data
#         self.items_per_page = items_per_page
#         self.table = QTableView()
#         self.table.setModel(PageModel(data, items_per_page))
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
#         prev_button = QPushButton("Prev")
#         prev_button.clicked.connect(self.prev_page)
#         next_button = QPushButton("Next")
#         next_button.clicked.connect(self.next_page)
#         layout = QVBoxLayout()
#         layout.addWidget(self.table)
#         layout.addWidget(prev_button)
#         layout.addWidget(next_button)
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#     def prev_page(self):
#         model = self.table.model()
#         if model.current_page > 0:
#             model.current_page -= 1
#             model.update_model()
#
#     def next_page(self):
#         model = self.table.model()
#         if model.current_page < len(model.data) // model.items_per_page:
#             model.current_page += 1
#             model.update_model()
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow([{"col1": 1, "col2": 2, "col3": 3} for i in range(100)])
#     window.show()
#     sys.exit(app.exec_())



# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
#
# class PageModel:
#     def __init__(self, page_size=10):
#         self.data = [i for i in range(100)]
#         self.page_size = page_size
#         self.current_page = 0
#
#     def get_page_data(self):
#         start = self.current_page * self.page_size
#         end = start + self.page_size
#         return self.data[start:end]
#
# class TableWidget(QTableWidget):
#     def __init__(self, parent=None, model=None):
#         super().__init__(parent)
#         self.model = model
#         self.setRowCount(self.model.page_size)
#         self.setColumnCount(1)
#         self.setHorizontalHeaderLabels(['Data'])
#
#     def update_table(self):
#         data = self.model.get_page_data()
#         for row, value in enumerate(data):
#             item = QTableWidgetItem(str(value))
#             self.setItem(row, 0, item)
#
# class MainWindow(QMainWindow):
#     def __init__(self, parent=None, model=None):
#         super().__init__(parent)
#         self.model = model
#         self.table_widget = TableWidget(model=model)
#         self.previous_button = QPushButton('Previous')
#         self.next_button = QPushButton('Next')
#         self.previous_button.setEnabled(False)
#         self.next_button.setEnabled(True)
#         self.previous_button.clicked.connect(self.previous_clicked)
#         self.next_button.clicked.connect(self.next_clicked)
#         layout = QVBoxLayout()
#         layout.addWidget(self.table_widget)
#         layout.addWidget(self.previous_button)
#         layout.addWidget(self.next_button)
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#         self.table_widget.update_table()
#
#     def previous_clicked(self):
#         self.model.current_page -= 1
#         self.previous_button.setEnabled(self.model.current_page > 0)
#         self.next_button.setEnabled(True)
#         self.table_widget.update_table()
#
#     def next_clicked(self):
#         self.model.current_page += 1
#         self.previous_button.setEnabled(True)
#         self.next_button.setEnabled(self.model.current_page < self.model.total_pages() - 1)
#         self.table_widget.update_table()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow([{"col1": 1, "col2": 2, "col3": 3} for i in range(100)])
#     window.show()
#     sys.exit(app.exec_())


# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Set up the UI
#         self.table = QTableWidget()
#         self.table.setColumnCount(2)
#         self.table.setHorizontalHeaderLabels(["Column 1", "Column 2"])
#
#         self.previous_button = QPushButton("Previous")
#         self.next_button = QPushButton("Next")
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.table)
#         layout.addWidget(self.previous_button)
#         layout.addWidget(self.next_button)
#
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#         self.current_page = 0
#         self.page_size = 10
#         self.row_count = 100
#
#         self.fill_table()
#
#         # Connect signals
#         self.previous_button.clicked.connect(self.previous_page)
#         self.next_button.clicked.connect(self.next_page)
#
#     def fill_table(self):
#         self.table.setRowCount(0)
#         self.table.setRowCount(self.page_size)
# #十页
#         for i in range(self.page_size):
# #这个很关键决定如何填充出所有数据 两个变量current_page和i
#             row = self.current_page * self.page_size + i
#
#             if row >= self.row_count:
#                 break
#
#             self.table.setItem(i, 0, QTableWidgetItem(str(row)))
#             self.table.setItem(i, 1, QTableWidgetItem(str(row)))
#
#     def previous_page(self):
#         if self.current_page > 0:
#             self.current_page -= 1
#             self.fill_table()
#
#     def next_page(self):
#         if self.current_page * self.page_size < self.row_count:
#             self.current_page += 1
#             self.fill_table()
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


# _*_ coding:utf-8 _*_
# author: zizle
# date 22/04/2019
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import pyqtSignal
#
#
# class TableWidget(QWidget):
#     control_signal = pyqtSignal(list)
#
#     def __init__(self, *args, **kwargs):
#         super(TableWidget, self).__init__(*args, **kwargs)
#         self.__init_ui()
#
#     def __init_ui(self):
#         style_sheet = """
#             QTableWidget {
#                 border: none;
#                 background-color:rgb(240,240,240)
#             }
#             QPushButton{
#                 max-width: 18ex;
#                 max-height: 6ex;
#                 font-size: 11px;
#             }
#             QLineEdit{
#                 max-width: 30px
#             }
#         """
#         self.table = QTableWidget(3, 5)  # 3 行 5 列的表格
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
#         self.__layout = QVBoxLayout()
#         self.__layout.addWidget(self.table)
#         self.setLayout(self.__layout)
#         self.setStyleSheet(style_sheet)
#
#     def setPageController(self, page):
#         """自定义页码控制器"""
#         control_layout = QHBoxLayout()
#         homePage = QPushButton("首页")
#         prePage = QPushButton("<上一页")
#         self.curPage = QLabel("1")
#         nextPage = QPushButton("下一页>")
#         finalPage = QPushButton("尾页")
#         self.totalPage = QLabel("共" + str(page) + "页")
#         skipLable_0 = QLabel("跳到")
#         self.skipPage = QLineEdit()
#         skipLabel_1 = QLabel("页")
#         confirmSkip = QPushButton("确定")
#         homePage.clicked.connect(self.__home_page)
#         prePage.clicked.connect(self.__pre_page)
#         nextPage.clicked.connect(self.__next_page)
#         finalPage.clicked.connect(self.__final_page)
#         confirmSkip.clicked.connect(self.__confirm_skip)
#         control_layout.addStretch(1)
#         control_layout.addWidget(homePage)
#         control_layout.addWidget(prePage)
#         control_layout.addWidget(self.curPage)
#         control_layout.addWidget(nextPage)
#         control_layout.addWidget(finalPage)
#         control_layout.addWidget(self.totalPage)
#         control_layout.addWidget(skipLable_0)
#         control_layout.addWidget(self.skipPage)
#         control_layout.addWidget(skipLabel_1)
#         control_layout.addWidget(confirmSkip)
#         control_layout.addStretch(1)
#         self.__layout.addLayout(control_layout)
#
#     def __home_page(self):
#         """点击首页信号"""
#         self.control_signal.emit(["home", self.curPage.text()])
#
#     def __pre_page(self):
#         """点击上一页信号"""
#         self.control_signal.emit(["pre", self.curPage.text()])
#
#     def __next_page(self):
#         """点击下一页信号"""
#         self.control_signal.emit(["next", self.curPage.text()])
#
#     def __final_page(self):
#         """尾页点击信号"""
#         self.control_signal.emit(["final", self.curPage.text()])
#
#     def __confirm_skip(self):
#         """跳转页码确定"""
#         self.control_signal.emit(["confirm", self.skipPage.text()])
#
#     def showTotalPage(self):
#         """返回当前总页数"""
#         return int(self.totalPage.text()[1:-1])
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.__init_ui()
#
#     def __init_ui(self):
#         self.resize(500, 250)
#         self.setWindowTitle("QTableWidget加页码控制器")
#         self.table_widget = TableWidget()  # 实例化表格
#         self.table_widget.setPageController(10)  # 表格设置页码控制
#         self.table_widget.control_signal.connect(self.page_controller)
#         self.setCentralWidget(self.table_widget)
#
#     def page_controller(self, signal):
#         total_page = self.table_widget.showTotalPage()
#         if "home" == signal[0]:
#             self.table_widget.curPage.setText("1")
#         elif "pre" == signal[0]:
#             if 1 == int(signal[1]):
#                 QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
#                 return
#             self.table_widget.curPage.setText(str(int(signal[1]) - 1))
#         elif "next" == signal[0]:
#             if total_page == int(signal[1]):
#                 QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
#                 return
#             self.table_widget.curPage.setText(str(int(signal[1]) + 1))
#         elif "final" == signal[0]:
#             self.table_widget.curPage.setText(str(total_page))
#         elif "confirm" == signal[0]:
#             if total_page < int(signal[1]) or int(signal[1]) < 0:
#                 QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
#                 return
#             self.table_widget.curPage.setText(signal[1])
#
#         self.changeTableContent()  # 改变表格内容
#
#     def changeTableContent(self):
#         """根据当前页改变表格的内容"""
#         cur_page = self.table_widget.curPage.text()
#         pass
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
#
from Database import HandleDatabase
if __name__ == '__main__':
    hd = HandleDatabase()
    hd.create_SubTaskDatabase(self,3)


