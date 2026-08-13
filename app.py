import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta
import warnings
from prophet import Prophet
from statsmodels.tsa.stattools import adfuller
warnings.filterwarnings('ignore')

# Page Title ___________________________________________________________
st.set_page_config(page_title="Stock Price Forecasting", page_icon="📈", layout="wide")

st.title("📈 Stock Price Forecasting")
st.caption("Time Series Analysis using Prophet")
st.markdown("---")

# Sidebar ___________________________________________________________
st.sidebar.header("Settings")

STOCK_NAMES = {
    "AAPL": "Apple (AAPL)",
    "GOOGL": "Google (GOOGL)",
    "MSFT": "Microsoft (MSFT)",
    "TSLA": "Tesla (TSLA)",
    "AMZN": "Amazon (AMZN)",
    "META": "Meta (META)",
    "NFLX": "Netflix (NFLX)",
    "NVDA": "NVIDIA (NVDA)"
}

ticker = st.sidebar.selectbox(
    "Select Stock",
    options=list(STOCK_NAMES.keys()),
    format_func=lambda x: STOCK_NAMES[x]
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
ax.set_title(f"{STOCK_NAMES.get(ticker, ticker)} Historical Stock Price", fontsize=14)
ax.set_ylabel("Price (USD)")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig, use_container_width=True)


# Stationarity Check___________________________________________________________
st.markdown("---")
st.header("Stationarity Check")

col_left, col_right = st.columns([4,1])

with col_left:
    rolling_mean = df['Price'].rolling(window=30).mean()
    rolling_std = df['Price'].rolling(window=30).std()
    
    fig2, ax2 = plt.subplots(figsize=(12,5))
    ax2.plot(df.index, df['Price'], color='steelblue', label="Price", linewidth=1.5)
    ax2.plot(rolling_mean, color='orange', label="Rolling Mean(30-day)", linewidth=1.8)
    ax2.plot(rolling_std, color='red', label="Rolling std(30-day)", linewidth=1.5)
    ax2.set_title('Rolling Mean and Standard Deviation (30-day window)', fontsize=14)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    
with col_right:
    adf_result = adfuller(df["Price"].dropna())
    
    p_value = adf_result[1]
    
    st.metric("p-value", f"{p_value:.4f}")
    
    if p_value < 0.05:
        st.success("Series is a stationary (p < 0.05).")
    else:
        st.warning("Series is a non-stationary (p>=0.05).")
        

# Using Prophet model for forecasting___________________________________________________________
st.markdown("---")
st.header(f"Prophet Forecast - Next {horizon} days")

try:
    df_prophet = df['Price'].reset_index()
    df_prophet.columns = ['ds', 'y']
    df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])

    with st.spinner("Fitting Prophet Model ..."):
        model = Prophet(weekly_seasonality=True, yearly_seasonality=True,daily_seasonality=False)
        model.fit(df_prophet)

        future = model.make_future_dataframe(periods=horizon, freq='B')
        forecast = model.predict(future)


    prophet_pred = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(horizon)


    fig3, ax3 = plt.subplots(figsize=(12,4))
    ax3.plot(df_prophet['ds'], df_prophet['y'], label='Stock History', color='steelblue', linewidth=1.5)
    ax3.plot(prophet_pred['ds'], prophet_pred['yhat'], label='Prophet Forecast', color='seagreen', linewidth=2, linestyle='--')
    ax3.fill_between(
        prophet_pred['ds'],
        prophet_pred['yhat_lower'],
        prophet_pred['yhat_upper'],
        alpha=0.2, color='seagreen', label='95% Uncertainty Interval'
    )
    ax3.set_title(f"{STOCK_NAMES.get(ticker, ticker)} Price Forecast — Next {horizon} Days", fontsize=14)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig3, use_container_width=True)

    st.markdown("---")

    csv = (
        prophet_pred
        .rename(columns={
            'ds': 'Date',
            'yhat': 'Forecast',
            'yhat_lower': 'Lower Bound',
            'yhat_upper': 'Upper Bound'
        })
        .to_csv(index=False)
        .encode('utf-8')
    )

    st.download_button(
        "Download Forecast CSV",
        csv,
        f"{ticker}_forecast.csv",
        "text/csv",
        type="tertiary"
    )

except ImportError:
    st.error("Please install Prophet.")

