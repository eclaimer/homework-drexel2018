'''
This file is to draw the scatter about timestamp vs tags (range: v4.x). X: timestamp, Y:tag
__license__ = "GPL V2"
__author__ = "Xiyuan Chang     Lanzhou University"
__version = '2.0'
__email__='xychang2018@lzu.edu.cn'
'''
from subprocess import Popen, PIPE, check_output,DEVNULL
import matplotlib.pyplot as plt
import re


def get_tags(repo,version):
    for ver in version:
        cmd_tag = 'git tag | grep {} | sort -n -k3 -t"."'.format(version)
        p = Popen(cmd_tag, stdout=PIPE, stderr=DEVNULL, shell=True, cwd=repo)
        data_releases, res = p.communicate()
        releases = [release for release in data_releases.decode("utf-8").split("\n") if release]
    return sorted(releases)

def get_time(repo,version):
    releases=get_tags(repo,version)
    totaltime=[]
    timestamp=[]
    for v in releases:
        cmd=['git','log','-1','--pretty=format:"%ct"',v]
        #cmd='git log -1 --pretty=format:"%ct" {}'.format(v)
        p = Popen(cmd, stdout=PIPE, stderr=DEVNULL, shell=True, cwd=repo)
        data_time,res=p.communicate()
        for times in data_time.decode("utf-8").split("\n"):
            if times =='':
                del times
            else:
                timestamp.append(int(times.replace('"','')))
               
        totaltime.append(timestamp)
    return totaltime

def plat_scatter(totaltime):
    j = 0
    for t in totaltime:
        l = []
        for k in range(len(t)):
            l.append(j)
        j += 1
        plt.scatter(t,l)
    plt.xlim(1.42e+09,1.49e+09)
    plt.xlabel('timestamp')
    plt.ylabel('versions')
    plt.title('tag_vs_time')
    plt.show()


if __name__ == '__main__':
    version=['v4.0','v4.1','v4.2','v4.3','v4.4','v4.5','v4.5','v4.6','v4.7']
    totaltime = get_time("D:/linux kernel/linux",version)
    plat_scatter(totaltime)
     
    
