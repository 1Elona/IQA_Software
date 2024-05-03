# from util import Database
# # def example_function(a, b, c):
# #     return a * b * c
# #
# from util import Util
# # # 函数名称作为字符串
# # func_name = 'example_function'
# #
# # # 参数字典
# # params = {'a': 2, 'b': 3, 'c': 4}
# #
# # # 动态调用 example_function 并传递参数
# # result = globals()[func_name](**params)
# #
# # print(result)  # 输出: 24
#
#
#
# # print(Database.selectDistinctOriPicName(1))
# print(len(Util.get_data_from_config('EXAMPLE_2')))


def panduan_zhishu(x):
    if x < 2:
        return False
    for i in range(2, x):
        if x % i == 0:
            return False
    return True

for i in range(2, 100):
    if panduan_zhishu(i):
        print(i)
