import csv
import os
import uuid

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QMessageBox, QApplication
import sys
import time

import pages.Page_Home
import service.Quanti
from util import Database
from util import Util
import service

class WorkerThread(QThread):
    progress_signal = pyqtSignal(int,str,int,int,float,int)  # 用于进度更新的信号
    finished_signal = pyqtSignal(float,float)  # 用于统计总时间

    def __init__(self, row,username):
        super().__init__()
        self.row = row
        # self.subid = d2
        self.is_running = True
        self.total_time = 0.0
        self.username = username
        # self.hasDone = []

    def run(self):
        print("=========正在执行增强算法代码==========")
        # 从数据库获取输入输出文件夹的路径
        input_folder = Database.selectMaintaskByRow(self.row,self.username)["input"]
        output_folder = Database.selectMaintaskByRow(self.row,self.username)["output"]
        for kkk in range(0,Database.count_table(self.username,self.row)):
            # if kkk not in self.hasDone:
                # 获取子任务数据
                subtask_data = Database.selectall_subdataById(self.row, False, False, False,self.username,kkk+1)
                if not subtask_data:
                    return

                # 执行所有子任务
                total_subtasks = len(subtask_data)
                for i,subtask in enumerate(subtask_data):
                    alg_name = subtask['Alg_Name']
                    isDone = subtask['isDone']
                    if isDone ==1:
                        continue
                    params = {paramname: subtask[paramname] for paramname in list(Util.get_data_from_config(alg_name))}

                    # 执行图像增强算法

                    start_time = time.time()  # 程序开始时间

                    executor = service.Optimize_ImageEhancement.AlgorithmExecutor(input_folder, output_folder)
                    executor.add_algorithm(alg_name, **params)
                    executor.test_sth()
                    # executor.apply_image_enhancement()

                    end_time = time.time()  # 程序结束时间
                    run_time = end_time - start_time  # 程序的运行时间，单位为秒
                    self.total_time = self.total_time+run_time
                    Database.editSubtaskByRowId(self.row, subtask['Subid'], format(run_time*1000, '.3f'),
                                                pages.Page_Home.Ui_Home.username,kkk+1)


                    # 这里你可以根据算法的执行进度发出进度更新的信号
                    progress_percentage = int((i + 1) / total_subtasks * 100)

                    self.progress_signal.emit(progress_percentage,'blue',0,self.row,float(format(run_time*1000, '.3f')),i)  # 假设图像增强算法完成了一半的进度

                # 执行指标计算
                # 注意：这里应该根据实际执行情况来更新进度
                print("=========正在执行生成指标csv算法代码==========")
                start_time2 = time.time()  # 程序结束时间
                csvname = service.Quanti.quant(self.progress_signal,len(Util.get_data_from_config(alg_name)), self.row,kkk+1,inputf=input_folder, outputf=output_folder)

                end_time2 = time.time()  # 程序结束时间
                index_time = end_time2 - start_time2  # 程序的运行时间，单位为秒
                #写回csv
                f = open(os.path.join(Util.unify_path().user_path, csvname), 'a', encoding='utf-8', newline='')
                csv_writer = csv.writer(f)
                title = []
                title.extend(['===============================================已完成==============================='])
                csv_writer.writerow(title)
                f.close()

                self.finished_signal.emit(self.total_time,index_time)
                Database.insert_stastic(uuid.UUID,format(self.total_time*1000, '.3f'),format(index_time*1000, '.3f'),self.row,kkk+1,self.username)
                # self.hasDone.append(kkk)