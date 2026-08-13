import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page Title ___________________________________________________________
st.set_page_config(page_title="Stock Price Forecasting", page_icon="📈", layout="wide")

st.title("📈 Stock Price Forecasting")
st.caption("Time Series Analysis using Prophet")
st.markdown("---")

# Sidebar ___________________________________________________________
st.sidebar.header("Settings")

ticker = st.sidebar.selectbox(
    "Select Stock",
    options=["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX", "NVDA"],
    format_func = lambda x: {
        "AAPL" : "Apple (AAPL)",
        "GOOGL": "Google (GOOGL)",
        "MSFT" : "Microsoft (MSFT)",
        "TSLA" : "Tesla (TSLA)",
        "AMZN" : "Amazon (AMZN)",
        "META" : "Meta (META)",
        "NFLX" : "Netflix (NFLX)",
        "NVDA" : "NVIDIA (NVDA)"
    }[x]
)

start_date = st.sidebar.date_input("Start Date", value=date.today() - timedelta(days=5*365))
end_date = st.sidebar.date_input("End Date", value=date.today())
horizon = st.sidebar.slider("Forecast Horizon (days)", min_value=7, max_value = 120, value=90, step=7)

with st.spinner(f"Downloading {ticker} data ..."):
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if data.empty:
            st.error(f"No data found for ticket {ticker}. Please try a different stock.")
            st.stop()
        df = data[['Close']].copy()
        df.columns = ['Price']
        df.index = pd.to_datetime(df.index)
    except Exception as e:
        st.error(f"Error Downloading date: {e}")
        st.stop()  

if len(df) < 60:
    st.error("Not enough data. Please select at least 60 trading days")
    st.stop()

# Stock Overview ___________________________________________________________

st.header("Stock Overview")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Current Price", f"${df['Price'].iloc[-1]:.2f}")
col2.metric("Period High", f"${df['Price'].max():.2f}")
col3.metric("Perido Low", f"${df['Price'].min():.2f}")
col4.metric("Trading days", f"{len(df)}")

fig, ax = plt.subplots(figsize=(12,4))
ax.plot(df.index, df['Price'], color='steelblue', linewidth=1.5)
ax.set_title(f"{ticker} Stock Price", fontsize=14)
ax.set_ylabel(f"Price (USD)")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig, use_container_width=True)


# Stationarity Check___________________________________________________________
