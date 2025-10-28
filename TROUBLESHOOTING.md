# Troubleshooting Guide

## Common Issues and Solutions

### 1. Installation Issues

#### Problem: `pip install -r requirements.txt` fails

**Solution A: Update pip**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Solution B: Install packages individually**
```bash
pip install streamlit==1.29.0
pip install yfinance==0.2.33
pip install pandas==2.1.4
pip install numpy==1.26.2
pip install plotly==5.18.0
```

**Solution C: Use virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Problem: `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
pip install xxx
# or
pip install -r requirements.txt --force-reinstall
```

### 2. Data Fetching Issues

#### Problem: "No data available for this instrument"

**Possible Causes & Solutions:**

1. **Wrong Symbol Format**
   - ✅ Correct: `GC=F` (Gold futures)
   - ❌ Wrong: `GOLD`, `GC`, `GCF`
   
   Check Yahoo Finance website for correct symbol format.

2. **Market Closed / No Recent Data**
   - Some instruments only trade during specific hours
   - Try a major index like `^GSPC` (S&P 500)
   - Wait for market opening hours

3. **Delisted / Invalid Symbol**
   - Verify symbol exists on Yahoo Finance
   - Some symbols may have changed

**Quick Test:**
```python
import yfinance as yf
ticker = yf.Ticker("GC=F")
print(ticker.history(period="1d"))
```

#### Problem: Data loads but shows "NaN" values

**Solution:**
- Not enough historical data for indicator calculation
- Try a longer period: Change in `app.py`:
  ```python
  df = get_market_data(instrument, period="6mo", interval="1m")
  ```

#### Problem: "Rate limit exceeded" or slow loading

**Solution:**
- Yahoo Finance has rate limits
- Wait 1-2 minutes between requests
- Disable auto-refresh temporarily
- Use longer intervals for testing

### 3. Indicator Calculation Issues

#### Problem: Indicators not displaying / showing NaN

**Cause:** Not enough data points

**Solution:**
```python
# In indicators.py, adjust periods
def calculate_sma(self, period=20):  # Reduce from 50 or 200
    return self.df['Close'].rolling(window=period).mean()
```

**Or fetch more data:**
```python
# In app.py
df = get_market_data(instrument, period="1y", interval="1d")
```

#### Problem: RSI always shows extreme values (0 or 100)

**Cause:** Insufficient price variation

**Solution:**
- Check if instrument is actively trading
- Try a different, more liquid instrument
- Verify data quality

### 4. Chart Display Issues

#### Problem: Charts not rendering

**Solution A: Clear Streamlit cache**
```bash
streamlit cache clear
```

**Solution B: Update Plotly**
```bash
pip install --upgrade plotly
```

**Solution C: Check browser console**
- Press F12 in browser
- Look for JavaScript errors
- Try a different browser

#### Problem: Charts display but are empty

**Cause:** Data filtering issue

**Solution:**
- Check if DataFrame is empty: `print(df.head())`
- Verify date range has data
- Try different time period

### 5. Database Issues

#### Problem: "database is locked"

**Solution:**
```bash
# Close any other instances of the app
# Delete and recreate database
rm trading_recommendations.db
streamlit run app.py
```

#### Problem: Recommendations not saving

**Solution:**
Check database permissions:
```bash
ls -la trading_recommendations.db
# Should have write permissions

# On Windows:
dir trading_recommendations.db
```

**Create database manually:**
```python
from database import Database
db = Database()
db.init_database()
```

### 6. Signal Generation Issues

#### Problem: Always shows "HOLD" signal

**Possible Causes:**

1. **Not enough data volatility**
   - Try a more volatile instrument
   - Check if market is open

2. **Thresholds too strict**
   - Reduce thresholds in `strategy.py`:
     ```python
     if total_score > 3:  # Changed from 5
         signal = "BUY"
     elif total_score < -3:  # Changed from -5
         signal = "SELL"
     ```

3. **All indicators neutral**
   - Normal during sideways markets
   - Wait for market movement

#### Problem: Confidence always low

**Solution:**
- Normal for ranging markets
- Check if indicators are conflicting
- Review indicator values in expandable section

#### Problem: Wrong buy/sell signals

**Remember:**
- Technical analysis is NOT 100% accurate
- Signals are based on historical patterns
- Always verify with your own analysis
- Not financial advice

### 7. Performance Issues

#### Problem: App is slow

**Solution A: Reduce data amount**
```python
# In app.py, change period
df = get_market_data(instrument, period="1mo", interval="5m")
```

**Solution B: Optimize indicators**
```python
# Calculate only needed indicators
def calculate_essential(self):
    indicators = {}
    indicators['RSI'] = self.calculate_rsi(14)
    indicators['MACD'], indicators['MACD_signal'], _ = self.calculate_macd()
    # Add only what you need
    return indicators
```

**Solution C: Disable auto-refresh**
- Uncheck "Auto-refresh" in sidebar
- Manually refresh when needed

#### Problem: Memory errors

**Solution:**
- Reduce data period
- Clear old database records
- Restart the app

### 8. Streamlit-Specific Issues

#### Problem: "Port 8501 is already in use"

**Solution:**
```bash
# Find and kill process using port 8501
# On Mac/Linux:
lsof -ti:8501 | xargs kill -9

# On Windows:
netstat -ano | findstr :8501
taskkill /PID <process_id> /F

# Or use different port:
streamlit run app.py --server.port 8502
```

#### Problem: App doesn't auto-reload on code changes

**Solution:**
```bash
# Run in development mode (default)
streamlit run app.py

# If not working, manually refresh browser
# Or restart: Ctrl+C then run again
```

#### Problem: Widgets not responding

**Solution:**
- Clear browser cache
- Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- Check browser console for errors

### 9. Deployment Issues (Streamlit Cloud)

#### Problem: App crashes after deployment

**Check Logs:**
1. Go to Streamlit Cloud dashboard
2. Click "Manage app"
3. View logs for error messages

**Common Causes:**

1. **Missing dependencies**
   - Verify `requirements.txt` is complete
   - Check for typos in package names

2. **Python version incompatibility**
   - Add `.streamlit/config.toml` with Python version
   - Or add `runtime.txt`:
     ```
     python-3.9
     ```

3. **File path issues**
   - Use relative paths, not absolute
   - Check file names (case-sensitive on Linux)

#### Problem: "App is sleeping" or takes long to wake

**This is normal for free tier:**
- Apps sleep after inactivity
- First visit after sleep takes 30-60 seconds
- Upgrade to paid tier for always-on apps

#### Problem: Can't access database

**Solution:**
- SQLite works on Streamlit Cloud
- Database is recreated on each deployment
- Data persists between sessions, not deployments

### 10. Data Accuracy Issues

#### Problem: Prices don't match other sources

**Reasons:**
1. **Time delay**: Yahoo Finance has slight delay
2. **Data source differences**: Different exchanges
3. **Bid/Ask spread**: May see different prices

**Verification:**
- Check timestamp of data
- Compare with Yahoo Finance website
- Consider this for educational use

#### Problem: Volume seems wrong

**Reasons:**
1. **Cumulative volume**: Some intervals show cumulative
2. **Low liquidity**: Some instruments trade less
3. **After-hours trading**: May have low volume

### 11. Auto-Refresh Issues

#### Problem: Auto-refresh not working

**Solution:**
```python
# Check in app.py that this code exists:
if auto_refresh:
    time.sleep(60)
    st.rerun()  # or st.experimental_rerun() in older versions
```

**Or:**
- Manually click "Refresh Now" button
- Check browser console for errors
- Ensure checkbox is actually checked

#### Problem: Auto-refresh too fast/slow

**Adjust timing:**
```python
# In app.py, change sleep time
time.sleep(120)  # Refresh every 2 minutes
```

### 12. Browser-Specific Issues

#### Chrome
- Clear cache: Ctrl+Shift+Delete
- Disable extensions
- Try incognito mode

#### Firefox
- Clear cache
- Check privacy settings
- Disable tracking protection for localhost

#### Safari
- Enable JavaScript
- Clear website data
- Check privacy settings

#### Mobile
- Use desktop mode
- Rotate to landscape for better view
- Some features may be limited

## Error Messages Decoded

### "KeyError: 'Close'"
- Data fetch failed
- Symbol might be invalid
- Check internet connection

### "IndexError: single positional indexer is out-of-bounds"
- Not enough data points
- Try longer time period
- Use different interval

### "ValueError: Length mismatch"
- Indicator calculation issue
- Check data alignment
- May need data cleanup

### "ConnectionError" or "Timeout"
- Network issue
- Yahoo Finance temporarily down
- Check internet connection
- Try again in a few minutes

### "sqlite3.OperationalError: database is locked"
- Another process using database
- Close other instances
- Restart app

## Best Practices to Avoid Issues

1. **Start Simple**
   - Test with one reliable symbol first (e.g., `^GSPC`)
   - Enable features gradually

2. **Monitor Data Quality**
   - Check raw data before indicators
   - Verify timestamps make sense
   - Look for gaps or anomalies

3. **Handle Errors Gracefully**
   - Use try-except blocks
   - Provide fallback values
   - Show meaningful error messages

4. **Regular Maintenance**
   - Update packages periodically
   - Clean old database records
   - Review and optimize code

5. **Testing**
   - Test with multiple instruments
   - Test during market hours and after hours
   - Test with different time periods

## Still Having Issues?

### Debug Mode

Add debugging to `app.py`:
```python
import streamlit as st

# At the top of main()
st.write("Debug Info:")
st.write(f"Symbol: {instrument}")
st.write(f"Data shape: {df.shape}")
st.write(f"Latest price: {df['Close'].iloc[-1]}")
st.write(f"Data range: {df.index[0]} to {df.index[-1]}")
```

### Check Versions

```python
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly

st.write(f"Streamlit: {st.__version__}")
st.write(f"yfinance: {yf.__version__}")
st.write(f"pandas: {pd.__version__}")
st.write(f"numpy: {np.__version__}")
st.write(f"plotly: {plotly.__version__}")
```

### Minimal Test App

Create `test.py`:
```python
import streamlit as st
import yfinance as yf

st.title("Minimal Test")

symbol = st.text_input("Symbol", "GC=F")

if st.button("Fetch"):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d")
        st.write(df)
        st.success("Success!")
    except Exception as e:
        st.error(f"Error: {e}")
```

Run: `streamlit run test.py`

### Get Help

1. **Check Logs**: Always check error messages
2. **Search Online**: Google the error message
3. **Streamlit Forum**: https://discuss.streamlit.io
4. **yFinance Issues**: https://github.com/ranaroussi/yfinance/issues
5. **Stack Overflow**: Tag with `streamlit` and `yfinance`

## Emergency Reset

If everything breaks:

```bash
# Backup your customizations first!

# Delete virtual environment
rm -rf venv/

# Delete database
rm trading_recommendations.db

# Delete cache
rm -rf __pycache__/
rm -rf .streamlit/

# Reinstall
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run fresh
streamlit run app.py
```

---

**Most issues are easily fixable with the solutions above. Don't give up! 💪**
