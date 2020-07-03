# -*- coding: utf-8 -*-
__author__ = "Jiang Zhou, 320180940681, CS 212"
__copyright__ = "Copyright (c) 2020, Lanzhou University, China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = "Jiang Zhou"
__email__ = "zhoujiang18@lzu.edu.cn"
__status__ = "Experimental"


from subprocess import Popen, PIPE
import matplotlib.pyplot as plt


class release_versions:
    base = 1113690036  # timestamp of the first version release: v2.6.12
    month_time = 60*60*24*30

    def __init__(self, filename):
        self.filename = filename

    def get_tag(self):
        cmd = ["git", "tag"]
        p = Popen(cmd, cwd = self.filename, stdout = PIPE)
        data, res = p.communicate()
        return data.decode("utf-8").split("\n")

    def get_time(self, tag):
        cmd = ['git', 'log', '--pretty=format:"%ct"', "-1", tag]
        p = Popen(cmd, cwd=self.filename, stdout=PIPE)
        data, res = p.communicate()
        if data == b'':
            return [], []
        time_stamp = []
        this_tag = []
        for seconds in data.decode("utf-8").split("\n"):
            month = round((int(seconds.strip('"')) - release_versions.base) / release_versions.month_time)
            if month not in time_stamp:
                time_stamp.append(month)
                this_tag.append(tag[0:4])
            else:
                pass
        return time_stamp, this_tag

if __name__ == "__main__":
    rv = release_versions("D:/git_repository/linux-stable")
    x = []
    y = []
    for tag in rv.get_tag():
        print(tag)
        time_stamp, this_tag = rv.get_time(tag)
        x += time_stamp
        y += this_tag
    plt.scatter(x, y)
    plt.title("release versions from June 2005")
    plt.xlabel("month")
    plt.ylabel("version")
    plt.show()
    

