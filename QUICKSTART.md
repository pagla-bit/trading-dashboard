# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

### 2. Run the App (10 seconds)

```bash
streamlit run app.py
```

### 3. Open Browser (automatic)

Your browser should automatically open to `http://localhost:8501`

If not, manually open: **http://localhost:8501**

### 4. Use the Dashboard

1. **Enter an instrument** in the sidebar (try "GC=F" for Gold)
2. Click **"Refresh Now"** to load data
3. View the **trading recommendation**
4. Explore **charts and indicators**
5. Enable **"Auto-refresh"** for live updates

## Popular Instrument Symbols

### Commodities
- Gold: `GC=F`
- Silver: `SI=F`
- Crude Oil: `CL=F`
- Natural Gas: `NG=F`

### Forex
- EUR/USD: `EURUSD=X`
- GBP/USD: `GBPUSD=X`
- USD/JPY: `JPY=X`
- USD/CHF: `CHF=X`

### Stock Indices
- S&P 500: `^GSPC`
- NASDAQ-100: `^NDX`
- Dow Jones: `^DJI`
- Russell 2000: `^RUT`

### Cryptocurrencies
- Bitcoin: `BTC-USD`
- Ethereum: `ETH-USD`
- Cardano: `ADA-USD`
- Solana: `SOL-USD`

### Popular Stocks
- Apple: `AAPL`
- Microsoft: `MSFT`
- Tesla: `TSLA`
- Amazon: `AMZN`
- Google: `GOOGL`
- NVIDIA: `NVDA`

## Understanding the Dashboard

### Top Metrics
- **Current Price**: Real-time price with % change
- **Volume**: Trading volume
- **RSI**: Momentum indicator (30=oversold, 70=overbought)
- **High/Low**: 24-hour range

### Trading Recommendation
- **Signal**: BUY 🟢 / SELL 🔴 / HOLD 🟡
- **Entry Price**: Suggested entry point
- **Confidence**: How confident the algorithm is (0-100%)
- **Stop Loss**: Where to exit if trade goes wrong
- **Profit Targets**: Three levels (3%, 5%, 10%)

### Charts
- **Price Chart**: Candlestick chart with volume bars
- **Technical Indicators**: All indicators visualized together

### Sidebar
- **Configuration**: Enter symbols and settings
- **Quick Select**: Fast access to popular instruments
- **Recent Recommendations**: History of signals

## Tips for Best Results

1. **Wait for High Confidence**: Signals with >70% confidence are stronger
2. **Check Multiple Timeframes**: Look at different periods
3. **Confirm with Volume**: Higher volume = more reliable signals
4. **Use Stop Losses**: Always protect your capital
5. **Don't Chase**: Wait for good entry points

## Common Issues

### "No data available"
- Check if symbol is correct
- Try adding suffix (e.g., `.L` for London stocks)
- Verify internet connection

### Slow Performance
- Close other programs
- Use shorter time periods
- Disable auto-refresh when not needed

### Indicators Not Showing
- Wait for more data to load
- Some indicators need minimum data points
- Try a longer time period

## Keyboard Shortcuts

- **Refresh Page**: `Ctrl+R` (Windows) / `Cmd+R` (Mac)
- **Toggle Sidebar**: Click hamburger menu (☰)
- **Zoom Charts**: Scroll wheel on chart area

## Next Steps

1. **Explore Different Instruments**: Try various markets
2. **Learn the Indicators**: Understand what each indicator means
3. **Track Performance**: Monitor which signals work best
4. **Customize**: Modify thresholds in `strategy.py`
5. **Deploy**: Follow `DEPLOYMENT.md` to go live

## Need Help?

- Read the full `README.md` for detailed information
- Check `DEPLOYMENT.md` for deployment instructions
- Review code comments for technical details

## Disclaimer

⚠️ **This tool is for educational purposes only. It is NOT financial advice.**

- Always do your own research
- Never invest more than you can afford to lose
- Past performance doesn't guarantee future results
- Consider consulting a financial advisor

---

**Happy Trading! 📈**

*Remember: The best trader is a disciplined trader.*
