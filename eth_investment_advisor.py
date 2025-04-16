#!/usr/bin/env python3
"""
ETH Investment Decision Module
------------------------------
This module implements the investment decision logic based on technical analysis.
It provides clear buy/sell/hold recommendations for ETH investments.

Author: Manus AI
Date: April 16, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class ETHInvestmentAdvisor:
    """Class for generating ETH investment recommendations"""
    
    def __init__(self, risk_tolerance="medium"):
        """
        Initialize the investment advisor
        
        Args:
            risk_tolerance (str): Risk tolerance level (low, medium, high)
        """
        self.risk_tolerance = risk_tolerance
        self.risk_weights = self._get_risk_weights(risk_tolerance)
    
    def _get_risk_weights(self, risk_tolerance):
        """
        Get indicator weights based on risk tolerance
        
        Args:
            risk_tolerance (str): Risk tolerance level
            
        Returns:
            dict: Dictionary of weights for different indicators
        """
        # Default weights (medium risk)
        weights = {
            "rsi": 1.0,
            "macd": 1.0,
            "moving_averages": 1.0,
            "support_resistance": 0.8,
            "trend": 1.0,
            "volatility": 0.7
        }
        
        # Adjust weights based on risk tolerance
        if risk_tolerance.lower() == "low":
            weights["rsi"] = 1.2
            weights["macd"] = 0.8
            weights["moving_averages"] = 1.3
            weights["support_resistance"] = 1.0
            weights["trend"] = 1.2
            weights["volatility"] = 0.5
        elif risk_tolerance.lower() == "high":
            weights["rsi"] = 0.8
            weights["macd"] = 1.2
            weights["moving_averages"] = 0.7
            weights["support_resistance"] = 0.6
            weights["trend"] = 0.8
            weights["volatility"] = 1.0
            
        return weights
    
    def set_risk_tolerance(self, risk_tolerance):
        """
        Update risk tolerance level
        
        Args:
            risk_tolerance (str): Risk tolerance level (low, medium, high)
        """
        self.risk_tolerance = risk_tolerance
        self.risk_weights = self._get_risk_weights(risk_tolerance)
        print(f"Risk tolerance set to {risk_tolerance}")
    
    def evaluate_rsi_signal(self, rsi_value):
        """
        Evaluate RSI indicator for buy/sell signals
        
        Args:
            rsi_value (float): RSI value
            
        Returns:
            dict: Signal strength and explanation
        """
        signal_strength = 0
        explanation = ""
        
        if rsi_value < 30:
            # Oversold condition - buy signal
            signal_strength = (30 - rsi_value) / 10  # Stronger as RSI gets lower
            if rsi_value < 20:
                explanation = f"RSI is extremely oversold ({rsi_value:.1f}), strong buy signal"
                signal_strength = min(signal_strength, 2.0)  # Cap at 2.0
            else:
                explanation = f"RSI is oversold ({rsi_value:.1f}), buy signal"
        elif rsi_value > 70:
            # Overbought condition - sell signal
            signal_strength = -1 * (rsi_value - 70) / 10  # Stronger as RSI gets higher
            if rsi_value > 80:
                explanation = f"RSI is extremely overbought ({rsi_value:.1f}), strong sell signal"
                signal_strength = max(signal_strength, -2.0)  # Cap at -2.0
            else:
                explanation = f"RSI is overbought ({rsi_value:.1f}), sell signal"
        else:
            # Neutral zone
            if rsi_value < 45:
                signal_strength = 0.3  # Slight buy bias
                explanation = f"RSI is neutral-low ({rsi_value:.1f}), slight buy bias"
            elif rsi_value > 55:
                signal_strength = -0.3  # Slight sell bias
                explanation = f"RSI is neutral-high ({rsi_value:.1f}), slight sell bias"
            else:
                signal_strength = 0
                explanation = f"RSI is neutral ({rsi_value:.1f}), no clear signal"
                
        return {
            "signal_strength": signal_strength,
            "explanation": explanation
        }
    
    def evaluate_macd_signal(self, macd_data):
        """
        Evaluate MACD indicator for buy/sell signals
        
        Args:
            macd_data (dict): MACD data including signal
            
        Returns:
            dict: Signal strength and explanation
        """
        signal_strength = 0
        explanation = ""
        
        # Extract MACD components
        macd_line = macd_data.get("macd_line", 0)
        signal_line = macd_data.get("signal_line", 0)
        histogram = macd_data.get("histogram", 0)
        signal = macd_data.get("signal", "neutral")
        
        if signal == "buy":
            # MACD line crossed above signal line
            signal_strength = 1.5
            explanation = "MACD line crossed above signal line, buy signal"
            
            # Stronger signal if both lines are below zero and turning up
            if macd_line < 0 and signal_line < 0 and histogram > 0:
                signal_strength = 2.0
                explanation = "MACD line crossed above signal line from below zero, strong buy signal"
        elif signal == "sell":
            # MACD line crossed below signal line
            signal_strength = -1.5
            explanation = "MACD line crossed below signal line, sell signal"
            
            # Stronger signal if both lines are above zero and turning down
            if macd_line > 0 and signal_line > 0 and histogram < 0:
                signal_strength = -2.0
                explanation = "MACD line crossed below signal line from above zero, strong sell signal"
        else:
            # No cross, but check for divergence or convergence
            if histogram > 0 and histogram > abs(macd_data.get("previous_histogram", 0)):
                signal_strength = 0.5
                explanation = "MACD histogram is positive and increasing, bullish momentum"
            elif histogram < 0 and abs(histogram) > abs(macd_data.get("previous_histogram", 0)):
                signal_strength = -0.5
                explanation = "MACD histogram is negative and decreasing, bearish momentum"
            else:
                explanation = "MACD shows no clear signal"
                
        return {
            "signal_strength": signal_strength,
            "explanation": explanation
        }
    
    def evaluate_moving_averages(self, ma_data):
        """
        Evaluate moving average signals
        
        Args:
            ma_data (dict): Moving average data
            
        Returns:
            dict: Signal strength and explanation
        """
        signal_strength = 0
        explanation = ""
        
        signal = ma_data.get("signal", "")
        
        if signal == "golden_cross":
            # Golden cross - strong buy signal
            signal_strength = 2.0
            explanation = "Golden cross detected (50-day MA crossed above 200-day MA), strong buy signal"
        elif signal == "death_cross":
            # Death cross - strong sell signal
            signal_strength = -2.0
            explanation = "Death cross detected (50-day MA crossed below 200-day MA), strong sell signal"
        elif signal == "above":
            # Price above long-term MA - bullish
            signal_strength = 1.0
            explanation = "Price is above 200-day MA, bullish trend"
        elif signal == "below":
            # Price below long-term MA - bearish
            signal_strength = -1.0
            explanation = "Price is below 200-day MA, bearish trend"
        else:
            explanation = "Moving averages show no clear signal"
            
        return {
            "signal_strength": signal_strength,
            "explanation": explanation
        }
    
    def evaluate_support_resistance(self, price, sr_levels):
        """
        Evaluate support and resistance levels
        
        Args:
            price (float): Current price
            sr_levels (dict): Support and resistance levels
            
        Returns:
            dict: Signal strength and explanation
        """
        signal_strength = 0
        explanation = ""
        
        support_levels = sr_levels.get("support", [])
        resistance_levels = sr_levels.get("resistance", [])
        
        # Check if price is near support
        if support_levels:
            closest_support = max(support_levels)
            support_distance = (price - closest_support) / price * 100  # Distance as percentage
            
            if support_distance < 1:
                signal_strength = 1.5
                explanation = f"Price is very close to support level (${closest_support:.2f}), strong buy signal"
            elif support_distance < 3:
                signal_strength = 1.0
                explanation = f"Price is near support level (${closest_support:.2f}), buy signal"
            elif support_distance < 5:
                signal_strength = 0.5
                explanation = f"Price is approaching support level (${closest_support:.2f}), potential buy zone"
                
        # Check if price is near resistance
        if resistance_levels:
            closest_resistance = min(resistance_levels)
            resistance_distance = (closest_resistance - price) / price * 100  # Distance as percentage
            
            if resistance_distance < 1:
                # This overrides support if resistance is closer
                signal_strength = -1.5
                explanation = f"Price is very close to resistance level (${closest_resistance:.2f}), strong sell signal"
            elif resistance_distance < 3:
                # This overrides support if resistance is closer and support is not very close
                if signal_strength < 1.5:
                    signal_strength = -1.0
                    explanation = f"Price is near resistance level (${closest_resistance:.2f}), sell signal"
            elif resistance_distance < 5:
                # This overrides support if resistance is closer and support is not close
                if signal_strength < 1.0:
                    signal_strength = -0.5
                    explanation = f"Price is approaching resistance level (${closest_resistance:.2f}), potential sell zone"
                    
        if not explanation:
            explanation = "Price is not near significant support or resistance levels"
            
        return {
            "signal_strength": signal_strength,
            "explanation": explanation
        }
    
    def evaluate_trend(self, prices, window=14):
        """
        Evaluate price trend
        
        Args:
            prices (list/array): List of price values
            window (int): Window for trend calculation
            
        Returns:
            dict: Signal strength and explanation
        """
        signal_strength = 0
        explanation = ""
        
        if len(prices) < window:
            return {
                "signal_strength": 0,
                "explanation": "Insufficient data for trend analysis"
            }
            
        # Get recent prices for trend analysis
        recent_prices = prices[-window:]
        
        # Calculate linear regression
        x = np.arange(len(recent_prices))
        y = np.array(recent_prices)
        
        # Calculate slope
        n = len(x)
        slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
        
        # Normalize slope as percentage of average price
        avg_price = np.mean(recent_prices)
        norm_slope = slope / avg_price * 100
        
        if norm_slope > 1.0:
            signal_strength = 1.5
            explanation = f"Strong upward trend detected ({norm_slope:.2f}% per period), buy signal"
        elif norm_slope > 0.3:
            signal_strength = 1.0
            explanation = f"Upward trend detected ({norm_slope:.2f}% per period), buy signal"
        elif norm_slope > 0.1:
            signal_strength = 0.5
            explanation = f"Slight upward trend detected ({norm_slope:.2f}% per period), weak buy signal"
        elif norm_slope < -1.0:
            signal_strength = -1.5
            explanation = f"Strong downward trend detected ({norm_slope:.2f}% per period), sell signal"
        elif norm_slope < -0.3:
            signal_strength = -1.0
            explanation = f"Downward trend detected ({norm_slope:.2f}% per period), sell signal"
        elif norm_slope < -0.1:
            signal_strength = -0.5
            explanation = f"Slight downward trend detected ({norm_slope:.2f}% per period), weak sell signal"
        else:
            explanation = f"No significant trend detected ({norm_slope:.2f}% per period)"
            
        return {
            "signal_strength": signal_strength,
            "explanation": explanation
        }
    
    def evaluate_volatility(self, prices, window=14):
        """
        Evaluate price volatility
        
        Args:
            prices (list/array): List of price values
            window (int): Window for volatility calculation
            
        Returns:
            dict: Signal strength and explanation
        """
        signal_strength = 0
        explanation = ""
        
        if len(prices) < window:
            return {
                "signal_strength": 0,
                "explanation": "Insufficient data for volatility analysis"
            }
            
        # Get recent prices for volatility analysis
        recent_prices = prices[-window:]
        
        # Calculate returns
        returns = np.diff(recent_prices) / recent_prices[:-1]
        
        # Calculate volatility (standard deviation of returns)
        volatility = np.std(returns) * 100  # Convert to percentage
        
        # Compare current volatility to historical
        if len(prices) >= window * 3:
            historical_returns = np.diff(prices[-(window*3):-window]) / prices[-(window*3):-window-1]
            historical_volatility = np.std(historical_returns) * 100
            
            volatility_ratio = volatility / historical_volatility
            
            if volatility_ratio > 2.0:
                signal_strength = -1.0
                explanation = f"Extremely high volatility ({volatility:.2f}%, {volatility_ratio:.1f}x normal), caution advised"
            elif volatility_ratio > 1.5:
                signal_strength = -0.5
                explanation = f"Elevated volatility ({volatility:.2f}%, {volatility_ratio:.1f}x normal), increased risk"
            elif volatility_ratio < 0.5:
                signal_strength = 0.5
                explanation = f"Low volatility ({volatility:.2f}%, {volatility_ratio:.1f}x normal), reduced risk"
            else:
                explanation = f"Normal volatility levels ({volatility:.2f}%)"
        else:
            # Without historical comparison
            if volatility > 5:
                signal_strength = -1.0
                explanation = f"High volatility detected ({volatility:.2f}%), caution advised"
            elif volatility < 1:
                signal_strength = 0.5
                explanation = f"Low volatility detected ({volatility:.2f}%), reduced risk"
            else:
                explanation = f"Moderate volatility ({volatility:.2f}%)"
                
        return {
            "signal_strength": signal_strength,
            "explanation": explanation
        }
    
    def generate_recommendation(self, analysis_data, price_data):
        """
        Generate investment recommendation based on technical analysis
        
        Args:
            analysis_data (dict): Technical analysis results
            price_data (DataFram
(Content truncated due to size limit. Use line ranges to read in chunks)