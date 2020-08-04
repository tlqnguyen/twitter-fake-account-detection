import re
import pickle
import pandas as pd
import seaborn as sns
import networkx as nx
from heapq import nlargest
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


### EDA 
# load the pickle files of full_tweet_data
infile = open('/data/full_tweet_data','rb')
df_full = pickle.load(infile)
infile.close()
print("Data full_tweet_data has been loaded")


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


df_fake=df_full[df_full['type']=='fake']
df_real=df_full[df_full['type']=='real']
df_spam=df_full[df_full['type']=='spam']

df_grouped=df_full.groupby('type').size()
df_grouped=df_grouped.sort_values(ascending=False)

drawbarplot(x=df_grouped.values, y=df_grouped.index, xlabel='Number of Tweets', ylabel='Type',title='Number of Tweets Per Account Type',withTypes=True,figsize=(15, 15),nameToSave='num_tweets_type')

df_1=df_full[['user_id','type']].drop_duplicates()
df_1=df_1.groupby('type').size()
df_1=df_1.sort_values(ascending=False)

drawbarplot(x=df_1.values, y=df_1.index, xlabel='Number of Accounts', ylabel='Type',
           title='Number of Accounts per Account Type',withTypes=True,
           figsize=(15, 15),nameToSave='num_accounts_type')



listName=['Real','Spam','Fake']
listDF=[df_real,df_spam,df_fake]

for i in range (0,3):
    df_full=listDF[i]
    name=listName[i]
    df_trends = df_full[['text', 'retweet_count']]
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

    df_full['source'] = df_full['source'].apply(rgx)
    count = df_full['source'].value_counts()
    count = count.sort_values()
    count = count.nlargest(5)
    drawbarplot(x=count.values, y=count.index, xlabel='Number of Tweets', ylabel='Source', title='Source Distribution For ' +name+' Tweets',
                figsize=(15, 15),nameToSave=name+'_num_tweets_source')

    df_full['timestamp'] = pd.to_datetime(df_full['timestamp'])
    df_full['TweetPostedTime_hour']=df_full['timestamp'].dt.hour

    count = df_full['TweetPostedTime_hour'].value_counts()
    count=count.sort_index()
    drawbarplot(x=count.values,y=count.index,xlabel='Number of Tweets',ylabel='Time of the Day',title='Time of the Day Distribution for '+name,figsize=(15,15),nameToSave=name+'_num_tweets_time')


### NETWORK GRAPHS ANALYSIS
df = pd.read_csv('/data/full_user_data.csv')
print("Data full_user_data has been loaded")


# define a color scheme per account type for later graphs and assigned each account to it
color_map = {"spam": "#FF0000", "fake":"#FFFF00", "real":"#A0CBE2"}
df['color'] = [color_map[i] for i in df['Account Type_follows']]


# map all accounts to the color scheme according to their type and create a list of colors for the graphs
act_user_cat = pd.Series(df['Account Type_actual'].values, index=df.name_actual).to_dict()
foll_user_cat = pd.Series(df['Account Type_follows'].values, index=df.name_follows).to_dict()
all_user_cat = {**act_user_cat, **foll_user_cat}


colors=[]
for u in all_user_cat.keys():
    colors.append(color_map[all_user_cat[u]])


# who follows whom?
# create a network graph using draw_networkx function and the nodes being colored to their account's type
graph = nx.from_pandas_edgelist(df, source = 'name_actual', target = 'name_follows', create_using = nx.DiGraph())
plt.figure(figsize=(20,20))
pos = nx.spring_layout(graph,k=0.20,iterations=20)
nx.draw_networkx(graph, pos, arrows=True, node_color=colors, width=4, with_labels=False)
plt.axis('off')
plt.savefig('plot_01.png')
plt.show()
print("Plot 01 - Twitter Network Graph, has been saved in the container")


# who follows whom? Part2
# create a network graph using draw function (more basic than draw_networkx) and the nodes being colored to their account's type
plt.figure(figsize=(15,15))
nx.draw(graph, with_labels=False, node_color=colors)
plt.savefig('plot_02.png')
plt.show()
print("Plot 02 - Twitter Network Graph #2, has been saved in the container")


# is there some correlation between account type and betweennness centrality measure?
# create a list of betweenness measure for each node and set the node size to that measure
rt_centrality = nx.betweenness_centrality(graph, seed=42)
node_size = [v * 1000000000 for v in rt_centrality.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(graph, with_labels=False, node_color=colors, node_size=node_size)
plt.axis('off')
plt.savefig('plot_03.png')
plt.show()
print("Plot 03 - Network Graph with Betweenness as node size, has been saved in the container")


# is there a relationship between betweenness centrality and out degree centrality?
# replace the account type coloring by the account's out degree centrality measure (the higher the measure the more yellow the node)
rt_centrality = nx.betweenness_centrality(graph, seed=42)
node_size = [200.0000000 * graph.out_degree(v) for v in graph]
node_color = [v * 1000000000.000000 for v in rt_centrality.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(graph, with_labels=False, node_color=node_color, node_size=node_size)
plt.title("Betweenness Centrality as Color Scheme and Out-Degree as Node Size", fontsize=35)
plt.axis('off')
plt.savefig('plot_04.png')
plt.show()
print("Plot 04 - Betweenness Centrality as Color Scheme and Out-Degree as Node Size, has been saved in the container")



# does swapping the coloring and sizing basis make a difference?
# set the in degree centrality as the node size and the betweenness as the color scheme
rt_centrality = nx.betweenness_centrality(graph, seed=42)
node_size = [200.0000000 * graph.in_degree(v) for v in graph]
node_color = [v * 1000000000000000 for v in rt_centrality.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(graph, with_labels=False, node_color=node_color, node_size=node_size)
plt.axis('off')
plt.title("Betweenness Centrality as Color Scheme and In-Degree as Node Size", fontsize=35)
plt.savefig('plot_05.png')
plt.show()
print("Plot 05, Betweenness Centrality as Color Scheme and In-Degree as Node Size, has been saved in the container")


# IN-DEGREE CENTRALITY
# check on the top 5 accounts with the highest in degree centrality scores
dic = nx.in_degree_centrality(graph)
FiveHighest = nlargest(5, dic, key = dic.get) 

# save the name of one of the top 5 accounts to a variable for further investigation
most_retweeting = nlargest(5, dic, key=dic.get)[0]

# filter the dataset on that account chosen
df_mr1 = df[(df['name_follows']==most_retweeting)]

# create a new color assignment for the filtered dataset
all_user_cat_mr1 = {**pd.Series(df_mr1['Account Type_actual'].values, index=df_mr1.name_actual).to_dict(), **pd.Series(df_mr1['Account Type_follows'].values, index=df_mr1.name_follows).to_dict()}

colors_mr1=[]
for u in all_user_cat_mr1.keys():
    colors_mr1.append(color_map[all_user_cat_mr1[u]])


# what kind of accounts is this account retweeting from?
# map all accounts that chosen account has retweeted from with the color scheme according to the account type
graph_mr1 = nx.from_pandas_edgelist(df_mr1, source = 'name_actual', target = 'name_follows', create_using = nx.DiGraph())
plt.figure(figsize=(10,10))
nx.draw(graph_mr1, with_labels=True, node_color=colors_mr1)
plt.savefig('plot_06.png')
plt.show()
print("Plot 06 - Network Graph for most retweeting user, has been saved in the container")
