#!/usr/bin/env python
# -*- coding:utf-8 -*-

import psycopg2
import yaml
from binascii import a2b_hex
from Crypto.Cipher import AES

config_file = '/etc/cloud/mon/server.yml'


def get_server_ip():
    with open(config_file,'r') as f:
        try:
            data = yaml.load(f,Loader=yaml.FullLoader)
            server_ip = data.get('keystone').get('DATABASES').get('default').get('HOST')
            port = data.get('keystone').get('DATABASES').get('default').get('PORT')
            password = data.get('keystone').get('DATABASES').get('default').get('PASSWORD')
            return server_ip, port, password
        except Exception:
            print "获取server_ip,数据库port失败，无法正常连接数据库"


def decrypt(text):
    """
    decrypt pass base the same key
    对称加密之解密，同一个加密随机数
    """
    KEY = '941enj9neshd1wes'
    if not text:
        return ""
    cryptor = AES.new(KEY, AES.MODE_CBC, b'8122ca7d906ad5e1')
    try:
        plain_text = cryptor.decrypt(a2b_hex(text))
    except:
        print 'error'
        return ""
    return plain_text.rstrip('\0')


def create_qga_matinode():
    host, port, password = get_server_ip()
    conn = psycopg2.connect(database="mon_cmdb", user="root", password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("select kwargs from assets_asset where is_delete=False and type = 1")
    conn.commit()
    rows = cursor.fetchall()
    with open('./qga_matinode', 'a') as f:
        f.write('[openstack_computer]\n')
        for i in rows:
            if 'openstack_computer' in i[0].get('service_role'):
                password = decrypt(i[0].get('password'))
                username = i[0].get('username')
                ip = i[0].get('ip')
                root_password = decrypt(i[0].get('root_password'))
                if root_password:
                    qga_data = '{} ansible_ssh_user={} ansible_ssh_pass={} ansible_ssh_port=22 ask_pass=true ' \
                           'ansible_su_pass={}\n'.format(ip, username, password, root_password)
                else:
                    qga_data = '{} ansible_ssh_user={} ansible_ssh_pass={} ansible_ssh_port=22 ask_pass=true ' \
                               'ansible_su_pass=''\n'.format(ip, username, password)
                f.write(qga_data)
        f.write('[openstack_controller]\n')
        for i in rows:
            if 'openstack_controller' in i[0].get('service_role'):
                password = decrypt(i[0].get('password'))
                username = i[0].get('username')
                ip = i[0].get('ip')
                root_password = decrypt(i[0].get('root_password'))
                if root_password:
                    qga_data = '{} ansible_ssh_user={} ansible_ssh_pass={} ansible_ssh_port=22 ask_pass=true ' \
                               'ansible_su_pass={}\n'.format(ip, username, password, root_password)
                else:
                    qga_data = '{} ansible_ssh_user={} ansible_ssh_pass={} ansible_ssh_port=22 ask_pass=true ' \
                               'ansible_su_pass=''\n'.format(ip, username, password)
                f.write(qga_data)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_qga_matinode()

