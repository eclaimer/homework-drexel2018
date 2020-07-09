#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description:

1. Purpose:
Plot the different version relasetime picture.

2. Result of function:
a) Function "load_csv_data" return two list without title. One list stores add ampliture and another stores del ampliture.
b) Function "clean_diff" clean the data of the difference of add list and del list. After cleaning, the function return a list which stores the index of cleaned elements.
c) Function "calculate_ampliture" delet the element according to the index list and calculate the fix ampliture.
d) Function "calculate_mean" calculate the mean of the fix ampliture of different versions. 

3. Run method:
Run the command "python3 plot_different_version.py" in shell.

"""

__author__ = "Yiqi Huang"
__copyright__ = "Copyright 2020, Yiqi Huang, China"
__license__ = "GPL V3"
__version__ = "1.0"
__studentid__ = "320180939801"
__email__ = ["huangyq2018@lzu.edu.cn"]
__status__ = "Done"

import subprocess, re
import matplotlib.pyplot as plt

class Plot_Versions_Time():
    """
    This class can get the plot of relasetime of the different versions.
    """
    def __init__(self, repo):
        self.repo = repo
        self.versions = self.get_version()

    def get_version(self):
        """
        Get the version number.
        Return a list which stores the version number.
        
        """
        gittag = subprocess.Popen("git tag", cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        gittag = re.findall('v[0-9].[0-9]', str(gittag.communicate()[0]))
        gitversions = []
        for i in gittag:
            if i not in gitversions:
                gitversions.append(i)
        gitversions.pop(0) #my clone git cannot find the time of the first version 2.6 so i deleted it.
        gitversions.pop()
        return gitversions

    def get_time(self):
        """
        Get the relasetime of each version.
        Return a list which stores the relasetime of each version.

        """
        seconds_times = []
        for i in range(0,len(self.versions)):
            cmd = "git log -1 --pretty=format:\"%ct\" " + self.versions[i]
            git_rev_list = subprocess.Popen(cmd, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            tag_counts = git_rev_list.communicate()[0]
            if i == 0:
                seconds_times.append(int(tag_counts))
            else:
                seconds_times.append((int(tag_counts) - seconds_times[0])//24//3600)
        seconds_times[0] = 0
        return seconds_times

    def draw_time_versions(self):
        """
        Plot the picture with x-axis "days" and y-axis "version".

        """
        plt.scatter(self.get_time(),self.versions)
        plt.title("Version modify days")
        plt.xlabel("days")
        plt.ylabel("version")
        plt.show()


if __name__ == "__main__":
    repo = "/home/huangyiqi/nicho/linux-stable"
    pvt = Plot_Versions_Time(repo)
    pvt.draw_time_versions()

