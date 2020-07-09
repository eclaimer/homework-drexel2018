#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple program on process the original data and present it in a line chart
with the number of horizontal axis as year and vertical axis as number of release.
Educational purpose only, do not use for other purpose please!
"""

__author__ = "TangMotong"
__copyright__ = "Copyright (c) 2020, Study Project in Lanzhou University , China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = "TianMotong"
__email__ = "tianmt18@lzu.edu.cn"
__status__ = "Experimental"


import matplotlib.pyplot as plt
f = open('sample_rawdata.txt')
str = f.read()
dict_str = eval(str)
time = [v for v in dict_str.values()]#Process raw data
fixed = [list(i.split(' ')) for i in time]#Process raw data


dic_count = {}
for i in fixed:
    if i[3] not in dic_count:
        dic_count[i[3]] = 1
    else:
        dic_count[i[3]] += 1

sort_dic = {}#Put the original dictionary in time order into the new dictionary
for j in sorted(dic_count):
    sort_dic[j] = dic_count[j]

x = []#Hold X-axis data
y = []#Hold Y-axis data
for k,v in sort_dic.items():
    x.append(k)
    y.append(v)
plt.ylabel('release time per year')
plt.xlabel('year')
plt.plot(x,y)
plt.show()
f.close()
