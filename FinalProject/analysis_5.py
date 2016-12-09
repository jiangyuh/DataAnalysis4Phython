import os
import glob
import json
import matplotlib.pyplot as plt
import argparse
import datetime
import pandas as pd


# create unexited folder
def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)


#aet argument
parser = argparse.ArgumentParser(description='Final Porject')
parser.add_argument("-d",help="Enter Date to Analysis", type=str,default="*")
parser.add_argument('-l', help='Enter a List of Cities', nargs='+',default="*")
args = parser.parse_args()

#red household income file
ori_income_df=pd.read_csv("data/median_household_income.csv",encoding = "ISO-8859-1")
new_df=ori_income_df["Metropolitan Statistical Area"].apply(lambda x:x.split("-")[0])
ori_income_df["City"]=new_df
income_df=ori_income_df[["City","Household Income"]]

#datetime
dt = datetime.datetime.now().strftime("%Y%m%d-%H")

#read the number of business
all_df=[]
total_dic={}
clist=args.l

for c in clist:
    for file_name in glob.glob('data/businessCount/' + args.d + '/' + c + '_*.json'):
        with open(file_name) as f:
            jsn = json.load(f)
            df = pd.DataFrame([])
            df["City"] = jsn.keys()
            df["Total_Business"] = jsn.values()
            all_df.append(df)
city_df = pd.concat(all_df)


df=pd.merge(city_df, income_df, how='inner', on=None, left_on=None, right_on=None,
      left_index=False, right_index=False, sort=True, copy=True, indicator=False)
final_df=df.set_index('City')
new_income_df=final_df[["Household Income"]]
new_num_df=final_df[["Total_Business"]]

# create a chart
fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)
new_income_df.plot(ax=axes[0],color='pink', alpha=0.7)
new_num_df.plot(ax=axes[1],color='gold', alpha=0.7)
axes[0].set_ylabel('Household Income(USD/Year)')
axes[1].set_ylabel('Number')
plt.xlabel('City Name')
plt.title("Relationship Between Household Income and Business Count")
file_exists("output/"+dt+"/analysis_5/")
plt.savefig("output/"+dt+"/analysis_5/analysis_5.png")
plt.clf()

#create dashborad
html = open("output/"+dt+"/analysis_5/analysis_5.html", 'w')
html.write("<html><head><title>Analysis</title></head><body>")
html.write("<div><h3>The Relationship Between City Median Income and the Number of Stores</h3><img src='analysis_5.png'/><br/><br/>")
html.write("</body></html>")
