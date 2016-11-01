import os
import glob
import json
from collections import Counter
import collections
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import argparse
import datetime

def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)


parser = argparse.ArgumentParser(description='Midterm Assignment')
parser.add_argument("-t",help="Enter the Topic you had entered", type=str)
args = parser.parse_args()

dt = datetime.datetime.now().strftime("%Y%m%d")

if args.t:
   file_exists(dt+"/")
   html = open(dt+"/result.html", 'w')
   html.write("<html><head><title>This is analysis result page</title></head><body>")
#Q1：
   if os.path.exists(args.t+'/Q1/'):

      sumq1=collections.Counter()
      for file_name in glob.glob(args.t+'/Q1/*.json'):
           with open(file_name) as f:
                  jsn = json.load(f)
                  sumq1.update(jsn)
      sumq1=dict(sumq1)

      for i, key in enumerate(sumq1):#Circulate both index and value(Here is key)
           plt.bar(i, sumq1[key], color="pink", width=0.2)
      plt.xticks(np.arange(len(sumq1))+0.1, sumq1.keys())#Translation
      plt.yticks(list(sumq1.values()))
      plt.xlabel("Topic")
      plt.ylabel("Times")
      plt.title("View_count in Different Languages")
      plt.grid(True)
      plt.savefig(dt+"/barChart.png")
      plt.cla()
      html.write("<div><h3>Question 1:During last month, among Python, Java, C++, C#, which tag gets the most questions?</h3><img src='barChart.png'/><br/><br/>")
   
#Q2:
   if os.path.exists(args.t+'/Q2/'):
      html.write("<h3>Question 2:During last month, Which type of badge do the users get who always mentioned python, show top 10?</h3><table>")
      badgeList=[]
      for file_name in glob.glob(args.t+'/Q2/*.json'):
           with open(file_name) as f:
                  jsn = json.load(f)
                  for txt in jsn:
                      badgeList.append(txt)
      aq2=dict(Counter(badgeList))
      badgeSort=sorted(aq2.items(), key=lambda x: x[1],reverse=True)
      i=1
      for txt in badgeSort[:10]:
           html.write("<tr><td>{0}</td><td>".format(i)+txt[0]+"</td></tr>")
           i=i+1
      html.write("</table><br/><br/>")
#Q3:
   if os.path.exists(args.t+'/Q3/'):
      html.write("<h3>Question 3: In the last year(2015-10-01~2016-10-01), who has the most valuable badge, show top 10?</h3><table>")
      dictMerge={}
      for file_name in glob.glob(args.t+'/Q3/*.json'):
           with open(file_name) as f:
                  jsn = json.load(f)
                  dictMerge=dict(dictMerge,**jsn)
      dsort=sorted(dictMerge.items(), key=lambda x: x[1],reverse=True)
      i=1
      for txt in dsort[:10]:
          html.write("<tr><td>{0}</td><td>".format(i)+txt[0]+"</td></tr>")
          i=i+1
      html.write("</table><br/><br/>")
#Q4:
   if os.path.exists(args.t+'/Q4/'):
      html.write("<h3>Question4:During last month, in the questions users frequently asked, show the top 10 ones which get the most answers</h3><table>")
      dMerge={}
      for file_name in glob.glob(args.t+'/Q4/*.json'):
          with open(file_name) as f:
                  jsn = json.load(f)
                  dMerge=dict(dMerge,**jsn)
      questionSort=sorted(dMerge.items(), key=lambda x: x[1],reverse=True)
      i=1
      for content in questionSort[:10]:
          html.write("<tr><td>{0}</td><td>".format(i)+content[0]+"</td></tr>")
          i=i+1

#Q5:
   if os.path.exists(args.t+'/Q5/'):
      d={"accepted":0,"unaccepted":0}
      for file_name in glob.glob(args.t+'/Q5/*.json'):
          with open(file_name) as f:
                  jsn = json.load(f)
                  d["accepted"]=d["accepted"]+jsn["accepted"]
      d["unaccepted"]=10000-d["accepted"]
      d["accepted"]=d["accepted"]/100
      d["unaccepted"]=d["unaccepted"]/100
      labels=list(d.keys())
      X=list(d.values())
      fig = plt.figure()
      plt.pie(X,labels=labels,autopct='%1.2f%%')
      plt.title("The Porportion of Accepted and Unaccepted Questions")
      plt.savefig(dt+"/PieChart.png")
      plt.cla()
      html.write("</table><br/><br/><h3>Question 5:During last month, what is the proportion between the accpeted_answers and unaccpted-ones</h3>")
      html.write("<img src='PieChart.png'/><br/><br/></div></body></html>")
      print("end")
else:
    print("No Argument Input.")