import typing
from dataclasses import dataclass
import json
from util import Util
def is_image_file(file_name):
    # 定义支持的图片文件扩展名列表
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp','tif'}
    # 获取文件名的扩展名
    extension = os.path.splitext(file_name)[1].lower()
    # 判断扩展名是否在支持的扩展名列表中
    return extension in image_extensions
@dataclass
class AlgorithmParamsInfo:
    params: typing.Any
    length: int


def get_data_from_config(algname):
        # 读取 JSON 配置文件
        with open(Util.unify_path().user_path + '/config/config.json', 'r') as f:
            data = json.load(f)

        # 获取算法列表
        alglist = data.get('alglist', [])

        # 查找并返回指定算法的参数
        for alg in alglist:
            if algname in alg:
                # 找到算法，返回参数信息
                return alg[algname]['param']

        # 如果没有找到算法，返回 None
        return None
# 返回一个(<class 'dict_keys'>,int)
def get_algname_from_config():
    with open(Util.unify_path().user_path + '/config/config.json', 'r') as f:
        data = json.load(f)
        # 初始化算法名的列表
        algorithm_names = []
        # 遍历字典中的 'alglist' 列表
        for alg_dict in data['alglist']:
            # 合并当前字典中的所有键（算法名）
            algorithm_names.extend(alg_dict.keys())
        return algorithm_names


def get_data_from_config(algname):
    # 读取 JSON 配置文件
    with open(Util.unify_path().user_path + '/config/config.json', 'r') as f:
        data = json.load(f)

    # 获取算法列表
    alglist = data.get('alglist', [])

    # 查找并返回指定算法的参数
    for alg in alglist:
        if algname in alg:
            # 找到算法，返回参数信息
            return alg[algname]['param']

    # 如果没有找到算法，返回 None
    return None


# 返回一个(<class 'dict_keys'>,int)
def get_algorithm_params_info(data,algname):
    print("get_algorithm_params_info的data++++++",data)
    length = len(data)
    return AlgorithmParamsInfo(data, length)
    # return data[algname]['param'], len(data[algname]['param'])


def crossjoin(my_dict):
    import itertools
    #     # my_dict = {'alpha': {'data_1': [1, 2, 3], 'data_2': [5.0, 5.5]}, 'kernel_size': {'data_1': [1, 2, 3]}, 'iterations': {'data_1': [100, 150, 200, 250, 300]}}

    keys = list(my_dict.keys())
    values = [list(itertools.chain.from_iterable(list(my_dict[key].values()))) for key in keys]
    print('crossjoin_values',values,sep=' ')
    cartesian_product = itertools.product(*values)

    result_list = []
    for combination in cartesian_product:
        result_dict = {key: value for key, value in zip(keys, combination)}
        result_list.append(result_dict)

    return result_list

# 初始化配置信息 json
def initConfig():
    # 范例
    import os
    # 定义你的 JSON 数据（范例）
    data = {
        "EXAMPLE": {
            "param": {
                "alpha": "(0,1]",
                "kernel_size": "[3,11]",
                "iterations": "[100,1000]"
            }
        },
        "Assurance": {
            "AMBE": "[-100,100]"
        }
    }

    # 指定你的 JSON 文件的路径（数据库和config.json都在该路径下）
    json_file_path = os.path.join(unify_path().user_path,"config.json")

    # 确保目录存在
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    # 将你的 JSON 数据写入文件
    with open(json_file_path, 'w') as f:
        # 使用 indent 参数来格式化 JSON 数据，使其更易于阅读
        json.dump(data, f, indent=4)
import os
import sys
#静态资源（图片等）可以放到_MEIPASS这个应用启动后的临时文件夹，路径用（0），数据库需要放在用户文件夹下。路径用（1）
from dataclasses import dataclass

@dataclass
class PathInfo:
    application_path: str
    user_path: str

def unify_path():
    # 判断是开发环境还是打包应用
    if getattr(sys, 'frozen', False):
        # 打包应用
        application_path = sys._MEIPASS
        user_path = os.path.join(os.path.expanduser("~"), "myapp_data")

    else:
        # 开发环境
        user_path = '/Users/elona/Desktop/pythonProject/IQA_Software2/IQA_Software'
        application_path = user_path

    return PathInfo(application_path, user_path)


