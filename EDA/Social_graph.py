import pandas as pd

df=pd.read_csv('user_full_info.csv')

df1=df[['user_id','Account Type_actual','Group Type_actual']]
df2=df[['follow_user_id','Account Type_follows','Group Type_follows']]
df2.columns=['user_id','Account Type_actual','Group Type_actual']
df_new=pd.concat([df1,df2])
df_new=df_new.drop_duplicates().reset_index()
df_new['my_index']=df_new.index
df_new=df_new.drop(columns=['index'],axis=1)
df_indexer=df_new[['user_id','my_index']]

df_graph=df[['user_id','follow_user_id']]
df_graph=df_graph.merge(df_indexer,how='left',on='user_id')
df_indexer.columns=['user_id','follow_my_index']
df_graph=df_graph.merge(df_indexer,how='left',left_on='follow_user_id',right_on='user_id')

df_graph=df_graph.drop_duplicates()

print ('qaq')
