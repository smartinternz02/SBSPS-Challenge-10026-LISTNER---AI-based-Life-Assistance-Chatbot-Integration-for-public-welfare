#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# In[4]:


df=pd.read_csv(r"C:\Users\Printech\Downloads\District_Wise_Mental_Health_Patients_2021-22.csv")


# In[5]:


df


# In[6]:


df.isnull()


# In[7]:


df.isnull().sum().sum()


# In[8]:


df.head()


# In[9]:


df.tail()


# In[10]:


df.info()


# In[11]:


df.describe()


# In[12]:


df.corr()


# In[13]:


sns.pairplot(df)


# In[14]:


plt.style.use("seaborn-whitegrid")
plt.figure(figsize=(10,12))
sns.heatmap(df.corr())
plt.show()


# In[15]:


df


# In[16]:


plt.title("Mental Health")
plt.figure(figsize=(12,10))
sns.histplot(x="SEVERE_MENTAL_DISORDER_(SMD)",hue="SL No",data=df)
plt.show()


# In[17]:


disorder = df[["SEVERE_MENTAL_DISORDER_(SMD)","Total","COMMON_MENTAL _DISORDER(CMD)"]]
figure = px.sunburst(disorder,path = ["SEVERE_MENTAL_DISORDER_(SMD)","COMMON_MENTAL _DISORDER(CMD)"],values = "Total",width = 700,height = 700,color_continuous_scale="RdY1Gn",title = "Mental Disorder")
figure.show()


# In[18]:


sns.distplot(df["ALCOHOL_&_SUBSTANCE_ABUSE"])
plt.title("Distribution - Alcohol and Substance Abuse")
plt.xlabel("ALCOHOL_&_SUBSTANCE_ABUSE")
plt.show()


# In[21]:


sns.distplot(df["SEVERE_MENTAL_DISORDER_(SMD)"])
plt.title("Distribution - SEVERE_MENTAL_DISORDER_(SMD)")
plt.xlabel("SEVERE_MENTAL_DISORDER_(SMD)")
plt.show()


# In[24]:


sns.distplot(df["COMMON_MENTAL _DISORDER(CMD)"])
plt.title("Distribution - COMMON_MENTAL _DISORDER(CMD)")
plt.xlabel("COMMON_MENTAL _DISORDER(CMD)")
plt.show()


# In[25]:


sns.distplot(df["CASES_REFERRED_TO_HIGHER_CENTRES"])
plt.title("Distribution - CASES_REFERRED_TO_HIGHER_CENTRES")
plt.xlabel("CASES_REFERRED_TO_HIGHER_CENTRES")
plt.show()


# In[26]:


sns.distplot(df["SUICIDE_ATTEMPT_CASES"])
plt.title("Distribution - SUICIDE_ATTEMPT_CASES")
plt.xlabel("SUICIDE_ATTEMPT_CASES")
plt.show()


# In[27]:


sns.distplot(df["Total"])
plt.title("Distribution - Total")
plt.xlabel("Total")
plt.show()


# In[ ]:


'''
count function in excel ->
1. count()
2. countif()
3. countifs()
4. countall()
5. countblank()

'''


# In[ ]:




