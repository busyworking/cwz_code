# -*- coding: utf-8 -*-
import yaml


def main():
    # 写入数据：
    data = {'config':{'hosts':['a','b','c'],'dates':{'date':'','s_time':8,'e_time':20}}}
    with open("../kvm_monitor_to_csv/config.yml", "w") as f:
        yaml.dump(data, f, default_flow_style=False,encoding='utf-8', allow_unicode=True)


if __name__ == '__main__':
    main()