import os
import glob
import json
import collections
import matplotlib.pyplot as plt
import argparse
import datetime
import pandas as pd

# create unexited folder
def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)

#set argument
parser = argparse.ArgumentParser(description='Final Porject')
parser.add_argument("-d",help="Enter Date to Analysis", type=str,default="*")
args = parser.parse_args()


#datetime
dt = datetime.datetime.now().strftime("%Y%m%d-%H")

ds = []
for file_name in glob.glob('data/topReviewCount/'+args.d+'/*.json'):
           with open(file_name) as f:
                  jsn = json.load(f)
                  ds.append(jsn)

#merge all dict with same key
dd = collections.defaultdict(list)
for d in ds: # you can list as many input dicts as you want here
    for key, value in d.items():
        dd[key].append(value)
dd=dict(dd)
df=pd.DataFrame(dict([ (k, pd.Series(v)) for k,v in dd.items() ]))


all_df=[]
for column in df.columns:
    sub_df=pd.DataFrame(df[column].value_counts().sort_index())
    all_df.append(sub_df)
topreview_df= pd.concat(all_df,axis=1)
topreview_df=topreview_df.T



#create bar chart
fig = plt.figure()
fig.set_size_inches(18,18)
ax = fig.add_subplot(1, 1,1)
topreview_df.plot(kind='bar',alpha=0.6,ax=ax)
ax.set_xticklabels(topreview_df.index,rotation=45, fontsize='12')
ax.set_ylabel('Business Name')
ax.set_ylabel('Count Number')
ax.set_title("The Numbers of Reviews with Different Stars")
file_exists("output/"+dt+"/analysis_1/")
plt.savefig("output/"+dt+"/analysis_1/analysis_1.png")

html = open("output/"+dt+"/analysis_1/analysis_1.html", 'w')
html.write("<html><head><title>Analysis</title></head><body>")
html.write("<div><h3>The Number of Different-Stars Reviews </h3><img src='analysis_1.png' width='1000'/><br/><br/>")
html.write("</body></html>")