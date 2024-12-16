# Cryptocurrency EMA Monitoring

This repository contains Python scripts for monitoring cryptocurrency prices and exponential moving averages (EMAs) using live data from Binance. The project tracks the top 10 cryptocurrencies and provides alerts when key EMA crossover conditions are met. Additionally, it integrates with InfluxDB for data storage and Grafana for data visualization.

## Features

1. **Live Data Fetching**:
   - Retrieves real-time price data for the top 10 cryptocurrencies from Binance.

2. **EMA Calculations**:
   - Calculates 9-day, 21-day, 50-day, and 200-day EMAs.
   - Monitors EMA crossovers:
     - Alerts when the 200-day EMA is reached and the 9-day, 21-day, and 50-day EMAs cross over each other.

3. **Data Storage**:
   - Pushes the calculated data and monitoring results to an InfluxDB instance.

4. **Data Visualization**:
   - Configures a Grafana dashboard to represent cryptocurrency price trends and EMA crossovers.

## Prerequisites

- **Python 3.8+**
- **Dependencies**: Install required Python packages via `requirements.txt`.
- **InfluxDB**: For time-series data storage.
- **Grafana**: For creating visual dashboards based on the stored data.
- **Binance API Key**: Required to access Binance's live data.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crypto-ema-monitoring.git
   cd crypto-ema-monitoring
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables for Binance API and InfluxDB:
   - Create a `.env` file:
     ```env
     BINANCE_API_KEY=your_binance_api_key
     BINANCE_SECRET_KEY=your_binance_secret_key
     INFLUXDB_URL=http://localhost:8086
     INFLUXDB_TOKEN=your_influxdb_token
     INFLUXDB_ORG=your_influxdb_organization
     INFLUXDB_BUCKET=crypto_data
     ```

4. Start InfluxDB and Grafana:
   - Ensure that InfluxDB is running locally or remotely and configured to accept data from the script.
   - Set up Grafana and connect it to your InfluxDB instance.

## Usage

1. Run the script to monitor cryptocurrencies:
   ```bash
   python monitor.py
   ```

2. Monitor the logs for alerts about EMA crossovers:
   - Example output:
     ```
     [INFO] BTC/USDT: 200-day EMA reached, and 9/21/50-day EMAs have crossed over.
     ```

3. Open Grafana to visualize the data:
   - Use the pre-configured dashboards to analyze price trends and EMA behavior.

## File Structure

- `monitor.py`: Main script for data fetching, EMA calculation, and monitoring.
- `requirements.txt`: List of Python dependencies.
- `.env`: Environment configuration file (user-created).

## Future Enhancements

- Add support for more cryptocurrencies.
- Incorporate additional technical indicators.
- Implement alerting mechanisms via email or messaging platforms.

## Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

