from subprocess import Popen, PIPE, check_output

def gitFileDynamics(repo):
    cmd = ['git', 'log', '--stat', '--oneline', '--follow', 'v4.4..v4.5', 'kernel/sched/core.c', '>', 'result.csv']
    p = Popen(cmd, cwd=repo, stdout=PIPE, shell=True)
    data, res = p.communicate()
    # print the git output as one blob
    #print(data.decode("utf-8"))
    # ...or print it split into lines
    for line in data.decode("utf-8").split("\n"):
       print(line)

gitFileDynamics(r'E:\个人\学习资料\Nico\linux-stable')