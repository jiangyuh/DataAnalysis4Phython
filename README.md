###Final Project 
#Yelp Dataset Analysis with Python 

##Synopsis
Yelp is a powerful App in current world. 
This project utilize Yelp Dataset, Yelp API and USA Median Household Income dataset to analysis and Performance Five Questions.

Analysis_1.Show the top5 popular businesses and the number of different stars in all reviews given by multiple users.

Analysis_2.Show in a specific catergory, the number of business with different price range.

Analysis_3.Show the open time, close time and opening hours in a specific day in one week

Analysis_4. Show the percentage of categories with the same price range

Analysis_5.Show the relationship between the income of cities and the number of business the city has.

All results will show in different figures and html files.

##Dataset:
1.yelp_dataset_challenge_academic_dataset

2.Yelp Fusion API

3.median_household_income.csv

##How to use the python files

####Step_1. Collect Data

```bash
$ python collect_data.py 
```

The users can enter the arguments they want to search, the arguments contains

_1. -t: One business category for data to perform Analysis_1 (The default is Restaurants)

_2. -c:One business category for data to perform Analysis_2 (The default is Restaurants)

_3. -d:One day for data to perform Analysis_3 (The default is Friday)
example:

_4. -p:One Price Range for data to perform Analysis_4 (The default is 3)

_5. -l:Some Cities for Analysis_5 (The default are San Francisco, Dallas, Buffalo, Oklahoma City, Orlando")

```bash
$ python collect_data.py -t Restaurants -c Restaurants -d Friday -p 3 -l San Francisco Buffalo Orlando
```
ps. The user could enter one or a few of these arguments

####Step_2. Perform Analysis 

#####Analysis One

The user could enter the date, the category they want to search or enter nothing.

```bash
$ python analysis_1.py 
$ python collect_data.py -d 20161208
```
#####Analysis Two

The user could enter the date, the category they want to search or enter nothing.

```bash
$ python analysis_2.py 
$ python collect_data.py -d 20161208 -c Restaurants
```

#####Analysis Three

The user could enter the date, the category they want to search or enter nothing.

```bash
$ python analysis_3.py 
$ python collect_data.py -d 20161208 -a Friday
```

#####Analysis Four

The user could enter the date, the category they want to search or enter nothing.

```bash
$ python analysis_4.py 
$ python collect_data.py -d 20161208 -l Restaurants Shopping Active Life Hotels & Travel Food Health & Medical Nightlife
```


#####Analysis Five

The user could enter the date, the category they want to search or enter nothing.

```bash
$ python analysis_3.py 
$ python collect_data.py -d 20161208 -l San Francisco Dallas Buffalo Oklahoma City Orlando
```
##Find the result 
The results will store in output/(the date you run the python file)/analysis_N.
In the folder, there will be a png file and html file.
The user can see the result in html file and they can get the figure as well.

