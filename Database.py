import os

from PyQt5.QtSql import QSqlDriver
# 当主任务设置好后点击加号则创建Subtask+_1的子任务表
# sub_id从1开始自增
import Util
from Page_Setting import Ui_Setting
# 最好不要文件名和类名一样

sub_id = 1

import sqlite3
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
#连接池
def initialize_database(db_path):
    if not os.path.exists(db_path):
        os.makedirs(db_path, exist_ok=True)

    db_file = os.path.join(db_path, "test.db")

    if not os.path.exists(db_file):
        # 创建新的空数据库文件
        conn = sqlite3.connect(db_file)

        conn.execute('''DROP TABLE IF EXISTS "Maintask";''')
        conn.execute('''
        CREATE TABLE "Maintask" (
          "Id" INTEGER NOT NULL,
          "task_name" TEXT NOT NULL,
          "progress" TEXT DEFAULT '',
          "input" TEXT NOT NULL,
          "output" TEXT NOT NULL,
          "status" TEXT NOT NULL,
          "create_time" TEXT NOT NULL,
          "mode" TEXT NOT NULL,
          "describe" TEXT DEFAULT '',
          "refer_folder" TEXT DEFAULT '',
          PRIMARY KEY ("task_name")
        );''')
        conn.execute('''PRAGMA foreign_keys = true;''')

        conn.close()

    return db_file
class ConnectionPool(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionPool, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if(self.__initialized): return
        self.__initialized = True
        #数据库所在的目录
        db_path = Util.unify_path().user_path
        self.dbName = initialize_database(db_path)
        #不能把数据库放在临时文件夹
        # self.dbName = os.path.join(Util.unify_path(),'test.db')
        self.maxPoolSize = 5
        self.timeout = 1000
        self.pool = []
        for i in range(self.maxPoolSize):
            db = QSqlDatabase.addDatabase('QSQLITE', 'connectionPool%d' % i)
            db.setDatabaseName(self.dbName)
            if not db.open():
                error = db.lastError().text()
                print(error)
                raise ValueError('Unable to open database')
            self.pool.append(db)
        print('当前的连接', self.dbName, sep=' ')

    def acquire(self):
        for db in self.pool:
            if db.isOpen() and db.driver().hasFeature(QSqlDriver.Transactions):
                print(self.dbName)

                return db

        db = QSqlDatabase.addDatabase('QSQLITE', 'connectionPool%d' % len(self.pool))
        db.setDatabaseName(self.dbName)
        if db.open():
            self.pool.append(db)
            return db
        else:
            error = db.lastError().text()
            print(error)
            raise ValueError('Unable to open database')

    def release(self, db):
        pass

    @staticmethod
    def instance():
        if not ConnectionPool._instance:
            ConnectionPool._instance = ConnectionPool()
        return ConnectionPool._instance




#获取服务器传来的参数个数和点击加号对应的主任务的id创建子任务表
def create_SubTaskDatabase(user_param_input_value,mainid):
    # 连接数据库 使用sqlite
    global tb_name
    tb_name = "Subtask" + str(mainid)

    # 创建任务表 一个子任务对应一个任务表
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)

    sql = 'CREATE TABLE {} ("Subid" INTEGER primary key ,"Taskname" TEXT,"Execute_Time" Double,"Alg_Name" TEXT,"Ori_Imgname" TEXT,"Index_Name" TEXT);'.format(tb_name)
    print("初始化子表",query.exec_(sql))
    # 实现动态列初始化（后续需要添加其他信息如执行时间，这里先测试整体逻辑）
    # columns = ["p{}".format(i) for i in range(1, num_columns + 1)]
    columns = ["{}".format(key) for key in user_param_input_value[0].keys()]
    add_column(columns, query)
    ConnectionPool.instance().release(db)

    return True
#add_column 实现子任务的动态参数
def add_column(columns, query):

    for a in columns:
        query.exec_("ALTER TABLE {} ADD COLUMN {} TEXT;".format(tb_name,a))

def insert_SubTaskData(taskname, execute_time, alg_name, ori_imgname, index_name, user_param_input_value):
    # 连接数据库
    print(user_param_input_value)
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)


    #现在表字段的动态已经实现（create_database）接下来实现值的动态
    # query.prepare("INSERT INTO task (p1,p2,p3) VALUES (:p1,:p2,:p3)") 原来为全静态改为动态后如下：

    columns = ["{}".format(key) for key in user_param_input_value]
    # columns = ["{}".format(i) for i in range(1, Page_Home.Ui_Home.num_columns + 1)]
    #动态添加
    print("动态参数:")
    print(columns) #['alpha', 'kernel_size', 'iterations']
    #利用.join将列表转化成字符串
    columns_str = ", ".join(columns)

    placeholders = ", ".join("?" * len(columns))
    print("动态占位符"+placeholders)#?, ?, ?, ?
    #表名和列名无法使用？占位符替换需要使用{}方式填充。（字符串格式化）
    global sub_id
    query.prepare("INSERT INTO {} (Subid,Taskname,Execute_Time,Alg_Name,Ori_Imgname,Index_Name,{}) VALUES (?,?,?,?,?,?,{})".format(tb_name,columns_str,placeholders))
    query.addBindValue(sub_id)
    query.addBindValue(taskname)
    query.addBindValue(execute_time)
    query.addBindValue(alg_name)
    query.addBindValue(ori_imgname)
    query.addBindValue(index_name)
    print(query.boundValues())
    for value in user_param_input_value.values():
        query.addBindValue(str(value))
    print("插入子表",query.exec_())
    sub_id = sub_id+1
    ConnectionPool.instance().release(db)





def insert_Maintaskdata(taskname,input,output,create_time,mode,describe,refer_folder,progress,status=1):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)

    #获取最后一行的id
    query.exec('SELECT * FROM Maintask ORDER BY Id DESC LIMIT 1')
    query.first()
    # print("插入的mainid",query.value(0))
    row = query.value(0)
    if row == None:
        row = 0


    print("初始化主任务数据",query.prepare("INSERT INTO Maintask (Id,task_name,input,output,status,create_time,mode,describe,refer_folder,progress) VALUES (:id,:taskname,:input,:output,:status,:create_time,:mode,:describe,:refer_folder,:progress);"))
    query.bindValue(":taskname", taskname)
    query.bindValue(":input", input)
    query.bindValue(":output", output)
    query.bindValue(":refer", refer_folder)
    query.bindValue(":describe", describe)
    query.bindValue(":create_time", create_time)
    query.bindValue(":mode", mode)
    query.bindValue(":refer_folder", refer_folder)
    query.bindValue(":status", str(status))
    query.bindValue(":progress", progress)
    query.bindValue(":id",row+1)
    query.exec_()
    ConnectionPool.instance().release(db)




#根据点击的行数查找数据库中对应的行数（解决删除后id和row不匹配的问题）这里复杂了可优化后面删除子任务就没有这样，功能一样
#删除或者编辑需要定位到该项
def selectMaintaskByRow(id):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    task_dict = {"Id":"","task_name": "", "desc": "", "progress": "", "status": "",
                 "input": "", "output": "","refer_folder":"","mode":"","create_time":""
                 }
    i = 0

    query.prepare("SELECT * FROM Maintask")
    print("Id",id)
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
    else:
        while query.next() :
            #id-1是数据库中的实际第几行
            if i==id-1:
                Id = query.value(0)
                task_name = query.value(1)
                progress = query.value(2)
                input = query.value(3)
                output = query.value(4)
                status = query.value(5)
                create_time = query.value(6)
                mode = query.value(7)
                describe = query.value(8)
                refer_folder = query.value(9)

                task_dict["Id"] = Id
                task_dict["task_name"] = task_name
                task_dict["input"] = input
                task_dict["output"] = output
                task_dict["status"] = status
                task_dict["create_time"] = create_time
                task_dict["mode"] = mode
                task_dict["desc"] = describe
                task_dict["refer_folder"] = refer_folder
                task_dict["progress"] = progress
                ConnectionPool.instance().release(db)
                return task_dict
            i = i+1



#查出所有主任务
def selectAll():
    # db = QSqlDatabase.addDatabase("QSQLITE")
    # db.setDatabaseName("test.db")


    list_all = []

    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    query.prepare("SELECT * FROM Maintask")
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
    else:
        while query.next():
            task_dict = {"Id": "", "task_name": "", "desc": "", "progress": "", "status": "",
                         "input": "", "output": "", "refer_folder": "", "mode": "", "create_time": ""
                         }
            Id = query.value(0)
            task_name = query.value(1)
            progress = query.value(2)
            input = query.value(3)
            output = query.value(4)
            status = query.value(5)
            create_time = query.value(6)
            mode = query.value(7)
            describe = query.value(8)
            refer_folder = query.value(9)

            task_dict["Id"] = Id
            task_dict["task_name"] = task_name
            task_dict["input"] = input
            task_dict["output"] = output
            task_dict["status"] = status
            task_dict["create_time"] = create_time
            task_dict["mode"] = mode
            task_dict["desc"] = describe
            task_dict["refer_folder"] = refer_folder
            task_dict["progress"] = progress
            list_all.append(task_dict)
        ConnectionPool.instance().release(db)
        return list_all


#删除所有子任务和主任务
def deleteAll():
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)


    for task in selectAll():
        sub_name = "Subtask"+str(task['Id'])

        print("删除子表"+str(sub_name), query.exec("delete from {};".format(sub_name)))

    print("删除主表", query.exec("delete from {};".format("Maintask")))
    ConnectionPool.instance().release(db)

#根据点击的行号先查出主任务的id再根据id删除（使用selectMaintaskByRow复杂了）
def deletebyRow(row):
    print('删除的行是',row)

    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    id = selectMaintaskByRow(row)['Id']
    print('删除的id是',id)


    query.prepare("DELETE FROM Maintask WHERE Id = ?;")
    query.addBindValue(id)
    query.exec_()
    ConnectionPool.instance().release(db)

def editMaintask(id,taskname,input,output,create_time,mode,describe,refer_folder,progress):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    idd = selectMaintaskByRow(id)['Id']

    query.prepare("UPDATE Maintask SET task_name = ?,input = ?, output = ? , create_time = ? , mode = ? , describe = ? , refer_folder = ? , progress = ? where Id = ?")
    query.addBindValue(taskname)
    query.addBindValue(input)
    query.addBindValue(output)
    query.addBindValue(create_time)
    query.addBindValue(mode)
    query.addBindValue(describe)
    query.addBindValue(refer_folder)
    query.addBindValue(progress)
    query.addBindValue(idd)
    if query.exec_():
        print('编辑完成')
    ConnectionPool.instance().release(db)
# 两个地方需要调用这个函数，一个是从首页点击加号的时候展示对应的数据 第二个地方是初始化表格结束后点击完成 所以需要根据点击传来的mainid来调用函数
# def selectall_subdataById(mainid):
#     db = ConnectionPool.instance().acquire()
#     query = QSqlQuery(db)
#     tbname = "Subtask" + str(mainid) #子表的表名
#     list_all = [] #查出来的所有子数据
#     p = 1 #动态参数
#     query.prepare("select * from {}".format(tbname))
#     if not query.exec_():
#         print("Query execution failed with error: " + query.lastError().text())
#         ConnectionPool.instance().release(db)
#     else:
#         while query.next():
#             #将每次查出来的子数据给到一个新字典
#             task_dict = {"Subid": "", "task_name": "", "exec_time": "", "alg_name": "", "ori_imgname": "",
#                          "index_name": ""
#                          }
#             task_dict["Subid"] = query.value(0)
#             task_dict["task_name"] = query.value(1)
#             task_dict["exec_time"] = query.value(2)
#             task_dict["alg_name"] = query.value(3)
#             task_dict["ori_imgname"] = query.value(4)
#             task_dict["index_name"] = query.value(5)
#             for i in range(6,query.record().count()):
#                 task_dict[f"p{p}"] = query.value(i)
#                 p+=1
#             list_all.append(task_dict)
#         ConnectionPool.instance().release(db)
#         return list_all
#这种定位id方式好很多

def selectall_subdataById(mainid):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    tbname = "Subtask" + str(mainid)  # 子表的表名
    list_all = []  # 查出来的所有子数据

    query.prepare("SELECT * FROM {}".format(tbname))
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return list_all

    record = query.record()
    columns = [record.fieldName(i) for i in range(record.count())]

    while query.next():
        task_dict = {column: query.value(column) for column in columns}
        list_all.append(task_dict)

    ConnectionPool.instance().release(db)
    return list_all

def delete_subdataByrow(row,subtableid):
    #先根据点击的行号找到数据库对应的行数然后删除
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    tablename = "Subtask"+str(subtableid)

    query.prepare("delete from {} where subid in (select subid from {} order by subid limit {},1);".format(tablename,tablename,row-1))
    print("delete from {} where subid in (select subid from {} order by subid limit {},1);".format(tablename,tablename,row-1))
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
def get_param_from_database():
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    query.exec_("PRAGMA table_info(Subtask1)")  # 替换为你的表名

    columns = []
    while query.next():
        columns.append(query.value(1))

    if 'Index_Name' in columns:
        index_position = columns.index('Index_Name')
        fields_after_index_name = columns[index_position + 1:]
        return fields_after_index_name
    else:
        print("Field 'Index_Name' not found.")
        return []