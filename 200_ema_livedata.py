import ccxt
import pandas as pd
import talib
import numpy as np
import time

def fetch_binance_data(symbol, timeframe, limit=500):
    """
    Fetches historical data from Binance using the ccxt library.
    
    Parameters:
    - symbol (str): The trading pair symbol (e.g., 'BTC/USDT').
    - timeframe (str): The candlestick timeframe (e.g., '1d', '1h').
    - limit (int): The number of data points to fetch (max 1000).
    
    Returns:
    - DataFrame: Historical price data with columns 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'.
    """
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True
    })
    
    # Fetch OHLCV data
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    data = pd.DataFrame(ohlcv, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data['Date'] = pd.to_datetime(data['Date'], unit='ms')
    data.set_index('Date', inplace=True)
    
    # Convert to float for TA-Lib compatibility
    data[['Open', 'High', 'Low', 'Close', 'Volume']] = data[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    
    return data

def check_signals(data):
    """
    Checks if the candlestick touches the 200 EMA and if the EMA crossover conditions are met.
    """
    # Calculate EMAs
    data['EMA_9'] = talib.EMA(data['Close'], timeperiod=9)
    data['EMA_21'] = talib.EMA(data['Close'], timeperiod=21)
    data['EMA_50'] = talib.EMA(data['Close'], timeperiod=50)
    data['EMA_200'] = talib.EMA(data['Close'], timeperiod=200)

    # Check if candlestick touches the 200 EMA
    data['Touch_200_EMA'] = np.where((data['Low'] <= data['EMA_200']) & (data['High'] >= data['EMA_200']), 1, 0)

    # Check EMA crossover conditions
    data['Cross_9_21'] = np.where((data['EMA_9'] > data['EMA_21']) & (data['EMA_9'].shift(1) <= data['EMA_21'].shift(1)), 1, 0)
    data['Cross_21_50'] = np.where((data['EMA_21'] > data['EMA_50']) & (data['EMA_21'].shift(1) <= data['EMA_50'].shift(1)), 1, 0)

    # Add a combined signal for EMA crossovers
    data['EMA_Cross_Signal'] = np.where((data['Cross_9_21'] == 1) & (data['Cross_21_50'] == 1), 1, 0)

    return data

def main():
    """
    Main function to fetch live data from Binance and check for signals.
    """
    symbol = 'BTC/USDT'  # Trading pair
    timeframe = '1d'     # Timeframe for candlesticks

    while True:
        try:
            print("Fetching data...")
            # Fetch data from Binance
            data = fetch_binance_data(symbol, timeframe)
            
            # Check signals
            data_with_signals = check_signals(data)
            
            # Get the most recent signal
            latest = data_with_signals.iloc[-1]
            print(f"Latest Close: {latest['Close']}")
            if latest['Touch_200_EMA']:
                print("Signal: Candlestick touched the 200 EMA!")
            if latest['EMA_Cross_Signal']:
                print("Signal: EMA crossover condition met!")
            
            # Wait before fetching new data (adjust as needed)
            time.sleep(60 * 60 * 24)  # Wait for the next daily candlestick
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()
