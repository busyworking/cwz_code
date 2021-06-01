# -*- coding: utf-8 -*-#
# Author: chenwenzhi
# Date: 2020/12/20


# def swap(dw):
#     # 下面代码实现dw的a、b两个元素的值交换
#     dw['a'], dw['b'] = dw['b'], dw['a']
#     print("swap函数里，a元素的值是",\
#         dw['a'], "；b元素的值是", dw['b'])
# dw = {'a': 6, 'b': 9}
# swap(dw)
# print("交换结束后，a元素的值是",\
#     dw['a'], "；b元素的值是", dw['b'])

# def foo(*args, **kwargs):
#     print 'args=', args
#     print 'kwargs=', kwargs
#     print '*' * 20
#
#
# if __name__ == '__main__':
#     # 只传参数*args=(1,2,3)
#     foo(1, 2, 3)
#
#     # 只传参数**kwargs=dict(a=1,b=2,c=3)
#     foo(a=1, b=2, c=3)
#
#     # 传入参数*args=(1,2,3)
#     # 传入参数**kwargs=dict(a=1,b=2,c=3)
#     foo(1, 2, 3, a=1, b=2, c=3)
#
#     # 传入参数*args=(1,'b','c')
#     # 传入参数**kwargs=dict(a=1,b='b',c='c')
#     foo(1, 'b', 'c', a=1, b='b', c='c')


# def bar(book, price, desc):
#     print(book, "VIP价格是:", price)
#
#     print('描述信息', desc)
#     return 1, 2, 3
#
#
# my_dict = {'price': 159, 'book': 'hello', 'desc': 'hahah'}
#
# # 按逆向收集的方式将my_dict的多个key-value传给bar()函数
#
# a = bar(**my_dict)
# print type(a)
# from functools import partial
#
#
# def add(a,b):
#     return a+b
#
# pl = partial(add, 99)
# print(pl(99))
# import time
# #全局变量
# Pyname = "Python教程"
# Pyadd = "http://c.biancheng.net/python/"
# def text():
#     """
#     test
#     :return:
#     """
#     #局部变量
#     Shename = "shell教程"
#     Sheadd= "http://c.biancheng.net/shell/"
# print(globals())
# #全局变量
# Pyname = "Python教程"
# Pyadd = "http://c.biancheng.net/python/"
# def text():
#     #局部变量
#     Shename = "shell教程"
#     Sheadd= "http://c.biancheng.net/shell/"
#     print("函数内部的 locals:")
#     print(locals())
# text()
# print("函数外部的 locals:")
# print(locals())
 #全局变量
# Pyname = "Python教程"
# Pyadd = "http://c.biancheng.net/python/"
# class Demo:
#     name = "Python 教程"
#     add = "http://c.biancheng.net/python/"
# print("有 object：")
# print(vars(Demo))
# print("无 object：")
# print(vars())
dic={} #定义一个字
dic['b'] = 3 #在 dic 中加一条元素，key 为 b
print (dic.keys()) #先将 dic 的 key 打印出来，有一个元素 b
exec("a = 4", dic) #在 exec 执行的语句后面跟一个作用域 dic
print(dic.keys()) #exec 后，dic 的 key 多了一个