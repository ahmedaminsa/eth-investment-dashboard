# ETH Investment Script - User Guide

## Introduction

Welcome to the ETH Investment Script! This comprehensive tool is designed specifically for beginners who want to focus on Ethereum (ETH) investments. It combines technical analysis, risk management, and performance tracking in a user-friendly interface to help you make more informed investment decisions.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Key Features](#key-features)
4. [Using the Dashboard](#using-the-dashboard)
5. [Understanding Technical Analysis](#understanding-technical-analysis)
6. [Risk Management](#risk-management)
7. [Performance Tracking](#performance-tracking)
8. [Google Sheets Integration](#google-sheets-integration)
9. [Command Line Options](#command-line-options)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)

## Installation

### Prerequisites

Before installing the ETH Investment Script, ensure you have:

- Python 3.6 or higher installed
- Internet connection
- Basic understanding of cryptocurrency concepts

### Step-by-Step Installation

1. **Download the script files**

   Download all the script files to your computer and place them in a dedicated folder.

2. **Install required Python packages**

   Open a terminal or command prompt and navigate to the script folder. Then run:

   ```
   pip install pandas numpy matplotlib gspread oauth2client requests
   ```

3. **Create configuration file (optional)**

   The script will create a default configuration file (`eth_config.json`) on first run, but you can create it manually if you want to customize settings before running.

4. **Set up Google Sheets integration (optional)**

   If you want to use Google Sheets integration:
   
   - Create a Google Cloud Platform project
   - Enable the Google Sheets API
   - Create service account credentials
   - Download the credentials JSON file
   - Update the configuration file with the credentials file path and spreadsheet ID

## Getting Started

### First Run

To run the script for the first time:

1. Open a terminal or command prompt
2. Navigate to the script folder
3. Run the main dashboard script:

   ```
   python eth_investment_dashboard.py
   ```

4. The script will perform an initial analysis and generate a beginner-friendly summary
5. Review the output and configuration settings

### Quick Start Guide

1. **Run a weekly analysis**
   ```
   python eth_investment_dashboard.py --run
   ```

2. **Record a buy trade**
   ```
   python eth_investment_dashboard.py --buy --price 3000 --amount 0.5
   ```

3. **Record a sell trade**
   ```
   python eth_investment_dashboard.py --sell --price 3500 --amount 0.25
   ```

4. **View the generated documentation**
   ```
   python eth_documentation_generator.py --html
   ```
   Then open `docs/html/index.html` in your web browser.

## Key Features

### ETH Price Tracking

- **Real-time price data**: Fetches current ETH price from reliable sources
- **Historical data**: Retrieves and analyzes historical price trends
- **Gas fee tracking**: Monitors Ethereum network transaction costs
- **Visualization**: Creates price charts with technical indicators

### Technical Analysis

- **Multiple indicators**: RSI, MACD, moving averages, support/resistance levels
- **Signal detection**: Identifies golden/death crosses and other significant signals
- **Trend analysis**: Determines overall market direction
- **Volatility measurement**: Assesses market risk levels

### Investment Recommendations

- **Clear signals**: STRONG BUY, BUY, HOLD, SELL, or STRONG SELL
- **Detailed explanations**: Provides reasoning behind each recommendation
- **Weighted analysis**: Considers multiple factors with appropriate weighting
- **Risk-adjusted**: Adapts to your risk tolerance level

### Risk Management

- **Stop-loss calculation**: Determines optimal stop-loss levels using multiple methods
- **Position sizing**: Calculates appropriate position size based on your risk parameters
- **Take-profit targets**: Sets multiple profit targets based on risk-reward ratios
- **Portfolio exposure limits**: Prevents overexposure to ETH

### Performance Tracking

- **Trade recording**: Logs all buy and sell transactions
- **Profit/loss calculation**: Tracks realized and unrealized gains/losses
- **Performance metrics**: Calculates ROI, annualized return, Sharpe ratio, etc.
- **Decision evaluation**: Assesses the accuracy of past investment recommendations

### User-Friendly Interface

- **Beginner-friendly summaries**: Explains analysis in simple terms
- **Visual charts**: Provides clear visualizations of price trends and performance
- **Google Sheets integration**: Exports data to Google Sheets for easy viewing
- **Command-line interface**: Simple commands for common operations

## Using the Dashboard

### Running a Weekly Analysis

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

The analysis results will be displayed in the terminal and saved to files in the configured data directory.

### Understanding the Analysis Output

The analysis output includes:

- **Current ETH price and recent change**: Shows the current price and 24-hour percentage change
- **Investment recommendation**: Indicates whether to BUY, SELL, or HOLD
- **Explanation of recommendation**: Details the technical factors behind the recommendation
- **Risk management parameters**: Provides stop-loss levels, position size, and take-profit targets
- **Performance metrics**: Shows your current portfolio status and historical performance

### Recording Trades

When you make an ETH trade, record it in the system to track your performance:

To record a buy:
```
python eth_investment_dashboard.py --buy --price 3000 --amount 0.5 --notes "Bought based on RSI oversold signal"
```

To record a sell:
```
python eth_investment_dashboard.py --sell --price 3500 --amount 0.25 --notes "Taking partial profits at resistance"
```

The `--notes` parameter is optional but useful for recording your reasoning.

### Scheduled Analysis

You can configure the script to run on a specific day of the week:

1. Edit the `eth_config.json` file
2. Set `"analysis_frequency"` to `"weekly"`
3. Set `"analysis_day"` to your preferred day (e.g., `"Monday"`)
4. Run the script with the `--schedule` flag:

```
python eth_investment_dashboard.py --schedule
```

This will only perform the analysis if today matches the configured day.

## Understanding Technical Analysis

The script uses several technical indicators to analyze ETH price movements. Here's a brief explanation of each:

### Relative Strength Index (RSI)

RSI measures the speed and change of price movements on a scale from 0 to 100.

- **RSI above 70**: ETH may be overbought (potential sell signal)
- **RSI below 30**: ETH may be oversold (potential buy signal)
- **RSI between 30-70**: ETH is in a neutral zone

### Moving Average Convergence Divergence (MACD)

MACD shows the relationship between two moving averages of ETH's price.

- **MACD line crosses above signal line**: Bullish signal (potential buy)
- **MACD line crosses below signal line**: Bearish signal (potential sell)
- **Histogram increasing**: Upward momentum is strengthening
- **Histogram decreasing**: Downward momentum is strengthening

### Moving Averages

Moving averages smooth out price data to identify the direction of the trend.

- **Golden Cross**: 50-day MA crosses above 200-day MA (bullish signal)
- **Death Cross**: 50-day MA crosses below 200-day MA (bearish signal)
- **Price above MA**: Uptrend
- **Price below MA**: Downtrend

### Support and Resistance Levels

- **Support**: Price level where ETH tends to stop falling
- **Resistance**: Price level where ETH tends to stop rising
- **Price approaching support**: Potential buying opportunity
- **Price approaching resistance**: Potential selling opportunity

For more detailed explanations, see the Technical Indicators Guide in the documentation.

## Risk Management

The script includes comprehensive risk management features to help protect your investment.

### Position Sizing

Position sizing determines how much ETH to buy or sell in each trade.

The script calculates position size based on:
- Your portfolio value
- Maximum risk per trade (default: 2%)
- Distance between entry price and stop-loss

This ensures that no single trade can significantly damage your portfolio.

### Stop-Loss Strategies

The script calculates stop-loss levels using three methods:

1. **Fixed percentage**: Set at a fixed percentage below entry price
2. **ATR-based**: Based on market volatility using Average True Range
3. **Support-based**: Set at the nearest support level below entry price

The script recommends the most appropriate method based on current market conditions.

### Take-Profit Targets

The script calculates multiple take-profit targets based on risk-reward ratios:

- **Target 1**: 1.5x the risk (conservative)
- **Target 2**: 2.5x the risk (moderate)
- **Target 3**: 3.5x the risk (aggressive)

This allows you to secure partial profits as the price rises.

### Portfolio Exposure Limits

The script limits how much of your total portfolio can be allocated to ETH (default: 25%).

This prevents concentration risk and ensures that a significant drop in ETH price won't devastate your entire portfolio.

For more detailed explanations, see the Risk Management Guide in the documentation.

## Performance Tracking

The script tracks your ETH investment performance over time.

### Trade Recording

Each buy or sell trade is recorded with:
- Date and time
- Price
- Amount
- Trade type (buy/sell)
- Notes

### Performance Metrics

The script calculates various performance metrics:

- **Total profit/loss**: Both realized and unrealized
- **Return on Investment (ROI)**: Percentage return on your investment
- **Annualized return**: Return normalized to a yearly rate
- **Sharpe ratio**: Risk-adjusted return
- **Maximum drawdown**: Largest percentage drop from peak to trough

### Decision Evaluation

The script evaluates the accuracy of past investment recommendations by comparing them to subsequent price movements.

This helps you understand how well the script's recommendations have performed historically.

## Google Sheets Integration

The script can export data to Google Sheets for easy visualization and sharing.

### Setup

1. Create a Google Cloud Platform project
2. Enable the Google Sheets API
3. Create service account credentials
4. Download the credentials JSON file
5. Create a new Google Sheet and share it with the service account email
6. Update the configuration file with:
   - `"google_sheets_enabled": true`
   - `"google_sheet_id": "your-sheet-id"`
   - `"google_credentials_file": "path/to/credentials.json"`

### Worksheets

The script creates and updates several worksheets:

- **Dashboard**: Summary of current status and recommendations
- **Price Data**: Current and historical price data
- **Technical Analysis**: Technical indicator values and signals
- **Recommendations**: History of investment recommendations
- **Risk Management**: Stop-loss, position size, and take-profit targets
- **Performance**: Portfolio value and performance metrics

## Command Line Options

The script supports various command-line options:

```
python eth_investment_dashboard.py [options]
```

Available options:

- `--config FILE`: Specify a custom configuration file
- `--run`: Run a manual analysis
- `--schedule`: Run scheduled analysis if due
- `--buy`: Record a buy trade
- `--sell`: Record a sell trade
- `--price PRICE`: Price for trade
- `--amount AMOUNT`: Amount for trade
- `--notes NOTES`: Notes for trade

Examples:

```
# Run manual analysis
python eth_investment_dashboard.py --run

# Run scheduled analysis
python eth_investment_dashboard.py --schedule

# Record buy trade
python eth_investment_dashboard.py --buy --price 3000 --amount 0.5 --notes "Test buy"

# Record sell trade
python eth_investment_dashboard.py --sell --price 3500 --amount 0.25 --notes "Test sell"

# Use custom config
python eth_investment_dashboard.py --config my_config.json --run
```

## Configuration

The script uses a JSON configuration file (`eth_config.json` by default) with the following settings:

```json
{
    "portfolio_value": 10000,
    "risk_tolerance": "medium",
    "max_risk_per_trade": 0.02,
    "max_portfolio_exposure": 0.25,
    "analysis_frequency": "weekly",
    "analysis_day": "Monday",
    "google_sheets_enabled": false,
    "google_sheet_id": "",
    "google_credentials_file": "",
    "save_charts": true,
    "charts_directory": "charts",
    "data_directory": "data"
}
```

### Configuration Options

- **portfolio_value**: Your total investment portfolio value in USD
- **risk_tolerance**: Risk tolerance level (low, medium, high)
- **max_risk_per_trade**: Maximum risk per trade as a fraction (0.02 = 2%)
- **max_portfolio_exposure**: Maximum portfolio exposure to ETH as a fraction (0.25 = 25%)
- **analysis_frequency**: How often to run analysis (weekly)
- **analysis_day**: Day of the week to run analysis (Monday)
- **google_sheets_enabled**: Whether to use Google Sheets integration
- **google_sheet_id**: ID of the Google Sheet to use
- **google_credentials_file**: Path to Google API credentials file
- **save_charts**: Whether to save charts as image files
- **charts_directory**: Directory to save chart images
- **data_directory**: Directory to save data files

## Troubleshooting

### Common Issues and Solutions

#### Script Won't Start

**Issue**: The script fails to start or crashes immediately.

**Solutions**:
- Ensure Python 3.6+ is installed (`python --version`)
- Verify all required packages are installed
- Check for syntax errors in the configuration file
- Try running with default configuration (`--config eth_config.json`)

#### API Connection Errors

**Issue**: The script fails to fetch price data.

**Solutions**:
- Check your internet connection
- Verify that the APIs are operational
- Try running the script again after a few minutes
- Check if you've exceeded API rate limits

#### Google Sheets Integration Problems

**Issue**: Google Sheets integration isn't working.

**Solutions**:
- Verify your credentials file path is correct
- Check that the spreadsheet ID is correct
- Ensure you've shared the spreadsheet with the service account email
- Check that the Google Sheets API is enabled in your Google Cloud project

#### Performance Tracking Issues

**Issue**: Performance metrics seem incorrect.

**Solutions**:
- Verify all trades have been recorded correctly
- Check for duplicate trade entries
- Ensure current price data is accurate
- Reset performance tracking by deleting trade history files (caution: this will lose all history)

### Error Messages

Here are some common error messages and their solutions:

#### "Error loading configuration"

- Check if the configuration file exists
- Verify the JSON syntax is correct
- Try using the default configuration

#### "Failed to get current price data"

- Check your internet connection
- Verify the API endpoints are accessible
- Try again later as the API might be temporarily unavailable

#### "Error recording trade"

- Ensure the price and amount parameters are valid numbers
- Check if the trade files are writable
- Verify the data directory exists and is accessible

## FAQ

### General Questions

#### How often should I run the analysis?

The script is designed for weekly analysis, which is a good frequency for most investors. Running it more frequently might lead to overtrading, while running it less frequently might miss important market changes.

#### Should I always follow the recommendations?

The recommendations are based on technical analysis and should be considered as one input to your investment decision. Always do your own research and consider other factors like news events, market sentiment, and your personal financial situation.

#### Can I use this script for other cryptocurrencies?

This version is specifically designed for ETH. While the technical analysis concepts would apply to other cryptocurrencies, you would need to modify the code to fetch and analyze data for other coins.

### Technical Questions

#### What risk tolerance should I set?

For beginners, a "medium" risk tolerance is recommended. As you gain experience, you can adjust this based on your comfort level with volatility and your investment goals.

#### How much of my portfolio should I allocate to ETH?

The script defaults to a maximum exposure of 25%, which is a reasonable starting point. Adjust this based on your overall investment strategy and diversification goals.

#### How are the technical indicators calculated?

The script uses standard formulas for technical indicators:
- RSI: 14-period Relative Strength Index
- MACD: 12-26-9 Moving Average Convergence Divergence
- Moving Averages: 50-day and 200-day Simple Moving Averages

#### Can I customize the technical indicators?

Yes, but it requires modifying the code. Look for the `eth_technical_analysis.py` file and adjust the parameters in the respective functions.

### Practical Questions

#### How do I record my existing ETH holdings?

Record them as a buy trade with the original purchase price and date:
```
python eth_investment_dashboard.py --buy --price 2000 --amount 1.5 --notes "Initial holdings"
```

#### Can I export my trade history?

The trade history is stored in JSON format in the data directory. You can open these files with any text editor or import them into other applications.

#### How do I update the script?

Download the latest version and replace the existing files. Your configuration and data files will remain unchanged as long as you keep them in the same location.

#### Is my data secure?

All data is stored locally on your computer. If you use Google Sheets integration, data is also stored in your Google account according to Google's security policies.

---

## Conclusion

The ETH Investment Script provides a structured approach to ETH investing, combining technical analysis, risk management, and performance tracking in a user-friendly interface. By following this guide, you should be able to use the script effectively to support your ETH investment decisions.

Remember that all investments carry risk, and this script should be used as a tool to support your decision-making, not replace it.

Happy investing!
