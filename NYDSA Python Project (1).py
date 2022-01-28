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
#  - Does the future for NETFLIX lie in the release of more TV shows than movie content
#  - Is movies still preferred by subscribers
#  - Are there countries with low content that presents a lost opportunity for the company?
#  
#  
# ### Future Analysis:
#  - Is NETFLIX losing market share to competitors like Amazon Prime, Disney+, Hulu etc
#  - What content can NETFLIX consider adding to increase it's market share i.e. gaming, augmented reality and virtual content?

# In[21]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


get_ipython().run_line_magic('matplotlib', 'inline')
df_net = pd.read_excel('Netflix Dataset Latest 2021.xlsx')


# In[22]:


df_net.info()


# ### Dataset Observations:
# 
# 1. "Movies or Series' a key column and it could be considered to be use as the Index. Consider renaming
# 2. Director and Writer has missing values but is not key to the analysis
# 3. Genre has repeating strings which will make it hard to classify the field, data clean-up will be required. There are also 25 titles with missing values
# 4. IMdb score has some missing values but this could stil be a valid value.  This column can be used as a standarised value to interpret wether TV shows have gained popularity
# 5. A comparison of content nominated for, which received a review can also provide valuable insights
# 6. IMDb Link, Summary, Image, Poster, TMDb Trailer and Trailer Site is not relavant to the analysis.

# In[24]:


# Rename #Column: "Series or Movies" to Type
df_net1=df_net.rename(columns={'Series or Movie':'Type'})
df_net1


# In[25]:


df_net1.head()


# In[38]:


'''
# Columns of interest:
Title
Genre
Languages
Type
Hidden Gem Score
Country Availability
Director
Actors 
View Rating 
Rotten Tomatoes Score
Metacritic Score 
IMDb Score
Awards Received
Awards Nominated For
Netflix Release Date

'''
#Filling Missing Values

#For interested columns with string as a type and close to the full data set of 9425, replace with most common value
df_net1['Genre'] = df_net1['Genre'].fillna(df_net1['Genre'].mode()[0])
df_net1['Languages'] = df_net1['Languages'].fillna(df_net1['Languages'].mode()[0])

#Hidden Gem Score. Replace null values with the mean of the ratings as there are few missing ratings

df_net1['Hidden Gem Score'] = df_net1['Hidden Gem Score'].fillna(df_net1['Hidden Gem Score'].mean())

# Country Availability could provide value insights into Netflix's coverage so replace missing values by "not known"
df_net1['Country Availability'].replace(np.nan, 'Not Known',inplace  = True)

# Would like to keep director to possible look at the link between directors and ratings. Replace missing values with "No Data"
df_net1['Director'].replace(np.nan, 'No Data',inplace  = True)

# Would like to keep actors to possible look at the link between directors and ratings. Replace missing values with "No Data"
df_net1['Actors'].replace(np.nan, 'No Data',inplace  = True)

# Would like to keep view rating to possible insights. Replace missing values with "No Rated"
df_net1['View Rating'].replace(np.nan, 'Not Rated',inplace  = True)

# Would like to keep Awards Received to possible insights. Replace missing values with "No Award"
df_net1['Awards Received'].replace(np.nan, 'No Award',inplace  = True)

# Would like to keep Awards Nominated For to possible insights. Replace missing values with "Not Nominated"
df_net1['Awards Nominated For'].replace(np.nan, 'Not Nominated',inplace  = True)

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

'''
#Drop NA's
df_net1.dropna(inplace=True)

#Drop any duplicates in the data frama
df_net1.drop_duplicates(inplace= True)

#Drop the irrelevant columns from the data set:
df_net2=df_net1.drop(labels=['Tags', 'Writer', 'Production House', 'Netflix Link', 'IMDb Link', 'TMDb Trailer', 'Trailer Site', 'Image', 'Poster', 'Summary'], axis = 1)
df_net2


# In[39]:


df_net2.isnull().sum()


# In[40]:


df_net2.isna().sum()


# # Let the Analysis and Visualisation Begin!
