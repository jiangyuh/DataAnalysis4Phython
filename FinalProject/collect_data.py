# coding: utf-8
import os
import glob
import json
import datetime
import requests
import argparse

# This script for collect data for five analysis
# 1. Show the top5 popular restaurant and the number of reviews for each star
# 2. Choose a catergory and show the number of different price range
# 3. Show the opening Time Range by a specific date
# 4.
# 5. Show the relationship between the income of cities and the behavior whether people perfer to eat in restaurants

# function for check if folder exit, if not create

app_id = 'z3sfW5vYMQ96me6IdbHkDA'
app_secret ='KLAqiLPzopFLuviCH45Qoz9INAPSWHjqHJAPiSCiI1YPZ3WYORwdEhQh210zhZ1j'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
token = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = token.json()['access_token']
headers = {'Authorization': 'bearer %s' % access_token}


# write data into json file
def write_in_json(filename, data):
    fp = open(filename, 'w')
    fp.write(json.dumps(data))
    fp.close()


# create unexited folder
def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)


# collect data for Analysis 1
# find review_count by business_id
def TopFive_review(jsn):
    top_reviewdict = {}
    if "review_count" in jsn.keys():
        business_id = jsn['business_id']
        name=jsn["name"]
        top_reviewdict[business_id+"&"+name] = jsn["review_count"]
    return top_reviewdict


def get_ReviewCountByids(jsn,name):
    reviewcount_dict={}
    reviewcount_dict[name]=jsn["stars"]
    return reviewcount_dict


# collect data for Analysis 2
# collect price range with business name:
def category_PriceRange(jsn):
    categoryPrice_dic = {}
    id=jsn["business_id"]
    categoryPrice_dic[id] = jsn['attributes']["Price Range"]
    return categoryPrice_dic

#collect data for analysis 3
#find open and close time
def open_TimeRange(jsn):
    timeRange_dic={}
    business_name =""
    business_name=jsn["business_id"]
    timeRange_dic["open"]=jsn["hours"]["Friday"]["open"]
    timeRange_dic["close"] = jsn["hours"]["Friday"]["close"]
    return  timeRange_dic,business_name


#collect data for analysis 4
def Price_category(jsn):
    priceCategory_dic = {}
    id=jsn["business_id"]
    priceCategory_dic[id] = jsn["categories"]
    return priceCategory_dic

#collect data for analysis 5
# get how many businesses in specific locations

def get_businessCount(data,city):
    businessCount_dic = {}
    jsn=json.loads(data)
    businessCount_dic[city]=jsn["total"]
    return businessCount_dic


dt = datetime.datetime.now().strftime("%Y%m%d")


#inpur arguements
parser = argparse.ArgumentParser(description='Final Porject')
parser.add_argument("-t",help="Enter the Category for Stars Review Count", type=str,default="Restaurants")
parser.add_argument("-c",help="Enter the Category for all price range", type=str,default="Restaurants")
parser.add_argument("-p",help="Enter the Price for all categories", type=int,default=3)
parser.add_argument("-d",help="Enter the Date for opening hours", type=str,default="Friday")
parser.add_argument('-l', help='Enter a List of Cities', nargs='+',default=["San Francisco","Dallas","Buffalo","Oklahoma City","Orlando"])
args = parser.parse_args()


# # read each dict in json file
dictMerge = {}
for eachdic in open("yelp_dataset_challenge_academic_dataset_sample/yelp_academic_dataset_business_sample.json"):
    eachdic = json.loads(eachdic)
    if args.t in eachdic["categories"]:
        top_reviewdata = TopFive_review(eachdic)
        dictMerge = dict(dictMerge, **top_reviewdata)


#find top 5 business ids
dsort = sorted(dictMerge.items(), key=lambda x: x[1], reverse=True)
dsort_five = dsort[:5]
idList=[]
for item in dsort_five:
    idList.append(item[0])

num=1
for id in idList:
    business_id=id.split("&")[0]
    name = id.split("&")[1]
    for file_name in glob.glob('yelp_dataset_challenge_academic_dataset_sample/yelp_academic_dataset_review_sample_*.json'):
        for eachdic in open(file_name):
            eachdic = json.loads(eachdic)
            if business_id in eachdic["business_id"]:
                num = num + 1
                reviewcount_data = get_ReviewCountByids(eachdic, name)
                file_exists("data/topReviewCount/" + dt + "/")
                write_in_json(
                    "data/topReviewCount/" + dt + "/" + business_id + "_" + dt + "_+" + "{0}.json".format(num),
                    reviewcount_data)

#find Price Range by specfic category
num=0
for file_name in glob.glob('yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business_*.json'):
    for eachdic in open(file_name):
        eachdic = json.loads(eachdic)
        for item in eachdic["categories"]:
            if args.c in item:
                if "Price Range" in eachdic['attributes']:
                    categoryPrice_data = category_PriceRange(eachdic)
                    file_exists("data/categoryPrice/" + args.c + "-" + dt + "/")
                    write_in_json("data/categoryPrice/" + args.c + "-" + dt + "/" + dt + "_" + "{0}.json".format(num),
                                  categoryPrice_data)
                    num = num + 1



# # Find time range in specific date

num=0
for file_name in glob.glob('yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business_*.json'):
    for eachdic in open(file_name):
        eachdic = json.loads(eachdic)
        if "hours" in eachdic.keys():
            if args.d in eachdic["hours"].keys():
                timeRange_data = open_TimeRange(eachdic)[0]
                name = open_TimeRange(eachdic)[1]
                num = num + 1
                file_exists("data/TimeRange/" + dt + "/" + args.d + "/")
                write_in_json("data/TimeRange/" + dt + "/" + args.d + "/" + name + "_" + dt + "_{0}.json".format(num),
                              timeRange_data)

# Find the category title by price
num=0
for file_name in glob.glob('yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business_*.json'):
    for eachdic in open(file_name):
        eachdic = json.loads(eachdic)
        if "Price Range" in eachdic['attributes']:
            if args.p == eachdic['attributes']["Price Range"]:
                priceCategory_data = Price_category(eachdic)
                file_exists("data/PriceTitle/" + dt + "/{0}/".format(args.p))
                write_in_json("data/PriceTitle/" + dt + "/{0}/".format(args.p) + dt + "_{0}.json".format(num),
                              priceCategory_data)
                num = num + 1


url="https://api.yelp.com/v3/businesses/search"
List_cities=args.l
for city in List_cities:
    params_city = {'location': city, 'term': 'Restaurant', 'limit': '50' }
    resp_city = requests.get(url=url, params=params_city, headers=headers)
    businessCount_data=get_businessCount(resp_city.text,city)
    file_exists("data/businessCount/" + dt + "/")
    write_in_json("data/businessCount/"+dt+"/"+ city + "_" + dt + ".json", businessCount_data)
