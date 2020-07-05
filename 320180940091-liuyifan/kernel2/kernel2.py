from subprocess import Popen, check_output, PIPE
import numpy as np
import matplotlib.pyplot as plt
import re

def gitGetVersion(repo):
    cmd = ['git', 'tag']
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    d = data.decode("utf-8").split("\n")
    ini = d[1][0:4]
    ver = [ini]
    for i in range(1, len(d)):
        s = d[i][0:4]
        if s != ini:
            ver.append(s)
            ini = s
    ver.remove('v2.6')
    ver.remove('v5.8')
    ver.pop()
    return ver


def gitGetDate(repo):
    ver = gitGetVersion(repo)
    time = []
    r = re.compile(r'^Date:   [0-9]+')
    for i in ver:
        cmd_time = ['git', 'show', i]
        p = Popen(cmd_time, cwd=repo, stdout=PIPE)
        data, res = p.communicate()
        da = data.decode("utf-8").split("\n")
        for rec in da:
            if r.match(rec):
                time.append(r.search(rec).group(0)[8::])
    time = time[::2]
    return time


def draw(list1, list2):
    x = list1
    y = list2
    plt.xlabel('The year of version')
    plt.ylabel('The version number')
    plt.plot(x, y)
    plt.savefig(r'E:\个人\学习资料\Nico\res.png')
    plt.show()

if __name__ == '__main__':
    path = r'E:\个人\学习资料\Nico\linux-stable\kernel'
    date = gitGetDate(path)
    version = gitGetVersion(path)
    draw(date,version)


