import numpy as np

def split_input_string(str_input):
    '''
    分割输入字符串为每一组数据
    eg: 返回 [['1-3', '1'], ['5-6', '0.3333']]
    :param str_input:
    :return:
    '''
    data_list = []
    for s in str_input.split(","):
        data_list.append(s.split("#"))
    return data_list

def get_groupdata(data):
    '''
    得到每一组数据 注意输入时sep是小数arrange循环第二个参数不需要+1
    :param data:
    :return:
    '''
    result = []

    for x in data:
        if x[1].isdigit():# x[1]是只有数字（整数）
            for i in np.arange(int(x[0].split('-')[0]),int(x[0].split('-')[1])+1,int(x[1])):
                result.append(i)
        else:
            sep_ = round(float(x[1]), 3)
            for i in np.arange(int(x[0].split('-')[0]),int(x[0].split('-')[1]),sep_):
                result.append(round(i,3))
    return result

def create_data_dict(datagroup_num):
    data_dict = {}
    for i in range(1, datagroup_num + 1):
        array_name = f"data_{i}"
        data_dict[array_name] = []
    return data_dict
def handle(str_input):# str_input = "1-3#1,5-6#0.5" 1-3#1

    data_list = split_input_string(str_input)
    #获取用户输入了几组数据
    datagroup_num = len(data_list)
    #初始化字典有datagroup_num个数组
    data_dict = create_data_dict(datagroup_num)
    #赋值
    for i, data in enumerate(data_list):
        array_name = f"data_{i+1}"
        data_dict[array_name] = get_groupdata([data])
    return data_dict

# print(handle("1-3#1,5-6#0.5"))

#遍历每一组数据存入
#用户输入需要保留下一次打开需要显示参数
