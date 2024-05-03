import multiprocessing
import os
import traceback

import cv2
import numpy as np
import cv2


# 数据库查出来的都是字符串需要对应自适应转换
def convert_str_to_number(value):
    try:
        # 首先尝试将字符串转换为整数
        return int(value)
    except ValueError:
        # 如果转换为整数失败，接着尝试转换为浮点数
        try:
            return float(value)
        except ValueError:
            # 如果转换为浮点数也失败，返回原始字符串
            return value
def EXAMPLE(image, alpha=0.5, kernel_size=5, iterations=200):
    alpha = convert_str_to_number(alpha)
    kernel_size = convert_str_to_number(kernel_size)
    iterations = convert_str_to_number(iterations)
    filtered = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    for i in range(int(iterations)):
        filtered = cv2.erode(filtered, None, iterations=1)
        filtered = cv2.dilate(filtered, None, iterations=1)
    return filtered
def REMOVE_WHITE_LINE(input_image_path, thresh_value=200, kernel_size=15, morph_kernel_size=3):
    """
    移除图像中的白线并显示原图与处理后的结果

    参数:
    - input_image_path: str, 输入图像的路径
    - thresh_value: int, 用于阈值化处理的值（默认200）
    - kernel_size: int, 均值滤波核的大小（默认15）
    - morph_kernel_size: int, 形态学操作核的大小（默认3）
    """
    thresh_value = convert_str_to_number(thresh_value)
    kernel_size = convert_str_to_number(kernel_size)
    morph_kernel_size = convert_str_to_number(morph_kernel_size)
    # 转换为灰度图像
    gray_image = cv2.cvtColor(input_image_path, cv2.COLOR_BGR2GRAY)

    # 阈值化处理
    _, threshold = cv2.threshold(gray_image, thresh_value, 255, cv2.THRESH_BINARY)

    # 均值滤波处理
    kernel = (kernel_size, kernel_size)
    filtered_image = cv2.blur(input_image_path, kernel)

    # 创建形态学操作的核
    morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morph_kernel_size, morph_kernel_size))

    # 将白线区域替换为滤波后的像素
    processed_image = input_image_path.copy()
    processed_image[np.where(threshold == 255)] = filtered_image[np.where(threshold == 255)]

    # 形态学开运算处理
    processed_image = cv2.morphologyEx(processed_image, cv2.MORPH_OPEN, morph_kernel, iterations=1)


    # 返回处理后的图像
    return processed_image

def ENHANCED_CONTRAST(image, clip_limit=2.0, tile_grid_size=8, contrast_alpha=0.5):
    """
    使用CLAHE来执行直方图均衡化的增强版。
    ...
    """
    # 确保参数是正确的数值类型
    clip_limit = convert_str_to_number(clip_limit)
    tile_grid_size = convert_str_to_number(tile_grid_size)
    contrast_alpha = convert_str_to_number(contrast_alpha)

    # 创建CLAHE对象
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))

    if image.ndim == 3:  # 如果图像是彩色的
        # 转换图像到YCrCb色彩空间
        ycrcb_img = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb_img)

        # 应用CLAHE到Y（亮度）通道
        y_eq = clahe.apply(y)

        # 融合原始亮度通道和增强的亮度通道
        y_blended = np.clip((1.0 - contrast_alpha) * y.astype('float32') + contrast_alpha * y_eq.astype('float32'), 0,
                            255).astype('uint8')

        # 合并通道
        merged_ycrcb = cv2.merge((y_blended, cr, cb))

        # 转换回BGR色彩空间
        equalized_image = cv2.cvtColor(merged_ycrcb, cv2.COLOR_YCrCb2BGR)
    else:  # 如果图像是灰度的
        # 直接应用CLAHE
        equalized_image = clahe.apply(image)

    return equalized_image
# def ENHANCED_CONTRAST(image, clip_limit=2.0, tile_grid_size=8, apply_on_color=1):
#     """
#     使用CLAHE来执行直方图均衡化的增强版。
#
#     参数:
#     - image: 输入的图像
#     - clip_limit: 对比度的剪辑限制。
#     - tile_grid_size: 定义了网格大小的元组。
#     - apply_on_color: 如果输入是彩色图像，设置此项为1来均衡每个颜色通道。
#
#     返回:
#     - 返回直方图均衡化后的图像。
#     """
#     # 转换参数
#     clip_limit = convert_str_to_number(clip_limit)
#     tile_grid = (convert_str_to_number(tile_grid_size), convert_str_to_number(tile_grid_size))
#
#     # 判断是否应用于颜色通道
#     apply_on_color = True if apply_on_color == 1 else False
#
#     # 创建CLAHE对象
#     clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
#
#     if apply_on_color and len(image.shape) == 3:
#         # 彩色图像，对每个颜色通道分别应用CLAHE
#         channels = cv2.split(image)
#         # 对每个通道应用CLAHE
#         channels = [clahe.apply(channel) for channel in channels]
#         # 重新合成颜色通道
#         equalized_image = cv2.merge(channels)
#     else:
#         # 不是彩色图像，或apply_on_color为False，则将图像转为灰度（如果尚未这样做）
#         if len(image.shape) == 3:
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         # 对灰度图像应用CLAHE
#         equalized_image = clahe.apply(image)
#
#     return equalized_image
# def ENHANCED_CONTRAST(image, clip_limit=2.0, tile_grid_size=8, apply_on_color=1):
#     """
#     使用CLAHE来执行直方图均衡化的增强版。
#
#     如果 apply_on_color 设为 1 并且输入是彩色图，会对 YCrCb 色彩空间的亮度通道（Y通道）应用CLAHE，
#     并将处理后的亮度通道与未处理的色度通道（CrCb通道）合成，返回合成后的彩色图像。
#     如果 apply_on_color 不为 1 或图像为灰度，将直接对图像应用CLAHE。
#
#     参数:
#     - image: 输入的图像
#     - clip_limit: 对比度的剪辑限制。
#     - tile_grid_size: 定义了网格大小。
#     - apply_on_color: 如果输入是彩色图像，并希望均衡每个颜色通道，设置此项为 1。
#
#     返回:
#     - 返回直方图均衡化后的图像。
#     """
#     # 转换参数
#     clip_limit = convert_str_to_number(clip_limit)
#     tile_grid = (convert_str_to_number(tile_grid_size), convert_str_to_number(tile_grid_size))
#
#     # 判断是否是彩色图像且需应用于颜色通道
#     if len(image.shape) == 3 and apply_on_color == 1:
#         # 将彩色图像从BGR转换到YCrCb颜色空间
#         ycrcb_img = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
#         # 分离YCrCb颜色空间的亮度和色度通道
#         y, cr, cb = cv2.split(ycrcb_img)
#
#         # 创建CLAHE对象并对亮度通道应用CLAHE
#         clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
#         y_eq = clahe.apply(y)
#
#         # 重新合成颜色通道
#         ycrcb_eq = cv2.merge((y_eq, cr, cb))
#         # 将图像从YCrCb转换回BGR颜色空间
#         equalized_image = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)
#     else:
#         # 如果不是彩色图像，或apply_on_color为False，则直接对图像应用CLAHE
#         gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
#         clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
#         equalized_image = clahe.apply(gray_img)
#
#     return equalized_image
class AlgorithmExecutor:
    def __init__(self, input_folder, output_folder):
        self.algorithms = {}
        self.algname = ""
        self.input_folder = input_folder
        self.output_folder = output_folder

    def add_algorithm(self, alg_name, **params):
        # 将算法和其参数名和值存储在字典中
        self.algorithms[alg_name] = params
        self.algname = alg_name

    def execute_algorithm(self, alg_name, image):
        # 执行指定的算法
        if alg_name in self.algorithms:
            params = self.algorithms[alg_name]
            # 假设每个算法都是一个可调用的函数
            # 你需要根据你的情况来实现或导入它们
            func = globals().get(alg_name)
            if func is not None:
                return func(image, **params)
            else:
                raise ValueError(f"Function {alg_name} not found in global scope.")
        else:
            raise ValueError(f"Algorithm {alg_name} not found.")

    def process_image(self, file):
        try:
            if file.endswith('.jpg') or file.endswith('.png'):
                input_file = os.path.join(self.input_folder, file)
                file_name, file_ext = os.path.splitext(file)
                joinedPicName = file_name+"%%"+self.algname
                # 遍历并打印字典的值
                for param_value in self.algorithms[self.algname].values():
                    joinedPicName = joinedPicName+"%%"+str(param_value)
                output_file = joinedPicName+file_ext
                print("输出文件名",os.path.join(self.output_folder, output_file))
                if os.path.basename(output_file) in os.listdir(self.output_folder):
                    return

                img = cv2.imread(input_file, -1)
                # Execute the algorithm with the name 'example_algorithm'
                filtered_img = self.execute_algorithm(self.algname, img)
                cv2.imwrite(os.path.join(self.output_folder, output_file), filtered_img)
        except Exception as e:
            traceback.print_exc()
            # 记录到用户异常表
            print(f"该文件执行算法失败 {input_file}: {e}")

    def apply_image_enhancement(self):
        with multiprocessing.Pool(processes=5) as pool:
            pool.map(self.process_image, os.listdir(self.input_folder))
    def test_sth(self):
        for file in os.listdir(self.input_folder):
            self.process_image(file)

