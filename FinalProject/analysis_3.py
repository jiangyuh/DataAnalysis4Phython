import os
import glob
import json
import matplotlib.pyplot as plt
import argparse
import datetime
import pandas as pd
import seaborn as sns


# create unexited folder
def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)

#set argument
parser = argparse.ArgumentParser(description='Final Porject')
parser.add_argument("-d",help="Enter Date to Analysis", type=str,default="*")
parser.add_argument("-a",help="Enter Day to Analysis", type=str,default="*")
args = parser.parse_args()

#datetime
dt = datetime.datetime.now().strftime("%Y%m%d-%H")


all_df=[]
for file_name in glob.glob('data/TimeRange/'+args.d+'/'+args.a+'/*.json'):
    with open(file_name) as f:
        jsn = json.load(f)
        df=pd.DataFrame(jsn,index=[0])
        all_df.append(df)
time_df = pd.concat(all_df)

time_df["time_Diff"]=pd.to_datetime(time_df['close'])-pd.to_datetime(time_df['open'])
time_df["time_Diff"]=time_df["time_Diff"].apply(lambda x:x.seconds/60./60)
timeDiff_df=pd.DataFrame(time_df["time_Diff"].value_counts().sort_index())
timeDiff_df["time"]=timeDiff_df.index
timeDiff_df=timeDiff_df.round(1)

hour_df=pd.concat([time_df["open"].value_counts(),time_df["close"].value_counts()],axis=1)
hour_df=hour_df.fillna(0)


# create a chart
fig, axes = plt.subplots(nrows=2, ncols=1)
hour_df.plot(alpha=0.6,ax=axes[0])
axes[0].set_ylabel('Number')
axes[1]=sns.stripplot(x="time", y="time_Diff",data=timeDiff_df, jitter=True, split=True)
axes[1].set_xticklabels(labels=timeDiff_df["time"],rotation=45,fontsize=7)
# axes[1].set(xticklabels=[])
axes[1].set_xlabel('Opening Hours Length')
axes[1].set_ylabel('Number')
file_exists("output/"+dt+"/analysis_3/")
plt.savefig("output/"+dt+"/analysis_3/analysis_3.png")

#create dashborad
html = open("output/"+dt+"/analysis_3/analysis_3.html", 'w')
html.write("<html><head><title>Analysis</title></head><body>")
html.write("<div><h3>The Number of Opening Hours</h3><img src='analysis_3.png'  width='1200'/><br/><br/>")
html.write("</body></html>")