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


{"desc": null, "name": "171云", "tags": [], "proxy": "9ba9ff0b-f33e-4033-a444-cb674841e969", "owners": [], "status": "在用", "user_name": "admin", "res_org_id": null, "cloudversion": null, "mcp_cloud_id": null, "mcp_cloud_name": null, "region_relation": [{"cephs": [{"id": "8f05ae1a-ea58-43a5-b15c-f8f12cdf92aa", "name": "ceph集群"}], "assets": [{"id": "1afb361f-1ecb-4d34-9099-43ada6932b45", "name": "control-45"}, {"id": "7e3af7a6-747b-4096-aeca-d3b3bd605e31", "name": "control-46"}, {"id": "684eab27-df2c-4c8d-9a7b-1194a5d63011", "name": "control-44"}], "region": "keystone"}, {"cephs": [{"id": "8f05ae1a-ea58-43a5-b15c-f8f12cdf92aa", "name": "ceph集群"}], "assets": [{"id": "1afb361f-1ecb-4d34-9099-43ada6932b45", "name": "control-45"}, {"id": "7e3af7a6-747b-4096-aeca-d3b3bd605e31", "name": "control-46"}, {"id": "684eab27-df2c-4c8d-9a7b-1194a5d63011", "name": "control-44"}], "region": "RegionKVM"}], "asset_update_type": "不自动扫描", "keystone_password": "wE8Uq8fwwz50DOTeRujMqdhxV2cd59upGLvs34LN", "keystone_project_id": "7dcf93decf9e449e8adb46ab98997d11", "keystone_server_url": "http://192.168.17.171:16191/v3"}

