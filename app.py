from cgitb import reset
from multiprocessing.sharedctypes import Value
from matplotlib.pyplot import axis
from matplotlib.style import use
import streamlit as st
import pandas as pd
import numpy as np
import pickle

#Important Files

batsman=pickle.load(open('batsman.pkl','rb'))
player_info=pickle.load(open('player_info.pkl','rb'))
bound_total=pickle.load(open('bound_total.pkl','rb'))
bowler_stats=pickle.load(open('bowler_stats.pkl','rb'))


st.sidebar.title('Wordcup Analysis')
st.sidebar.image('icon.png',width=50)
st.sidebar.header(f'Hello user')


user_input=st.sidebar.radio('Please Select',('Team Info','Batsman Stats','Bowler Stats','Top Stats'))

#st.header(f"{user_input}")

#Show team names for expander
def team_names(df):
    return df.columns.tolist()
#Player name for expander
def player_name1(country_name):
    return player_info[country_name].dropna().tolist()

country_name=team_names(player_info)

#Batsman Info
#player info me name list ke liye
def player_name(df):
    return df['Batsman'].values

# total runs ke liye 
def total_runs(df,name):
    return df[df['Batsman']==name]['Runs1'].values[0]

#6 ke liye  
def total_runs_6(df,name):
    return df[df['Batsman']==name]['6s1'].values[0]

#4 ke liye
def total_runs_4(df,name):
    return df[df['Batsman']==name]['4s1'].values[0]
# avg
def total_runs_avg(df,name):
    value=df[df['Batsman']==name]['avg'].values[0]
    return f'{value:.2f}'

# strike rate
def total_runs_sr(df,name):
    value=df[df['Batsman']==name]['SR'].values[0]
    return f'{value:.2f}'



#Bowler Info
#player info me name list ke liye
def player_name_bowler(df):
    return df['Bowler'].values

# total runs ke liye 
def total_runs_bowler(df,name):
    return df[df['Bowler']==name]['Runs'].values[0]

# Total Wickets  
def total_wickets_bowler(df,name):
    return df[df['Bowler']==name]['Wkts'].values[0]

#Average
def total_average_bowler(df,name):
    value=df[df['Bowler']==name]['AVG'].values[0]
    return f'{value:.2f}'
# Maiden
def total_maiden_bowler(df,name):
    return df[df['Bowler']==name]['Mdns'].values[0]
    
# strike rate
def total_runs_sr_bowler(df,name):
    value=df[df['Bowler']==name]['SR'].values[0]
    return f'{value:.2f}'




#Maximum runs
def maximum_runs(df,player_name):
    player_info=df[df['Batsman']==player_name]
    max_val=player_info['Bat11'].max()
    maxi=player_info[player_info['Bat11']==max_val]['Bat1'].values[0]
    return maxi


# Team Information
if user_input=='Team Info':
    st.header(f'{user_input}')
    team_list=team_names(player_info)
    for i, team_name in enumerate(team_list):
        with st.expander(team_name):
            player_names=player_name1(team_name)
            for name in player_names:
                st.text(name)

# Player Informantion
#Batsman
if user_input=='Batsman Stats':
    st.header(f'{user_input}')
    name=st.selectbox('',(player_name(bound_total)))
    st.title(name)

    col1, col2, col3 = st.columns(3)
#total runs
    with col1:
        st.header('Total Runs')
        st.subheader(total_runs(bound_total,name))
    
#Sixes 
    with col2:
        st.header('Sixes')
        st.subheader(total_runs_6(bound_total,name))
# Fours        
    with col3:
        st.header('Boundries')
        st.subheader(total_runs_4(bound_total,name))

    col1, col2, col3 = st.columns(3)
#Batting Average
    with col1:
        st.header('Batting Avg.')
        st.subheader(total_runs_avg(bound_total,name))
    with col2:
        st.header('Highest')
        st.subheader(maximum_runs(batsman,name))
        
    with col3:
        st.header('Strike rate')
        st.subheader(total_runs_sr(bound_total,name))

#player info
#bowler stats

if user_input=='Bowler Stats':
    st.header(f'{user_input}')
    name=st.selectbox('',(player_name_bowler(bowler_stats)))
    st.title(name)

    col1, col2, col3 = st.columns(3)
#total runs
    with col1:
        st.header('Total Ball')
        st.subheader(total_runs_bowler(bowler_stats,name))
    
#Wickets 
    with col2:
        st.header('Wickets')
        st.subheader(total_wickets_bowler(bowler_stats,name))
# Average        
    with col3:
        st.header('Average')
        st.subheader(total_average_bowler(bowler_stats,name))

    col1, col2, col3 = st.columns(3)
#Maiden
    with col1:
        st.header('Maiden Overs')
        st.subheader(total_maiden_bowler(bowler_stats,name))
    with col2:
        st.header('SR')
        st.subheader(total_runs_sr_bowler(bowler_stats,name))

#Batsman

batsman_top={'Top Scorers':'Runs1','Most Sixes':"6s1",'Most Boundries':'4s1','Top Averages':'avg','Top Strike Rate':'SR'}
def top_batman_stats(df,key):
    value=batsman_top[key]
    df=df.sort_values(value,ascending=False).head(10)
    df=df[['Batsman',f'{value}']].reset_index()
    df=df.drop(['index'],axis=1)
    df=df.rename(columns={f'{value}':f'{key}'})
    df.index = np.arange(1, len(df)+1)
    return df

#bowler
bowler_top={"Best Bowler":'ball_thrown',
            'Top wicket takers':'Wkts','Maiden Overs':'Mdns','Top Averages':'AVG','Top Strike Rate':'SR'}

def top_bowler_stats(df,key):
    value=bowler_top[key]
    df=df.sort_values(value,ascending=False).head(10)
    df=df[['Bowler',f'{value}']].reset_index()
    df=df.drop(['index'],axis=1)
    df=df.rename(columns={f'{value}':f'{key}'})
    df.index = np.arange(1, len(df)+1)
    return df

if user_input=='Top Stats':
    top_input=st.sidebar.selectbox('Please select',('Batsman','Bowler'))
    
    if top_input=="Batsman":
        st.header(f'{user_input} {top_input}')
        for key in batsman_top:
            with st.expander(key):
                st.table(top_batman_stats(bound_total,key))
    if top_input=="Bowler":
        st.header(f'{user_input} {top_input}')
        for key in bowler_top:
            value=bowler_top[key]
            with st.expander(key):
                st.table(top_bowler_stats(bowler_stats,key))

# compleated