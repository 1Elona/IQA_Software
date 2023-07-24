import json



def get_data_from_config(algname):
    with open(os.path.join(unify_path()[1],'config.json')) as f:
        data = json.load(f)
        if algname not in data:
            print(     f'{algname} is not in config.json.')
            return False
        return data
# 返回一个(<class 'dict_keys'>,int)

def get_algorithm_params_info(data,algname):
    return data[algname]['param'], len(data[algname]['param'])


def crossjoin(my_dict):
    import itertools

    # my_dict = {'alpha': {'data_1': [1, 2, 3], 'data_2': [5.0, 5.5]}, 'kernel_size': {'data_1': [1, 2, 3]}, 'iterations': {'data_1': [100, 150, 200, 250, 300]}}

    # 获取每个键的值列表
    alpha_values = list(my_dict['alpha'].values())
    kernel_size_values = list(my_dict['kernel_size'].values())
    iterations_values = list(my_dict['iterations'].values())

    # 将 alpha 的所有值合并
    alpha_all_values = list(itertools.chain.from_iterable(alpha_values))

    # 排列组合
    cartesian_product = itertools.product(alpha_all_values, kernel_size_values[0], iterations_values[0])

    # 将排列组合结果存储在列表中
    result_list = []
    for combination in cartesian_product:
        result_dict = {'alpha': combination[0], 'kernel_size': combination[1], 'iterations': combination[2]}
        result_list.append(result_dict)

    return result_list

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

    json_file_path = os.path.join(unify_path()[1],"config.json")

    # 确保目录存在
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    # 将你的 JSON 数据写入文件
    with open(json_file_path, 'w') as f:
        # 使用 indent 参数来格式化 JSON 数据，使其更易于阅读
        json.dump(data, f, indent=4)
import os
import sys
#静态资源（图片等）可以放到_MEIPASS这个应用启动后的临时文件夹，路径用（0），数据库需要放在用户文件夹下。路径用（1）
def unify_path():
    # 判断是开发环境还是打包应用
    if getattr(sys, 'frozen', False):
        # 打包应用
        application_path = sys._MEIPASS

        return os.path.join(application_path, 'Contents/Resources'),os.path.join(os.path.expanduser("~"), "myapp_data")

    else:
        # 开发环境
        application_path = os.path.dirname(os.path.abspath(__file__))
        return application_path

