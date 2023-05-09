#!/usr/bin/env python
# coding: utf-8

# In[18]:


import yfinance as yf
import pandas as pd
import sqlite3

# Download ETF prices
etfs = ["SPY", "TLT", "HYG", "LQD", "VNQ"]
data = yf.download(etfs, start="2020-01-01", end="2023-01-01")["Adj Close"]

# Calculate monthly returns
monthly_returns = data.resample("M").last().pct_change().dropna()

# Store monthly returns in SQLite database
conn = sqlite3.connect("etfs.db")
monthly_returns.to_sql("monthly_returns", conn, if_exists="replace")


# In[19]:


def top_performing_ETF_last_year():
    query = """
    SELECT *
    FROM monthly_returns
    WHERE date >= '2022-01-01'
    ORDER BY SPY DESC
    LIMIT 1
    """
    result =pd.read_sql_query(query, conn)
    return result.columns[2]

def best_two_ETFs_last_month():
    query = """
    SELECT *
    FROM monthly_returns
    WHERE date >= '2022-12-01'
    ORDER BY SPY DESC
    LIMIT 2
    """
    result = pd.read_sql_query(query, conn)
    return result.columns[2:4].tolist()

def did_SPY_outperform_TLT_last_year():
    query = """
    SELECT SPY, TLT
    FROM monthly_returns
    WHERE date >= '2022-01-01'
    """
    result = pd.read_sql_query(query, conn)
    if result["SPY"].mean() > result["TLT"].mean():
        return "Yes"
    else:
        return "No"


# In[20]:


print("Top performing ETF last year:")
print(top_performing_ETF_last_year())


# In[21]:


print("\nBest two ETFs last month:")
print(best_two_ETFs_last_month())


# In[22]:


print("\nDid SPY outperform TLT last year:")
print(did_SPY_outperform_TLT_last_year())


# In[23]:


from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize


# In[51]:


def ask_question(question):
    question = question.lower()
    conn = sqlite3.connect('etfs.db')
    if 'top performing etf last year' in question:
        query = """
        SELECT *
        FROM monthly_returns
        WHERE date >= '2022-01-01'
        ORDER BY SPY DESC
        LIMIT 1
        """
        result =pd.read_sql_query(query, conn)
        return result.columns[2]

    elif 'best two etfs last month' in question:
        query = """
        SELECT *
        FROM monthly_returns
        WHERE date >= '2022-12-01'
        ORDER BY SPY DESC
        LIMIT 2
        """
        result = pd.read_sql_query(query, conn)
        return result.columns[2:4].tolist()
    elif 'spy outperform tlt last year' in question:
        query = """
        SELECT SPY, TLT
        FROM monthly_returns
        WHERE date >= '2022-01-01'
        """
        result = pd.read_sql_query(query, conn)
        if result["SPY"].mean() > result["TLT"].mean():
            return "Yes, SPY outperformed TLT last year"
        else:
            return "No,SPY did not outperform TLT last year"
        
            


# In[33]:


question = 'Did SPY outperform TLT last year?'
print(ask_question(question))


# In[34]:


question1 = 'top performing ETF last year'
print(ask_question(question1))


# In[35]:


question2 = 'Best two ETFs last month'
print(ask_question(question2))


# In[36]:


import nltk
from nltk.tokenize import word_tokenize


# In[54]:


def process_input(input_text):
    # Tokenize the input text
    words = word_tokenize(input_text)
    words_set = set(words)
    conn = sqlite3.connect('etfs.db')
    if "top" in words_set and "year" in words_set:
        query = """
        SELECT *
        FROM monthly_returns
        WHERE date >= '2022-01-01'
        ORDER BY SPY DESC
        LIMIT 1
        """
        result = pd.read_sql_query(query, conn)
        return result.columns[2]
    elif "best" in words_set:
        query = """
        SELECT *
        FROM monthly_returns
        WHERE date >= '2022-12-01'
        ORDER BY SPY DESC
        LIMIT 2
        """
        result = pd.read_sql_query(query, conn)
        return result.columns[2:4].tolist()
    else:
        return "Keyword not recognized"



    
    


# In[55]:


question1 = 'top performing ETF last year'
print(process_input(question1))


# In[41]:


import nltk


# In[42]:


nltk.download('punkt')


# In[ ]:




