import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
#import matplotlib.pyplot as plt

timeperiod=252
ticker="BTC-USD"
df = yf.Ticker(ticker).history(period="max")
df['ln_rets'] = np.log((df['Close']/df['Close'].shift()))
volatility = df['ln_rets'].std()*timeperiod**.5

print(volatility)

#df = yf.Ticker("BTC-USD").history(period="max").reset_index()[["Date","Open"]]


















"""

df = yf.Ticker("BTC-USD").history(period="max").reset_index()[["Date","Open"]]
df = df.rename(columns = {"Open":"open"})
#df["date"] = pd.to_datetime(df["Date"])

#df["ret"] = 100 *(df["btc"]/df["btc"].shift(timeperiod)-1)
df["a"] = np.log((df["open"]/df["open"].shift(timeperiod))-1)
df["hv"] = df["a"].rolling(timeperiod).std()

#df["btcstd"] = df["btcret"].rolling(timeperiod).std()
#print(df["ret"])
print(df)

#df["btcsharpe"] = df["btcret"]/df["btcstd"]
#df["xmrsharpe"] = df["xmrret"]/df["xmrstd"]

btc = yf.Ticker("BTC-USD").history(period="max").reset_index()[["Date","btc"]]
btc = btc.merge(btc, on="Date", how="left")
eth = yf.Ticker("ETH-USD").history(period="max").reset_index()[["Date","eth"]]
eth = eth.merge(eth, on="Date", how="left")
df = btc.merge(eth, on="Date", how="left")
print(df)


df = df.rename(columns = {"Open":"btc"})
df["Date"] = pd.to_datetime(df["Date"])

xmrdata = xmrdata.rename(columns = {"Open":"xmr"})
xmrdata["Date"] = pd.to_datetime(xmrdata["Date"])


df["btcret"] = 100 *(df["btc"]/df["btc"].shift(timeperiod) -1)
df["xmrret"] = 100 (df["xmr"]/df["xmr"].shift(timeperiod) -1)

df["btcsharpe"] = df["btcret"]/df["btcstd"]
df["xmrsharpe"] = df["xmrret"]/df["xmrstd"]

plt.style.use("dark_background")

plt.plot(df["Date"],df["btcsharpe"], label="BTC")
plt.plot(df["Date"],df["xmrsharpe"], label="XMR")
#plt.plot(df["Date"],df["xmrsharpe"] - df["btcsharpe"], label="XMR - BTC")
plt.title("Sharpe Ratios of BTC and XMR", #df["btcstd"] = df["btcret"].rolling(timeperiod).std()
#df["xmrstd"] = df["xmrret"].rolling(timeperiod).std()
size = 20)
plt.legend()
plt.plot(df["Date"],df["btcret"], label="BTC")
plt.show()
"""