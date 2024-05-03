import hashlib
import os

from PyQt5.QtSql import QSqlDriver
# 当主任务设置好后点击加号则创建Subtask+_1的子任务表
# sub_id从1开始自增
import util.Util
from pages.Page_Setting import Ui_Setting
# 最好不要文件名和类名一样

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
        db_path = util.Util.unify_path().user_path+"/config"
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
def create_SubTaskDatabase(user_param_input_value,username,id):
    # 连接数据库 使用sqlite 全局变量实现自增
    global subtask_id
    subtask_id = 1 # 维护子任务的subid字段的自增
    index = 1
    if not count_table(username,id) is 0:
    # 第一个id表示主任务id  第二个表示用户名  第三个表示字一个主任务的不同算法产生的不同子表
        index = count_table(username,id)+1
    tb_name = "Subtask" + str(id)+'_'+str(username)+'_'+str(index)




    # 创建任务表 一个子任务对应一个任务表
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)

    sql = 'CREATE TABLE {} ("Subid" INTEGER primary key ,"Taskname" TEXT,"Execute_Time" Double,"Alg_Name" TEXT,"Ori_Imgname" TEXT,"isDone" INTEGER);'.format(tb_name)
    print("初始化子表")
    if not query.exec_(sql):
        print("Query execution failed with error: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return None  # Or handle error as appropriate
    # 实现动态列初始化（后续需要添加其他信息如执行时间，这里先测试整体逻辑）
    # columns = ["p{}".format(i) for i in range(1, num_columns + 1)]
    columns = ["{}".format(key) for key in user_param_input_value[0].keys()]
    add_column(columns, query,tb_name)
    ConnectionPool.instance().release(db)
    return index
#add_column 实现子任务的动态参数
def add_column(columns, query,tb_name):

    for a in columns:
        query.exec_("ALTER TABLE {} ADD COLUMN {} TEXT;".format(tb_name,a))

def insert_SubTaskData(subid,taskname, username,index,execute_time, alg_name, ori_imgname, index_name, user_param_input_value):
    # 连接数据库
    print(user_param_input_value)
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    tb_name = "Subtask" + str(subid)+'_'+str(username)+'_'+str(index)


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
    query.prepare("INSERT INTO {} (Subid,Taskname,Execute_Time,Alg_Name,Ori_Imgname,isDone,{}) VALUES (?,?,?,?,?,0,{})".format(tb_name,columns_str,placeholders))
    # 使用自增
    global subtask_id
    query.addBindValue(subtask_id)
    query.addBindValue(taskname)
    query.addBindValue(execute_time)
    query.addBindValue(alg_name)
    query.addBindValue(ori_imgname)
    print(query.boundValues())
    for value in user_param_input_value.values():
        query.addBindValue(str(value))
    print("插入子表")
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return None  # Or handle error as appropriate
    subtask_id +=1
    ConnectionPool.instance().release(db)





def insert_Maintaskdata(taskname,input,output,username,create_time,mode,describe,refer_folder,progress,status=1):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)

    #获取最后一行的id
    query.exec("SELECT * FROM Maintask where username = '{}' ORDER BY Id DESC LIMIT 1 ".format(username))
    query.first()
    # print("插入的mainid",query.value(0))
    row = query.value(0)
    if row == None:
        row = 0


    print("初始化主任务数据",query.prepare("INSERT INTO Maintask (Id,task_name,input,output,status,create_time,mode,describe,refer_folder,progress,username) VALUES (:id,:taskname,:input,:output,:status,:create_time,:mode,:describe,:refer_folder,:progress,:username);"))
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
    query.bindValue(":username",username)
    query.exec_()
    ConnectionPool.instance().release(db)




#根据点击的行数查找数据库中对应的行数（解决删除后id和row不匹配的问题）这里复杂了可优化后面删除子任务就没有这样，功能一样
#删除或者编辑需要定位到该项
def selectMaintaskByRow(id,username):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    task_dict = {
        "Id": "",
        "task_name": "",
        "desc": "",
        "progress": "",
        "status": "",
        "input": "",
        "output": "",
        "refer_folder": "",
        "mode": "",
        "create_time": ""
    }

    # 使用参数化查询以提高安全性和效率
    query.prepare("SELECT * FROM Maintask WHERE id = ? and username = ?;")
    query.addBindValue(id)
    query.addBindValue(username)

    print("正在查询Id为", id)

    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return None  # Or handle error as appropriate
    else:
        if query.next():
            task_dict["Id"] = query.value(0)
            task_dict["task_name"] = query.value(1)
            task_dict["progress"] = query.value(2)
            task_dict["input"] = query.value(3)
            task_dict["output"] = query.value(4)
            task_dict["status"] = query.value(5)
            task_dict["create_time"] = query.value(6)
            task_dict["mode"] = query.value(7)
            task_dict["desc"] = query.value(8)
            task_dict["refer_folder"] = query.value(9)
        else:
            print("No result found for ID:", id)
            task_dict = None  # No result found

        ConnectionPool.instance().release(db)
        return task_dict


#查出所有主任务
def selectAll(username):
    # db = QSqlDatabase.addDatabase("QSQLITE")
    # db.setDatabaseName("test.db")


    list_all = []

    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    query.prepare("SELECT * FROM Maintask where username = '{}' ".format(username))
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
def selectDistinctOriPicName(mainid,username,subtable_id):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    tb_name = "Subtask" + str(mainid)+'_'+str(username)+'_'+str(subtable_id)
    list_all = []  # 查出来的所有子数据
    query.prepare("SELECT DISTINCT Ori_Imgname FROM {}".format(tb_name))
    if query.exec_():
        while query.next():
                # Assume the field 'Ori_Imgname' is the first field in SELECT
                ori_imgname = query.value(0)
                list_all.append(ori_imgname)
        ConnectionPool.instance().release(db)
        return list_all
    else :
        print("Query execution failed with error: " + query.lastError().text())



#删除所有子任务和主任务
def deleteSth(username,row):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    if not row is None:
        prefix_name = "Subtask" + str(row) + '_' + str(username)
        if query.exec_("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '{}%'".format(prefix_name)):
            # 使用一个列表收集所有表名，因为我们不能在遍历查询结果时更改数据库结构
            tables_to_drop = []
            while query.next():
                tables_to_drop.append(query.value(0))
            # 遍历收集到的表名，逐个删除表
            for table_name in tables_to_drop:
                if not query.exec_(f'DROP TABLE "{table_name}"'):
                    print("Query execution failed with error: " + query.lastError().text())
                    ConnectionPool.instance().release(db)
        else:
            print("Query execution failed with error: " + query.lastError().text())
            ConnectionPool.instance().release(db)
            return False
    else:
        for task in selectAll(username):
            prefix_name = "Subtask"+str(task['Id'])+'_'+username
            if query.exec_("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '{}%'".format(prefix_name)):
                # 使用一个列表收集所有表名，因为我们不能在遍历查询结果时更改数据库结构
                tables_to_drop = []
                while query.next():
                    tables_to_drop.append(query.value(0))
                # 遍历收集到的表名，逐个删除表
                for table_name in tables_to_drop:
                    if not query.exec_(f'DROP TABLE "{table_name}"'):
                        print("Query execution failed with error: " + query.lastError().text())
                        ConnectionPool.instance().release(db)
            else:
                print("Query execution failed with error: " + query.lastError().text())
                ConnectionPool.instance().release(db)
                return False
        print("删除主表", query.exec("delete from {};".format("Maintask")))
    ConnectionPool.instance().release(db)









#根据点击的行号先查出主任务的id再根据id删除（使用selectMaintaskByRow复杂了）
def deletebyRow(row,username):
    print('删除的行是',row)

    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    id = selectMaintaskByRow(row)['Id']
    print('删除的id是',id)


    query.prepare("DELETE FROM Maintask WHERE Id = ? and username = ?;")
    query.addBindValue(id)
    query.addBindValue(username)
    query.exec_()
    ConnectionPool.instance().release(db)

def editMaintask(id,taskname,input,output,username,create_time,mode,describe,refer_folder,progress):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    idd = selectMaintaskByRow(id,username)['Id']
    query.prepare("UPDATE Maintask SET task_name = ?,input = ?, output = ? , create_time = ? , mode = ? , describe = ? , refer_folder = ? , progress = ? where Id = ? and username = ?")
    query.addBindValue(taskname)
    query.addBindValue(input)
    query.addBindValue(output)
    query.addBindValue(create_time)
    query.addBindValue(mode)
    query.addBindValue(describe)
    query.addBindValue(refer_folder)
    query.addBindValue(progress)
    query.addBindValue(idd)
    query.addBindValue(username)
    if query.exec_():
        print('编辑完成')
    ConnectionPool.instance().release(db)
def editSubtaskByRowId(mainid,rowid,execute_time,username,subtable_id):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    tb_name = "Subtask" + str(mainid)+'_'+str(username)+'_'+str(subtable_id)

    print("正在执行sql","UPDATE {} SET execute_time = ?,isDone = 1 where Subid = ?".format(tb_name),sep=' ')
    query.prepare("UPDATE {} SET execute_time = ? ,isDone = 1 where Subid = ?".format(tb_name))
    query.addBindValue(execute_time)
    query.addBindValue(rowid)

    if query.exec_():
        print('编辑子任务完成')
    else:
        print("Query execution failed with error: " + query.lastError().text())
    ConnectionPool.instance().release(db)

# 一个主任务的多个子任务
def selectall_subdataById(mainid,isqueryone,isqueryOriPic,oriPicName,username,subtable_id):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    tbname = "Subtask" + str(mainid)+'_'+str(username)+'_'+str(subtable_id)

    list_all = []  # 查出来的所有子数据
    if isqueryone:
        query.prepare("SELECT * FROM {} limit 1".format(tbname))
    elif isqueryOriPic:
        query.prepare("SELECT * FROM {} WHERE Ori_Imgname like '{}' ".format(tbname,oriPicName))
        print("SELECT * FROM {} WHERE Ori_Imgname like %{}%".format(tbname,oriPicName))
    else :
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


def delete_subdataByrow(row,subtableid,username):
    #先根据点击的行号找到数据库对应的行数然后删除
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    tablename = "Subtask"+str(subtableid)+username

    query.prepare("delete from {} where subid in (select subid from {} order by subid limit {},1);".format(tablename,tablename,row-1))
    print("delete from {} where subid in (select subid from {} order by subid limit {},1);".format(tablename,tablename,row-1))
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())

def get_param_from_database(mainid):
    print("正在查找用户配置的算法的参数值")
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    query.exec_("PRAGMA table_info(Subtask{})".format(mainid))
    columns = []
    while query.next():
        columns.append(query.value(1))
    if 'Ori_Imgname' in columns:
        index_position = columns.index('Ori_Imgname')
        fields_after_index_name = columns[index_position + 1:]
        return fields_after_index_name
    else:
        print("Field 'Index_Name' not found.")
        return []


def hash_password(password):
    # 使用 SHA-256 哈希算法
    return hashlib.sha256(password.encode()).hexdigest()

def registPerson(username, password,yhsf):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)

    # 检查用户名是否已存在
    query.prepare("SELECT COUNT(*) FROM userinfo WHERE username = :username")
    query.bindValue(":username", username)
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return

    query.next()
    if query.value(0) > 0:
        print("用户名已存在")
        ConnectionPool.instance().release(db)
        return 1

    # 用户名不存在，继续注册
    hashed_password = hash_password(password)
    query.prepare("INSERT INTO userinfo (username, password,yhsf) VALUES (:username, :password,:yhsf)")
    query.bindValue(":username", username)
    query.bindValue(":password", hashed_password)
    query.bindValue(":yhsf", yhsf)
    if not query.exec_():
        print("注册失败，错误信息: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return 2
    ConnectionPool.instance().release(db)
    return 3
def login(username, password):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)

    query.prepare("SELECT password FROM userinfo WHERE username = :username")
    query.bindValue(":username", username)
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return False

    if query.next():
        stored_password = query.value(0)
        if stored_password == hash_password(password):
            print("登录成功")
            ConnectionPool.instance().release(db)
            return True
        else:
            print("密码错误")
    else:
        print("用户名不存在")

    ConnectionPool.instance().release(db)
    return False



def count_table(username,mainid):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)

    query.prepare("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'Subtask{}_{}%'".format(mainid,username))
    if not query.exec_():
        print("Query execution failed with error: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return False
    while query.next():
        return query.value(0)

def insert_stastic(id, total_algtime, total_indextime, mainid, subid, username):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    query.prepare(
        "INSERT INTO stastic (id, total_algtime,total_indextime,mainid,subid,username) VALUES (:id, :total_algtime,:total_indextime,mainid,subid,username)")
    query.bindValue(":id", id)
    query.bindValue(":total_algtime", total_algtime)
    query.bindValue(":total_indextime", total_indextime)
    query.bindValue(":mainid", mainid)
    query.bindValue(":subid", subid)
    query.bindValue(":username", username)
    if not query.exec_():
        print("insert_stastic错误信息: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return False
    ConnectionPool.instance().release(db)
    return True

def select_stastic(mainid, subid, username):
    db = ConnectionPool.instance().acquire()
    query = QSqlQuery(db)
    query.prepare("SELECT total_algtime,total_indextime FROM stastic WHERE username = ? AND mainid = ? AND subid = ?")
    query.addBindValue(username)
    query.addBindValue(mainid)
    query.addBindValue(subid)

    if not query.exec_():
        print("insert_stastic错误信息: " + query.lastError().text())
        ConnectionPool.instance().release(db)
        return False
    # 返回查询到的字典
    result = {}
    while query.next():
        result['total_algtime'] = query.value(0)
        result['total_indextime'] = query.value(1)
    ConnectionPool.instance().release(db)
    return result