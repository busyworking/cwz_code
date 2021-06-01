# -*- coding: utf-8 -*-#
# Author: chenwenzhi
# Date: 2021/3/18

import os
import subprocess


def get_dic_path(dic):
    file_dic_list = os.listdir(dic)
    if file_dic_list:
        return file_dic_list


def run_cmd(commond_str, check_code=True):
    p = subprocess.Popen(commond_str, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout = p.stdout.read()
    stderr = p.stderr.read()
    p.wait()
    result = ''
    if stdout:
        result = stdout
    if stderr:
        result = stderr
    if check_code:
        code = p.returncode
        return code, result
    else:
        return result


def tar_scp_remove_tar(dic, file_dic_list, des_ip, des_path):
    for i in file_dic_list:
        cmd_tar = 'cd {} & tar -zcf {}{} {}'.format(dic, i, '.tar.gz', i)
        run_cmd(cmd_tar)
        cmd_scp = 'cd {} & scp {}{} {}:{}'.format(dic, i, '.tar.gz', des_ip, des_path)
        print("{}{}---->{}:{}".format(i, ".tar.gz", des_ip, des_path))
        run_cmd(cmd_scp)
        cmd_del_tar = 'cd {} & rm -f {}{}'.format(dic, i, '.tar.gz')
        run_cmd(cmd_del_tar)


if __name__ == "__main__":
    psql_data_file_path = '/home/psql_data/base'
    rrd_data_file_path = '/home/cloud-data/6070'
    des_ip = '192.168.17.29'
    dic_list = [psql_data_file_path, rrd_data_file_path]
    for i in dic_list:
        file_dic_list = get_dic_path(i)
        tar_scp_remove_tar(i, file_dic_list, des_ip, i)