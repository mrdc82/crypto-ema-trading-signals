import influxdb_client, os, time
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision
import ccxt
import pandas as pd
import talib
import numpy as np

# InfluxDB settings
INFLUXDB_URL = "http://localhost:8086"  # Change to your InfluxDB URL
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")  # Replace with your InfluxDB token
INFLUXDB_ORG = "dinosville"      # Replace with your organization name
INFLUXDB_BUCKET = "trading_signals"     # Replace with your bucket name

# Initialize InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def fetch_binance_data(symbol, timeframe, limit=500):
    """
    Fetches historical data from Binance using the ccxt library.
    """
    exchange = ccxt.binance({'rateLimit': 1200, 'enableRateLimit': True})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    data = pd.DataFrame(ohlcv, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data['Date'] = pd.to_datetime(data['Date'], unit='ms')
    data.set_index('Date', inplace=True)
    data[['Open', 'High', 'Low', 'Close', 'Volume']] = data[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    return data

def check_signals(data):
    """
    Checks if the candlestick touches the 200 EMA and if the EMA crossover conditions are met.
    """
    data['EMA_9'] = talib.EMA(data['Close'], timeperiod=9)
    data['EMA_21'] = talib.EMA(data['Close'], timeperiod=21)
    data['EMA_50'] = talib.EMA(data['Close'], timeperiod=50)
    data['EMA_200'] = talib.EMA(data['Close'], timeperiod=200)
    data['Touch_200_EMA'] = np.where((data['Low'] <= data['EMA_200']) & (data['High'] >= data['EMA_200']), 1, 0)
    data['Cross_9_21'] = np.where((data['EMA_9'] > data['EMA_21']) & (data['EMA_9'].shift(1) <= data['EMA_21'].shift(1)), 1, 0)
    data['Cross_21_50'] = np.where((data['EMA_21'] > data['EMA_50']) & (data['EMA_21'].shift(1) <= data['EMA_50'].shift(1)), 1, 0)
    data['EMA_Cross_Signal'] = np.where((data['Cross_9_21'] == 1) & (data['Cross_21_50'] == 1), 1, 0)
    return data

def send_to_influxdb(data):
    """
    Sends the latest signal data to InfluxDB.
    """
    latest = data.iloc[-1]
    point = Point("trading_signals") \
        .tag("symbol", symbol) \
        .field("Close", float(latest['Close'])) \
        .field("Touch_200_EMA", int(latest['Touch_200_EMA'])) \
        .field("EMA_Cross_Signal", int(latest['EMA_Cross_Signal'])) \
        .time(latest.name, WritePrecision.MS)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    print(f"Sent data to InfluxDB: {point}")

def main():
    global symbol
    top10 = ['BTC/USDT','ETH/USDT','XRP/USDT']
    #symbol = 'BTC/USDT'
    timeframe = '1m'
    i = 0
    while True:
        if i < len(top10):
            symbol = top10[i]
            try:
                print("Fetching data...")
                data = fetch_binance_data(symbol, timeframe)
                data_with_signals = check_signals(data)
                send_to_influxdb(data_with_signals)
                #time.sleep(60 * 60 * 24)  # Wait for the next daily candlestick
                time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)
            i = i+1
        elif i == len(top10):
            i = 0

if __name__ == "__main__":
    main()
