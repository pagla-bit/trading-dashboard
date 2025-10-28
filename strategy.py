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
        try:
            self.current_price = float(df['Close'].iloc[-1])
        except (TypeError, ValueError, KeyError, IndexError) as e:
            print(f"Error getting current price: {e}")
            self.current_price = 0.0
    
    def safe_get_value(self, indicator_name):
        """Safely extract indicator value and convert to float"""
        try:
            value = self.indicators[indicator_name].iloc[-1]
            if pd.isna(value):
                return None
            return float(value)
        except (KeyError, IndexError, TypeError, ValueError):
            return None
    
    def safe_compare(self, val1, val2, default=0):
        """Safely compare two values, return default if either is None"""
        if val1 is None or val2 is None:
            return default
        try:
            val1 = float(val1)
            val2 = float(val2)
            return val1, val2
        except (TypeError, ValueError):
            return default
    
    def analyze_trend(self):
        """Analyze trend using moving averages"""
        score = 0
        signals = {}
        
        # Get values safely
        sma_20 = self.safe_get_value('SMA_20')
        sma_50 = self.safe_get_value('SMA_50')
        ema_12 = self.safe_get_value('EMA_12')
        ema_26 = self.safe_get_value('EMA_26')
        
        # SMA crossover
        if sma_20 is not None and sma_50 is not None:
            if sma_20 > sma_50:
                score += 1
                signals['SMA_Crossover'] = 1
            elif sma_20 < sma_50:
                score -= 1
                signals['SMA_Crossover'] = -1
            else:
                signals['SMA_Crossover'] = 0
        else:
            signals['SMA_Crossover'] = 0
        
        # Price vs SMA
        if sma_20 is not None:
            if self.current_price > sma_20:
                score += 0.5
                signals['Price_vs_SMA20'] = 1
            else:
                score -= 0.5
                signals['Price_vs_SMA20'] = -1
        else:
            signals['Price_vs_SMA20'] = 0
        
        # EMA alignment
        if ema_12 is not None and ema_26 is not None:
            if ema_12 > ema_26:
                score += 1
                signals['EMA_Alignment'] = 1
            else:
                score -= 1
                signals['EMA_Alignment'] = -1
        else:
            signals['EMA_Alignment'] = 0
        
        return score, signals
    
    def analyze_momentum(self):
        """Analyze momentum indicators"""
        score = 0
        signals = {}
        
        # RSI
        rsi = self.safe_get_value('RSI')
        if rsi is not None:
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
        else:
            signals['RSI'] = 0
        
        # MACD
        macd = self.safe_get_value('MACD')
        macd_signal = self.safe_get_value('MACD_signal')
        hist = self.safe_get_value('MACD_hist')
        
        if macd is not None and macd_signal is not None and hist is not None:
            if macd > macd_signal and hist > 0:
                score += 1.5
                signals['MACD'] = 1
            elif macd < macd_signal and hist < 0:
                score -= 1.5
                signals['MACD'] = -1
            else:
                signals['MACD'] = 0
        else:
            signals['MACD'] = 0
        
        # Stochastic
        stoch_k = self.safe_get_value('Stoch_K')
        stoch_d = self.safe_get_value('Stoch_D')
        
        if stoch_k is not None and stoch_d is not None:
            if stoch_k < 20 and stoch_k > stoch_d:
                score += 1.5
                signals['Stochastic'] = 1
            elif stoch_k > 80 and stoch_k < stoch_d:
                score -= 1.5
                signals['Stochastic'] = -1
            else:
                signals['Stochastic'] = 0
        else:
            signals['Stochastic'] = 0
        
        # CCI
        cci = self.safe_get_value('CCI')
        if cci is not None:
            if cci < -100:
                score += 1
                signals['CCI'] = 1
            elif cci > 100:
                score -= 1
                signals['CCI'] = -1
            else:
                signals['CCI'] = 0
        else:
            signals['CCI'] = 0
        
        # Williams %R
        williams = self.safe_get_value('Williams_R')
        if williams is not None:
            if williams < -80:
                score += 1
                signals['Williams_R'] = 1
            elif williams > -20:
                score -= 1
                signals['Williams_R'] = -1
            else:
                signals['Williams_R'] = 0
        else:
            signals['Williams_R'] = 0
        
        # MFI (Money Flow Index)
        mfi = self.safe_get_value('MFI')
        if mfi is not None:
            if mfi < 20:
                score += 1
                signals['MFI'] = 1
            elif mfi > 80:
                score -= 1
                signals['MFI'] = -1
            else:
                signals['MFI'] = 0
        else:
            signals['MFI'] = 0
        
        return score, signals
    
    def analyze_volatility(self):
        """Analyze volatility and price position"""
        score = 0
        signals = {}
        
        # Bollinger Bands
        bb_upper = self.safe_get_value('BB_upper')
        bb_lower = self.safe_get_value('BB_lower')
        bb_middle = self.safe_get_value('BB_middle')
        
        if bb_upper is not None and bb_lower is not None and bb_middle is not None:
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
        else:
            signals['Bollinger_Bands'] = 0
        
        # ATR for volatility context
        atr = self.safe_get_value('ATR')
        if atr is not None and atr > 0:
            atr_pct = (atr / self.current_price) * 100
            
            if atr_pct > 5:
                signals['Volatility'] = 'High'
            elif atr_pct > 2:
                signals['Volatility'] = 'Medium'
            else:
                signals['Volatility'] = 'Low'
        else:
            signals['Volatility'] = 'Unknown'
        
        return score, signals
    
    def analyze_volume(self):
        """Analyze volume patterns"""
        score = 0
        signals = {}
        
        try:
            # OBV trend
            obv = self.indicators['OBV']
            obv_sma = obv.rolling(window=20).mean()
            
            obv_val = self.safe_get_value('OBV')
            obv_sma_val = float(obv_sma.iloc[-1]) if not pd.isna(obv_sma.iloc[-1]) else None
            
            if obv_val is not None and obv_sma_val is not None:
                if obv_val > obv_sma_val:
                    score += 1
                    signals['OBV'] = 1
                else:
                    score -= 1
                    signals['OBV'] = -1
            else:
                signals['OBV'] = 0
        except Exception:
            signals['OBV'] = 0
        
        try:
            # Volume spike
            avg_volume = self.df['Volume'].rolling(window=20).mean().iloc[-1]
            current_volume = float(self.df['Volume'].iloc[-1])
            
            if not pd.isna(avg_volume) and not pd.isna(current_volume):
                if current_volume > float(avg_volume) * 1.5:
                    signals['Volume_Spike'] = 'High'
                    # Volume confirmation
                    price_change = float(self.df['Close'].iloc[-1]) - float(self.df['Close'].iloc[-2])
                    if price_change > 0:
                        score += 0.5
                    else:
                        score -= 0.5
                else:
                    signals['Volume_Spike'] = 'Normal'
            else:
                signals['Volume_Spike'] = 'Normal'
        except Exception:
            signals['Volume_Spike'] = 'Normal'
        
        # VWAP
        vwap = self.safe_get_value('VWAP')
        if vwap is not None:
            if self.current_price > vwap:
                score += 0.5
                signals['VWAP'] = 1
            else:
                score -= 0.5
                signals['VWAP'] = -1
        else:
            signals['VWAP'] = 0
        
        return score, signals
    
    def analyze_strength(self):
        """Analyze trend strength using ADX"""
        score = 0
        signals = {}
        
        adx = self.safe_get_value('ADX')
        plus_di = self.safe_get_value('Plus_DI')
        minus_di = self.safe_get_value('Minus_DI')
        
        # ADX shows trend strength
        if adx is not None and plus_di is not None and minus_di is not None:
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
        else:
            signals['Trend_Strength'] = 'Unknown'
            signals['ADX_Direction'] = 0
        
        return score, signals
    
    def calculate_targets(self, signal, entry_price, margin=1000, leverage=1, position_size=1):
        """
        Calculate profit targets and stop loss for CFD trading
        
        Args:
            signal: BUY/SELL/HOLD
            entry_price: Entry price for the trade
            margin: Trading margin/capital (default: $1000)
            leverage: Leverage multiplier (default: 1x, no leverage)
            position_size: Number of units/contracts (default: 1)
        
        Returns:
            targets: Dictionary with profit targets
            stop_loss: Stop loss price
            cfd_calculations: Dictionary with CFD-specific calculations
        """
        cfd_calculations = {
            'margin': margin,
            'leverage': leverage,
            'position_size': position_size,
            'effective_capital': margin * leverage,
            'cost_per_unit': entry_price,
            'total_position_value': entry_price * position_size,
            'required_margin': (entry_price * position_size) / leverage if leverage > 0 else entry_price * position_size,
            'profit_3pct': 0,
            'profit_5pct': 0,
            'profit_10pct': 0,
            'loss_at_stop': 0
        }
        
        if signal == "BUY":
            # Long position - profit when price goes up
            targets = {
                '3%': entry_price * 1.03,
                '5%': entry_price * 1.05,
                '10%': entry_price * 1.10
            }
            stop_loss = entry_price * 0.98  # 2% stop loss
            
            # Calculate actual profit/loss in dollars with leverage
            price_move_3pct = (targets['3%'] - entry_price) * position_size
            price_move_5pct = (targets['5%'] - entry_price) * position_size
            price_move_10pct = (targets['10%'] - entry_price) * position_size
            price_move_stop = (stop_loss - entry_price) * position_size
            
            cfd_calculations['profit_3pct'] = price_move_3pct * leverage
            cfd_calculations['profit_5pct'] = price_move_5pct * leverage
            cfd_calculations['profit_10pct'] = price_move_10pct * leverage
            cfd_calculations['loss_at_stop'] = price_move_stop * leverage
            
            # Calculate ROI on margin
            cfd_calculations['roi_3pct'] = (cfd_calculations['profit_3pct'] / margin) * 100
            cfd_calculations['roi_5pct'] = (cfd_calculations['profit_5pct'] / margin) * 100
            cfd_calculations['roi_10pct'] = (cfd_calculations['profit_10pct'] / margin) * 100
            cfd_calculations['roi_at_stop'] = (cfd_calculations['loss_at_stop'] / margin) * 100
            
        elif signal == "SELL":
            # Short position - profit when price goes down
            targets = {
                '3%': entry_price * 0.97,
                '5%': entry_price * 0.95,
                '10%': entry_price * 0.90
            }
            stop_loss = entry_price * 1.02  # 2% stop loss
            
            # Calculate actual profit/loss in dollars with leverage
            price_move_3pct = (entry_price - targets['3%']) * position_size
            price_move_5pct = (entry_price - targets['5%']) * position_size
            price_move_10pct = (entry_price - targets['10%']) * position_size
            price_move_stop = (entry_price - stop_loss) * position_size
            
            cfd_calculations['profit_3pct'] = price_move_3pct * leverage
            cfd_calculations['profit_5pct'] = price_move_5pct * leverage
            cfd_calculations['profit_10pct'] = price_move_10pct * leverage
            cfd_calculations['loss_at_stop'] = price_move_stop * leverage
            
            # Calculate ROI on margin
            cfd_calculations['roi_3pct'] = (cfd_calculations['profit_3pct'] / margin) * 100
            cfd_calculations['roi_5pct'] = (cfd_calculations['profit_5pct'] / margin) * 100
            cfd_calculations['roi_10pct'] = (cfd_calculations['profit_10pct'] / margin) * 100
            cfd_calculations['roi_at_stop'] = (cfd_calculations['loss_at_stop'] / margin) * 100
            
        else:
            targets = {'3%': 0, '5%': 0, '10%': 0}
            stop_loss = 0
        
        return targets, stop_loss, cfd_calculations
    
    def generate_signal(self, margin=1000, leverage=1, position_size=1):
        """
        Generate trading signal based on all indicators
        Returns recommendation with confidence score and CFD calculations
        
        Args:
            margin: Trading capital/margin (default: $1000)
            leverage: Leverage multiplier (default: 1x)
            position_size: Number of units/contracts (default: 1)
        """
        try:
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
            
            # Calculate targets with CFD parameters
            targets, stop_loss, cfd_calculations = self.calculate_targets(
                signal, self.current_price, margin, leverage, position_size
            )
            
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
                'indicators': all_signals,
                'cfd': cfd_calculations
            }
        except Exception as e:
            print(f"Error in generate_signal: {e}")
            import traceback
            traceback.print_exc()
            # Return safe default
            return {
                'signal': 'HOLD',
                'entry_price': self.current_price,
                'targets': {'3%': 0, '5%': 0, '10%': 0},
                'stop_loss': 0,
                'confidence': 0,
                'total_score': 0,
                'indicators': {},
                'cfd': {'margin': margin, 'leverage': leverage, 'error': str(e)}
            }
