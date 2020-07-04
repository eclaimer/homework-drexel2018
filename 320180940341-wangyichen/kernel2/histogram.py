#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple program on making histogram.
Educational purpose only, do not use for other purpose please!
"""

__author__ = "WangYichen"
__copyright__ = "Copyright (c) 2020, Study Project in Lanzhou University , China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = "WangYichen"
__email__ = "ychwang2018@lzu.edu.cn"
__status__ = "Experimental"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
 
def draw_bar(labels,quants):
    width = 0.4
    ind = np.linspace(0.5,9.5,4)
    # make a square figure
    fig = plt.figure(1)
    ax  = fig.add_subplot(111)
    # Bar Plot
    ax.bar(ind-width/2,quants,width,color='green')
    # Set the ticks on x-axis
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    # labels
    ax.set_xlabel('Versions')
    ax.set_ylabel('Release time(timestamp)')
    # title
    ax.set_title('linux kernel versions\'release time', bbox={'facecolor':'0.8', 'pad':5})
    plt.grid(True)
    plt.show()
    plt.savefig("bar.jpg")
    plt.close()
 
labels = []
quants = []
fh = open("time.txt","r").read()
output = eval(fh)
for i in output.keys():
    labels.append(i)
    quants.append(output[i])
 
draw_bar(labels,quants)
