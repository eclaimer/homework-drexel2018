from subprocess import Popen,PIPE
from matplotlib import pyplot as plt

ver = "v4.4"

address = r'D:\Data Science Programing\linux-stable'
shell_cmd_tag = 'git tag -l ' + '"' + ver + '.*"' # Command for get tags start with v4.4

ver_time = Popen(shell_cmd_tag, cwd=address, stdout=PIPE)
ver,res = ver_time.communicate()

tags = ver.decode('utf-8').encode('utf8').decode('utf8').split("\n")

X_time = []
for tag in tags:
    shell_cmd_time = 'git log -1 --pretty=format:\"%ct\" ' + tag # Command for get time for a specific tag
    time = str(Popen(shell_cmd_time, cwd=address, stdout=PIPE).communicate())[3:12]
    X_time.append(shell_cmd_time)


# draw scatter plot
plt.title('Time & Tags(release order)')
plt.scatter(X_time,tags, s=6, marker='x')

plt.xlabel('Time')
plt.ylabel('Tags', rotation=360)

plt.show()
