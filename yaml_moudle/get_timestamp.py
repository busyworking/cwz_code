# -*- coding: utf-8 -*-#
# Author: chenwenzhi
# Date: 2021/3/3
import time, datetime


def gettime():
    timestamp_list = []
    for x in range(24):
        a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % x

        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")

        timeStamp = int(time.mktime(timeArray))
        timestamp_list.append(timeStamp)
        # print(timeStamp)
    print(timestamp_list)


if __name__ == "__main__":
    gettime()