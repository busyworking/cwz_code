# -*- coding: utf-8 -*-#
# Author: chenwenzhi
# Date: 2021/3/3

import requests
import os
import yaml
import datetime
import psycopg2
import time
import sys
import xlwt


pwd = os.path.dirname(os.path.abspath(__file__))


def get_host(vip, port):
    host_info = {}
    conn = psycopg2.connect(database="mon_cmdb", user="root", password="yTgMa8G,", host=vip, port=port)
    cursor = conn.cursor()
    cursor.execute("select kwargs from assets_asset where type = 501 and is_delete='f';")
    conn.commit()
    rows = cursor.fetchall()
    for item in rows:
        host_ip = item[0].get('ip')
        vm_uuid = item[0].get('vm_uuid')
        if vm_uuid and vm_uuid in host_info.values():
            continue
        else:
            host_info.update({vm_uuid: host_ip})
    cursor.close()
    conn.close()
    return host_info


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def get_monitor_data(s_time, e_time, metric_name, vm_uuid, monitor_url, date):
    date_start = date + ' ' + '{}:0:0'.format(s_time)
    date_end = date + ' ' + '{}:0:0'.format(e_time + 1)
    s_timestamp = int(time.mktime(time.strptime(date_start, "%Y-%m-%d %H:%M:%S")))
    e_timestamp = int(time.mktime(time.strptime(date_end, "%Y-%m-%d %H:%M:%S")))
    data = {
        "start_time": s_timestamp,
        "end_time": e_timestamp,
        "counters": metric_name,
        "hostnames": vm_uuid,
        "consol_fun": "AVERAGE",
        "rstep": 3600,
    }
    response = requests.post(monitor_url, json=data)
    data = response.json()
    step = 3
    data_list = [data[i:i + step] for i in range(0, len(data), step)]
    return data_list


def get_config():
    config_file = pwd + '/config.yml'
    try:
        with open(config_file, 'r') as f:
            config = yaml.load(f.read())
            return config
    except:
        print('当前文件加下不存在脚本执行所需要的配置文件，请确认配置文件是否异常！')
        exit(1)


def main():
    print('开始执行脚本，执行前请确保配置文件已修完完毕！')
    config = get_config()
    ip = config.get("config").get('monitor_ip')
    db_port = config.get("config").get('db_port')
    port = int(config.get("config").get('monitor_url_port'))
    date = config.get("config").get('dates').get('date')
    if not date:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    s_time = int(config.get("config").get('dates').get('s_time'))
    e_time = int(config.get("config").get('dates').get('e_time'))
    hosts_black_sheet = config.get("config").get('hosts_black_sheet')
    metric_name = ['cpu.busy/name=cpu,type=vm', 'mem.memused.percent/name=memory,type=vm',
                   'mem.memtotal/name=memory, type=vm']
    host_info = get_host(ip, db_port)
    del_dict = {}
    if host_info and hosts_black_sheet:
        for k, v in host_info.items():
            if v in hosts_black_sheet:
                del_dict.update({k: v})
        for i in del_dict.keys():
            del host_info[i]
    vm_uuid = host_info.keys()
    if not host_info:
        vm_uuid = []
    monitor_url = 'http://{ip}:{port}/api/v1/graph/history'.format(ip=ip, port=port)
    response_data = get_monitor_data(s_time, e_time, metric_name, vm_uuid, monitor_url, date)
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
    files = xlwt.Workbook(encoding='utf-8')
    # 创建sheet
    sheet1 = files.add_sheet(u'{}'.format(date), cell_overwrite_ok=True)

    # 写入数据
    row0 = [u'整点时间', u'虚拟机名称', u'CPU使用率（%）', u'内存使用量（GB)']

    # 设置列宽
    for item in range(len(row0)):
        col_width = sheet1.col(item)  # xlwt中是行和列都是从0开始计算的
        col_width.width = 360 * 20
    # 标题格式
    alignment = xlwt.Alignment()  # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style = xlwt.XFStyle()  # Create Style
    style.alignment = alignment  # Add Alignment to Style
    font = xlwt.Font()  # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True  # 黑体
    font.height = 280
    style.font = font  # 设定样式

    # 内容格式
    default_style = xlwt.XFStyle()  # 格式信息
    font = xlwt.Font()  # 字体基本设置
    font.name = u'微软雅黑'
    font.color = 'black'
    font.height = 240  # 字体大小，220就是11号字体，大概就是11*20得来的吧
    default_style.font = font
    alignment = xlwt.Alignment()  # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
    default_style.alignment = alignment
    len_list = range(0, len(row0))
    # 生成第一行
    for i in len_list:
        sheet1.write(0, i, row0[i], style)

    data_list = []
    f = open(pwd + '/outs/{}.csv'.format(date), "w")
    f.write('整点时间点,虚拟机名称,CPU使用率(%),内存使用量（GB)\n')

    cpu_val = []
    mem_used_percent = []
    mem_used_total = []

    for item in response_data:
        times = range(s_time, e_time + 1)
        vm_name = host_info.get(item[0]['endpoint'])
        for i in item[0]["Values"]:
            if i['value']:
                cpu_val.append(i['value'])
        for j in item[1]["Values"]:
            if j['value']:
                mem_used_percent.append(round(j['value'], 2))
        for k in item[2]["Values"]:
            if k['value']:
                mem_used_total.append(round(k['value']/1024.0/1024.0/1024.0, 2))
        mem_used_gb = map(lambda (a, b): round(a*b*0.01, 2), zip(mem_used_percent, mem_used_total))
        for n in times:
            try:
                cpu = round(cpu_val[times.index(n)], 2)
            except:
                cpu = 'null'

            try:
                mem = round(mem_used_gb[times.index(n)], 2)
            except:
                mem = 'null'

            f.write('{time},  {name},  {cpu},  {mem}\n'.format(time=n, name=vm_name, cpu=cpu, mem=mem))
            data_list.append(n)
            data_list.append(vm_name)
            data_list.append(cpu)
            data_list.append(mem)
        del cpu_val[0:]
        del mem_used_gb[0:]
    counts = 1
    i = 0
    for item in data_list:
        sheet1.write(counts, i, item, default_style)
        i = i + 1
        if i > 3:
            i = 0
            counts = counts+1
    if os.path.exists('{}/outs/{}.xls'.format(pwd, date)):
        os.remove('{}/outs/{}.xls'.format(pwd, date))
    files.save('{}/outs/{}.xls'.format(pwd, date))


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
