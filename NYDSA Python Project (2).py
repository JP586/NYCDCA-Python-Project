#!/usr/bin/env python
# coding: utf-8

# ![charles-deluvio-9uS7yhHjSuY-unsplash.jpg](attachment:charles-deluvio-9uS7yhHjSuY-unsplash.jpg)

# ### NETFLIX 
# 
# #### A brief background of the Streaming Giant:
# 
# It is undeniable that streaming services has taken over the world as a preferred medium for consumers to access anything from, music, sports and entertainment.  Netflix has been around since 1997 and even though its formation was inspired by a fine paid for the late return of a DVD, it's business model has evolved through time to make it one of the most popular streaming services available today.
# 
# It wasn't however until 2007 that Netflix began delivering content via streaming content to TVs, computers and laptops.  Since then, the company experienced exponential growth. 
# 
# Today Netfix is a listed company with more that 200 million subscribers, 15,000 titles across all their international libraries, available in 190 countries.
# 

# ### Project Objective:
# 
# The aim of this project is to analyse the content released by Netflix and gain some insights into the way forward for the company.  Traditionally the streaming service has focused mainly in movie content, but from a bird's eye overview of the data, TV shows and series content has grown rapidly.
# 
# #### Questions aimed to be answered:
#  - In terms of content, what dominates? Movies or Series
#  - In which country is the most content released?
#  - What is the average release time by Netflix for Movies and Series?
#  
#  
# #### Analysis of the data to assist to answer the above questions:
#  - How many Movies and series?
#  - Which country has the most content?
#  - How has the release of content evolved over the years?
#  - What is leadtime between the release and production dates on Netflix?
#  - How do the avg ratings compare between Movies and Series?
#  - Which Genres are most popular?
#  - What audience does Netflix target the most?
#  
#  
# #### Future work and analysis:
#  - Is NETFLIX losing market share to competitors like Amazon Prime, Disney+, Hulu etc
#  - What content can NETFLIX consider adding to increase it's market share i.e. gaming, augmented reality and virtual content?

# ### Data loading:

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import init_notebook_mode, iplot


get_ipython().run_line_magic('matplotlib', 'inline')
df_net = pd.read_excel('Netflix Dataset Latest 2021.xlsx')


# In[2]:


df_net.info()


# In[3]:


df_net.head()


# In[4]:


# Rename #Column: "Series or Movies" to Type and 'Country Availability to Country
df_net1=df_net.rename(columns={'Series or Movie':'Type', 'Country Availability':'Country'})
df_net1


# In[5]:


#sort df_net from the least recent to most recent date:
df_net1 = df_net1.sort_values('Netflix Release Date', ascending=True)


# In[6]:


df_net1.head()


# In[7]:


#Check for NAN values:
df_net1.isna().sum()


# #### Preparing the data for analysis

# ##### Columns of interest
# Title;
# Genre;
# Languages;
# Type;
# Hidden Gem Score;
# Country Availability;
# Director;
# Actors; 
# View Rating; 
# Rotten Tomatoes Score;
# Metacritic Score;
# IMDb Score;
# Awards Received;
# Awards Nominated For;
# Netflix Release Date;
# 

# In[8]:


#Filling Missing Values

#For interested columns with string as a type and close to the full data set of 9425, replace with most common value
df_net1['Genre'] = df_net1['Genre'].fillna(df_net1['Genre'].mode()[0])
df_net1['Languages'] = df_net1['Languages'].fillna(df_net1['Languages'].mode()[0])

#Hidden Gem Score. Replace null values with the mean of the ratings as there are few missing ratings

df_net1['Hidden Gem Score'] = df_net1['Hidden Gem Score'].fillna(df_net1['Hidden Gem Score'].mean())

#IMDb Score. Replace null values with the mean of the ratings as there are few missing ratings
df_net1['IMDb Score'] = df_net1['IMDb Score'].fillna(df_net1['IMDb Score'].mean())

#IMDb Votes. Replace null values with the mean of the ratings as there are few missing ratings
df_net1['IMDb Votes'] = df_net1['IMDb Votes'].fillna(df_net1['IMDb Score'].mean())

# Country Availability could provide value insights into Netflix's coverage so replace missing values by "not known"
df_net1['Country'].replace(np.nan, 'other',inplace  = True)

# Would like to keep director to possible look at the link between directors and ratings. Replace missing values with "No Data"
df_net1['Director'].replace(np.nan, 'Unknown',inplace  = True)

# Would like to keep actors to possible look at the link between directors and ratings. Replace missing values with "No Data"
df_net1['Actors'].replace(np.nan, 'Unknown',inplace  = True)

# Would like to keep view rating to possible insights. Replace the missing ratings with the highest frequency rating in the data set.
df_net1['View Rating'].fillna(value=df_net1['View Rating'].value_counts().idxmax())

# Would like to keep Awards Received to possible insights. Replace missing values with "No Award"
df_net1['Awards Received'].replace(np.nan, 'No Award',inplace  = True)

# Would like to keep Awards Nominated For to possible insights. Replace missing values with "Not Nominated"
df_net1['Awards Nominated For'].replace(np.nan, 'Not Nominated',inplace  = True)

# Rotten Tomatoes Score could provide value insights into Netflix's coverage so replace missing values by "Not Rated"
df_net1['Rotten Tomatoes Score'].replace(np.nan, 'Not Rated',inplace  = True)

#Metacritic Score could provide value insights into Netflix's coverage so replace missing values by "Not Rated"
df_net1['Metacritic Score'].replace(np.nan, 'Not Rated',inplace  = True)


# Cleaning rest of missing data and dropping irrelevant data:
'''
# Drops:
Tags
Writer
Production House
Netflix Link
IMDb Link
Image
TMDDB Trailer
Trailer Site
Summary
RunTime
Boxoffice

'''
#Drop the irrelevant columns from the data set:
df_net2=df_net1.drop(labels=['Tags', 'Writer', 'Production House', 'Netflix Link', 'IMDb Link', 'TMDb Trailer', 'Trailer Site', 'Image', 'Poster', 'Summary', 'Runtime','Boxoffice'], axis = 1)
df_net2


# In[28]:


df_net2.isnull().sum()


# In[29]:


df_net2.isna().sum()


# In[11]:


# Repeat Replace the missing ratings with the highest frequency rating in the data set.
df_net2['View Rating'] = df_net2['View Rating'].fillna(value=df_net2['View Rating'].value_counts().idxmax())


# In[12]:


# delete the NaN rows in the Release Date column
df_net2.dropna(subset=['Release Date'],inplace=True)


# In[13]:


df_net2.isna().sum()


# In[16]:


df_net2.Country.unique()


# In[17]:


# Converted the string values in the country column to an array which will make it easier to visualize.
# The same is done for Genre, Languages and Actors
def ar_country_col(data):
    new_col = []
    for row in data["Country"]:
        new_col.append(row.split(","))
    return new_col

def ar_genre_col(data):
    new_col = []
    for row in data['Genre']:
        new_col.append(row.split(","))
    return new_col

def ar_lang_col(data):
    new_col = []
    for row in data['Languages']:
        new_col.append(row.split(","))
    return new_col

def ar_act_col(data):
    new_col = []
    for row in data['Actors']:
        new_col.append(row.split(","))
    return new_col


# In[18]:


df_net2['Country'] = ar_country_col(df_net2)


# In[19]:


df_net2['Genre'] = ar_genre_col(df_net2)


# In[20]:


df_net2['Languages'] = ar_lang_col(df_net2)


# In[21]:


df_net2['Actors'] = ar_act_col(df_net2)


# In[22]:


#Converting Release Date to Year
df_net2['Release Date'] = [col.strftime('%Y') for col in df_net2['Release Date']]


# In[23]:


#Converting Netflix Release Date to Year
df_net2['Netflix Release Date'] = [col.strftime('%Y') for col in df_net2['Netflix Release Date']]


# In[33]:


df_net2


# # Let the Analysis and Visualisation Begin!
# 
#  - To make the presentation look credible and professional i will be using a color palette consistent with the colors of the client through my project.
#  
#  https://brand.netflix.com/en/assets/brand-symbol/
# 

# In[25]:


types = df_net2['Type'].value_counts().reset_index()

trace = go.Pie(labels=types['index'], values=types['Type'],
               pull=[0.1,0], marker=dict(colors=['black', 'red']),
               title = 'NETFLIX CONTENT')

fig=go.Figure([trace])
fig.show()
                                                 


# In[44]:


movies = df_net2[df_net2["Type"]=="Movie"]['Release Date'].value_counts().rename('count').reset_index()
series = df_net2[df_net2["Type"]=="Series"]['Release Date'].value_counts().rename('count').reset_index()

#Sorting addtion of content by year
movies = movies.sort_values(by="index")
series = series.sort_values(by="index")

bar_movies = go.Scatter(x=movies['index'], 
                    y=movies['count'],
                    name="Movies",
                    marker_color='red')
bar_series = go.Scatter(x=series['index'], 
                    y=series['count'],
                    name="Series",
                    marker_color='black')
layout = go.Layout(title="ACTUAL RELEASE YEAR", height=700)
fig = go.Figure([bar_movies,bar_series], layout=layout)
fig.show()


# In[43]:


movies = df_net2[df_net2["Type"]=="Movie"]['Netflix Release Date'].value_counts().rename('count').reset_index()
series = df_net2[df_net2["Type"]=="Series"]['Netflix Release Date'].value_counts().rename('count').reset_index()

#Sorting addtion of content by year
movies = movies.sort_values(by="index")
series = series.sort_values(by="index")

bar_movies = go.Bar(x=movies['index'], 
                    y=movies['count'],
                    name="Movies",
                    marker_color='red')
bar_series = go.Bar(x=series['index'], 
                    y=series['count'],
                    name="Series",
                    marker_color='black')
layout = go.Layout(title="NETFLIX RELEASE YEAR", height=500)
fig = go.Figure([bar_movies,bar_series], layout=layout)
fig.show()


# In[48]:


ratings_movie = df_net2[df_net2["Type"]=="Movie"].groupby("View Rating").size().reset_index()
ratings_series = df_net2[df_net2["Type"]=="Series"].groupby("View Rating").size().reset_index()
ratings_movie.columns = ["rating", "size"]
ratings_series.columns = ["rating", "size"]

trace1 = go.Bar(x=ratings_movie['rating'],
               y=ratings_movie['size'],
               marker_color='red')

trace1 = go.Bar(x=ratings_series['rating'],
               y=ratings_series['size'],
               marker_color='red')

layout = go.Layout(title="Ratings", height=500)
fig = go.Figure([trace1,trace2], layout=layout)
fig.show()


# In[53]:


df_net2.to_excel("Netflix_EDA.xlsx")

