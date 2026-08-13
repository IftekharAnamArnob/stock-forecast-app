# 📈 Stock Price Forecasting with Prophet

An interactive **Streamlit** application for exploring historical stock prices and generating future stock price forecasts using **Prophet**. The application downloads stock market data dynamically through `yfinance` and provides visual analysis, a stationarity check, forecasting, uncertainty intervals, and CSV export.

## 📌 Project Overview

This project demonstrates a **time series forecasting workflow** for stock prices.

The Streamlit application allows users to:

- Select a stock from a predefined list
- Select a historical date range
- Choose a forecast horizon from 7 to 120 days
- View key stock statistics
- Visualize historical closing prices
- Perform a stationarity check using rolling statistics and the Augmented Dickey-Fuller (ADF) test
- Generate forecasts using Prophet
- Visualize forecasted prices with an uncertainty interval
- Download forecast results as a CSV file

The application uses the **closing price (`Close`)** as the forecasting target. 

## 📈 Supported Stocks

The application currently supports:

| Ticker | Company |
|---|---|
| `AAPL` | Apple |
| `GOOGL` | Google |
| `MSFT` | Microsoft |
| `TSLA` | Tesla |
| `AMZN` | Amazon |
| `META` | Meta |
| `NFLX` | Netflix |
| `NVDA` | NVIDIA |

These stocks are available through the application's sidebar selector. 

## 🛠️ Technologies Used

- **Python**
- **Streamlit** — interactive web application
- **yfinance** — stock market data retrieval
- **Pandas** — data processing
- **NumPy** — numerical operations
- **Matplotlib** — data visualization
- **Prophet** — time series forecasting
- **Statsmodels** — Augmented Dickey-Fuller stationarity test

## 📊 Data Collection

Historical stock data is downloaded dynamically using `yfinance` according to the user's selected stock and date range. The application retains only the `Close` column and renames it to `Price`. 

The application also requires at least **60 trading days** of data before continuing. 

## 📋 Stock Overview

The application displays four key metrics:

- **Current Price**
- **Period High**
- **Period Low**
- **Trading Days**

It also provides a historical stock-price chart for the selected period. 

## 📉 Stationarity Check

The application includes a stationarity analysis before forecasting.

### Rolling Statistics

A **30-day rolling window** is used to calculate and visualize:

- Rolling Mean
- Rolling Standard Deviation

alongside the original stock-price series.

### Augmented Dickey-Fuller Test

The application performs the **Augmented Dickey-Fuller (ADF) test** on the closing-price series and displays the resulting p-value.

The application's interpretation is:

- **p-value < 0.05** → Series is considered stationary
- **p-value ≥ 0.05** → Series is considered non-stationary 

## 📈 Forecast Visualization

The forecast chart displays:

- Historical stock prices
- Prophet's predicted price (`yhat`)
- A **95% uncertainty interval** using the lower and upper forecast bounds

The uncertainty interval is displayed as a shaded area around the forecast. 

The forecast horizon can be selected from **7 to 120 days**, in increments of 7 days. 

## ⬇️ Download Forecast

The application provides a **Download Forecast CSV** button.

The exported file contains:

| Column | Description |
|---|---|
| `Date` | Forecast date |
| `Forecast` | Prophet predicted price |
| `Lower Bound` | Lower forecast bound |
| `Upper Bound` | Upper forecast bound |

The filename is generated using the selected stock ticker, for example:

```text
AAPL_forecast.csv
```

The export functionality is implemented directly in the Streamlit application. 

## 🖥️ Project Structure

```text
stock-forecast-app/
│
├── app.py
├── README.md
└── requirements.txt
```

## Installation

## 1.📦 Clone the repository

```bash
git clone https://github.com/IftekharAnamArnob/stock-forecast-app
cd stock-forecast-app
```

## 2.📦 Install dependencies

```bash
pip install -r requirements.txt
```

## 3.▶️ Run the Application

```bash
streamlit run app.py

Streamlit will start a local server and open the application in your browser.

## 🔄 Application Workflow

```text
Select Stock
      ↓
Select Start & End Dates
      ↓
Download Historical Data using yfinance
      ↓
Extract Closing Price
      ↓
Display Stock Overview
      ↓
Perform Stationarity Check
      ↓
Configure Prophet
      ↓
Generate Future Business Days
      ↓
Predict Future Prices
      ↓
Visualize Forecast + Uncertainty Interval
      ↓
Download Forecast CSV
```

## ⚙️ User Controls

The sidebar provides:

- **Select Stock** — choose from the supported tickers
- **Start Date** — choose the beginning of the historical period
- **End Date** — choose the end of the historical period
- **Forecast Horizon** — select 7–120 future days

## ⚠️ Notes and Limitations

- The application uses **closing prices only** for forecasting.
- An internet connection is required because historical data is retrieved dynamically through `yfinance`.
- The application does not provide financial advice or a trading strategy.
- Forecast quality depends on the historical period and patterns captured by the model.
- At least **60 trading days** of data are required.
- Future dates are generated using business-day frequency.

## 👤 Project

**Stock Price Forecasting using Prophet**

Built as an interactive time series forecasting application with Streamlit.

### 🚀 Live Demo

👉 **[Try the Stock Price Forecasting App](https://stock-forecast-app-trkecev88evbf69lvm7gy7.streamlit.app/)**

Click the link above to open the deployed application and interact with the Stock Price Forecasting model directly.
