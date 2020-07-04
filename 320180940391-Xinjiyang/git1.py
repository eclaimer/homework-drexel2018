from subprocess import Popen, PIPE, check_output


def gitFileDynamics(repo):
    cmd = ['git', 'log', '--stat', '--oneline', '--follow', 'v4.4..v4.5', 'kernel/sched/core.c', '>', 'result.csv']
    p = Popen(cmd, cwd=repo, stdout=PIPE, shell=True)
    data, res = p.communicate()
    for line in data.decode("utf-8").split("\n"):
       print(line)


gitFileDynamics(r'D:\学习\Python-杨民强\Nico\linux-stable')