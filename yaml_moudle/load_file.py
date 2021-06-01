# -*- coding: utf-8 -*-#
# Author: chenwenzhi
# Date: 2021/2/3
import os
import yaml

# base_dir = os.path.dirname(os.path.abspath(__file__))
#
#
# def load_config(name, dir=base_dir):
#     config_file = os.path.join(dir, name)
#     if os.path.isdir(config_file):
#         res = []
#         for i in os.listdir(config_file):
#             res += load_config(i, config_file)
#         return res
#     with open(config_file, 'r') as f:
#         config = yaml.load(f)
#     return config



# if __name__ == '__main__':
#     name = "config.yml"
#     load_config(name)

# import pdb
#
# a = "just"
# b = "do"
#
# pdb.set_trace()
#
# c = ['p', 'y', 't', 'h', 'o', 'n']

# 字符串模板中使用key
# temp = '教程是:%(name)s, 价格是:%(price)010.2f, 出版社是:%(publish)s'
# book = {'name':'Python基础教程', 'price': 99, 'publish': 'C语言中文网'}
# # 使用字典为字符串模板中的key传入值
# print(temp % book)
# book = {'name':'C语言小白变怪兽', 'price':159, 'publish': 'C语言中文网'}
# # 使用字典为字符串模板中的key传入值
# print(temp % book)

a = 'hello %(name)s'
tmp = {"name": "zhangsan"}
print a % tmp