import pandas as pd

import numpy as np

df_tweets=pd.read_csv('tweets_graph.csv')
df_users=pd.read_csv('users_graph.csv')

df_tweets.replace(0, np.nan, inplace=True)
df_tweets = df_tweets.dropna(subset=['in_reply_to_user_id', 'retweeted_status_id'], how='all')
df_tweets = df_tweets.loc[:, ~df_tweets.columns.str.contains('^Unnamed')]
df_users = df_users.loc[:, ~df_users.columns.str.contains('^Unnamed')]

df_tweets_2=df_tweets[['id','user_id']]

df_tweets_2.rename(columns={'user_id': 'retweeted_user_id'}, inplace=True)
df_tomerge = df_tweets[df_tweets['retweeted_status_id'].notna()]
df_tomerge = df_tomerge[df_tomerge['retweeted_status_id']!=1]
df_tomerge=df_tomerge.set_index('retweeted_status_id')
df_tweets_2=df_tweets_2.set_index('id')
# df_tomerge=df_tweets[~df_tweets['retweeted_status_id']==1]

df_merged_tweets=df_tomerge.merge(df_tweets_2,how='left',left_index=True,right_index=True)

df_merged_tweets.to_csv('finalMerged.csv')
