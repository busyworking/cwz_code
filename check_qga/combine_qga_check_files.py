#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

pwd = os.path.dirname(os.path.abspath(__file__))
qga_check_value_path = pwd + "/qga_check_value/"
qga_check_value_file_list = []


def getFlist(dir_path):
    for root, dirs, files in os.walk(dir_path):
        if files:
            qga_check_value_file_list.append(root + '/' + files[0])
    return qga_check_value_file_list


def combine_all_check_result():
    files = getFlist(qga_check_value_path)
    for item in files:
        with open(item, 'r') as f:
            data = f.readlines()
            with open('./all_qga_check_value', 'a') as p:
                for i in data:
                    p.write(i)


if __name__ == "__main__":
    combine_all_check_result()