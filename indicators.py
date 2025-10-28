import pandas as pd
import numpy as np

class TechnicalIndicators:
    """Calculate various technical indicators for trading analysis"""
    
    def __init__(self, df):
        self.df = df.copy()
    
    def calculate_sma(self, period):
        """Simple Moving Average"""
        return self.df['Close'].rolling(window=period).mean()
    
    def calculate_ema(self, period):
        """Exponential Moving Average"""
        return self.df['Close'].ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, period=14):
        """Relative Strength Index"""
        delta = self.df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """Moving Average Convergence Divergence"""
        ema_fast = self.df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = self.df['Close'].ewm(span=slow, adjust=False).mean()
        
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal, adjust=False).mean()
        macd_hist = macd - macd_signal
        
        return macd, macd_signal, macd_hist
    
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """Bollinger Bands"""
        sma = self.df['Close'].rolling(window=period).mean()
        std = self.df['Close'].rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return upper_band, sma, lower_band
    
    def calculate_stochastic(self, period=14):
        """Stochastic Oscillator"""
        low_min = self.df['Low'].rolling(window=period).min()
        high_max = self.df['High'].rolling(window=period).max()
        
        k = 100 * (self.df['Close'] - low_min) / (high_max - low_min)
        d = k.rolling(window=3).mean()
        
        return k, d
    
    def calculate_atr(self, period=14):
        """Average True Range"""
        high_low = self.df['High'] - self.df['Low']
        high_close = np.abs(self.df['High'] - self.df['Close'].shift())
        low_close = np.abs(self.df['Low'] - self.df['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(period).mean()
        
        return atr
    
    def calculate_obv(self):
        """On-Balance Volume"""
        obv = (np.sign(self.df['Close'].diff()) * self.df['Volume']).fillna(0).cumsum()
        return obv
    
    def calculate_adx(self, period=14):
        """Average Directional Index"""
        high_diff = self.df['High'].diff()
        low_diff = -self.df['Low'].diff()
        
        pos_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        neg_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
        
        atr = self.calculate_atr(period)
        
        pos_di = 100 * (pos_dm.rolling(window=period).mean() / atr)
        neg_di = 100 * (neg_dm.rolling(window=period).mean() / atr)
        
        dx = 100 * np.abs(pos_di - neg_di) / (pos_di + neg_di)
        adx = dx.rolling(window=period).mean()
        
        return adx, pos_di, neg_di
    
    def calculate_cci(self, period=20):
        """Commodity Channel Index"""
        tp = (self.df['High'] + self.df['Low'] + self.df['Close']) / 3
        sma_tp = tp.rolling(window=period).mean()
        mad = tp.rolling(window=period).apply(lambda x: np.abs(x - x.mean()).mean())
        
        cci = (tp - sma_tp) / (0.015 * mad)
        return cci
    
    def calculate_williams_r(self, period=14):
        """Williams %R"""
        high_max = self.df['High'].rolling(window=period).max()
        low_min = self.df['Low'].rolling(window=period).min()
        
        williams_r = -100 * (high_max - self.df['Close']) / (high_max - low_min)
        return williams_r
    
    def calculate_mfi(self, period=14):
        """Money Flow Index"""
        typical_price = (self.df['High'] + self.df['Low'] + self.df['Close']) / 3
        money_flow = typical_price * self.df['Volume']
        
        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
        
        positive_mf = positive_flow.rolling(window=period).sum()
        negative_mf = negative_flow.rolling(window=period).sum()
        
        mfr = positive_mf / negative_mf
        mfi = 100 - (100 / (1 + mfr))
        
        return mfi
    
    def calculate_vwap(self):
        """Volume Weighted Average Price"""
        typical_price = (self.df['High'] + self.df['Low'] + self.df['Close']) / 3
        vwap = (typical_price * self.df['Volume']).cumsum() / self.df['Volume'].cumsum()
        return vwap
    
    def calculate_all(self):
        """Calculate all technical indicators"""
        indicators = {}
        
        # Moving Averages
        indicators['SMA_20'] = self.calculate_sma(20)
        indicators['SMA_50'] = self.calculate_sma(50)
        indicators['SMA_200'] = self.calculate_sma(200)
        indicators['EMA_12'] = self.calculate_ema(12)
        indicators['EMA_26'] = self.calculate_ema(26)
        
        # RSI
        indicators['RSI'] = self.calculate_rsi(14)
        
        # MACD
        macd, signal, hist = self.calculate_macd()
        indicators['MACD'] = macd
        indicators['MACD_signal'] = signal
        indicators['MACD_hist'] = hist
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands()
        indicators['BB_upper'] = bb_upper
        indicators['BB_middle'] = bb_middle
        indicators['BB_lower'] = bb_lower
        
        # Stochastic
        stoch_k, stoch_d = self.calculate_stochastic()
        indicators['Stoch_K'] = stoch_k
        indicators['Stoch_D'] = stoch_d
        
        # ATR
        indicators['ATR'] = self.calculate_atr()
        
        # OBV
        indicators['OBV'] = self.calculate_obv()
        
        # ADX
        adx, pos_di, neg_di = self.calculate_adx()
        indicators['ADX'] = adx
        indicators['Plus_DI'] = pos_di
        indicators['Minus_DI'] = neg_di
        
        # CCI
        indicators['CCI'] = self.calculate_cci()
        
        # Williams %R
        indicators['Williams_R'] = self.calculate_williams_r()
        
        # MFI
        indicators['MFI'] = self.calculate_mfi()
        
        # VWAP
        indicators['VWAP'] = self.calculate_vwap()
        
        return indicators
