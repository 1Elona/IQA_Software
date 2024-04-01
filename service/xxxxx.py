# #coding:utf-8
import numpy as np
def fun(losskey):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    Loss = pd.read_csv(r"lossqq.csv")  ##rsr
    # loss = pd.read_csv(r"lossrar1.csv")##rsr
    # loss = pd.read_csv(r"losst2.csv")##整数扩张
    # loss = pd.read_csv("lossc.csv")##
    Loss = Loss[~(Loss['Unnamed: 0'].isnull())]

    # print(Loss.head(10))
    aa=set(Loss['Unnamed: 0'])
    bb=set(Loss['Unnamed: 1'])

    # print(aa)#############
    x = sorted(aa)  # 图
    y = sorted(bb)  # modle
    # print(x)
    # print(y)
    X = sorted(set(x))
    Y = sorted(set(y))
    X.sort()
    Y.sort()
    print(losskey)
    di={}
    for m in y:
        l = Loss.loc[(Loss['Unnamed: 1'] == m)][losskey]
        # print(m,np.mean(l))
        plt.figure(num=losskey, figsize=(120, 30))
        if len(x)==len(l):
            print(len(x))###################################################
            print(len(l))##############################################
            plt.plot(x, l)
            print('ok')##########################
            plt.legend(y, loc="right")
            di[m]=np.mean(l)

        # print(m)

    di=sorted(di.items(), key=lambda d: d[1])
    # print(di)
    for i in range(len(di)):
        print(di[i], '\n', end="")
    plt.xticks(rotation=270)
    # plt.legend(y, loc="lower right")
    # plt.show()
    plt.savefig(losskey)

Losskey=['AMBE','MSE','Entropy','si','ssimloss','ssim','EC','psnr']
# Losskey=['EME','CII']#根据需求改
a=10
b=20

for k in Losskey:
    fun(k)


# losskey ='Style'
# losskey ='BRISQUE'
# losskey ='Content'
# losskey ='DISTS'
# losskey ='DSS'
# losskey ='FSIM'
# losskey ='GMSD'
# losskey ='HaarPSI'
# losskey ='LPIPS'
# losskey ='MDSI'
# losskey ='MS-SSIM'
# losskey ='MS-GMSDc'
# losskey ='PieAPP'
# losskey ='SSIM'
# losskey ='Style'
# losskey ='TV'
# losskey ='VIFp'
# losskey ='VSI'
# losskey ='SR-SIM'
# losskey ='pnsr_index'
# losskey ='ssim_index'
# losskey ='ssim_loss'
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# Loss = pd.read_csv(r"loss5.csv")##rsr
# # loss = pd.read_csv(r"lossrar1.csv")##rsr
# # loss = pd.read_csv(r"losst2.csv")##整数扩张
# # loss = pd.read_csv("lossc.csv")##
#
# print(Loss.head(10))
# x = sorted(set(Loss['Unnamed: 0']))#图
# y = sorted(set(Loss['Unnamed: 1']))#modle
# print(x)
# print(y)
# X = sorted(set(x))
# Y = sorted(set(y))
# X.sort()
# Y.sort()
# for m in y:
#     l=Loss.loc[(Loss['Unnamed: 1'] == m)][losskey]
#     plt.figure(num=losskey, figsize=(20, 30))
#     plt.plot(x, l)
# plt.xticks(rotation=270)
# plt.legend(y, loc="lower right")
# plt.show()


#
# for kk in t:
#     loss=Loss[Loss['Unnamed: 1']==kk]
#     x = []
#     y = []
#     key = loss['Unnamed: 0']
#     # print(loss)
#     print(key)

import matplotlib.pyplot as plt
import numpy as np
#
# x = np.linspace(-3, 3, 5)  # 设置横轴的取值点
# y=[]
# y1 = 2 * x + 1
# y.append(y1)
# # 曲线1
# y2 = x ** 2
# y.append(y2)
# y3 = x ** 3
# y.append(y3)
# y4 = x ** 4
# # 曲线2
# x=['a','bb','tc','d','e']
# for i in y:
#     plt.figure(num=3, figsize=(8, 5))
#     plt.plot(x, i)
#
#
# plt.legend(["1", "2","3"], loc="lower right")
# plt.show()