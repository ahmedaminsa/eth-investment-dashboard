#!/usr/bin/env python3
"""
ETH Technical Analysis Module
-----------------------------
This module implements technical indicators and analysis tools for ETH price data.
It works with the ETHPriceTracker module to provide investment signals.

Author: Manus AI
Date: April 16, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

class ETHTechnicalAnalysis:
    """Class for performing technical analysis on ETH price data"""
    
    def __init__(self):
        """Initialize the technical analysis module"""
        pass
    
    def calculate_rsi(self, prices, window=14):
        """
        Calculate the Relative Strength Index (RSI) for a given price series
        
        Args:
            prices (list/array): List of price values
            window (int): The RSI window/period (default: 14)
            
        Returns:
            float: The current RSI value
        """
        if len(prices) < window + 1:
            print(f"Warning: Not enough data to calculate RSI. Need {window+1}, got {len(prices)}")
            return 50  # Not enough data, return neutral RSI
            
        try:
            # Convert to numpy array if it's not already
            prices_array = np.array(prices)
            
            # Calculate price changes
            price_diff = np.diff(prices_array)
            
            # Create arrays for gains and losses
            gains = np.copy(price_diff)
            losses = np.copy(price_diff)
            gains[gains < 0] = 0
            losses[losses > 0] = 0
            losses = np.abs(losses)
            
            # Calculate average gains and losses
            avg_gain = np.mean(gains[:window])
            avg_loss = np.mean(losses[:window])
            
            if avg_loss == 0:
                return 100  # No losses, RSI is 100
                
            # Calculate RS and RSI
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception as e:
            print(f"Error calculating RSI: {str(e)}")
            return 50  # Return neutral RSI on error
    
    def calculate_macd(self, prices, fast_period=12, slow_period=26, signal_period=9):
        """
        Calculate the Moving Average Convergence Divergence (MACD)
        
        Args:
            prices (list/array): List of price values
            fast_period (int): Fast EMA period (default: 12)
            slow_period (int): Slow EMA period (default: 26)
            signal_period (int): Signal line period (default: 9)
            
        Returns:
            dict: Dictionary containing MACD line, signal line, histogram, and signal
        """
        try:
            if len(prices) < slow_period + signal_period:
                print(f"Warning: Not enough data for MACD calculation. Need {slow_period+signal_period}, got {len(prices)}")
                return {"signal": "neutral"}
                
            # Convert to pandas Series if it's not already
            prices_series = pd.Series(prices)
            
            # Calculate EMAs
            ema_fast = prices_series.ewm(span=fast_period, adjust=False).mean()
            ema_slow = prices_series.ewm(span=slow_period, adjust=False).mean()
            
            # Calculate MACD line and signal line
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
            
            # Calculate histogram
            histogram = macd_line - signal_line
            
            # Determine buy/sell signal
            if len(histogram) < 2:
                signal = "neutral"
            else:
                current_histogram = histogram.iloc[-1]
                previous_histogram = histogram.iloc[-2]
                
                if current_histogram > 0 and previous_histogram < 0:
                    signal = "buy"
                elif current_histogram < 0 and previous_histogram > 0:
                    signal = "sell"
                else:
                    signal = "neutral"
            
            return {
                "macd_line": macd_line.iloc[-1],
                "signal_line": signal_line.iloc[-1],
                "histogram": histogram.iloc[-1],
                "signal": signal
            }
            
        except Exception as e:
            print(f"Error calculating MACD: {str(e)}")
            return {"signal": "neutral"}
    
    def check_moving_averages(self, prices, ma_short=50, ma_long=200):
        """
        Check for golden/death crosses in moving averages
        
        Args:
            prices (list/array): List of price values
            ma_short (int): Short-term MA period (default: 50)
            ma_long (int): Long-term MA period (default: 200)
            
        Returns:
            dict: Dictionary containing MA values and cross signal
        """
        try:
            if len(prices) < ma_long:
                print(f"Warning: Not enough data for moving average analysis. Need {ma_long}, got {len(prices)}")
                return {"signal": "insufficient_data"}
                
            # Convert to pandas Series if it's not already
            prices_series = pd.Series(prices)
            
            # Calculate MAs
            ma_short_values = prices_series.rolling(window=ma_short).mean()
            ma_long_values = prices_series.rolling(window=ma_long).mean()
            
            # Get current and previous values
            ma_short_current = ma_short_values.iloc[-1]
            ma_long_current = ma_long_values.iloc[-1]
            
            if pd.isna(ma_short_current) or pd.isna(ma_long_current):
                return {"signal": "insufficient_data"}
                
            # Check if we have enough data for previous values
            if len(ma_short_values) < 3 or len(ma_long_values) < 3:
                # Just check current state
                if ma_short_current > ma_long_current:
                    signal = "above"
                else:
                    signal = "below"
            else:
                ma_short_previous = ma_short_values.iloc[-2]
                ma_long_previous = ma_long_values.iloc[-2]
                
                if pd.isna(ma_short_previous) or pd.isna(ma_long_previous):
                    # Just check current state
                    if ma_short_current > ma_long_current:
                        signal = "above"
                    else:
                        signal = "below"
                else:
                    # Check for golden cross (short MA crosses above long MA)
                    if ma_short_current > ma_long_current and ma_short_previous <= ma_long_previous:
                        signal = "golden_cross"
                    # Check for death cross (short MA crosses below long MA)
                    elif ma_short_current < ma_long_current and ma_short_previous >= ma_long_previous:
                        signal = "death_cross"
                    # Check if currently in golden cross state
                    elif ma_short_current > ma_long_current:
                        signal = "above"
                    else:
                        signal = "below"
            
            return {
                "ma_short": ma_short_current,
                "ma_long": ma_long_current,
                "signal": signal,
                "golden_cross": signal == "golden_cross",
                "death_cross": signal == "death_cross"
            }
            
        except Exception as e:
            print(f"Error checking moving averages: {str(e)}")
            return {"signal": "error"}
    
    def identify_support_resistance(self, prices, window=10):
        """
        Identify support and resistance levels
        
        Args:
            prices (list/array): List of price values
            window (int): Window size for local min/max detection
            
        Returns:
            dict: Dictionary containing support and resistance levels
        """
        try:
            if len(prices) < window * 3:
                print(f"Warning: Not enough data for support/resistance analysis. Need {window*3}, got {len(prices)}")
                return {"support": [], "resistance": []}
                
            # Convert to numpy array if it's not already
            prices_array = np.array(prices)
            
            # Find local minima and maxima
            support_levels = []
            resistance_levels = []
            
            for i in range(window, len(prices_array) - window):
                # Check if this point is a local minimum (support)
                if all(prices_array[i] <= prices_array[i-window:i]) and all(prices_array[i] <= prices_array[i+1:i+window+1]):
                    support_levels.append(prices_array[i])
                
                # Check if this point is a local maximum (resistance)
                if all(prices_array[i] >= prices_array[i-window:i]) and all(prices_array[i] >= prices_array[i+1:i+window+1]):
                    resistance_levels.append(prices_array[i])
            
            # Get the most recent price
            current_price = prices_array[-1]
            
            # Filter levels that are close to current price
            relevant_support = [level for level in support_levels if level < current_price]
            relevant_resistance = [level for level in resistance_levels if level > current_price]
            
            # Sort levels
            relevant_support.sort(reverse=True)  # Highest support first
            relevant_resistance.sort()  # Lowest resistance first
            
            # Take top 3 most relevant levels
            top_support = relevant_support[:3] if relevant_support else []
            top_resistance = relevant_resistance[:3] if relevant_resistance else []
            
            return {
                "support": top_support,
                "resistance": top_resistance
            }
            
        except Exception as e:
            print(f"Error identifying support/resistance: {str(e)}")
            return {"support": [], "resistance": []}
    
    def analyze_price_data(self, df):
        """
        Perform comprehensive technical analysis on price data
        
        Args:
            df (DataFrame): DataFrame with price data
            
        Returns:
            dict: Dictionary containing analysis results
        """
        try:
            if df.empty:
                print("Error: Empty DataFrame provided for analysis")
                return {}
                
            # Extract price data
            prices = df["price"].values
            current_price = prices[-1]
            
            # Calculate technical indicators
            rsi = self.calculate_rsi(prices)
            macd_result = self.calculate_macd(prices)
            ma_result = self.check_moving_averages(prices)
            sr_levels = self.identify_support_resistance(prices)
            
            # Determine buy/sell signals
            buy_signals = 0
            sell_signals = 0
            
            # RSI signals
            if rsi < 30:
                buy_signals += 1
            elif rsi > 70:
                sell_signals += 1
                
            # MACD signals
            if macd_result["signal"] == "buy":
                buy_signals += 1
            elif macd_result["signal"] == "sell":
                sell_signals += 1
                
            # Moving average signals
            if ma_result["signal"] == "golden_cross":
                buy_signals += 2
            elif ma_result["signal"] == "death_cross":
                sell_signals += 2
            elif ma_result["signal"] == "above":
                buy_signals += 0.5
            elif ma_result["signal"] == "below":
                sell_signals += 0.5
                
            # Support/Resistance proximity
            if sr_levels["support"] and min(abs(current_price - s) for s in sr_levels["support"]) / current_price < 0.05:
                buy_signals += 0.5
            if sr_levels["resistance"] and min(abs(current_price - r) for r in sr_levels["resistance"]) / current_price < 0.05:
                sell_signals += 0.5
                
            # Generate recommendation
            if buy_signals >= 2 and buy_signals > sell_signals:
                if buy_signals >= 3:
                    recommendation = "STRONG BUY"
                else:
                    recommendation = "BUY"
            elif sell_signals >= 2 and sell_signals > buy_signals:
                if sell_signals >= 3:
                    recommendation = "STRONG SELL"
                else:
                    recommendation = "SELL"
            else:
                recommendation = "HOLD"
                
            # Compile explanation
            explanation = []
            
            if rsi < 30:
                explanation.append(f"RSI is oversold ({rsi:.1f})")
            elif rsi > 70:
                explanation.append(f"RSI is overbought ({rsi:.1f})")
            else:
                explanation.append(f"RSI is neutral ({rsi:.1f})")
                
            explanation.append(f"MACD signal is {macd_result['signal']}")
            
            if ma_result["signal"] == "golden_cross":
                explanation.append("Golden cross detected (bullish)")
            elif ma_result["signal"] == "death_cross":
                explanation.append("Death cross detected (bearish)")
            elif ma_result["signal"] == "above":
                explanation.append(f"Price is above {ma_result['ma_long']:.2f} MA (bullish)")
            elif ma_result["signal"] == "below":
                explanation.append(f"Price is below {ma_result['ma_long']:.2f} MA (bearish)")
                
            # Compile results
            analysis_results = {
                "price": current_price,
                "rsi": rsi,
                "macd_signal": macd_result["signal"],
                "golden_cross": ma_result.get("golden_cross", False),
                "death_cross": ma_result.get("death_cross", False),
                "support_levels": sr_levels["support"],
                "resistance_levels": sr_levels["resistance"],
                "buy_score": buy_signals,
                "sell_score": sell_signals,
                "recommendation": recommendation,
                "explanation": explanation
            }
            
            return analysis_results
            
        except Exception as e:
            print(f"Error analyzing price data: {str(e)}")
            return {}
    
    def plot_price_chart(self, df, indicators=True, save_path=None):
        """
        Create a price chart with technical indicators
        
        Args:
            df (DataFrame): DataFrame with price data
            indicators (bool): Whether to include indicators
            save_path (str): Path to save the chart image
            
        Returns:
            bool: Success status
        """
        try:
            if df.empty:
                print("Error: Empty DataFrame provided for plotting")
                return False
                
            # Create figure and primary axis for price
            fig, ax1 = plt.subplots(figsize=(12, 8))
            
            # Plot price
            ax1.plot(df["timestamp"], df["price"], label="ETH Price", color="blue")
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Price (USD)", color="blue")
            ax1.tick_params(axis="y", labelcolor="blue")
            
            if indicators:
                # Calculate and plot moving averages
                df["MA50"] = df["price"].rolling(window=50).mean()
                df["MA200"] = df["price"].rolling(window=200).mean()
                
                ax1.plot(df["timestamp"], df["MA50"], label="50-day MA",
(Content truncated due to size limit. Use line ranges to read in chunks)