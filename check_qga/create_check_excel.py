#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlwt
import os
import datetime
import psycopg2
import yaml

pwd = os.path.dirname(os.path.abspath(__file__))
all_check_value_path = pwd + "/image_check_value/"
all_check_value_file_list = []
config_file = '/etc/cloud/mon/server.yml'


def get_server_ip():
    with open(config_file, 'r') as f:
        try:
            data = yaml.load(f, Loader=yaml.FullLoader)
            server_ip = data.get('keystone').get('DATABASES').get('default').get('HOST')
            port = data.get('keystone').get('DATABASES').get('default').get('PORT')
            password = data.get('keystone').get('DATABASES').get('default').get('PASSWORD')
            return server_ip, port, password
        except Exception as e:
            print "获取server_ip,数据库port失败，无法正常连接数据库"


def get_openstak_name():
    host, port, password = get_server_ip()
    if not host and not port and not password:
        print '获取server_ip,数据库port失败，无法正常连接数据库'
        exit(1)
    conn = psycopg2.connect(database="mon_cmdb", user="root", password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("select name from assets_asset where type=5")
    conn.commit()
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def getFlist(dir_path):
    for root, dirs, files in os.walk(dir_path):
        if files:
            all_check_value_file_list.append(root + '/' + files[0])
    return all_check_value_file_list


def get_all_check_result(path):
    files = getFlist(path)
    with open(files[0], 'r') as f:
        data = f.readlines()
    return data


# 设置表格样式
def set_stlye(name, height, bold=False):
    # 初始化样式
    style = xlwt.XFStyle()
    # 创建字体
    font = xlwt.Font()
    font.bold = bold
    font.colour_index = 4
    font.height = height
    font.name = name
    style.font = font
    return style


# 写入数据
def write_excel():
    f = xlwt.Workbook(encoding = 'utf-8')
    # 创建sheet
    sheet1 = f.add_sheet(u'QGA检查结果', cell_overwrite_ok=True)

    #写入数据
    row0 = [u'云主机ip',  u'云主机主机名', u'云主机uuid',u'云主机运行状态', u'云主机对应镜像名', u'云主机对应镜像uuid',
            u'云主机镜像是否配置qga', u'云主机所在计算节点主机名', u'云主机可监控(为0可监控)', u'不可监控原因']
    data = get_all_check_result(all_check_value_path)

    #设置列宽
    for item in range(len(row0)):
        col_width = sheet1.col(item)  # xlwt中是行和列都是从0开始计算的
        col_width.width = 580 * 20
    # 标题格式
    alignment = xlwt.Alignment()  # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    style = xlwt.XFStyle()  # Create Style
    style.alignment = alignment  # Add Alignment to Style
    font = xlwt.Font()  # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True  # 黑体
    font.height = 320
    style.font = font  # 设定样式
    #内容格式
    default_style = xlwt.XFStyle()  # 格式信息
    font = xlwt.Font()  # 字体基本设置
    font.name = u'微软雅黑'
    font.color = 'black'
    font.height = 220  # 字体大小，220就是11号字体，大概就是11*20得来的吧
    default_style.font = font
    alignment = xlwt.Alignment()  # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
    default_style.alignment = alignment
    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], style)

    # 写入检查数据
    for k, item in enumerate(data, 1):
        item = item.strip().split(' ')
        if ',' in item[0].strip():
            val = item[0].strip() + item[1].strip()
            sheet1.write(k, 0, val, default_style)
            for v in range(1, len(item) - 1):
                sheet1.write(k, v, item[v+1], default_style)
                if 'yes' not in item[7]:
                    sheet1.write(k, 9, u'云主机对应镜像未配置QGA', default_style)
                elif '1' in item[8]:
                    sheet1.write(k, 9, u'错误：Guest agent is not responding', default_style)

        else:
            for v in range(0, len(item)):
                val = item[v].strip()
                sheet1.write(k, v, val, default_style)
                if 'yes' not in item[6]:
                    sheet1.write(k, 9, u'云主机对应镜像未配置QGA', default_style)
                elif '1' in item[8]:
                    sheet1.write(k, 9, u'错误：Guest agent is not responding', default_style)

    f.save('{}/kvm_qga_image_check_report/qga_checkout_report_{}.xls'.format(pwd, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))


if __name__ == '__main__':
    write_excel()

