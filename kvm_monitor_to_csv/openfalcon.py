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
        host_name = item[0].get('vm_name')
        vm_uuid = item[0].get('vm_uuid')
        if vm_uuid and vm_uuid in host_info.values():
            continue
        else:
            host_info.update({vm_uuid:host_name})
    cursor.close()
    conn.close()
    return host_info


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def get_monitor_data(s_time, e_time, metric_name, vm_uuid, monitor_url, date):
    date_start= date + ' ' + '{}:0:0'.format(s_time)
    date_end = date + ' ' + '{}:0:0'.format(e_time)
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
    hosts = config.get("config").get('hosts')
    metric_name = config.get("config").get('metric_name')
    if not hosts:
        host_info = get_host(ip, db_port)
        hosts = host_info.values()
        vm_uuid = host_info.keys()
    monitor_url = 'http://{ip}:{port}/api/v1/graph/history'.format(ip=ip, port=port)
    response_data = get_monitor_data(s_time, e_time, metric_name, vm_uuid, monitor_url, date)

    f = open(pwd + '/outs/{}'.format(date), "w")
    f.write('整点时间点，虚拟机名称，CPU使用率（%），内存使用量（GB)\n')
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
        mem_used_GB = map(lambda (a, b):round(a*b*0.01, 2),zip(mem_used_percent,mem_used_total))
        for n in times:
            try:
                cpu = cpu_val[times.index(n)]
                mem = mem_used_GB[times.index(n)]
            except:
                cpu = 'null'
                mem = 'null'
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('{}'.format(date))
            style = xlwt.XFStyle()  # 初始化样式

            f.write(u'{time},  {name},  {cpu},  {mem}\n'.format(time=n, name=vm_name,cpu=cpu,mem=mem))
        del cpu_val[0:]
        del mem_used_GB[0:]


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
