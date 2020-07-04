#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Jialun Cao"
__studentID__ = "320180939541"
__email__ = "caojl2018@lzu.edu.cn"
__version__ = "v1.0"

from subprocess import PIPE, Popen
import unicodedata
import matplotlib.pyplot as plt

class kernel_homework:
    
    def __init__(self, cmd):
        self.cmd = cmd
        self.repo = "D:/linux-stable"
    
    def pro_cess(self):
        p = Popen(self.cmd, cwd=self.repo, stdout=PIPE)
        name, time = p.communicate()
        name = unicodedata.normalize(u'NFKD', name.decode(encoding="utf-8", errors="ignore"))
        return name
    
    def plot(self, x, y):
        plt.scatter(x, y)
        plt.title("Version modify days")
        plt.xlabel("days")
        plt.ylabel("version")
        plt.show()
        
def main():
    cmd_1 = "git tag"
    test = kernel_homework(cmd_1)   
    test1 = test.pro_cess()
    result_li = [] 
    for i in test1.split("\n"):
        if i:
            result_li.append(i)
    time_li = []
    ver_li = []
    for ver in result_li:
        cmd_2 = "git log -1 {} --pretty=format:\%ct"
        time_collect = kernel_homework(cmd_2.format(ver))
        time_collect = time_collect.pro_cess()
        if time_collect:
            time_li.append(time_collect[1:])
            ver_li.append(ver)
    fig = test.plot(time_li, ver_li)

if __name__ == '__main__':
    main()

