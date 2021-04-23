import streamlit as st
import pandas as pd
import numpy as np
import requests
import config
import tweepy
from datetime import datetime, timedelta
import json
import yfinance as yf
import pandas as pd

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


option = st.sidebar.selectbox("Select Dashboard:", ('News', 'Twitter','Global','Stock Chart'))

if option == 'Twitter':
    for username in config.TWITTER_USERNAMES:
        
        user = api.get_user(username)
        tweets = api.user_timeline(username, tweet_mode="extended")

        st.write("___________________________")
        st.image(user.profile_image_url)
        st.header("**_Source:_** "+ username)
        st.write("___________________________")

        for tweet in tweets:
                st.write(tweet.full_text) #full trext of tweets
                st.write("__________")  



if option == 'Global':
    symbol = st.sidebar.text_input('Symbol',value = 'TSLA', max_chars=5)
    st.subheader("Global Stock Tweets")
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json") 
    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write("User: ",message['user']['username']) 
        st.write("Time: ",message['created_at'])
        st.write("->",message['body'])
        st.write("___________________________________________________")
        
        
if option == 'Stock Chart': 
    st.write('Put .NS suffix to any indian stock name for its chart.')
    stocksymbol = st.text_input("stock name:  NS => NSE | BO => BSE", 'RELIANCE.NS')
    opendate = st.text_input("open date (yyyy-mm-dd) : (make sure it's less than close date, duh..)", '2021-1-1')
    closedate = st.text_input("close date (yyyy-mm-dd)", '2021-4-12')
    #screen = st.sidebar.selectbox("View", ('Overview', 'Fundamentals', 'News', 'Ownership', 'Technicals'), index=1)
    stockdata = yf.Ticker(stocksymbol)
    tickerDf = stockdata.history(period='1d', start=opendate, end=closedate)
    st.write('Price fluctuations:-')
    st.line_chart(tickerDf.Close)
    st.write('Share volume movement:-')
    st.line_chart(tickerDf.Volume)
    stockinfo = stockdata.info
    st.header('Stock Overview:-')
    holders = stockdata.major_holders
    st.write('BALANCE SHEET')
    st.write(stockdata.balance_sheet)
    st.write('MAJOR HOLDERS')
    st.write(holders)
    for key,value in stockinfo.items():
        st.subheader(key)
        st.write(value)

if option == 'News':
    newstype = st.sidebar.selectbox("Select:", ('Top Headlines', 'Business', 'Technology'))
    if newstype ==  'Business':
        st.header('Business News')
        r = requests.get('https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=0445aaf7459344f0a5624b61cdcc0594')
        data = json.loads(r.content)

        for i in range(15):
            news = data['articles'][i]['title']
            st.subheader(news)
           
            st.write('______')
            
            image = data['articles'][i]['urlToImage']
            try:
                st.image(image)
            except:
                pass
            else:
                pass

            content = data['articles'][i]['content']
            st.write(content)

            url = data['articles'][i]['url']
            st.write(url)

            

    if newstype ==  'Top Headlines':
        
        st.header('Top Headlines')
        r = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=0445aaf7459344f0a5624b61cdcc0594')
        data = json.loads(r.content)

        for i in range(15):
            news = data['articles'][i]['title'] #branching in
            st.subheader(news)
            st.write('______')
            image = data['articles'][i]['urlToImage']
            try:
                st.image(image)
            except:
                pass
            else:
                pass

            content = data['articles'][i]['content']
            st.write(content)

            url = data['articles'][i]['url']
            st.write(url)

    
    if newstype == 'Technology':
        st.header('Technology News')
        r = requests.get('https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=0445aaf7459344f0a5624b61cdcc0594')
        data = json.loads(r.content)

        for i in range(15):
            news = data['articles'][i]['title'] #branching in
            st.subheader(news)
            st.write('______')
            image = data['articles'][i]['urlToImage']

            try:
                st.image(image)
            except:
                pass
            else:
                pass
            

            content = data['articles'][i]['content']
            st.write(content)

            url = data['articles'][i]['url']
            st.write(url)




    

    




































