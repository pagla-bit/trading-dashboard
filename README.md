# Live Trading Dashboard

A comprehensive Streamlit-based trading dashboard that provides real-time market analysis and trading recommendations using multiple technical indicators.

## Features

- **Real-time Market Data**: Live data from Yahoo Finance, updated every minute
- **Multiple Technical Indicators**: 
  - Moving Averages (SMA, EMA)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Stochastic Oscillator
  - ATR (Average True Range)
  - ADX (Average Directional Index)
  - CCI (Commodity Channel Index)
  - Williams %R
  - MFI (Money Flow Index)
  - OBV (On-Balance Volume)
  - VWAP (Volume Weighted Average Price)

- **Trading Recommendations**: 
  - BUY/SELL/HOLD signals with confidence scores
  - Entry prices
  - Three profit targets (3%, 5%, 10%)
  - Stop-loss recommendations

- **Interactive Charts**:
  - Candlestick price charts with volume
  - Technical indicator overlays
  - Historical data visualization

- **Database Storage**: 
  - Stores up to 100 most recent recommendations
  - SQLite database (no external database needed)

- **Alert System**: Visual alerts for buy/sell signals

- **Auto-refresh**: Optional 1-minute auto-refresh for live monitoring

## Supported Instruments

The dashboard supports any instrument available on Yahoo Finance, including:

- **Commodities**: Gold (GC=F), Silver (SI=F), Oil (CL=F)
- **Forex**: EUR/USD (EURUSD=X), GBP/USD (GBPUSD=X)
- **Indices**: NASDAQ-100 (^NDX), S&P 500 (^GSPC), Dow Jones (^DJI)
- **Cryptocurrencies**: Bitcoin (BTC-USD), Ethereum (ETH-USD)
- **Stocks**: Any stock symbol (e.g., AAPL, GOOGL, TSLA)

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd trading-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## Deployment to Streamlit Cloud

1. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push all files to the repository

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path: `app.py`
   - Click "Deploy"

3. **Important Notes**:
   - The app will automatically install dependencies from `requirements.txt`
   - The SQLite database will be created automatically
   - Free tier includes sufficient resources for this application

## Usage

1. **Select an Instrument**:
   - Enter a Yahoo Finance symbol in the sidebar (e.g., GC=F for Gold)
   - Or use the quick select buttons for common instruments

2. **View Analysis**:
   - Current price and key metrics are displayed at the top
   - Trading recommendation with confidence score
   - Entry price, stop-loss, and three profit targets

3. **Explore Charts**:
   - **Price Chart Tab**: Candlestick chart with volume
   - **Technical Indicators Tab**: All indicators visualized

4. **Enable Auto-Refresh**:
   - Check "Auto-refresh (1 min)" in the sidebar
   - The dashboard will update every minute automatically

5. **View History**:
   - Recent recommendations appear in the sidebar
   - Full history stored in database

## Technical Indicators Explained

### Trend Indicators
- **SMA (Simple Moving Average)**: Average price over a period
- **EMA (Exponential Moving Average)**: Weighted average giving more importance to recent prices

### Momentum Indicators
- **RSI**: Measures speed and magnitude of price changes (0-100)
  - Below 30: Oversold (potential buy)
  - Above 70: Overbought (potential sell)
- **MACD**: Shows relationship between two moving averages
- **Stochastic**: Compares closing price to price range over time

### Volatility Indicators
- **Bollinger Bands**: Price envelope around moving average
- **ATR**: Measures market volatility

### Volume Indicators
- **OBV**: Relates volume to price change
- **MFI**: Volume-weighted RSI
- **VWAP**: Average price weighted by volume

## Trading Strategy

The dashboard uses a **combined multi-indicator strategy**:

1. **Trend Analysis**: Moving average crossovers and alignment
2. **Momentum Analysis**: RSI, MACD, Stochastic, CCI, Williams %R, MFI
3. **Volatility Analysis**: Bollinger Bands, ATR
4. **Volume Analysis**: OBV, Volume spikes, VWAP
5. **Strength Analysis**: ADX for trend strength

Each indicator contributes to a composite score, which determines:
- **BUY signal**: Strong positive score (score > 5)
- **SELL signal**: Strong negative score (score < -5)
- **HOLD signal**: Neutral score (-5 to 5)

**Confidence Score**: Calculated based on the strength of all indicators combined (0-100%)

## File Structure

```
trading-dashboard/
├── app.py                 # Main Streamlit application
├── indicators.py          # Technical indicators calculations
├── strategy.py           # Trading strategy and signal generation
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── trading_recommendations.db  # SQLite database (auto-created)
```

## Customization

### Adjust Indicator Parameters

Edit `indicators.py` to modify default periods:
- RSI period (default: 14)
- MACD periods (default: 12, 26, 9)
- Bollinger Bands (default: 20, 2 std dev)

### Modify Strategy Weights

Edit `strategy.py` in the `generate_signal()` method to adjust how much each indicator category influences the final signal.

### Change Signal Thresholds

Modify the score thresholds in `strategy.py`:
```python
if total_score > 5:  # Adjust this for more/less aggressive BUY signals
    signal = "BUY"
elif total_score < -5:  # Adjust this for more/less aggressive SELL signals
    signal = "SELL"
```

### Adjust Profit Targets

Edit `calculate_targets()` in `strategy.py` to modify profit targets and stop-loss percentages.

## Important Disclaimers

⚠️ **This dashboard is for educational and informational purposes only.**

- Not financial advice
- Past performance does not guarantee future results
- Always do your own research before trading
- Consider consulting with a financial advisor
- Trading involves risk of loss
- The creators are not responsible for any trading losses

## Yahoo Finance API Limits

Yahoo Finance is free but has rate limits:
- Avoid making too many rapid requests
- The 1-minute update interval is safe for normal use
- If you encounter rate limiting, increase the refresh interval

## Troubleshooting

### Data Not Loading
- Verify the symbol is correct for Yahoo Finance
- Check your internet connection
- Some symbols may require specific suffixes (e.g., .L for London stocks)

### Indicators Not Calculating
- Ensure sufficient historical data is available
- Some indicators require minimum data points (e.g., 200 for SMA-200)

### Database Errors
- Delete `trading_recommendations.db` to reset the database
- Ensure write permissions in the application directory

## Future Enhancements

Possible additions:
- Email/SMS alerts
- Multiple watchlists
- Backtesting capabilities
- Performance tracking
- More chart types
- Custom indicator builder
- Paper trading simulation

## Contributing

Feel free to fork this repository and submit pull requests for improvements!

## License

MIT License - Feel free to use and modify for your needs.

## Support

For issues or questions:
- Open an issue on GitHub
- Check Yahoo Finance API documentation
- Review Streamlit documentation

---

**Happy Trading! 📈**

*Remember: Always trade responsibly and never risk more than you can afford to lose.*
