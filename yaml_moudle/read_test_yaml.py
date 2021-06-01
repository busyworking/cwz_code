# -*- coding: utf-8 -*-#
# Author: chenwenzhi
# Date: 2021/1/14

import yaml
import os

filePath = "/Users/chenwenzhi/PycharmProjects/ms-deploy/group_vars"

yamlPath = os.path.join(filePath, 'proxy_news.yml')
print(yamlPath)

f = open(yamlPath, 'r')
data = f.read()
x = yaml.load(data)
print x

proxy = [{'MON_VIP': '192.168.113.133', 'server': [{'HIGH_AVAILABILITY': True}, {'username': 'root', 'slave': 'master', 'ip': '192.168.113.127', 'password': 'ecwbs@V587', 'port': 22, 'su_password': 'ecwbs@V587'}, {'username': 'root', 'slave': 'backup', 'ip': '192.168.113.127', 'password': 'ecwbs@V587', 'port': 22, 'su_password': 'ecwbs@V587'}]}, {'PROXY_VIP': '192.168.113.133', 'proxy': [{'PROXY_HIGH_AVAILABILITY': True}, {'username': 'root', 'slave': 'master', 'ip': '192.168.113.126', 'password': 'ecwbs@V587', 'port': 22, 'su_password': 'ecwbs@V587'}, {'username': 'root', 'slave': 'backup', 'ip': '192.168.113.127', 'password': 'ecwbs@V587', 'port': 22, 'su_password': 'ecwbs@V587'}]}, {'PROXY_VIP': '192.168.113.133', 'proxy': [{'PROXY_HIGH_AVAILABILITY': True}, {'username': 'root', 'slave': 'master', 'ip': '192.168.113.126', 'password': 'ecwbs@V587', 'port': 22, 'su_password': 'ecwbs@V587'}, {'username': 'root', 'slave': 'backup', 'ip': '192.168.113.127', 'password': 'ecwbs@V587', 'port': 22, 'su_password': 'ecwbs@V587'}]}, {'ENABLE_PERMISSIONS': True}]


f = open('../kvm_monitor_to_csv/config.yml', 'a')
yaml.dump(x,f)

