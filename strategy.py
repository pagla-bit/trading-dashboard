import numpy as np
import pandas as pd

class TradingStrategy:
    """
    Combined trading strategy using multiple technical indicators
    Generates buy/sell signals with confidence scores
    """
    
    def __init__(self, df, indicators):
        self.df = df
        self.indicators = indicators
        self.current_price = df['Close'].iloc[-1]
    
    def analyze_trend(self):
        """Analyze trend using moving averages"""
        score = 0
        signals = {}
        
        # SMA crossover
        if self.indicators['SMA_20'].iloc[-1] > self.indicators['SMA_50'].iloc[-1]:
            score += 1
            signals['SMA_Crossover'] = 1
        elif self.indicators['SMA_20'].iloc[-1] < self.indicators['SMA_50'].iloc[-1]:
            score -= 1
            signals['SMA_Crossover'] = -1
        else:
            signals['SMA_Crossover'] = 0
        
        # Price vs SMA
        if self.current_price > self.indicators['SMA_20'].iloc[-1]:
            score += 0.5
            signals['Price_vs_SMA20'] = 1
        else:
            score -= 0.5
            signals['Price_vs_SMA20'] = -1
        
        # EMA alignment
        if self.indicators['EMA_12'].iloc[-1] > self.indicators['EMA_26'].iloc[-1]:
            score += 1
            signals['EMA_Alignment'] = 1
        else:
            score -= 1
            signals['EMA_Alignment'] = -1
        
        return score, signals
    
    def analyze_momentum(self):
        """Analyze momentum indicators"""
        score = 0
        signals = {}
        
        # RSI
        rsi = self.indicators['RSI'].iloc[-1]
        if rsi < 30:
            score += 2  # Oversold - strong buy
            signals['RSI'] = 2
        elif rsi < 40:
            score += 1  # Approaching oversold
            signals['RSI'] = 1
        elif rsi > 70:
            score -= 2  # Overbought - strong sell
            signals['RSI'] = -2
        elif rsi > 60:
            score -= 1  # Approaching overbought
            signals['RSI'] = -1
        else:
            signals['RSI'] = 0
        
        # MACD
        macd = self.indicators['MACD'].iloc[-1]
        signal = self.indicators['MACD_signal'].iloc[-1]
        hist = self.indicators['MACD_hist'].iloc[-1]
        
        if macd > signal and hist > 0:
            score += 1.5
            signals['MACD'] = 1
        elif macd < signal and hist < 0:
            score -= 1.5
            signals['MACD'] = -1
        else:
            signals['MACD'] = 0
        
        # Stochastic
        stoch_k = self.indicators['Stoch_K'].iloc[-1]
        stoch_d = self.indicators['Stoch_D'].iloc[-1]
        
        if stoch_k < 20 and stoch_k > stoch_d:
            score += 1.5
            signals['Stochastic'] = 1
        elif stoch_k > 80 and stoch_k < stoch_d:
            score -= 1.5
            signals['Stochastic'] = -1
        else:
            signals['Stochastic'] = 0
        
        # CCI
        cci = self.indicators['CCI'].iloc[-1]
        if cci < -100:
            score += 1
            signals['CCI'] = 1
        elif cci > 100:
            score -= 1
            signals['CCI'] = -1
        else:
            signals['CCI'] = 0
        
        # Williams %R
        williams = self.indicators['Williams_R'].iloc[-1]
        if williams < -80:
            score += 1
            signals['Williams_R'] = 1
        elif williams > -20:
            score -= 1
            signals['Williams_R'] = -1
        else:
            signals['Williams_R'] = 0
        
        # MFI (Money Flow Index)
        mfi = self.indicators['MFI'].iloc[-1]
        if mfi < 20:
            score += 1
            signals['MFI'] = 1
        elif mfi > 80:
            score -= 1
            signals['MFI'] = -1
        else:
            signals['MFI'] = 0
        
        return score, signals
    
    def analyze_volatility(self):
        """Analyze volatility and price position"""
        score = 0
        signals = {}
        
        # Bollinger Bands
        bb_upper = self.indicators['BB_upper'].iloc[-1]
        bb_lower = self.indicators['BB_lower'].iloc[-1]
        bb_middle = self.indicators['BB_middle'].iloc[-1]
        
        if self.current_price < bb_lower:
            score += 2  # Price below lower band - oversold
            signals['Bollinger_Bands'] = 2
        elif self.current_price < bb_middle:
            score += 1
            signals['Bollinger_Bands'] = 1
        elif self.current_price > bb_upper:
            score -= 2  # Price above upper band - overbought
            signals['Bollinger_Bands'] = -2
        elif self.current_price > bb_middle:
            score -= 1
            signals['Bollinger_Bands'] = -1
        else:
            signals['Bollinger_Bands'] = 0
        
        # ATR for volatility context
        atr = self.indicators['ATR'].iloc[-1]
        atr_pct = (atr / self.current_price) * 100
        
        if atr_pct > 5:
            signals['Volatility'] = 'High'
        elif atr_pct > 2:
            signals['Volatility'] = 'Medium'
        else:
            signals['Volatility'] = 'Low'
        
        return score, signals
    
    def analyze_volume(self):
        """Analyze volume patterns"""
        score = 0
        signals = {}
        
        # OBV trend
        obv = self.indicators['OBV']
        obv_sma = obv.rolling(window=20).mean()
        
        if obv.iloc[-1] > obv_sma.iloc[-1]:
            score += 1
            signals['OBV'] = 1
        else:
            score -= 1
            signals['OBV'] = -1
        
        # Volume spike
        avg_volume = self.df['Volume'].rolling(window=20).mean().iloc[-1]
        current_volume = self.df['Volume'].iloc[-1]
        
        if current_volume > avg_volume * 1.5:
            signals['Volume_Spike'] = 'High'
            # Volume confirmation
            price_change = self.df['Close'].iloc[-1] - self.df['Close'].iloc[-2]
            if price_change > 0:
                score += 0.5
            else:
                score -= 0.5
        else:
            signals['Volume_Spike'] = 'Normal'
        
        # VWAP
        vwap = self.indicators['VWAP'].iloc[-1]
        if self.current_price > vwap:
            score += 0.5
            signals['VWAP'] = 1
        else:
            score -= 0.5
            signals['VWAP'] = -1
        
        return score, signals
    
    def analyze_strength(self):
        """Analyze trend strength using ADX"""
        score = 0
        signals = {}
        
        adx = self.indicators['ADX'].iloc[-1]
        plus_di = self.indicators['Plus_DI'].iloc[-1]
        minus_di = self.indicators['Minus_DI'].iloc[-1]
        
        # ADX shows trend strength
        if adx > 25:
            signals['Trend_Strength'] = 'Strong'
            if plus_di > minus_di:
                score += 1
                signals['ADX_Direction'] = 1
            else:
                score -= 1
                signals['ADX_Direction'] = -1
        elif adx > 20:
            signals['Trend_Strength'] = 'Moderate'
            if plus_di > minus_di:
                score += 0.5
                signals['ADX_Direction'] = 1
            else:
                score -= 0.5
                signals['ADX_Direction'] = -1
        else:
            signals['Trend_Strength'] = 'Weak'
            signals['ADX_Direction'] = 0
        
        return score, signals
    
    def calculate_targets(self, signal, entry_price):
        """Calculate profit targets and stop loss"""
        if signal == "BUY":
            targets = {
                '3%': entry_price * 1.03,
                '5%': entry_price * 1.05,
                '10%': entry_price * 1.10
            }
            stop_loss = entry_price * 0.98  # 2% stop loss
        elif signal == "SELL":
            targets = {
                '3%': entry_price * 0.97,
                '5%': entry_price * 0.95,
                '10%': entry_price * 0.90
            }
            stop_loss = entry_price * 1.02  # 2% stop loss
        else:
            targets = {'3%': 0, '5%': 0, '10%': 0}
            stop_loss = 0
        
        return targets, stop_loss
    
    def generate_signal(self):
        """
        Generate trading signal based on all indicators
        Returns recommendation with confidence score
        """
        # Analyze all aspects
        trend_score, trend_signals = self.analyze_trend()
        momentum_score, momentum_signals = self.analyze_momentum()
        volatility_score, volatility_signals = self.analyze_volatility()
        volume_score, volume_signals = self.analyze_volume()
        strength_score, strength_signals = self.analyze_strength()
        
        # Combine all signals
        total_score = (
            trend_score * 1.5 +      # Trend is important
            momentum_score * 2.0 +    # Momentum is very important
            volatility_score * 1.0 +  # Volatility context
            volume_score * 1.2 +      # Volume confirmation
            strength_score * 1.0      # Trend strength
        )
        
        # Normalize to get confidence (0-100%)
        max_possible_score = abs(1.5 * 2.5 + 2.0 * 9.5 + 1.0 * 4 + 1.2 * 2 + 1.0 * 1.5)
        confidence = min(100, (abs(total_score) / max_possible_score) * 100)
        
        # Determine signal
        if total_score > 5:
            signal = "BUY"
        elif total_score < -5:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        # Calculate targets
        targets, stop_loss = self.calculate_targets(signal, self.current_price)
        
        # Combine all indicator signals
        all_signals = {
            **trend_signals,
            **momentum_signals,
            **volatility_signals,
            **volume_signals,
            **strength_signals
        }
        
        return {
            'signal': signal,
            'entry_price': self.current_price,
            'targets': targets,
            'stop_loss': stop_loss,
            'confidence': confidence,
            'total_score': total_score,
            'indicators': all_signals
        }
