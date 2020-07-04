"""
A simple program hope to process the original data and present it in a line chart
with the number of horizontal axis as year and vertical axis as number of release.
"""

__author__ = "WangZiyao"
__collaborator__ = "WangYichen(He get the raw data)"
__copyright__ = "Copyright (c) 2020, Study Project in Lanzhou University"
__version__ = "1.0"
__email__ = "wangziyao2018@lzu.edu.cn"



import matplotlib.pyplot as plt

def proraw(path):
    #receive the rawdata txt file path and process the raw data,return a list
    f = open(path)
    str = f.read()
    dictstr = eval(str)
    time = [v for v in dictstr.values()]
    fix = [list(i.split(' ')) for i in time]
    return fix


def draw(xy):
    x = []#Hold X-axis data
    y = []#Hold Y-axis data
    for i, j in xy.items():
        x.append(i)
        y.append(j)
    plt.ylabel('release time per year')
    plt.xlabel('year')
    plt.plot(x,y)
    plt.show()
    f.close()

def main():
    processdata = proraw('rawdata.txt')
    diccount = {}
    for i in processdata:
        if i[3] not in diccount:
            diccount[i[3]] = 1
        else:
            diccount[i[3]] += 1

    sortdic = {}#Put the original dictionary in time order into the new dictionary
    for j in sorted(diccount):
        sortdic[j] = diccount[j]
    draw(sortdic)

if __name__ == '__main__':
    main()
