import os
import json
import requests
import datetime
import argparse


def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)

# define a function to write data in json
def write_in_json(filename, data):
    fp = open(filename, 'w')
    fp.write(json.dumps(data))
    fp.close()


def findcountBytag(dat):
    data = json.loads(dat)
    i = 0
    python = 0
    c = 0
    cpp = 0
    java = 0
    cs = 0
    d = {"python": 0, "c++": 0, "java": 0, "c#": 0, "c":0}
    try:
    #if "items" in data.keys():
        for line in data["items"]:
            if "pyhton" in data["items"][i]["tags"]:
                python = python + 1
            if "c++" in data["items"][i]["tags"]:
                cpp = cpp + 1
            if "java" in data["items"][i]["tags"]:
                java = java + 1
            if "c#" in data["items"][i]["tags"]:
                cs = cs + 1
            if "c" in data["items"][i]["tags"]:
                c = c + 1
            i = i + 1
        d["python"] = python
        d["c++"] = cpp
        d["c#"] = cs
        d["java"] = java
        d["c"] = c
    except:
        print("findcountBytag"+dat)
    return d


def get_user_id(dat):
    data = json.loads(dat)
    lis = []
    i = 0
    try:
    #if "items" in data.keys():
        for line in data["items"]:
            if "user_id" in data["items"][i]["owner"].keys():
                name = data["items"][i]["owner"]["user_id"]
                lis.append(name)
            i = i + 1
    except:
        print("get_user_id"+dat)
    return lis


def getTagtype(dat):
    data = json.loads(dat)
    lis = []
    i = 0
    try:
    #if "items" in data.keys():
        for line in data["items"]:
            name = data["items"][i]["name"]
            lis.append(name)
            i = i + 1
    except:
        print("getTagtype"+dat)
    return lis


def rateBybadge(dat):
    data = json.loads(dat)
    i = 0
    d = {}
    try:
    #if "items" in data.keys():
        for line in data["items"]:
            name = data["items"][i]["display_name"]
            d[name] = data["items"][i]["badge_counts"]["bronze"] * 0.2 + data["items"][i]["badge_counts"][
                                                                             "silver"] * 0.3 + \
                      data["items"][i]["badge_counts"]["gold"] * 0.5
            i = i + 1
    except:
        print("rateBybadge"+dat)
    return d


def fre_view(dat):
    data = json.loads(dat)
    i = 0
    d = {}
    try:
    #if "items" in data.keys():
        for line in data["items"]:
            ques = data["items"][i]["title"]
            d[ques] = data["items"][i]["answer_count"]
            i = i + 1
    except:
        print("fre_view"+dat)
    return d


def acc_Ans(dat):
    data = json.loads(dat)
    i = 0
    d = {"accepted": 0}
    try:
    #if "items" in data.keys():
        for line in data["items"]:
            if data["items"][i]["is_answered"]:
                d["accepted"] = d["accepted"] + 1
            i = i + 1
    except:
        print("acc_Ans"+dat)
    return d


# key = "dMz8TcQs1lHxFbvPo5p8*w(("

dt = datetime.datetime.now().strftime("%Y%m%d")

parser = argparse.ArgumentParser(description='Twitter API Assignment')
parser.add_argument("-t",help="Choose a Topic to enter, java, python, c++,c,c#", type=str)
parser.add_argument("-q1",help="Choose to implment Q1", type=str)
parser.add_argument("-q2",help="Choose to implment Q2", type=str)
parser.add_argument("-q3",help="Choose to implment Q3", type=str)
parser.add_argument("-q4",help="Choose to implment Q4", type=str)
parser.add_argument("-q5",help="Choose to implment Q5", type=str)
args = parser.parse_args()


if args.t=="java" or args.t=="c" or args.t=="c++" or args.t=="c#" or args.t=='python':
#Q1:
    if args.q1:
       for page in range(1, 101):
           q1 = "https://api.stackexchange.com/2.2/questions?page={0}&pagesize=100&fromdate=1472688000&todate=1475280000&order=desc&sort=activity&site=stackoverflow&key=dMz8TcQs1lHxFbvPo5p8*w((".format(page)
           dataq1 = requests.get(q1)
           dq1 = findcountBytag(dataq1.text)
           file_exists(args.t + "/Q1/")
           write_in_json(args.t + "/Q1/" + dt + "-{0}.json".format(page), dq1)


#Q2:
    if args.q2:
       for page in range(1, 101):
           q2 = "https://api.stackexchange.com/2.2/search?page={0}&pagesize=100&fromdate=1472688000&todate=1475280000&order=desc&sort=activity&intitle=python&site=stackoverflow&key=dMz8TcQs1lHxFbvPo5p8*w((".format(page)
           dataq2 = requests.get(q2)
           nameList = get_user_id(dataq2.text)
           for record in nameList:
                q22 = "https://api.stackexchange.com/2.2/users/{0}/badges?page=1&pagesize=100&order=desc&sort=rank&site=stackoverflow&key=dMz8TcQs1lHxFbvPo5p8*w((".format(record)
                dataq22 = requests.get(q22)
                dataq22 = dataq22.text
                dq22 = getTagtype(dataq22)
                file_exists(args.t+ "/Q2/")
                write_in_json(args.t + "/Q2/" + dt + "-{0}.json".format(record), dq22)

#Q3
    if args.q3:
       for page in range(1, 6):
           q3 = "https://api.stackexchange.com/2.2/users?page={0}&pagesize=20&fromdate=1443657600&todate=1475280000&order=desc&sort=reputation&site=stackoverflow&key=dMz8TcQs1lHxFbvPo5p8*w((".format(page)
           dataq3 = requests.get(q3)
           dq3 = rateBybadge(dataq3.text)
           file_exists(args.t + "/Q3/")
           write_in_json(args.t + "/Q3/" + dt + "-{0}.json".format(page), dq3)

# Q4:
    if args.q4:
       for page in range(1, 51):
           q4 = "https://api.stackexchange.com/2.2/tags/python/faq?page={0}&pagesize=50&site=stackoverflow&key=dMz8TcQs1lHxFbvPo5p8*w((".format(page)
           dataq4 = requests.get(q4)
           dataq4 = dataq4.text
           data = json.loads(dataq4)
           qidList = []
           i = 0
           if "items" in data.keys():
               for line in data["items"]:
                  qid = data["items"][i]["question_id"]
                  qidList.append(qid)
                  i = i + 1
           else:
               print("There something wrong during running.")
           for txt in qidList:
                query = "https://api.stackexchange.com/2.2/questions/{0}?page=1&pagesize=50&order=desc&sort=activity&site=stackoverflow&key=dMz8TcQs1lHxFbvPo5p8*w((".format(txt)
                dataq42 = requests.get(query)
                dataq42 = dataq42.text
                dq4 = fre_view(dataq42)
                file_exists(args.t + "/Q4/")
                write_in_json(args.t + "/Q4/" + dt + "-{0}.json".format(txt), dq4)

# Q5:
    if args.q5:
       for page in range(1, 101):
           q5 = "https://api.stackexchange.com/2.2/questions?page={0}&pagesize=100&fromdate=1472688000&todate=1475280000&order=desc&sort=activity&tagged=python&site=stackoverflow&key=dMz8TcQs1lHxFbvPo5p8*w((".format(page)
           dataq5 = requests.get(q5)
           dataq5 = dataq5.text
           dq5 = acc_Ans(dataq5)
           file_exists(args.t + "/Q5/")
           write_in_json(args.t + "/Q5/"+ dt + "-{0}.json".format(page), dq5)

else:
    print("Enter Error!")