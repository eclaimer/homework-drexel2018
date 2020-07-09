# -*- coding: utf-8 -*-


__license__ = "GPL V2"
__author__ = "Cao Yuxuan"
__version = '1.0'

import re
import pandas as pd
import numpy as np
import time
import unicodedata
from subprocess import  PIPE, DEVNULL, Popen
import matplotlib.pyplot as plt



def collect(kernels, allversion):  #get the list of times in a kernel
    resultlist = []

    for version in kernels:
        cmd = 'git tag | grep {} | sort -n -k3 -t"."'.format(version)
        p = Popen(cmd, cwd=allversion, stdout=PIPE, shell=True)
        data, res = p.communicate()
        data = data.decode('latin').encode('utf8').decode('utf8').split("\n")
        Timestamp_list = []

        for i in data:
            cmd_1 = 'git log -1 --pretty=format:"%ct" {}'.format(i)
            p = Popen(cmd_1, cwd=allversion, stdout=PIPE, shell=True)
            Timestamp, res = p.communicate()
            Timestamp = int(Timestamp.decode('latin').encode('utf8').decode('utf8'))
            # the shape of time should be time.mktime(time.strptime(Timestamp,'%Y-%m-%d %H:%M:%S'))
            Timestamp_list.append(Timestamp)

        resultlist.append(Timestamp_list)

    print(resultlist)

    return (resultlist)


def makeimg(all_Timestamp_list):  #make the picture and show it
    count = 0
    for i in all_Timestamp_list:
        j = []
        for a in range(len(i)):
            j.append(count)
        count = count + 1
        # plt.scatter(i,j)
        plt.xlim(1.42e+09, 1.49e+09)
        # plt.ylim(0,10)
        plt.xlabel('seconds')
        plt.ylabel('kernel——versions')
        plt.scatter(i, j)
        plt.title ('timestamps')
    plt.show()


allversion = '/Users/tsaoyuxuan/linux-stable'
versions = ['v4.2', 'v4.3', 'v4.4', 'v4.5', 'v4.6', 'v4.7', 'v4.8']
resultlist = collect(versions, allversion)
makeimg(resultlist)

