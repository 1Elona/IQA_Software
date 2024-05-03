"""
@ProjectName: ${IQA_Soft_ware}
@Author  : elona
@Time    : 2022.11.17
@QQ: 1137489622
"""
import sys

import controller.switchpage
from PyQt5 import QtWidgets
from util import Util
from controller.switchpage import Controller


# 指定系统入口
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_Login()
    sys.exit(app.exec_())



if __name__ == '__main__':
    Util.initConfig()
    main()
