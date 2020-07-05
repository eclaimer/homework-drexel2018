'''
This file is to draw the scatter about timestamp vs tags. X: timestamp, Y:tag
__license__ = "GPL V2"
__author__ = "Xiyuan Chang     Lanzhou University"
__version = '1.0'
__email__='xychang2018@lzu.edu.cn'
'''

from subprocess import Popen, PIPE, check_output,DEVNULL
import matplotlib.pyplot as plt
import re

def get_tags(repo):
    tagl=set()
    """Query 'git tag' in linux-stable, and get releases of [v2.6.1, v2.6.2...]"""
    cmd_tag=['git','tag']
    p = Popen(cmd_tag, stdout=PIPE, stderr=DEVNULL, shell=True, cwd=repo)
    data_releases, res = p.communicate()
    releases = [release for release in data_releases.decode("utf-8").split("\n") if release]
    return sorted(releases)



def get_time(repo):
    releases=get_tags(repo)
    timestamp={}
    for v in releases:
        cmd=['git','log','-1','--pretty=format:"%ct"',v]
        p = Popen(cmd, stdout=PIPE, stderr=DEVNULL, shell=True, cwd=repo)
        data_time,res=p.communicate()
        for times in data_time.decode("utf-8").split("\n"):
            if times =='':
                del times
            else:
                timestamp[v]=int(times.replace('"',''))
    return timestamp

def spli(dic):#split tag v = ['v3.2.1-rc1','v3.2.6','v3.7.1-rc2'] -->[['v3', '2', '1-rc1'], ['v3', '2', '6'], ['v3', '7', '1-rc2']]
	l=[]
	for i in dic:
		k=i.split('-')[0].split('.')
		l.append(k)
	return l


def pro(timestamp):
    rk = timestamp.keys()
    sk = spli(rk)
    val={}
    for key in list(rk):
        if str(key.split('-')[0].split('.')[:2]) not in val.keys():
            tmp=[]
            for j in sk:
                if key.split('-')[0].split('.')[:2] == j[:2]:
                    tmp.append(timestamp['.'.join(j)])
            
                    tmp.append(timestamp['.'.join(j)])
                    val['.'.join(key.split('-')[0].split('.')[:2])] = tmp
    sortval = {}
    for k in sorted(val):
        sortval[k]=val[k]
    return sortval   






def plot_scatter(x_times, sub_versions):
    j = 0
    for x_time in x_times:
        y_version = [sub_versions[j] for i in range(len(x_time))]
        plt.scatter(x_time, y_version)
        j += 1
    plt.xlabel("timestamps")
    plt.ylabel("patch level in linux-stable")
    plt.title("timestamps of all tags for all kernel versions")
    plt.show()



