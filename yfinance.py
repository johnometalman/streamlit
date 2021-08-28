import yfinance as yf
import pandas as pd 
import streamlit as st

st.write("""
# Simple Stock Price App 

Shown are the stock closing price and volume of Google

""")

symbol = 'GOOGL'

data = yf.Ticker(symbol)

symbol_df = symbol.history(period='id', start='2010-5-31', end='2020-5-31')

st.line_chart(period.Close)
st.line_chart(period.Volume)


