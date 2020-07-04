#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple program on finging commits and its time.
Educational purpose only, do not use for other purpose please!
"""

__author__ = "WangYichen"
__copyright__ = "Copyright (c) 2020, Study Project in Lanzhou University , China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = "WangYichen"
__email__ = "ychwang2018@lzu.edu.cn"
__status__ = "Experimental"

import re
import time
import unicodedata
from subprocess import Popen, PIPE

class log():
    """
    the log itself would be a class object
    """
    def __init__(self,verran):
        """
        For each log you need to provide the range in a certain version you need to check
        Key arguments:
        verran -- the range in a certain version
        commit_time -- a dic to store the commits and its time
        commit -- the re to capture every commit
        date -- the re to capture every date
        """
        self.verran = verran
        self.repo = "D:/kernel/linux-stable"
        self.commit_time = {}
        self.bug_timediff = {}
        self.commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
        self.date = re.compile('^Date:\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([1-9]|[1-2]\d|3[0-1]) [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4} (\+|\-)[0-9]{4}$', re.IGNORECASE)

    def get_data(self,verran):
        """
        to get data from a certain range
        """
        cmd = ["git", "log", "-P", "--no-merges", self.verran]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data, res = p.communicate()
        data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
        return data
    
    def time_transfer(self,t):
        """
        change the str into time stamp
        """
        date = time.strptime(t,'%b %d %H:%M:%S %Y %z')
        timeStamp = int(time.mktime(date))
        #print (timeStamp)
        return (timeStamp)

    def get_commit_time(self):
        """
        to get bugs and its related time
        """
        sum1 = 0
        for line in self.get_data(self.verran).split("\n"):
            if(self.commit.match(line)):
                cur_commit = line
            if(self.date.match(line)):
                sum1 += 1
                self.commit_time.update({sum1:self.time_transfer(line[12:])})
        print("There are total ",sum1," commits!", end="\n")
        return self.commit_time

def main():
    verran = input("please input a range of commits you wanna check")
    b = log(str(verran)).get_commit_time()
    with open("output.txt","w") as f:
        f.write(str(b))

if __name__ == "__main__":
    main() 
    
    
