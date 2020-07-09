# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:53:06 2020

@author: caoji
"""

from subprocess import Popen, PIPE
import unicodedata

class git_log:
    
    def __init__(self,cmd):
        self.cmd = cmd
        self.repo = "D:/linux-stable"
    
    def pro_cess(self):
        data = Popen(self.cmd, cwd=self.repo, stdout=PIPE)
        collect = data.communicate()[0]
        collect = unicodedata.normalize(u'NFKD', collect.decode(encoding="utf-8", errors="ignore"))
        return collect
    
def main():
    cmd = 'git log --stat --oneline --follow v4.4..v4.5 kernel/sched/core.c'
    g = git_log(cmd)
    with open('collect.txt','w') as f:
        f.write(g)

if __name__ == '__main__':
    main()