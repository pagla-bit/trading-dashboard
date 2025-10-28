import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from database import Database
from indicators import TechnicalIndicators
from strategy import TradingStrategy

# Page configuration
st.set_page_config(
    page_title="Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db = Database()

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .buy-signal {
        color: #00ff00;
        font-weight: bold;
        font-size: 24px;
    }
    .sell-signal {
        color: #ff0000;
        font-weight: bold;
        font-size: 24px;
    }
    .hold-signal {
        color: #ffaa00;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_market_data(symbol, period="3mo", interval="1m"):
    """Fetch market data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def create_candlestick_chart(df, symbol):
    """Create candlestick chart with volume"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{symbol} Price', 'Volume'),
        row_heights=[0.7, 0.3]
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # Volume bars
    colors = ['red' if df['Close'].iloc[i] < df['Open'].iloc[i] else 'green' 
              for i in range(len(df))]
    fig.add_trace(
        go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color=colors),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        xaxis_rangeslider_visible=False
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

def create_indicators_chart(df, indicators_data):
    """Create technical indicators chart"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Price with Moving Averages', 'RSI', 'MACD'),
        row_heights=[0.5, 0.25, 0.25]
    )
    
    # Price with MAs
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Close'], name='Close', line=dict(color='blue')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['SMA_20'], name='SMA 20', 
                   line=dict(color='orange', dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['SMA_50'], name='SMA 50', 
                   line=dict(color='red', dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['EMA_12'], name='EMA 12', 
                   line=dict(color='purple', dash='dot')),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['BB_upper'], name='BB Upper',
                   line=dict(color='gray', dash='dash'), opacity=0.5),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['BB_lower'], name='BB Lower',
                   line=dict(color='gray', dash='dash'), opacity=0.5,
                   fill='tonexty', fillcolor='rgba(128,128,128,0.2)'),
        row=1, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['RSI'], name='RSI', 
                   line=dict(color='purple')),
        row=2, col=1
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # MACD
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['MACD'], name='MACD', 
                   line=dict(color='blue')),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=indicators_data['MACD_signal'], name='Signal', 
                   line=dict(color='red')),
        row=3, col=1
    )
    fig.add_trace(
        go.Bar(x=df.index, y=indicators_data['MACD_hist'], name='Histogram'),
        row=3, col=1
    )
    
    fig.update_layout(height=800, showlegend=True)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    
    return fig

def display_recommendation(signal, entry_price, targets, stop_loss, confidence):
    """Display trading recommendation"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if signal == "BUY":
            st.markdown('<p class="buy-signal">🟢 BUY SIGNAL</p>', unsafe_allow_html=True)
        elif signal == "SELL":
            st.markdown('<p class="sell-signal">🔴 SELL SIGNAL</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="hold-signal">🟡 HOLD</p>', unsafe_allow_html=True)
    
    with col2:
        st.metric("Entry Price", f"${entry_price:.2f}")
        st.metric("Stop Loss", f"${stop_loss:.2f}")
    
    with col3:
        st.metric("Confidence", f"{confidence:.1f}%")
    
    if signal in ["BUY", "SELL"]:
        st.subheader("Profit Targets")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**3% Target**\n\n${targets['3%']:.2f}")
        with col2:
            st.info(f"**5% Target**\n\n${targets['5%']:.2f}")
        with col3:
            st.info(f"**10% Target**\n\n${targets['10%']:.2f}")

def main():
    st.title("📈 Live Trading Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Instrument selection
        instrument = st.text_input(
            "Enter Instrument Symbol",
            value="GC=F",
            help="Examples: GC=F (Gold), EURUSD=X (EUR/USD), ^NDX (NASDAQ-100)"
        )
        
        st.markdown("---")
        st.subheader("Common Instruments")
        if st.button("Gold (GC=F)"):
            instrument = "GC=F"
        if st.button("EUR/USD (EURUSD=X)"):
            instrument = "EURUSD=X"
        if st.button("NASDAQ-100 (^NDX)"):
            instrument = "^NDX"
        if st.button("S&P 500 (^GSPC)"):
            instrument = "^GSPC"
        if st.button("Bitcoin (BTC-USD)"):
            instrument = "BTC-USD"
        
        st.markdown("---")
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-refresh (1 min)", value=False)
        
        if st.button("🔄 Refresh Now"):
            st.rerun()
        
        st.markdown("---")
        st.subheader("Recent Recommendations")
        recent = db.get_recent_recommendations(5)
        if not recent.empty:
            for _, rec in recent.iterrows():
                with st.expander(f"{rec['symbol']} - {rec['signal']}"):
                    st.write(f"Time: {rec['timestamp']}")
                    st.write(f"Price: ${rec['entry_price']:.2f}")
                    st.write(f"Confidence: {rec['confidence']:.1f}%")
    
    # Main content
    if instrument:
        try:
            # Fetch data
            with st.spinner("Fetching market data..."):
                df = get_market_data(instrument, period="3mo", interval="1m")
            
            if df is not None and not df.empty:
                # Calculate indicators
                ti = TechnicalIndicators(df)
                indicators_data = ti.calculate_all()
                
                # Generate trading signal
                strategy = TradingStrategy(df, indicators_data)
                recommendation = strategy.generate_signal()
                
                # Display current price and key metrics
                current_price = df['Close'].iloc[-1]
                price_change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
                price_change_pct = (price_change / df['Close'].iloc[-2]) * 100
                
                st.header(f"{instrument}")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric(
                        "Current Price",
                        f"${current_price:.2f}",
                        f"{price_change_pct:+.2f}%"
                    )
                
                with col2:
                    st.metric("Volume", f"{df['Volume'].iloc[-1]:,.0f}")
                
                with col3:
                    st.metric("RSI", f"{indicators_data['RSI'].iloc[-1]:.1f}")
                
                with col4:
                    st.metric("High (24h)", f"${df['High'].max():.2f}")
                
                with col5:
                    st.metric("Low (24h)", f"${df['Low'].min():.2f}")
                
                st.markdown("---")
                
                # Display recommendation
                st.header("Trading Recommendation")
                display_recommendation(
                    recommendation['signal'],
                    recommendation['entry_price'],
                    recommendation['targets'],
                    recommendation['stop_loss'],
                    recommendation['confidence']
                )
                
                # Save to database
                if recommendation['signal'] in ["BUY", "SELL"]:
                    db.add_recommendation(
                        symbol=instrument,
                        signal=recommendation['signal'],
                        entry_price=recommendation['entry_price'],
                        target_3=recommendation['targets']['3%'],
                        target_5=recommendation['targets']['5%'],
                        target_10=recommendation['targets']['10%'],
                        stop_loss=recommendation['stop_loss'],
                        confidence=recommendation['confidence'],
                        indicators=str(recommendation['indicators'])
                    )
                
                st.markdown("---")
                
                # Charts
                tab1, tab2 = st.tabs(["📊 Price Chart", "📈 Technical Indicators"])
                
                with tab1:
                    st.plotly_chart(create_candlestick_chart(df, instrument), use_container_width=True)
                
                with tab2:
                    st.plotly_chart(create_indicators_chart(df, indicators_data), use_container_width=True)
                
                # Detailed indicators
                with st.expander("📊 Detailed Indicator Values"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("Trend Indicators")
                        st.write(f"SMA 20: ${indicators_data['SMA_20'].iloc[-1]:.2f}")
                        st.write(f"SMA 50: ${indicators_data['SMA_50'].iloc[-1]:.2f}")
                        st.write(f"EMA 12: ${indicators_data['EMA_12'].iloc[-1]:.2f}")
                        st.write(f"EMA 26: ${indicators_data['EMA_26'].iloc[-1]:.2f}")
                    
                    with col2:
                        st.subheader("Momentum Indicators")
                        st.write(f"RSI: {indicators_data['RSI'].iloc[-1]:.2f}")
                        st.write(f"MACD: {indicators_data['MACD'].iloc[-1]:.4f}")
                        st.write(f"MACD Signal: {indicators_data['MACD_signal'].iloc[-1]:.4f}")
                        st.write(f"Stochastic: {indicators_data['Stoch_K'].iloc[-1]:.2f}")
                    
                    with col3:
                        st.subheader("Volatility Indicators")
                        st.write(f"BB Upper: ${indicators_data['BB_upper'].iloc[-1]:.2f}")
                        st.write(f"BB Middle: ${indicators_data['BB_middle'].iloc[-1]:.2f}")
                        st.write(f"BB Lower: ${indicators_data['BB_lower'].iloc[-1]:.2f}")
                        st.write(f"ATR: {indicators_data['ATR'].iloc[-1]:.2f}")
                
                # Signal explanation
                with st.expander("🔍 Signal Breakdown"):
                    st.write("**Factors Contributing to Signal:**")
                    for indicator, value in recommendation['indicators'].items():
                        if value > 0:
                            st.success(f"✓ {indicator}: Bullish signal")
                        elif value < 0:
                            st.error(f"✗ {indicator}: Bearish signal")
                        else:
                            st.info(f"○ {indicator}: Neutral")
                
                # Last update time
                st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Auto-refresh
                if auto_refresh:
                    time.sleep(60)
                    st.rerun()
            
            else:
                st.error("No data available for this instrument. Please check the symbol.")
        
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Please make sure you entered a valid Yahoo Finance symbol.")

if __name__ == "__main__":
    main()
