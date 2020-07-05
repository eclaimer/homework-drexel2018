# -*- coding: utf-8 -*-

__author__ = "Cai Qiqi"
__sid__ = "320180939530"
__email__ = "caiqq18@lzu.edu.cn"

import re
import pandas as pd
import time
from subprocess import Popen, PIPE, DEVNULL
import unicodedata
import matplotlib.pyplot as plt
import numpy as np

#get the list of times
def get_list(versions, repo): 
    total_time_stamp_list = []
    for version in versions:
        cmd = 'git tag | grep {} | sort -n -k3 -t"."'.format(version)
        p = Popen(cmd, cwd=repo, stdout=PIPE, shell=True)
        data, res = p.communicate()
        data = data.decode('latin').encode('utf8').decode('utf8').split("\n")
        time_stamp_list = []

        for w in data:
            cmd_1 = 'git log -1 --pretty=format:"%ct" {}'.format(w)
            p = Popen(cmd_1, cwd=repo, stdout=PIPE, shell=True)
            time_stamp, res = p.communicate()
            time_stamp = int(time_stamp.decode('latin').encode('utf8').decode('utf8'))
            time_stamp_list.append(time_stamp)
        total_time_stamp_list.append(time_stamp_list)
    print(total_time_stamp_list)
    return (total_time_stamp_list)

#draw pictures
def draw_picture(all_time_stamp_list): 
    count_value = 0
    for i in all_time_stamp_list:
        j = []
        for v in range(len(i)):
            j.append(count_value)
        count_value = count_value + 1
        plt.xlim(1.42e+09, 1.49e+09)
        plt.xlabel('seconds')
        plt.ylabel('patchlevel')
        plt.scatter(i, j)
        plt.title ('Timestamps')
    plt.show()

repo = '/Users/Administrator/linux-stable'
versions = ['v4.1', 'v4.2', 'v4.3', 'v4.4', 'v4.5', 'v4.6', 'v4.7', 'v4.8', 'v4.9']
total_time_stamp_list = get_list(versions, repo)
draw_picture(total_time_stamp_list)
