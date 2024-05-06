import streamlit as st
import numpy as np
import yfinance as yf
import plotly.express as px
import pandas as pd
import datetime
import requests

# Set up the app title
st.title("Stock Price Prediction")

# Create a sidebar for user input
ticker = st.sidebar.text_input("Enter Stock Ticker")
start_date = st.sidebar.date_input("Enter Start Date",datetime.date(2019,7,6))
end_date = st.sidebar.date_input("Enter End Date")


if ticker != "" :
    # Define a function to download stock data
    def download_stock_data(ticker, start_date, end_date):
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            return stock_data
        except Exception as e:
            st.error(f"Error: {e}")
        return None

    # Download stock data
    stock_data = download_stock_data(ticker, start_date, end_date)

    # Create a plotly chart
    if stock_data is not None:
        fig = px.line(x=stock_data.index, y=stock_data["Close"], title=ticker)
        st.plotly_chart(fig)

    # Create tabs for different types of data
    pricing_data, fundamental_data, news = st.tabs(
        ["Pricing Data", "Fundamental Data", "News"]
    )

    with pricing_data:
        st.header("Pricing Data")
        st.write(stock_data)

    # Fundamental Data tab
    with fundamental_data:
        st.write("Fundamental Data")

    # News tab
    from stocknews import StockNews

    with news:
        st.header(f"News of {ticker}")
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()

        for i in range(10):
            st.subheader(f"News {i+1}")
            st.write(df_news["title"][i])
            st.write(df_news["published"][i])
            st.write(df_news["summary"][i])
            title_sentiment = df_news["sentiment_title"][i]
            st.write(f"Sentiment: {title_sentiment}")
            if "sentiment_news" in df_news.columns:
                news_sentiment = df_news["sentiment_news"][i]
                st.write(f"Sentiment: {news_sentiment}")
            else:
                st.write("Sentiment score not available for this news article.")
