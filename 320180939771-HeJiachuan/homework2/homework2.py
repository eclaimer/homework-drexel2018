#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
__author__ = "Jiachuan He - 320180939771"
__copyright__ = "Copyright 2020, Jiachuan_He homework2"
__time__ = "2020-6-1"
__version__ = "1.1.0"
__title__ = "homework2"
__email__ = "hejch2018@lzu.edu.cn"
__status__ = "Production"
"""

from subprocess import Popen, PIPE, DEVNULL
from matplotlib import pyplot as plt


class Kernel2:
    def __init__(self, repo, ver1, ver2):
        self.repo = repo
        self.ver1 = ver1
        # Combine ver1 and ver2 to get the full version number
        for i in range(ver2):
            self.ver = ver1 + '.{}'.format(str(i))
        self.v_list = []
        self.t_list = []

    # Get the versions of tags and save them in v_list
    def get_versions(self):
        git_tag = 'git tag | grep {} | sort -n -k3 -t"."'.format(self.ver)
        popen1 = Popen(git_tag, cwd=self.repo, stdout=PIPE, shell=True)
        all1, res1 = popen1.communicate()
        for line in all1.decode('utf-8').split('\n'):
            self.v_list.append(line)
        return self.v_list

    # Get the timestamps of tags and save them in t_list
    def get_timestamps(self):
        for i in self.v_list:
            git_log = 'git log -1 --pretty=format:"%cd" {}'.format(i)
            popen2 = Popen(git_log, cwd=self.repo, stdout=PIPE, shell=True, stderr=DEVNULL)
            all2, res2 = popen2.communicate()
            for line in all2.decode("utf-8").split("\n"):
                self.t_list.append(int(line))
        return self.t_list

    # Plot it with x-axis is time in some suitable unit and y-axis is release in order
    def draw(self):
        for i in range(len(self.t_list)):
            plt.scatter(self.t_list[i], self.v_list[i])
        plt.title('Kernel2_homework')
        plt.xlabel('Time')
        plt.ylabel('Release in order')
        plt.savefig('Plot_%s.png' % self.ver1)


def run(fp, v1):
    if v1 == 'v3':
        v2 = 19
        Kernel2(fp, v1, v2).draw()
    elif v1 == 'v4':
        v2 = 20
        Kernel2(fp, v1, v2).draw()
    elif v1 == 'v5':
        v2 = 7
        Kernel2(fp, v1, v2).draw()
    else:
        print("Error: Input the version from v3, v4, or v5!")


if __name__ == '__main__':
    filepath = input("Please input the absolute path of linux-stable,\n"
                     "such as 'C:/Users/40485/Documents/linux-stable':\n")
    version = input("Please input the version(v3/v4/v5) you want to get:\n")
    run(filepath, version)
