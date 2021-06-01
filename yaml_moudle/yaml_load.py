# -*- coding: utf-8 -*-
import datetime
#
#
# pdf_dir = '/Users/chenwenzhi/PycharmProjects/myproject/yaml_moudle'
# try:
#     with open(pdf_dir + "/mon_alias_name", 'r') as f:
#         mon_alias_name = f.read().strip()
# except:
#     mon_alias_name = raw_input("首次执行mon自巡检请输入您为该环境起的别名：\n").strip()
#     with open(pdf_dir + "/mon_alias_name", 'w') as f:
#         f.write(mon_alias_name)
#
# pdf_file_name = '{}_mon_check{}.pdf'.format(mon_alias_name, datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M'))
# print pdf_file_name

names = {'Age': 7, 'Name': 'Manni', 'aa': 'cc'}
print names.keys()
for k,v in names.items():
    print k,v

for k in names.values():
    print k