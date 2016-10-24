
# coding: utf-8

# #Question 

# In[9]:

#!/usr/bin python

import os
import re
import datetime
import json
import glob
import argparse
import requests
import operator 
import oauth2 as oauth

#define a function to check folder
def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
        
        
#define a function to write data in json 
def write_in_json(filename,data):
    fp=open(filename,'a')
    fp.write(json.dumps(data))
    fp.close()
    

    #Get retweet_count and favorite_count 
def Interest_count(data):
    t=json.loads(data)
    d={}
    i=0
    for txt in t['statuses']:
        myid=t['statuses'][i]['id']
        d[myid]=t['statuses'][i]['retweet_count']
        i=i+1
    return d
        
#Get friend count
def friend_count(data):
    t=json.loads(data)
    d={}
    i=0
    for txt in t['statuses']:
        myid=t['statuses'][i]['id']
        d[myid]=t['statuses'][i]['user']['followers_count']
        i=i+1
    return d

#Get state info
def state_Info(data):
    t=json.loads(data)
    d={}
    i=0
    for txt in t['statuses']:
        myid=t['statuses'][i]['id']
        state=t['statuses'][i]['user']['location']
        recount=t['statuses'][i]['retweet_count']
        d[myid]={"state":state,"recount":recount}
        i=i+1
    return d

#Get Top Topic
def top_topic(data):
    t=json.loads(data)
    i=0
    dc={}
    for txt in t[0]['trends']:
        if not t[0]['trends'][i]['tweet_volume']==None:
            topic=t[0]['trends'][i]['name']
            dc[topic]=t[0]['trends'][i]['tweet_volume']
        i=i+1
    return dc


#Top ten tweet mentioned presidential debate
def top_Tweet(data):
    t=json.loads(data)
    d={}
    i=0
    for txt in t['statuses']:
        textin=t['statuses'][i]['text']
        d[textin]=t['statuses'][i]['retweet_count']
        i=i+1
    return d


# oauth for twitter 
access_token = "3793453276-pEHHfk0P44PmGdqRIIb81aGq34JwOgr3a9WPtha"
access_token_secret = "SKdgl6XLz6jq876vSIGPmS8JntLqxMQweNvrYtKpIdAYt"
consumer_key = "9zYe1wOu7U9daKNJUD9x0feLY"
consumer_secret = "scsDufZCLBMOhU3xRufDTIQpLf3J4TlFvJc6jzOTK6y6nuR0i2"

consumer=oauth.Consumer(key=consumer_key,secret=consumer_secret)
access_token= oauth.Token(key=access_token,secret=access_token_secret)
client= oauth.Client(consumer,access_token)

dt=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

argparse
parser = argparse.ArgumentParser(description='Twitter API Assignment')
parser.add_argument("-t",help="enter first item you want to search", type=str)
parser.add_argument("-c",help="enter second item you want to search", type=str)
parser.add_argument("-p",help="enter third item you want to search", type=str)
args = parser.parse_args() 
arg0=args.t
arg1=args.c
arg2=args.p

#find tweets about Trump and Hillary 
if args.t and args.c:
    searchT="https://api.twitter.com/1.1/search/tweets.json?q=%23"+arg0+"&result_type=recent&count=100"
    response1,data1=client.request(searchT)
    data1=data1.decode('utf-8')
    q1t=Interest_count(data1)
    q2t=friend_count(data1)
    q3t=state_Info(data1)
    file_exists(arg0+'/Q1/')
    write_in_json(arg0+'/Q1/' + dt + ".json",q1t)
    file_exists(arg0+'/Q2/')
    write_in_json(arg0+'/Q2/'+dt+'.json',q2t)
    file_exists(arg0+'/Q3/')
    write_in_json(arg0+'/Q3/'+dt+'.json',q3t)
    file_exists(arg0+'/Raw/')
    write_in_json(arg0+'/Raw/'+dt+'.json',data1)

    searchH="https://api.twitter.com/1.1/search/tweets.json?q=%23"+arg1+"&result_type=recent&count=100"
    response2,data2=client.request(searchH)
    data2=data2.decode('utf-8')
    q1h=Interest_count(data2)
    q2h=friend_count(data2)
    q3h=state_Info(data2)
    file_exists(arg1+'/Q1/')
    write_in_json(arg1+'/Q1/'+dt+'.json',q1h)
    file_exists(arg1+'/Q2/')
    write_in_json(arg1+'/Q2/'+dt+'.json',q2h)
    file_exists(arg1+'/Q3/')
    write_in_json(arg1+'/Q3/'+dt+'.json',q3h)
    file_exists(arg1+'/Raw/')
    write_in_json(arg1+'/Raw/'+dt+'.json',data2)
else:
    print("You must input two search items!")


if args.p:
    #find what are they talkin about PD
    searchPD="https://api.twitter.com/1.1/search/tweets.json?q="+arg2+"&result_type=popular&count=100"
    response3,data3=client.request(searchPD)
    data3=data3.decode('utf-8')
    file_exists(arg2+'/Raw/')
    write_in_json(arg2+'/Raw/'+dt+'.json',data3)
    file_exists(arg2+'/')
    write_in_json(arg2+'/'+dt+'.json',top_Tweet(data3))
else:
    print("There is no search item and the default key word is presidential debate" )
    searchPD="https://api.twitter.com/1.1/search/tweets.json?q=presidential%20debate&result_type=popular&count=100"
    response3,data3=client.request(searchPD)
    data3=data3.decode('utf-8')
    file_exists('President/Raw/')
    write_in_json('President/Raw/'+dt+'.json',data3)
    file_exists('President/')
    write_in_json('President/'+dt+'.json',top_Tweet(data3))


# find the hot topic in USA
# topTopic="https://api.twitter.com/1.1/trends/place.json?id=23424977&count=10"
# responseTopic,dataTopic=client.request(topTopic)
# dataTopic=dataTopic.decode('utf-8')
# dc=top_topic(dataTopic)
# dc=sorted(dc.items(), key=lambda x: x[1],reverse=True)
# file_exists('Trend/Raw/')
# write_in_json('Trend/Raw/'+dt+'.json',dc)
# file_exists('Trend')
# write_in_json('Trend/'+dt+'.json',dc[:10])



# In[ ]:



