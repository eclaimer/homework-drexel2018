# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 09:56:08 2020

@author: yan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

import re, sys,shlex
from subprocess import Popen, DEVNULL, PIPE
from argparse import ArgumentParser
import re
list1=[]
time =[]
class ContentException(BaseException):
    def __str__(self):
        error = 'Please check if the argument is appropriate.'
        return error
    
class GetGitLog:
    def __init__(self):
        # Set the arguments required for the class.
        
        self.basetime = 1452466892
        self.fir =[]   
        
        self.get_log()
        self.get()
    def get_tag_days(self, git_cmd, base):
       try:
           seconds = git_cmd.communicate()[0]
           SecPerHour = 3600
           if seconds == 0:
               raise ContentException
       except ContentException as err:
           print(err)
           sys.exit(2)
       return (int(seconds)-base)//SecPerHour
    def get_co(self, git_cmd):
        try:
            raw_counts = git_cmd.communicate()[0]
            if raw_counts == 0:
               raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(2)
            # if we request something that does not exist -> 0
        else:
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
            #print(str(raw_counts)[:1000])
            return len(cnt)
    
    def get_commit_cnt(self, git_cmd):
        
        #print(str(git_cmd.communicate()[0]).split('\n'))
    
        raw_counts = git_cmd.communicate()[0]
        #print(type(git_cmd.communicate()))
        a = str(raw_counts).split(r'\n')
        a = [a[i][10:32] for i in range(len(a)) if len(a[i])>20 and a[i][9]== '/'] 
        for i in range(len(a)):
            while not a[i][-1].isdigit():
                a[i] = a[i][:-1]
        a = [i for i in a if i[-3]=='-'][1:]
        self.fir =[i[:-10] for i in a if i[1] == '3']       
        self.fir.sort(key=lambda x:tuple(ord(str(v)[0]) for v in re.split('-|\.',x))) 
        #a = [    for i in a for j in i]
        print(self.fir)
        print(len(self.fir))
        #plt.plot(time,fir) 
#        plt.title("development of fixes over sublevel") 
#        plt.ylabel("kernel sublevel stable release") 
#        plt.xlabel("stable fix commits") 
#        plt.savefig("1v4.4.png") 
        
        #print(time_li)
        # if we request something that does not exist -> 0
        #mat = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})",str(raw_counts))
        
        #print (mat)
        
    def get(self):
        for i in range(1,len(self.fir)):
            #print(self.fir[i-1],self.fir[i])
        
            
            gitcnt1 = "git rev-list --pretty=format:\"%ai\" " + self.fir[i-1].strip() + "..." + self.fir[i].strip()
            #print(gitcnt1)
            
            git_rev_list = Popen(gitcnt1, stdout=PIPE, stderr=DEVNULL,shell=True)# grap it
            #print(git_rev_list)
            commit_cnt = self.get_co(git_rev_list)# grap it
            
            gittag = "git log -1 --pretty=format:\"%ct\" " + self.fir[i].strip()
            git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)# grap it
            
            days = self.get_tag_days(git_tag_date, self.basetime) # grap it
            
            #print("%d %d" % (days,commit_cnt))   
            
            
            
            
            
            
            #print(commit_cnt)
            time.append(days)
            list1.append(commit_cnt)
            #print(i)
            
            
            
    def get_log(self):
        # setup and fill in the table
        #print("#sublevel commits %s stable fixes" % self.rev)
        #print("lv hour bugs") #tag for R data.frame
        
        
        # base time of v4.1 and v4.4 as ref base
        # fix this to extract the time of the base commit from git !
        # hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
        # 1452466892
        #
        self.sublevels ,self.release_days,self.commits =[],[],[]
        
        
        
        
        #gitcnt = 'git log -1'
        gitcnt=shlex.split('git for-each-ref --sort=taggerdate --format  \'%(refname) %(taggerdate:short) %(subject)\'')
        #print(gitcnt)
        #print(gitcnt)
        git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL)# grap it
        #print(git_rev_list)
        commit_cnt = self.get_commit_cnt(git_rev_list)# grap it
        #print(commit_cnt)
        #print(commit_cnt)
                
        
        # if get back 0 then its an invalid revision number
        #print(commit_cnt)
        
            
        #print(commit_cnt)
                
                #self.collect.append((sl,days,commit_cnt))# colect them into list
          
    def draw(self):
        print(self.commits)
        self.commits = [self.commits[0]]+[self.commits[i]-self.commits[i-1]  for i in range(1,len(self.commits))]
        #print(self.release_days,self.commits)
        plt.plot(self.release_days,self.commits,c ='red') 
        plt.title("development of fixes over sublevel") 
        plt.ylabel("kernel sublevel stable release") 
        plt.xlabel("stable fix commits") 
        plt.savefig("1v4.4.png") 
        
        
        plt.show()
if __name__ == '__main__':
    getlog = GetGitLog()
    
    #getlog.draw()
    plt.plot(sorted(time),list1) #v3 release number between nearest version tag
    plt.show()
    plt.xlabel('v 3.0 - before v4 version')
    plt.ylabel('the number of commits')
    plt.title('the commits number of v3.0 version ')