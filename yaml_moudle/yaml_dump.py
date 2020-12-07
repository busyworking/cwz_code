# -*- coding: utf-8 -*-
import yaml


def main():
    # 写入数据：
    data = {"S_data": {"test1": "hello"}, "Sdata2": {"name": "汉字"}}
    with open("./test.yml", "w") as f:
        yaml.dump(data, f, default_flow_style=False,encoding='utf-8', allow_unicode=True)


if __name__ == '__main__':
    main()