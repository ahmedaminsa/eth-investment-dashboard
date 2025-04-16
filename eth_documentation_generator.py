#!/usr/bin/env python3
"""
ETH Investment Documentation Generator
--------------------------------------
This module adds beginner-friendly documentation to the ETH investment script.
It creates a comprehensive user guide with explanations of technical concepts.

Author: Manus AI
Date: April 16, 2025
"""

import os
import sys
import re
import json
import markdown
from datetime import datetime

class ETHDocumentationGenerator:
    """Class for generating beginner-friendly documentation for the ETH investment script"""
    
    def __init__(self, source_dir=".", output_dir="docs"):
        """
        Initialize the documentation generator
        
        Args:
            source_dir (str): Directory containing source code files
            output_dir (str): Directory to save documentation
        """
        self.source_dir = source_dir
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
    
    def extract_docstrings(self, file_path):
        """
        Extract docstrings from a Python file
        
        Args:
            file_path (str): Path to the Python file
            
        Returns:
            dict: Dictionary of docstrings by function/class
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Extract module docstring
            module_docstring = ""
            module_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if module_match:
                module_docstring = module_match.group(1).strip()
                
            # Extract class and function docstrings
            docstrings = {
                "module": module_docstring,
                "classes": {},
                "functions": {}
            }
            
            # Extract class docstrings
            class_matches = re.finditer(r'class\s+(\w+).*?:\s*?"""(.*?)"""', content, re.DOTALL)
            for match in class_matches:
                class_name = match.group(1)
                class_docstring = match.group(2).strip()
                docstrings["classes"][class_name] = class_docstring
                
            # Extract function docstrings
            function_matches = re.finditer(r'def\s+(\w+).*?:\s*?"""(.*?)"""', content, re.DOTALL)
            for match in function_matches:
                function_name = match.group(1)
                function_docstring = match.group(2).strip()
                docstrings["functions"][function_name] = function_docstring
                
            return docstrings
        except Exception as e:
            print(f"Error extracting docstrings from {file_path}: {str(e)}")
            return None
    
    def generate_technical_indicators_guide(self):
        """
        Generate a guide explaining technical indicators used in the script
        
        Returns:
            str: Markdown content for technical indicators guide
        """
        try:
            content = """
# Technical Indicators Guide

This guide explains the technical indicators used in the ETH investment script in beginner-friendly terms.

## Relative Strength Index (RSI)

**What it is:** RSI measures the speed and change of price movements on a scale from 0 to 100.

**How to interpret it:**
- RSI above 70: ETH may be **overbought** (potentially overvalued)
- RSI below 30: ETH may be **oversold** (potentially undervalued)
- RSI between 30-70: ETH is in a **neutral** zone

**How we use it:** The script uses RSI to identify potential buying opportunities when ETH is oversold (RSI < 30) and potential selling opportunities when ETH is overbought (RSI > 70).

## Moving Average Convergence Divergence (MACD)

**What it is:** MACD is a trend-following momentum indicator that shows the relationship between two moving averages of ETH's price.

**Components:**
- MACD Line: The difference between the 12-period and 26-period Exponential Moving Averages (EMA)
- Signal Line: The 9-period EMA of the MACD Line
- Histogram: The difference between the MACD Line and Signal Line

**How to interpret it:**
- MACD Line crosses above Signal Line: Bullish signal (potential buy)
- MACD Line crosses below Signal Line: Bearish signal (potential sell)
- Histogram increasing: Upward momentum is strengthening
- Histogram decreasing: Downward momentum is strengthening

**How we use it:** The script uses MACD crossovers to identify potential trend changes and generate buy/sell signals.

## Moving Averages

**What it is:** Moving averages smooth out price data to create a single flowing line, making it easier to identify the direction of the trend.

**Types used:**
- Simple Moving Average (SMA): Average of prices over a specific period
- Exponential Moving Average (EMA): Weighted average that gives more importance to recent prices

**Key concepts:**
- Golden Cross: When the 50-day MA crosses above the 200-day MA (bullish signal)
- Death Cross: When the 50-day MA crosses below the 200-day MA (bearish signal)

**How to interpret it:**
- Price above MA: Uptrend
- Price below MA: Downtrend
- MA slope up: Strengthening trend
- MA slope down: Weakening trend

**How we use it:** The script uses moving averages to identify the overall trend direction and significant trend changes through golden and death crosses.

## Support and Resistance Levels

**What it is:** 
- Support: Price level where ETH tends to stop falling and bounce back up
- Resistance: Price level where ETH tends to stop rising and fall back down

**How to interpret it:**
- Price approaching support: Potential buying opportunity
- Price approaching resistance: Potential selling opportunity
- Price breaking through support: Previous support may become resistance
- Price breaking through resistance: Previous resistance may become support

**How we use it:** The script identifies support and resistance levels to determine optimal entry and exit points, as well as stop-loss levels.

## Average True Range (ATR)

**What it is:** ATR measures market volatility by decomposing the entire range of an asset price for a period.

**How to interpret it:**
- Higher ATR: Higher volatility
- Lower ATR: Lower volatility

**How we use it:** The script uses ATR to set appropriate stop-loss levels based on current market volatility rather than using fixed percentages.

## Trend Analysis

**What it is:** Trend analysis examines the direction of ETH's price movement over time.

**Types of trends:**
- Uptrend: Series of higher highs and higher lows
- Downtrend: Series of lower highs and lower lows
- Sideways/Ranging: No clear direction

**How we use it:** The script analyzes trends to determine the overall market direction and adjust investment strategies accordingly.

## Volatility

**What it is:** Volatility measures how much the price of ETH fluctuates over time.

**How to interpret it:**
- High volatility: Large price swings (higher risk and potential reward)
- Low volatility: Small price swings (lower risk and potential reward)

**How we use it:** The script measures volatility to adjust position sizing and risk management parameters.
"""
            return content
        except Exception as e:
            print(f"Error generating technical indicators guide: {str(e)}")
            return ""
    
    def generate_risk_management_guide(self):
        """
        Generate a guide explaining risk management concepts used in the script
        
        Returns:
            str: Markdown content for risk management guide
        """
        try:
            content = """
# Risk Management Guide

This guide explains the risk management concepts used in the ETH investment script in beginner-friendly terms.

## Position Sizing

**What it is:** Position sizing determines how much ETH to buy or sell in each trade.

**Key concepts:**
- Fixed percentage risk: Risking a fixed percentage of your portfolio on each trade
- Position size calculation: Based on the distance between entry price and stop-loss

**How we calculate it:**
1. Determine the maximum amount you're willing to risk per trade (e.g., 2% of portfolio)
2. Calculate the difference between entry price and stop-loss price
3. Divide the risk amount by the price difference to get the position size in ETH

**Example:**
- Portfolio value: $10,000
- Risk per trade: 2% = $200
- Entry price: $3,000
- Stop-loss price: $2,800 (difference of $200)
- Position size: $200 ÷ $200 = 1 ETH

**Why it matters:** Proper position sizing ensures that no single trade can significantly damage your portfolio, allowing you to withstand a series of losing trades.

## Stop-Loss Strategies

**What it is:** A stop-loss is a predetermined price level at which you'll sell to limit potential losses.

**Types implemented:**
- Fixed percentage: Set at a fixed percentage below entry price
- ATR-based: Based on market volatility using Average True Range
- Support-based: Set at the nearest support level below entry price

**How to use it:**
- Always set a stop-loss when entering a trade
- Consider adjusting stop-loss as the trade moves in your favor (trailing stop)
- Never move a stop-loss to increase potential loss

**Why it matters:** Stop-losses protect your capital by limiting the loss on any single trade, which is crucial for long-term success.

## Take-Profit Targets

**What it is:** Take-profit targets are predetermined price levels at which you'll sell to secure profits.

**Concepts:**
- Risk-reward ratio: The ratio between potential profit and potential loss
- Multiple targets: Setting several price targets to secure partial profits

**How we calculate it:**
1. Determine the risk (entry price - stop-loss price)
2. Multiply the risk by desired risk-reward ratios (e.g., 1.5R, 2.5R, 3.5R)
3. Add the result to entry price to get take-profit targets

**Example:**
- Entry price: $3,000
- Stop-loss price: $2,800 (risk of $200)
- Take-profit targets:
  - Target 1 (1.5R): $3,000 + ($200 × 1.5) = $3,300
  - Target 2 (2.5R): $3,000 + ($200 × 2.5) = $3,500
  - Target 3 (3.5R): $3,000 + ($200 × 3.5) = $3,700

**Why it matters:** Take-profit targets help you secure profits and avoid the common mistake of holding winning trades too long.

## Portfolio Exposure Limits

**What it is:** Portfolio exposure limits restrict how much of your total portfolio can be allocated to ETH.

**Key concepts:**
- Maximum exposure: The maximum percentage of your portfolio allocated to ETH
- Diversification: Spreading risk across different assets

**How we implement it:**
- Set a maximum percentage of portfolio value for ETH exposure (e.g., 25%)
- Adjust position sizes to respect this limit
- Monitor and rebalance as needed

**Why it matters:** Limiting exposure prevents concentration risk, ensuring that a significant drop in ETH price won't devastate your entire portfolio.

## Trailing Stops

**What it is:** A trailing stop is a stop-loss that moves up as the price increases, locking in profits while still allowing for further gains.

**How it works:**
1. Set initial stop-loss when entering a trade
2. As price moves favorably, adjust stop-loss to maintain a fixed percentage or amount below the highest price reached
3. Sell when price hits the trailing stop

**Example:**
- Entry price: $3,000
- Initial stop-loss: $2,800
- Price rises to $3,500
- Trailing stop (0.5% trail): $3,500 × (1 - 0.005) = $3,482.50

**Why it matters:** Trailing stops help you capture more profit in strong trends while protecting gains if the trend reverses.

## Risk-Reward Ratio

**What it is:** The risk-reward ratio compares the potential profit of a trade to its potential loss.

**How to calculate it:**
- Risk = Entry price - Stop-loss price
- Reward = Take-profit price - Entry price
- Risk-reward ratio = Reward ÷ Risk

**Recommended ratios:**
- Minimum: 1:1.5 (risking $1 to potentially gain $1.50)
- Ideal: 1:2 or higher

**Why it matters:** A favorable risk-reward ratio means you can be profitable even if you're wrong more often than you're right.

## Weekly Analysis Frequency

**What it is:** The script performs a comprehensive analysis on a weekly basis rather than daily or hourly.

**Benefits:**
- Reduces noise in the data
- Minimizes overtrading
- Focuses on more significant trends
- Reduces emotional decision-making

**Why it matters:** Weekly analysis helps avoid the pitfalls of short-term market fluctuations and encourages a more disciplined approach to ETH investing.
"""
            return content
        except Exception as e:
            print(f"Error generating risk management guide: {str(e)}")
            return ""
    
    def generate_user_guide(self):
        """
        Generate a comprehensive user guide for the ETH investment script
        
        Returns:
            str: Markdown content for user guide
        """
        try:
            content = """
# ETH Investment Script - User Guide

## Introduction

Welcome to the ETH Investment Script! This guide will help you understand how to use the script to make informed investment decisions about Ethereum (ETH).

This script is designed specifically for beginners who want to focus on ETH investments. It provides technical analysis, risk management, and performance tracking in a user-friendly interface.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Internet connection
- Basic understanding of cryptocurrency investing

### Installation

1. Download the script files to your computer
2. Install required Python packages:
   ```
   pip install pandas numpy matplotlib gspread oauth2client requests
   ```
3. Run the main dashboard script:
   ```
   python eth_investment_dashboard.py
   ```

## Main Features

### 1. ETH Price Tracking

The script automatically fetches current and historical ETH price data from reliable sources. It also tracks gas fees, which are important for understanding transaction costs on the Ethereum network.

### 2. Technical Analysis

The script analyzes ETH price data using various technical indicators:
- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Moving Averages (including Golden/Death Cross detection)
- Support and Resistance levels

See the [Technical Indicators Guide](#) for detailed explanations of these concepts.

### 3. Investment Recommendations

Based on technical analysis, the script provides clear investment recommendations:
- STRONG BUY
- BUY
- HOLD
- SELL
- STRONG SELL

Each recommendation includes a detailed explanation of the factors that led to it, helping you understand the reasoning behind the advice.

### 4. Risk Management

The script includes comprehensive risk management features:
- Stop-loss calculation
- Position sizing
- Take-profit targets
- Portfolio exposure limits
- Trailing stops

See the [Risk Management Guide](#) for detailed explanations of these concepts.

### 5. Performance Tracking

Track your ETH investment performance over time:
- Record buy/sell trades
- Calculate profit/loss
- Measure ROI and other performance metrics
- Evaluate the accuracy of past investment decisions

### 6. Google Sheets Integration

Optionally connect the script to Google Sheets for easy visualization and sharing of data:
- Current price and recommendation
- Technical analysis results
- Risk management parameters
- Performance metrics

## How to Use

### Weekly Analysis

The script is designed to perform a comprehensive analysis on a weekly basis. This frequency helps avoid overtrading and focuses on more significant trends.

To run a weekly analysis:
```
python eth_investment_dashboard.py --run
```

This will:
1. Fetch current ETH price data
2. Analyze historical price trends
3. Generate an investment recommendation
4. Calculate risk management parameters
5. Update performance metrics
6. Create a beginner-friendly summary

### Recording Trades

When you make an ETH trade, record it in the 
(Content truncated due to size limit. Use line ranges to read in chunks)