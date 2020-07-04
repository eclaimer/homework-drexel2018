#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""homework2.py: Scatter plot"""

__author__      = "Xiangwen Qiao(320180940161),class4, Data science, Lanzhou university"
__copyright__   = "Copyright 2020, Project of Data science in python"
__version__ = "0.1"

from subprocess import Popen, PIPE, DEVNULL
import matplotlib.pyplot as plt
import numpy as np;import pandas as pd
import unicodedata;import re
import time

def analyst(kernels, repo):
    Result = []

    for version in kernels:
        cmd = 'git tag | grep {} | sort -n -k3 -t"."'.format(version)
        data, res = Popen(cmd, cwd=repo, stdout=PIPE, shell=True).communicate();data = data.decode('').encode('utf8').decode('utf8').split("\n")
        TimeLine = []

        for v in data:
            cmd_1 = 'git log -1 --pretty=format:"%ct" {}'.format(v)
            Stamp, res = Popen(cmd_1, cwd=repo, stdout=PIPE, shell=1).communicate()
            Stamp = int(Stamp.decode('latin').encode('utf8').decode('utf8'))
            TimeLine.append(Stamp)
        Result.append(TimeLine)

    print(Result)
    return (Result)

def The_Plot(x):
    num = 0
    for i in x:
        j = []
        for a in range(len(i)):
            j.append(num)
        num = num + 1
        plt.xlim(1.42e+09, 1.49e+09)
        plt.title('times_tamps');plt.xlabel('seconds')
        plt.ylabel('The_patch_level');plt.scatter(i, j)
    plt.show()

versions = ['v4.0','v4.1', 'v4.2', 'v4.3', 'v4.4', 'v4.5', 'v4.6', 'v4.7', 'v4.8', 'v4.9']
Result = analyst(versions, '/Users/乔向文/desktop/linux-stable')
The_Plot(Result)