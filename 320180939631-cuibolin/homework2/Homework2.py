'''
Author:Bolin Cui
Student ID:320180939631
'''


from subprocess import Popen,PIPE
from matplotlib import pyplot as plt

ver = "v4.4"
repo = r"D:\Git\linux-stable" #  The location of my git warehouse .
cmd_tag = 'git tag -l ' + '"' + ver + '.*"'
ver_time = Popen(cmd_tag, cwd=repo, stdout=PIPE)
ver,res = ver_time.communicate()

y = ver.decode('latin').encode('utf8').decode('utf8').split("\n")

print(y)
x_time = []
for tag in y:
    cmd_time = 'git log -1 --pretty=format:\"%ct\" ' + tag
    time = str(Popen(cmd_time, cwd=address, stdout=PIPE).communicate())[3:12]
    x_time.append(cmd_time)

#  print(1) a small test to show the program can run to here

plt.scatter(x_time,y)
plt.title('Release order with time')
plt.xlabel('x,time')
plt.ylabel('y,release order')
plt.show()
