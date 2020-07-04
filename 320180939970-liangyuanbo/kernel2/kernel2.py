from subprocess import Popen, PIPE
import matplotlib.pyplot as plt
import re

def gitGetVersion():
    cmd = ['git', 'tag']
    p = Popen(cmd, cwd=r'linux-next\kernel', stdout=PIPE)
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
    #ver.remove('v5.8')
    ver.pop()
    return ver




def gitGetDate(repo):
    ver = gitGetVersion()
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
    plt.xlabel('date of version')
    plt.ylabel('The number of times this version was submitted in a year')
    plt.plot(x, y)
    plt.savefig('res.png')
    plt.show()
    

if __name__ == '__main__':
    date = gitGetDate(r'linux-next\kernel')
    version = gitGetVersion()
    draw(date,version[1::])


