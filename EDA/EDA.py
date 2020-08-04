import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import re

def rgx(text):
    if (isinstance(text, float)):
        return text
    if (text[0]!='<'):
        return text
    return re.split("<|>",text)[2]


def drawbarplot(x, y, xlabel,ylabel, title,withTypes=False, figsize=(15, 15),nameToSave='none'):
    plt.figure(figsize=figsize)
    if(withTypes):
        color_dict = {'spam': '#FF0000', 'fake': '#FFFF00','real':'#A0CBE2'}
    else:
        color_dict='terrain'
    sns.barplot(x=x, y=y, palette=color_dict, orient='h', order=y)
    for i, v in enumerate(x):
        plt.text(0.8, i, v, color='k', fontsize=15)

    plt.title(title, fontsize=30)
    plt.xlabel(xlabel, fontsize=24)
    plt.ylabel(ylabel, fontsize=24)
    plt.rc('xtick', labelsize=25)
    plt.rc('ytick', labelsize=25)
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=24)
    ax.legend(loc='best', fontsize=25)
    plt.savefig(nameToSave+'.png')
    plt.show()

df=pd.read_csv('full_tweet_data.csv')
df_fake=df[df['type']=='fake']
df_real=df[df['type']=='real']
df_spam=df[df['type']=='spam']

df_grouped=df.groupby('type').size()
df_grouped=df_grouped.sort_values(ascending=False)

drawbarplot(x=df_grouped.values, y=df_grouped.index, xlabel='Number of Tweets', ylabel='Type',title='Number of Tweets Per Account Type',withTypes=True,figsize=(15, 15),nameToSave='num_tweets_type')

df_1=df[['user_id','type']].drop_duplicates()
df_1=df_1.groupby('type').size()
df_1=df_1.sort_values(ascending=False)

drawbarplot(x=df_1.values, y=df_1.index, xlabel='Number of Accounts', ylabel='Type',
           title='Number of Accounts per account type',withTypes=True,
           figsize=(15, 15),nameToSave='num_accounts_type')




listName=['Real','Spam','Fake']
listDF=[df_real,df_spam,df_fake]
for i in range (0,3):
    df=listDF[i]
    name=listName[i]
    df_trends = df[['text', 'retweet_count']]
    df_trends = df_trends[df_trends['retweet_count'] >= 1]

    df_trends['text'] = df_trends['text'].str.lower()
    df_trends = df_trends.drop_duplicates()
    st_words = set(STOPWORDS)
    # enhancing stopword by removing @mentions and shorthands
    st_words.update(['https', 'CO', 'RT', 'Please', 'via', 'amp', 'place', 'new', 'ttot', 'best', 'great', 'top', 'ht',
                     'ysecrettravel', 'ysecrettravel_'])

    wc = WordCloud(height=600, repeat=False, width=1400, max_words=1000, stopwords=st_words, colormap='terrain',
                   background_color='White', mode='RGBA').generate(' '.join(df_trends['text'].dropna().astype(str)))
    plt.figure(figsize=(16, 16))
    plt.imshow(wc)
    plt.title(name+' '+'Tweets Wordcloud',fontsize=30)
    plt.axis('off')
    plt.savefig(name+'_worldcloud.png')
    plt.show()

    df['source'] = df['source'].apply(rgx)
    count = df['source'].value_counts()
    count = count.sort_values()
    count = count.nlargest(5)
    drawbarplot(x=count.values, y=count.index, xlabel='Number of Tweets', ylabel='Source', title='Source Distribution For ' +name+' Tweets',
                figsize=(15, 15),nameToSave=name+'_num_tweets_source')

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['TweetPostedTime_hour']=df['timestamp'].dt.hour

    count =  df['TweetPostedTime_hour'].value_counts()
    count=count.sort_index()
    drawbarplot(x=count.values,y=count.index,xlabel='Number of Tweets',ylabel='Time of the Day',title='Time of the day distribution for '+name,figsize=(15,15),nameToSave=name+'_num_tweets_time')

