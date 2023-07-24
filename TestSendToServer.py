#输入参数发送请求给后端并持久化数据到数据库（主体逻辑）
import sys
from functools import partial

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import requests
class MainWindow(QWidget):

    #这个页面的功能函数
    def insert_data(self, num_columns):
        #存放用户输入
        user_param_input_value = []
        # 连接数据库
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("test.db")
        if not db.open():
            print("无法连接数据库")
            return
        query = QSqlQuery()



        #现在表字段的动态已经实现（create_database）接下来实现值的动态
        # query.prepare("INSERT INTO task (p1,p2,p3) VALUES (:p1,:p2,:p3)") 原来为全静态改为动态后如下：
        columns = ["p{}".format(i) for i in range(1, num_columns + 1)]
        #动态添加
        print("动态参数:")
        print(columns) #['p1', 'p2', 'p3', 'p4']
        placeholders = ", ".join("?" * len(columns))
        print("动态占位符"+placeholders)#?, ?, ?, ?

        #如何获取刚才初始化界面中的动态文本框的文本内容？
        #先拿到所有的QLineEdit然后进行过滤
        line_edits = QObject.findChildren(self, QLineEdit)
        for line_edit in line_edits:
            if "text_edit" in line_edit.objectName():
                user_param_input_value.append(line_edit.text())
        #利用.join将列表转化成字符串
        columns_str = ", ".join(columns)
        print("执行的语句:"+"INSERT INTO task (taskname,describe,{}) VALUES (:taskname,?,{})".format(columns_str,placeholders))
        #INSERT INTO task (taskname,describe,p1, p2, p3, p4) VALUES (:taskname,?,?, ?, ?, ?)
        query.prepare("INSERT INTO task (taskname,describe,{}) VALUES (:taskname,'describe',{})".format(columns_str,placeholders))
        # #静态
        # query.exec_("INSERT INTO task (taskname) VALUES (:taskname)")


        # 绑定数据为变量 常用的zip遍历数据(也分静态动态且顺序需一致)
        #先绑静态
        query.addBindValue('describe')#拿到前端来的描述
        query.bindValue(":taskname", self.text_edit_tkname.text())
        #再绑动态
        for i,j in list(zip(range(num_columns),user_param_input_value)):
            query.addBindValue(j)
        print(query.boundValues())


        try:
            if not query.exec_():
                print("插入失败")
                print(query.lastError().text())
            else:
                print("插入成功")
                #这里也需要动态生成字典思路是用zip函数让两个列表一一对应生成字典
                data = zip(columns,user_param_input_value)

                print("发送给后端的数据：")

                # send POST request
                response = requests.get('http://httpbin.org/get', params=data)

                # check status code
                print(response.status_code)

                # print response content
                print(response.content)



        except Exception as e:
            print(e)

    def add_column(self,columns, query):  # column是自己定义的规范即 字段名 数据结构 count_p是字段的数量
        for a in columns:
            print("ALTER TABLE task ADD COLUMN {} INTEGER;".format(a))
            query.exec_("ALTER TABLE task ADD COLUMN {};".format(a))

    # num_columns是参数的个数
    def create_database(self,num_columns):
        # 连接数据库 使用sqlite
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('test.db')
        if not db.open():
            print('无法连接数据库')
            return False
        # 创建任务表
        query = QSqlQuery()

        # 静态列初始化
        query.exec_(
            "CREATE TABLE task (id INTEGER PRIMARY KEY AUTOINCREMENT, taskname varchar not null, describe varchar);")
        # 实现动态列初始化（后续需要添加其他信息如执行时间，这里先测试整体逻辑）
        columns = ["p{}".format(i) for i in range(1, num_columns + 1)]
        self.add_column(columns, query)
        print("初始化数据库完成")
        return True

    def __init__(self,num_columns):
        super().__init__()
        self.setWindowTitle("Insert Data to Database")
        #创建数据库
        self.create_database(num_columns)


        #静态数量输入框
        self.text_edit_tkname = QLineEdit() # taskname

        #原本如下
        # self.text_edit1 = QLineEdit() #p1
        # self.text_edit2 = QLineEdit() #p2
        # self.text_edit3 = QLineEdit()  #p3
        #改为动态数量的输入框后如下
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit_tkname)
        for i in range(num_columns):
            line_edit = QLineEdit()
            line_edit.setObjectName("text_edit" + str(i))
            layout.addWidget(line_edit)
        self.button = QPushButton("Insert")
        # functools.partial是Python内置库functools中的一个函数，它可以将一个函数封装成另一个函数，并在调用时自动传入一些参数。
        self.button.clicked.connect(partial(self.insert_data,num_columns))
        layout.addWidget(self.button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 在前端选择对应的算法发送给后端后后端需要返回算法参数的个数，参数名等等，并显示在前端，这里假设已经拿到数据了（待完成）
    # 算法参数个数
    num_columns = 9
    window = MainWindow(num_columns)
    window.show()
    sys.exit(app.exec_())
