import os,re,sys
from subprocess import Popen
from datetime import datetime as dt

class record():
    """commit record"""
    def __init__(self,gitcnt,gittag,base):
        self.gitcnt = gitcnt
        self.gittag = gittag
        self.base = base
        """key arguments:
           gitcnt -- the git command of rev-list
           gittag -- the git command of log
           base -- the base time of the version"""
    def get_cnt(self,gitcnt):
        try:
            git_rev_list = subprocess.Popen(self.gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        except:
            print("accident: ")
        else:
            cnt = 0
            raw_counts = git_rev_list.communicate()[0]
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
            return len(cnt)
    def get_tag_days(self,gittag,base):
        try:
            git_tag_date = subprocess.Popen(self.gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        except:
            print("accident: ")
        else:
            seconds = git_tag_date.communicate()[0]
            hour_second = 3600
            return ((int(seconds)-self.base))//hour_second
 
rev = sys.argv[1]
cumulative = 0
if len(sys.argv) == 4:
    if (sys.argv[3] == "c"):
        cumulative = 1
if not cumulative == 1:
    print("  wrong input!")
    sys.exit(-1)
rev_range = int(sys.argv[2])

print("#sublevel commits %s stable fixes" % rev)
print("lv hour bugs") #tag for R data.frame
rev1 = rev
version = "v4.4"
gitcommand = "git log -1 --pretty=format:'{ver}'".format(ver='version')
base_time = int(os.Popen(gitcommand,"r").read())

for sl in range(1,rev_range+1):
    rev2 = rev + "." + str(sl)
    gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
    gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
    commit_cnt = record.get_cnt(gitcnt)
    if cumulative == 0:
        rev1 = rev2
    if commit_cnt:
        days = record.get_tag_days(gittag,case_time)
        print("%d %d %d" % (sl,days,commit_cnt))
    else:
        break
