# import json
#
# import cv2
# import os
#
# import Util
# import handleuserinput
# v1
# #一个subtask实体，执行时间
# class ImageEnhancement:
#     #如何设计一个软件包含多个算法，一个算法又有多个参数，一个参数又有多个值(add_algdict_info)
#
#     def __init__(self, input_folder, output_folder, userinput,algname):
#         #构造之前先查询是否config.json里配置里该算法的信息
#         self.data = Util.get_data_from_config(algname)
#
#         #根据算法名获取各个指标的范围
#
#
#         self.input_folder = input_folder
#         self.output_folder = output_folder
#         self.userinput = userinput
#         self.algname = algname
#
#
#  # 根据用户选择的算法名获取参数名以及验证输入是否合法
#  #    def is_valid(self,value, range_str):
#  #            range_str = range_str.strip()
#  #            lower_inclusive = range_str.startswith('[')
#  #            upper_inclusive = range_str.endswith(']')
#  #
#  #            # 提取数值范围
#  #            lower_bound, upper_bound = map(float, range_str.strip('[]()').split(','))
#  #
#  #            if lower_inclusive:
#  #                if value < lower_bound:
#  #                    return False
#  #            else:
#  #                if value <= lower_bound:
#  #                    return False
#  #
#  #            if upper_inclusive:
#  #                if value > upper_bound:
#  #                    return False
#  #            else:
#  #                if value >= upper_bound:
#  #                    return False
#  #
#  #            return True
#  #
#
#
#
#
#
#         # params = {"alpha": 0.1, "kernel_size": 5, "iterations": 500}
#         #
#         # params_valid = all(is_valid(value, self.data[algorithm]['param'][key]) for key, value in params.items())
#         #
#         # print(f"Algorithm '{algorithm}' has {get_algorithm_params_count(algorithm)} parameters.")
#         # print(f"Parameter values valid: {params_valid}")
#
#
#
#
#     def apply_filter(self, image):
#         if self.algname == "EXAMPLE":
#             filtered = cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)
#
#
#
#
#         elif self.filter_type == "THRESHOLD":
#             _, filtered = cv2.threshold(image, self.threshold, 255, cv2.THRESH_BINARY)
#         else:
#             filtered = image
#
#         for i in range(self.iterations):
#             filtered = cv2.erode(filtered, None, iterations=1)
#             filtered = cv2.dilate(filtered, None, iterations=1)
#
#         return filtered
#
#     def apply_image_enhancement(self):
#         # 遍历输入文件夹中的所有图像文件
#         for file in os.listdir(self.input_folder):
#             if file.endswith('.jpg') or file.endswith('.png'):
#                 input_file = os.path.join(self.input_folder, file)
#
#                 img                = cv2.imread(input_file,0)
#
#                 # 进行图像增强操作
#                 filtered_img = self.apply_filter(img)
#
#                 # 保存增强后的图像
#                 file_name, file_ext = os.path.splitext(file)
#                 output_file = os.path.join(self.output_folder, f"{file_name}%%{self.algname}%%{self.existed_algdict['index']}%%{self.kernel_size}{file_ext}")
#                 cv2.imwrite(output_file, filtered_img)
#
#         # 返回算法的参数个数、执行状态等信息
#         return {
#             "params_count": len([p for p in [self.filter_type, self.kernel_size, self.threshold, self.iterations] if p is not None]),
#             "status": "success"
#         }
# if __name__ == '__main__':
#     a = ImageEnhancement("/Users/elona/Desktop/pythonProject/IQA_Software2/IQA_Software/need","/Users/elona/Desktop/pythonProject/IQA_Software2/IQA_Software/oout","1-3#1,5-6#0.5","EXAMPLE")
#     print(a.get_algorithm_params_count()[0])


import json
import multiprocessing

import cv2
import os
import Util
import handleuserinput
import Database

class ImageEnhancement:
    def __init__(self, input_folder, output_folder, algname,params,alpha,kernel_size,iterations):
        self.data = Util.get_data_from_config(algname)
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.algname = algname
        self.params = params
        self.alpha = alpha
        self.kernel_size = kernel_size
        self.iterations = iterations
        self.filters = {
            "EXAMPLE": self.example_filter,
            "THRESHOLD": self.threshold_filter

        }

    def is_valid(self, value, range_str):
        range_str = range_str.strip()
        lower_inclusive = range_str.startswith('[')
        upper_inclusive = range_str.endswith(']')

        lower_bound, upper_bound = map(float, range_str.strip('[]()').split(','))

        if lower_inclusive:
            if value < lower_bound:
                return False
        else:
            if value <= lower_bound:
                return False

        if upper_inclusive:
            if value > upper_bound:
                return False
        else:
            if value >= upper_bound:
                return False

        return True

    def example_filter(self, image):
        #如何去使用这个参数由管理员自己决定
        # print('该算法收到的param列表:',self.params,sep=' ')
        alpha = self.alpha
        kernel_size = self.kernel_size  # 获取kernel_size参数，如果不存在就使用默认值5
        iterations = self.iterations  # 获取iterations参
        filtered = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return self.iterative_filter(filtered)

    def iterative_filter(self, image):
        for i in range(self.iterations):
            image = cv2.erode(image, None, iterations=1)
            image = cv2.dilate(image, None, iterations=1)
        return image

    def threshold_filter(self, image):
        _, filtered = cv2.threshold(image, self.threshold, 255, cv2.THRESH_BINARY)
        return self.iterative_filter(filtered)

    # def process_image(self, file):
    #     try:
    #         if self.is_image_file(file):
    #             input_file = os.path.join(self.input_folder, file)
    #             file_name, file_ext = os.path.splitext(file)
    #             output_file = os.path.join(self.output_folder,
    #                                        f"{file_name}%%{self.algname}%%{self.alpha}%%{self.iterations}%%{self.kernel_size}{file_ext}")
    #             if os.path.basename(output_file) in os.listdir(self.output_folder):
    #                 return
    #
    #             img = cv2.imread(input_file, -1)
    #             filtered_img = self.apply_filter(img)
    #             cv2.imwrite(output_file, filtered_img)
    #     except Exception as e:
    #         print(f"文件{input_file}可能出问题", e)

    def is_image_file(self, file):
        return file.endswith('.jpg') or file.endswith('.png')

    def apply_filter(self, image):
        return self.filters[self.algname](image)

    def process_image(self, file):
        try:
            if file.endswith('.jpg') or file.endswith('.png'):
                input_file = os.path.join(self.input_folder, file)
                file_name, file_ext = os.path.splitext(file)
                output_file = os.path.join(self.output_folder,
                                           f"{file_name}%%{self.algname}%%{self.alpha}%%{self.iterations}%%{self.kernel_size}{file_ext}")
                if os.path.basename(output_file) in os.listdir(self.output_folder):
                    return

                img = cv2.imread(input_file, -1)
                filtered_img = self.apply_filter(img)
                cv2.imwrite(output_file, filtered_img)
        except Exception as e:
            print(f"文件{input_file}可能出问题", e)

    def apply_image_enhancement(self):
        with multiprocessing.Pool(processes=5) as pool:
            pool.map(self.process_image, os.listdir(self.input_folder))

    # def apply_image_enhancement(self):
    #     for file in os.listdir(self.input_folder):
    #         try:
    #             if file.endswith('.jpg') or file.endswith('.png'):
    #                 input_file = os.path.join(self.input_folder, file)
    #                 file_name, file_ext = os.path.splitext(file)
    #                 output_file = os.path.join(self.output_folder, f"{file_name}%%{self.algname}%%{self.alpha}%%{self.iterations}%%{self.kernel_size}{file_ext}")
    #                 if os.path.basename(output_file) in os.listdir(self.output_folder):
    #                     continue
    #
    #                 img = cv2.imread(input_file, -1)
    #                 filtered_img = self.apply_filter(img)
    #
    #
    #                 cv2.imwrite(output_file, filtered_img)
    #         except Exception as e:
    #             print(f"文件{input_file}可能出问题",e)
    #             continue
    #


