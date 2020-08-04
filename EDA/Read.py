import pandas as pd

# df=pd.read_json('cresci-rtbust-2019/cresci-rtbust-2019_tweets.json')
# df=pd.read_csv('datasets_full.csv/extracted_data_BigData/genuine_accounts/tweets.csv')
# print (df)
import numpy as np
import os
users=[]
tweets=[]
for directory,subdirlist,filelist in os.walk('datasets_full.csv/extracted_data_BigData/'):
    if((len(subdirlist)!=0) or ('crowdflower_results' in directory)):
        continue
    actualDir=directory.split('/')[-1]
    for f in filelist:
        group_type=actualDir.split('_')
        if ('spam' in group_type[1]):
            accountType='spam'
        elif ('followers' in group_type[1]):
            accountType='fake'
        else:
            accountType='real'
        if ('tweet' in f):
            print('a')
            df=pd.read_csv((directory+'/'+f),low_memory=False)
            df['type']=accountType

            tweets.append(df)


df_tweets=pd.concat(tweets)
df_tweets.to_csv('full_tweet_data.csv')
