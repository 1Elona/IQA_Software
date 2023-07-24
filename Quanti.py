import time
# import torch
# import piq
import csv
import os
import re
import numpy as np
import math
import cv2
import sys

import Util


class Quantitation:
    # https://github.com/Nguyen-Hoang-Nam/image-enhancement/blob/9396e403842fa46551a52883cf2e9793ad92d894/image_enhancement/quantitation.py
    # Absolute Mean Brightness Error

    # Mean Square Error
    def MSE(image_input, image_output):
        err = np.sum((image_input.astype("float") - image_output.astype("float")) ** 2)
        err /= float(image_input.shape[0] * image_input.shape[1])

        return err

    # Entropy
    def Entropy(image_output):
        pdf, _ = np.histogram(image_output, 256, [0, 255])
        pdf = pdf / float(image_output.shape[0] * image_output.shape[1])

        ent = 0
        for probility in pdf:
            if probility>0:
                ent += probility * math.log2(probility)

        return -ent

    def si(img1, img2, L=255):
        """Calculate SSIM (structural similarity) for one channel images.
        Args:
            img1 (ndarray): Images with range [0, 255].
            img2 (ndarray): Images with range [0, 255].
        Returns:
            float: ssim result.
        """
        K1 = 0.01
        K2 = 0.03
        C1 = (K1 * L) ** 2
        C2 = (K2 * L) ** 2
        C3 = C2 / 2

        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)

        # img1 = (img1 - np.min(img1)) / (np.max(img1) - np.min(img1))
        # img2 = (img2 - np.min(img2)) / (np.max(img2) - np.min(img2))

        print(img1)
        print("/n")
        print(img2)
        # ux
        ux = img1.mean()
        # uy
        uy = img2.mean()
        # ux^2
        ux_sq = ux ** 2
        # uy^2
        uy_sq = uy ** 2
        # ux*uy
        uxuy = ux * uy
        # ox、oy方差计算
        ox_sq = np.var(img1, ddof=1)  # 方差
        oy_sq = np.var(img2, ddof=1)
        ox = np.sqrt(ox_sq)  # 标准差
        oy = np.sqrt(oy_sq)
        oxoy = ox * oy
        oxy = np.mean((img1 - ux) * (img2 - uy))  # 协方差
        # 公式一计算
        L = (2 * uxuy + C1) / (ux_sq + uy_sq + C1)

        C = (2 * ox * oy + C2) / (ox_sq + oy_sq + C2)  # 对比度

        S = (oxy + C3) / (oxoy + C3)


        return L


    def ssim(img1, img2, L=255):
        """Calculate SSIM (structural similarity) for one channel images.
        Args:
            img1 (ndarray): Images with range [0, 255].
            img2 (ndarray): Images with range [0, 255].
        Returns:
            float: ssim result.
        """
        K1 = 0.01
        K2 = 0.03
        C1 = (K1 * L) ** 2
        C2 = (K2 * L) ** 2
        C3 = C2 / 2

        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)

        # img1 = (img1 - np.min(img1)) / (np.max(img1) - np.min(img1))
        # img2 = (img2 - np.min(img2)) / (np.max(img2) - np.min(img2))

        print(img1)
        print("/n")
        print(img2)
        # ux
        ux = img1.mean()
        # uy
        uy = img2.mean()
        # ux^2
        ux_sq = ux ** 2
        # uy^2
        uy_sq = uy ** 2
        # ux*uy
        uxuy = ux * uy
        # ox、oy方差计算
        ox_sq = np.var(img1, ddof=1)  # 方差
        oy_sq = np.var(img2, ddof=1)
        ox = np.sqrt(ox_sq)  # 标准差
        oy = np.sqrt(oy_sq)
        oxoy = ox * oy
        oxy = np.mean((img1 - ux) * (img2 - uy))  # 协方差
        # 公式一计算
        L = (2 * uxuy + C1) / (ux_sq + uy_sq + C1)

        C = (2 * ox * oy + C2) / (ox_sq + oy_sq + C2)  # 对比度

        S = (oxy + C3) / (oxoy + C3)


        ssim = L * C * S
        return ssim


    def calEC(img):
        container = np.copy(img)
        size = container.shape
        for i in range(1, size[0] - 1):
            for j in range(1, size[1] - 1):
                gx = (img[i - 1][j - 1] + 2 * img[i][j - 1] + img[i + 1][j - 1]) - (
                            img[i - 1][j + 1] + 2 * img[i][j + 1] + img[i + 1][j + 1])
                gy = (img[i - 1][j - 1] + 2 * img[i - 1][j] + img[i - 1][j + 1]) - (
                            img[i + 1][j - 1] + 2 * img[i + 1][j] + img[i + 1][j + 1])
                container[i][j] = min(255, np.sqrt(gx ** 2 + gy ** 2))
        EC = np.mean(container)

        return EC

    def psnr(img1, img2):
        img1 = np.float64(img1)
        img2 = np.float64(img2)
        mse = np.mean((img1 - img2) ** 2)
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

    def AMBE(image_input, image_output):
        return abs(np.mean(image_input) - np.mean(image_output))



def test_iqa(parameters, original_path, result_path):
    print(original_path,"++++++++++",result_path,"++++++++++",sep=' ')

    x = cv2.imread(original_path)
    y = cv2.imread(result_path)

    x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    y = cv2.cvtColor(y, cv2.COLOR_BGR2GRAY)

    image_name = os.path.splitext(os.path.basename(original_path))[0]

    li = []

    li.append(image_name)
    for strr in parameters:
        li.append(strr)



    li.append(Quantitation.AMBE(x, y))
    li.append(Quantitation.MSE(x, y))
    li.append(Quantitation.Entropy(y))
    li.append(Quantitation.si(x, y))
    li.append(Quantitation.ssim(x, y))
    try:
        li.append(Quantitation.calEC(y))
    except:
        print('ec出问题',original_path,sep=' ')
        li.append('null')

    li.append(Quantitation.psnr(x, y))

    with open(os.path.join(Util.unify_path()[1],'quant.csv'), 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(li)

    print('ok')




def get_loss(index_num,inputf,outputf):
    input_dir = inputf
    output_dir = outputf
    print(outputf,"+++++++",sep='')

    files = os.listdir(output_dir)
    for file in files:
        if not os.path.isdir(file):
            file_name = os.path.splitext(file)[0]
            print('filename:',file_name,sep=' ')
            if file_name == '.DS_Store':
                continue
            parts = file_name.split('%%')

            imgname = parts[0]
            print('imgname:',imgname,sep=' ')
            parameters = []
            for k in range(1,index_num+2):

                parameters.append(parts[k])
            print('parameters:',parameters,sep=' ')

            original_path = os.path.join(input_dir, imgname + '.jpg')

            result_path = os.path.join(outputf, file)
            print('result_path:',result_path,sep=' ')

            test_iqa(parameters, original_path, result_path)
            print('End')

def quant(alg_index_num,inputf,outputf):
    f = open(os.path.join(Util.unify_path()[1],'quant.csv'), 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)

    title = []
    for i in range(alg_index_num+2):
        title.append('')
    title.extend(['AMBE', 'MSE', 'Entropy', 'si', 'ssim', 'EC', 'psnr'])
    print('title:',title,sep= '')
    csv_writer.writerow(title)

    f.close()
    get_loss(alg_index_num,inputf,outputf)









