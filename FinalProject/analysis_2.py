import os
import glob
import json
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import argparse
import datetime
import pandas as pd

# create unexited folder
def file_exists(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)

#input arguements
parser = argparse.ArgumentParser(description='Final Porject')
parser.add_argument("-d",help="Enter Date you want to search", type=str,default="*")
parser.add_argument("-c",help="Enter Category want to search", type=str,default="*")
args = parser.parse_args()

#datetime
dt = datetime.datetime.now().strftime("%Y%m%d-%H")

total_dic={}
for file_name in glob.glob('data/categoryPrice/'+args.c+'-'+args.c+'/*.json'):
    with open(file_name) as f:
        jsn = json.load(f)
        total_dic=dict(total_dic,**jsn)
df = pd.DataFrame.from_dict(total_dic, orient='index')
df.columns = ["price_range"]
new_df=pd.DataFrame(df["price_range"].value_counts().sort_index())

fig = plt.figure()
fig.set_size_inches(18,18)
ax = fig.add_subplot(1, 1, 1)
new_df.plot(kind='bar',color='pink',alpha=0.6,ax=ax)
ax.set_xticklabels(new_df.index,rotation=45, fontsize='12')
ax.set_xlabel('Price Range')
ax.set_ylabel('Count Number')
ax.set_title("The Numbers of Different Price Range")
ax.legend_.remove()
file_exists("output/"+dt+"/analysis_2/")
plt.savefig("output/"+dt+"/analysis_2/analysis_2.png")

html = open("output/"+dt+"/analysis_2/analysis_2.html", 'w')
html.write("<html><head><title>Analysis</title></head><body>")
html.write("<div><h3>The Number of Different-Stars Reviews </h3><img src='analysis_2.png' width='1000'/><br/><br/>")
html.write("</body></html>")

