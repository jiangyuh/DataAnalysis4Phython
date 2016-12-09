import os
import glob
import json
import matplotlib.pyplot as plt
import matplotlib
import argparse
import datetime
import pandas as pd


# create unexited folder
def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)

#inpur arguements
parser = argparse.ArgumentParser(description='Final Porject')
parser.add_argument("-d",help="Enter the Date for opening hours", type=str,default="*")
parser.add_argument('-l', help='Enter a List of Cities', nargs='+',default=["Restaurants",
            "Shopping","Active Life","Hotels & Travel","Food","Health & Medical","Nightlife"])
args = parser.parse_args()

category_dic={"Others":0}
for category in args.l:
    category_dic[category]=0

total_count=0
item_count=0
for file_name in glob.glob('data/PriceTitle/*/*/*.json'):
    total_count=total_count+1
    with open(file_name) as f:
        jsn = json.load(f)
        for c in category_dic.keys():
            for txt in jsn.values():
                if c in txt:
                    category_dic[c] = category_dic[c] + 1
                    item_count=item_count+1
category_dic["Others"]=total_count-item_count

df = pd.DataFrame.from_dict(category_dic, orient='index')
df.columns = ["Numbers"]
total=df["Numbers"].sum()
df["Percent"]=pd.to_numeric(df["Numbers"]/total)* 100

#datetime
dt = datetime.datetime.now().strftime("%Y%m%d-%H")
# create chart
fig = plt.figure()
fig.set_size_inches(18,18)
plt.style.use('ggplot')
# Create a list of colors (from iWantHue)
colors = ["#E74C3C", "#8E44AD", "#3498DB", "#16A085", "#F1C40F", "#D35400", "#AAB7B8","#5D6D7E"]
matplotlib.rcParams['font.size'] = 24
matplotlib.rcParams['legend.frameon'] = 'False'
# Create a pie chart
plt.pie(
    # using data total)arrests
    df["Percent"],
    # with no shadows
    shadow=False,
    # with colors
    colors=colors,
    # with one slide exploded out
    explode=(0.1,0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05),
    # with the start angle at 90%
    startangle=90,
    # with the percent listed as a fraction
    autopct='%1.0f%%',pctdistance=1.1 )
plt.legend(loc=3, labels=df.index, fontsize=20)
# View the plot drop above
plt.axis('equal')
file_exists("output/"+dt+"/analysis_4/")
plt.savefig("output/"+dt+"/analysis_4/analysis_4.png")

#create dashborad
html = open("output/"+dt+"/analysis_4/analysis_4.html", 'w')
html.write("<html><head><title>Analysis</title></head><body>")
html.write("<div><h3>The Percentage of Categories with Same Price Range</h3><img src='analysis_4.png' width='1000'/><br/><br/>")
html.write("</body></html>")