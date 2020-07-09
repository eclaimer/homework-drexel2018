from datetime import datetime
from subprocess import PIPE, Popen

from matplotlib import pyplot as plt

cmd = "git tag"
address = r"D:\nico\.git"
info = Popen(cmd, cwd=address, stdout=PIPE).communicate()
ver = str(info[0]).split('\\n')
ver[0] = "v2.12.1"
ver.pop()

time_list = []
for i in ver:
    cmd = "git log -1  --pretty=format:'%cd' " + i
    data = str(Popen(cmd, cwd=address, stdout=PIPE).communicate()[0])
    date = ''.join(list(data)[3:-2])
    if date == '':
        time_list.append('')
        continue
    else:
        time = str(datetime.strptime(date,
                                     "%a %b %d %H:%M:%S %Y %z")).split()[0]
        time_list.append(time)

plt.figure(figsize=(100, 100))
plt.xlabel('time')
plt.ylabel('verson')
x_ticks = [time_list[i] for i in range(0, len(time_list), 20)]
y_ticks = [ver[i] for i in range(0, len(ver), 20)]
plt.xticks(fontsize=2)
plt.yticks(fontsize=2)
plt.title('relation between version and time')
plt.scatter(time_list, ver)

plt.show()
