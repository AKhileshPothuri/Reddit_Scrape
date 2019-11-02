# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:16:57 2019

@author: Akhilesh
"""

import praw
import pandas as pd
import datetime as dt
reddit = praw.Reddit(client_id='4ivP6A1DKxc6qw',client_secret='uyfftUKf6EfmDRdme6D0vSPEchk',user_agent='Scraping')
url=input("Enter url to scrape data")
category=url.split('/')[-3]
sort=str(url.split('/')[-2])
subreddit = reddit.subreddit(category)
if(sort=="top"):
    content_subreddit = subreddit.top(limit=1000)
if(sort=="hot"):
    content_subreddit = subreddit.hot(limit=1000)
if(sort=="new"):
    content_subreddit = subreddit.new(limit=1000)
if(sort=="controversial"):
    content_subreddit = subreddit.controversial(limit=1000)
if(sort=="rising"):
    content_subreddit = subreddit.rising(limit=1000)#for submission in subreddit.top(limit=1000):
 #   print(submission.title, submission.id)
topics_dict = { "id":[],"author":[],"category":[],"summary":[],"title":[], "url":[],"created": []}
for submission in content_subreddit:
    topics_dict["id"].append(submission.id)
    topics_dict["author"].append(submission.author)
    topics_dict["category"].append(submission.subreddit)
    topics_dict["summary"].append(submission.selftext)
    topics_dict["title"].append(submission.title)
    topics_dict["url"].append(submission.url)    
    topics_dict["created"].append(submission.created)
    
    
    #topics_dict["summary"].append(submission.description)
topics_data = pd.DataFrame(topics_dict)

#print(topics_data)
def get_date(created):
    return dt.datetime.fromtimestamp(created)
_timestamp = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp = _timestamp)
topics_data=topics_data.drop(columns="created")
df_tmp = pd.read_csv("Reddit_data.csv",error_bad_lines=False) 
data=topics_data.append(df_tmp,ignore_index=True)
data.to_csv('Reddit_data.csv',index=False) 
print("Data Scrapping Sucessfull")