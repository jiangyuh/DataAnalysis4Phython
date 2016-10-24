
# coding: utf-8

# In[10]:

#!/usr/bin python
import glob
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json
import plotly 
plotly.offline.init_notebook_mode()
import plotly.plotly as py
import pandas as pd
import csv
import argparse

def  dict2csv(dict,file):
    with open(file,'w') as f:
        w=csv.writer(f)
        w.writerow(['state','count'])
        for (key,value) in dict.items():
            lis=[]
            lis.append(key)
            lis.append(value)
            w.writerow(lis)
            
def strtodatetime(datestr,format):     
    return datetime.datetime.strptime(datestr,format)  

def datediff(beginDate,endDate):  
    format="%Y%m%d"; 
    bd=strtodatetime(beginDate,format)  
    ed=strtodatetime(endDate,format)     
    oneday=datetime.timedelta(days=1)  
    count=0
    while bd!=ed: 
        ed=ed-oneday  
        count+=1
    return count 

def datetostr(date):   
    return  str(date)[0:10]  

def getDays(beginDate,endDate):  
    format="%Y%m%d"; 
    bd=strtodatetime(beginDate,format)  
    ed=strtodatetime(endDate,format)  
    oneday=datetime.timedelta(days=1)  
    num=datediff(beginDate,endDate)+1  
    li=[] 
    for i in range(0,num):  
        li.append(datetostr(ed)) 
        ed=ed-oneday  
    return li 

def get_streamdate(beginDate,endDate):
    l=getDays(beginDate,endDate)
    lis=[]
    for line in l:
        line=line.replace("-","")
        lis.append(line)
    
    return lis



def count_retweet(foldname,listt):
    tcount=0
    d={}
    for file_name in glob.glob(foldname +'*.json'):
        with open(file_name) as f:
            for txt in listt:
                date=file_name.split('/')[2].split('-')[0]
                if date==txt:
                    jsn = json.load(f)
                    for (key, value) in jsn.items():
                        tcount=tcount+value
                    d[date]=tcount
    return d   

def count_follower(foldname,listt):
    count=0
    num=0
    d={}
    for file_name in glob.glob(foldname +'*.json'):
        with open(file_name) as f:
            for txt in listt:
                date=file_name.split('/')[2].split('-')[0]
                if date==txt:
                    jsn = json.load(f)
                    for (key, value) in jsn.items():
                        num=num+1
                        count=count+value
                    d[date]=(count/num)
    return d

def get_Toptopic(foldname):
    d={}
    for file_name in glob.glob(foldname +'*.json'):
        with open(file_name) as f:
            jsn = json.load(f)
            for line in jsn:
                key=line[0]
                d[key]=line[1]
    d=sorted(d.items(), key=lambda x: x[1],reverse=True)        
    return d[:10]

def get_Date(dictory):
    lis=[]
    for i in dictory:
        lis.append(i)
    return lis

def get_recordByDate(date,dic):
    l=[]
    for d in date:
        if d in dic:
            l.append(dic[d])
    return l
 
def draw_barchart(dic1,dic2,ym,out,name):
    scores=[]
    names = name
    subjects = get_Date(dic1)
    scores.append(get_recordByDate(subjects,dic1))
    scores.append(get_recordByDate(subjects,dic2))

    bar_width = 0.2
    index = np.arange(len(scores[0]))
    rects1 = plt.bar(index, scores[0], bar_width, color='#0072BC', label=names[0])
    rects2 = plt.bar(index + bar_width, scores[1], bar_width, color='#ED1C24', label=names[1])
    plt.xticks(index + bar_width,subjects)
    plt.ylim(ymax=ym,ymin=0)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=2)
    plt.savefig(out)
    

def uni_state(foldname,listt):
    d={'AL':0,'AK':0,'CA':0,'CO':0,'CT':0,'DE':0,'FL':0,'GA':0,'HI':0,'ID':0,'IL':0,'IN':0,'IA':0,'KS':0,
               'KY':0,'LA':0,'ME':0,'MD':0,'ME':0,'MI':0,'MN':0,'MS':0,'MO':0,'MT':0,'NE':0,'NY':0,'NJ':0,
               'NV':0,'NH':0,'NM':0,'NC':0,'ND':0,'OH':0,'OK':0,'OR':0,'PA':0,'RI':0,'SC':0,'SD':0,'TN':0,'TX':0,
               'UT':0,'VT':0,'VA':0,'WA':0,'WV':0,'WI':0,'WY':0,'AZ':0,'AR':0,'MA':0}
    for file_name in glob.glob(foldname +'*.json'):
        with open(file_name) as f:
            for txt in listt:
                date=file_name.split('/')[2].split('-')[0]
                if date==txt:
                    jsn = json.load(f)
                    for (key, value) in jsn.items():
                        if not value['state']=='':
                            if 'Alabama' in value['state'] or ', AL' in value['state'] :
                                d['AL']=d['AL']+value['recount']
                            if 'Alaska' in value['state'] or ', AK' in value['state']:
                                d['AK']=d['AK']+value['recount']
                            if 'Arizona' in value['state'] or ', AZ' in value['state'] :
                                d['AZ']=d['AZ']+value['recount']
                            if 'Arkansas' in value['state'] or ', AR' in value['state']:
                                d['AR']=d['AR']+value['recount']
                            if 'California' in value['state'] or ',CA' in value['state']:
                                d['CA']=d['CA']+value['recount']
                            if 'Colorado' in value['state'] or ', CO' in value['state']:
                                d['CO']=d['CO']+value['recount']
                            if 'Connecticut' in value['state'] or ', CT' in value['state']:
                                d['CT']=d['CT']+value['recount']
                            if 'Delaware' in value['state'] or ', DE' in value['state']:
                                d['DE']=d['DE']+value['recount']
                            if 'Florida' in value['state'] or ', FL' in value['state']:
                                d['FL']=d['FL']+value['recount']
                            if 'Georgia' in value['state'] or ', GA'in value['state']:
                                d['GA']=d['GA']+value['recount']
                            if 'Hawaii' in value['state'] or ', HI' in value['state']:
                                d['HI']=d['HI']+value['recount']
                            if 'Idaho'  in value['state']or ', ID' in value['state']:
                                d['ID']=d['ID']+value['recount']
                            if 'Illinois' in value['state'] or ', IL' in value['state']:
                                d['IL']=d['IL']+value['recount']
                            if 'Indiana' in value['state'] or ', IN' in value['state']:
                                d['IN']=d['IN']+value['recount']
                            if 'Iowa' in value['state'] or ', IA' in value['state']:
                                d['IA']=d['IA']+value['recount']
                            if 'Kansas' in value['state'] or ', KS' in value['state']:
                                d['KS']=d['KS']+value['recount']
                            if 'Kentucky' in value['state'] or ', KY' in value['state']:
                                d['KY']=d['KY']+value['recount']
                            if 'Louisiana' in value['state'] or ', LA' in value['state']:
                                d['LA']=d['LA']+value['recount']
                            if 'Maine' in value['state']or ', ME' in value['state']:
                                d['ME']=d['ME']+value['recount']
                            if 'Maryland' in value['state'] or ', MD' in value['state']:
                                d['MD']=d['MD']+value['recount']
                            if 'Massachusetts' in value['state'] or ', MA' in value['state']:
                                d['MA']=d['MA']+value['recount']
                            if 'Michigan' in value['state'] or ', MI' in value['state']:
                                d['MI']=d['MI']+value['recount']
                            if 'Minnesota' in value['state'] or ', MN' in value['state']:
                                d['MN']=d['MN']+value['recount']
                            if 'Mississippi' in value['state'] or ', MS' in value['state']:
                                d['MS']=d['MS']+value['recount']
                            if 'Missouri' in value['state'] or ', MO' in value['state']:
                                d['MO']=d['MO']+value['recount']
                            if 'Montana' in value['state'] or ', MT' in value['state']:
                                d['MT']=d['MT']+value['recount']
                            if 'Nebraska' in value['state']  or ', NE' in value['state']:
                                d['NE']=d['NE']+value['recount']
                            if 'Nevada' in value['state'] or ', NV' in value['state']:
                                d['NV']=d['NV']+value['recount']
                            if 'New Hampshire' in value['state'] or ', NH' in value['state']:
                                d['NH']=d['NH']+value['recount']
                            if 'New Jersey' in value['state'] or ', NJ' in value['state']:
                                d['NJ']=d['NJ']+value['recount']
                            if 'New Mexico' in value['state'] or ', NM' in value['state']:
                                d['NM']=d['NM']+value['recount']
                            if 'New York' in value['state'] or ', NY' in value['state']:
                                d['NY']=d['NY']+value['recount']
                            if 'North Carolina' in value['state']  or ', NC' in value['state']:
                                d['NC']=d['NC']+value['recount']
                            if 'North Dakota' in value['state'] or ', ND' in value['state']:
                                d['ND']=d['ND']+value['recount']
                            if 'Ohio' in value['state']  or ', OH' in value['state']:
                                d['OH']=d['OH']+value['recount']
                            if 'Oklahoma' in value['state'] or ', OK' in value['state']:
                                d['OK']=d['OK']+value['recount']
                            if 'Oregon' in value['state'] or ', OR' in value['state']:
                                d['OR']=d['OR']+value['recount']
                            if 'Pennsylvania' in value['state'] or ', PA' in value['state']:
                                d['PA']=d['PA']+value['recount']
                            if 'Rhode Island' in value['state'] or ',RI' in value['state']:
                                d['RI']=d['RI']+value['recount']
                            if 'South Carolina' in value['state'] or ', SC' in value['state']:
                                d['SC']=d['SC']+value['recount']
                            if 'South Dakota' in value['state'] or ', SD' in value['state']:
                                d['SD']=d['SD']+value['recount']        
                            if 'Tennessee' in value['state'] or ', TN' in value['state']:
                                d['TN']=d['TN']+value['recount']
                            if 'Texas' in value['state'] or ', TX' in value['state']:
                                d['TX']=d['TX']+value['recount']
                            if 'Utah' in value['state'] or ', UT' in value['state']:
                                d['UT']=d['UT']+value['recount']
                            if 'Vermont' in value['state'] or ', VT' in value['state']:
                                d['VT']=d['VT']+value['recount']
                            if 'Virginia' in value['state'] or ', VA' in value['state']:
                                d['VA']=d['VA']+value['recount']
                            if 'Washington' in value['state'] or ', WA' in value['state']:
                                d['WA']=d['WA']+value['recount']
                            if 'West Virginia' in value['state'] or ', WV' in value['state']: 
                                d['WV']=d['WV']+value['recount']
                            if 'Wisconsin' in value['state'] or ', WI' in value['state']:
                                d['WI']=d['WI']+value['recount']
                            if 'Wyoming' in value['state'] or ', WY' in value['state']:
                                d['WY']=d['WY']+value['recount']
    return d
        
def gene_mapping(inputfile,outputfile,t):
    df = pd.read_csv(inputfile)

    for col in df.columns:
        df[col] = df[col].astype(str)

    scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]


    data = [ dict(type='choropleth',colorscale = scl,autocolorscale = False,locations = df['state'],
                  z = df['count'].astype(float),locationmode = 'USA-states',marker = dict(line = dict (
                color = 'rgb(255,255,255)',
                width = 2) ),colorbar = dict(title = "Number of Retweet")) ]

    layout = dict(title =t,geo = dict(scope='usa',projection=dict( type='albers usa' ),                                                       showlakes = True,lakecolor = 'rgb(255, 255, 255)'),)
    fig = dict( data=data, layout=layout )
    plotly.offline.plot(fig, filename=outputfile)

    
def get_Record (foldname):
    d={}
    for file_name in glob.glob(foldname +'*.json'):
        with open(file_name) as f:
            jsn = json.load(f)
            dictMerged=dict(d,**jsn)
    d=sorted(dictMerged.items(), key=lambda x: x[1],reverse=True)        
    return d[:5]

#argparse
parser = argparse.ArgumentParser(description='Twitter API Assignment')
parser = argparse.ArgumentParser(description='Twitter API Assignment')
parser.add_argument("-t",help="enter first item you entered in scrpit1", type=str)
parser.add_argument("-c",help="enter second item you entered in scrpit1", type=str)
parser.add_argument("-p",help="enter third item you entered in scrpit1", type=str)
parser.add_argument("-mind",help="enter min date you want to search", type=str)
parser.add_argument("-maxd",help="enter max date you want to search", type=str)
args = parser.parse_args() 
arg0=args.t
arg1=args.c
arg2=args.p
mid=args.mind
mad=args.maxd

# arg0="Trump"
# arg1="Hillary"
# arg2="Pesident"
# mid="20161020"
# mad="20161022"
if args.t and args.c and args.p and args.mind and args.maxd:
    l=get_streamdate(mid,mad)
    namelist=[arg0,arg1]


    print("Q1: Which are retweet more times, the tweets mentioned FIRST ITEM or SECOND ITEM?")
    print("It will show you in q1.png")
    dic1=count_retweet(arg0+'/Q1/',l)
    dic2=count_retweet(arg1+'/Q1/',l)
    draw_barchart(dic1,dic2,3000000,'Analysis/q1.png',namelist)

    print("Q2: Which is more influncial, the tweet mentioned FIRST ITEM or SENCOND ITEM?")
    print("It will show you in q2.png")
    dq1=count_follower(arg0+'/Q2/',l)
    dq2=count_follower(arg1+'/Q2/',l)
    draw_barchart(dq1,dq2,5000000,'Analysis/q2.png',namelist)

    print("Q3: States attention to FIRST ITEM or SECOND ITEM")
    print("It will show you in p1.html and p2.html")

    plotly.tools.set_credentials_file(username='yhj', api_key='qrgljn4zya')
    s1=uni_state(arg0+'/Q3/',l)
    s2=uni_state(arg1+'/Q3/',l)

    dict2csv(s1,"Analysis/test1.csv")
    dict2csv(s2,"Analysis/test2.csv")
    gene_mapping("Analysis/test1.csv","Analysis/p1.html",arg0) 
    gene_mapping("Analysis/test2.csv","Analysis/p2.html",arg1) 

    print("Q4:What are people talking about THIRD TOPIC?")
    print(get_Record(arg2+"/"))
    print("####################################")
    print("Q5: The most popular topic in USA")
    print(get_Toptopic("Trend/"))
else:
    print("every argument should be entered!!!!")


# In[ ]:




# In[ ]:




# In[ ]:



