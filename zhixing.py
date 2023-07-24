#
# # 点击执行按钮
#     try:
#         if not query.exec_():
#             print("插入失败")
#             print(query.lastError().text())
#         else:
#             print("插入成功")
#             #这里也需要动态生成字典思路是用zip函数让两个列表一一对应生成字典
#             data = zip(columns,user_param_input_value)
#
#             print("发送给后端的数据：")
#
#             # send POST request
#             response = requests.get('http://httpbin.org/get', params=data)
#
#             # check status code
#             print(response.status_code)
#
#             # print response content
#             print(response.content)
#     except Exception as e:
#         print(e)

# import json
#
# json_data = '''
# {
#     "EXAMPLE": {
#         "param": {
#             "alpha": "(0,1]",
#             "kernel_size": "[3,11]",
#             "iterations": "[100,1000]"
#         }
#     },
#     "Assurance": {
#         "AMBE": "[-100,100]"
#     }
# }
# '''
#
# # 将JSON字符串解析为字典
# data = json.loads(json_data)
#
#
# def is_valid(value, range_str):
#     range_str = range_str.strip()
#     lower_inclusive = range_str.startswith('[')
#     upper_inclusive = range_str.endswith(']')
#
#     # 提取数值范围
#     lower_bound, upper_bound = map(float, range_str.strip('[]()').split(','))
#
#     if lower_inclusive:
#         if value < lower_bound:
#             return False
#     else:
#         if value <= lower_bound:
#             return False
#
#     if upper_inclusive:
#         if value > upper_bound:
#             return False
#     else:
#         if value >= upper_bound:
#             return False
#
#     return True
#
#
# def get_algorithm_params_count(algorithm):
#     return len(data[algorithm]['param'])
#
#
# # 示例
# algorithm = "EXAMPLE"
# params = {"alpha": 0.5, "kernel_size": 5, "iterations": 500}
# for key, value in params.items():
#     print(data[algorithm]['param'][key])
#
# params_valid = all(is_valid(value, data[algorithm]['param'][key]) for key, value in params.items())
#
# print(f"Algorithm '{algorithm}' has {get_algorithm_params_count(algorithm)} parameters.")
# print(f"Parameter values valid: {params_valid}")
#ex 3


