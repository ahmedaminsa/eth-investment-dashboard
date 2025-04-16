#!/usr/bin/env python3
"""
ETH Price Tracker Module
------------------------
This module handles the collection of ETH price data from various APIs.
It's designed to be a core component of the ETH investment script.

Author: Manus AI
Date: April 16, 2025
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os

# Configuration
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"
ETH_ID = "ethereum"  # CoinGecko ID for Ethereum
FIAT_CURRENCY = "usd"  # Default currency for price data

# You can add your API keys here if you have them
COINGECKO_API_KEY = ""  # Optional, can use free tier with rate limits
ETHERSCAN_API_KEY = ""  # Required for Etherscan API

class ETHPriceTracker:
    """Class for tracking ETH prices and related metrics"""
    
    def __init__(self, coingecko_api_key=COINGECKO_API_KEY, etherscan_api_key=ETHERSCAN_API_KEY):
        """Initialize the ETH price tracker with API keys"""
        self.coingecko_api_key = coingecko_api_key
        self.etherscan_api_key = etherscan_api_key
        self.headers = {}
        
        # Set up headers if API key is provided
        if coingecko_api_key:
            self.headers["x-cg-pro-api-key"] = coingecko_api_key
    
    def get_current_price(self):
        """Get current ETH price from CoinGecko"""
        try:
            url = f"{COINGECKO_BASE_URL}/simple/price"
            params = {
                "ids": ETH_ID,
                "vs_currencies": FIAT_CURRENCY,
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true"
            }
            
            print(f"Requesting current ETH price data from CoinGecko...")
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code != 200:
                print(f"API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
            
            data = response.json()
            
            # Extract ETH data
            eth_data = data.get(ETH_ID, {})
            
            result = {
                "price": eth_data.get(FIAT_CURRENCY, 0),
                "market_cap": eth_data.get(f"{FIAT_CURRENCY}_market_cap", 0),
                "volume_24h": eth_data.get(f"{FIAT_CURRENCY}_24h_vol", 0),
                "change_24h": eth_data.get(f"{FIAT_CURRENCY}_24h_change", 0),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"Current ETH price: ${result['price']:.2f}")
            return result
            
        except Exception as e:
            print(f"Error getting current price: {str(e)}")
            return None
    
    def get_historical_prices(self, days=90, interval="daily"):
        """Get historical ETH price data from CoinGecko"""
        try:
            url = f"{COINGECKO_BASE_URL}/coins/{ETH_ID}/market_chart"
            params = {
                "vs_currency": FIAT_CURRENCY,
                "days": days,
                "interval": interval
            }
            
            print(f"Requesting historical ETH data for the past {days} days from CoinGecko...")
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code != 200:
                print(f"API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return pd.DataFrame()
            
            data = response.json()
            
            # Extract price data [timestamp, price]
            prices_data = data.get("prices", [])
            
            # Convert to DataFrame
            df = pd.DataFrame(prices_data, columns=["timestamp", "price"])
            
            # Convert timestamp from milliseconds to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            
            # Add market cap and volume if available
            if "market_caps" in data:
                market_caps = data["market_caps"]
                df["market_cap"] = [item[1] for item in market_caps]
            
            if "total_volumes" in data:
                volumes = data["total_volumes"]
                df["volume"] = [item[1] for item in volumes]
            
            print(f"Retrieved {len(df)} days of historical data for ETH")
            return df
            
        except Exception as e:
            print(f"Error getting historical prices: {str(e)}")
            return pd.DataFrame()
    
    def get_gas_prices(self):
        """Get current ETH gas prices from Etherscan"""
        try:
            if not self.etherscan_api_key:
                print("Etherscan API key is required for gas price data")
                return None
                
            url = f"{ETHERSCAN_BASE_URL}"
            params = {
                "module": "gastracker",
                "action": "gasoracle",
                "apikey": self.etherscan_api_key
            }
            
            print(f"Requesting current gas prices from Etherscan...")
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                print(f"API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
            
            data = response.json()
            
            if data.get("status") != "1":
                print(f"API Error: {data.get('message')}")
                return None
            
            result = data.get("result", {})
            
            gas_data = {
                "safe_gas_price": result.get("SafeGasPrice"),
                "propose_gas_price": result.get("ProposeGasPrice"),
                "fast_gas_price": result.get("FastGasPrice"),
                "base_fee": result.get("suggestBaseFee"),
                "gas_used_ratio": result.get("gasUsedRatio"),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"Current ETH gas prices - Safe: {gas_data['safe_gas_price']} Gwei, Fast: {gas_data['fast_gas_price']} Gwei")
            return gas_data
            
        except Exception as e:
            print(f"Error getting gas prices: {str(e)}")
            return None
    
    def get_weekly_price_summary(self):
        """Get a weekly summary of ETH price performance"""
        try:
            # Get historical data for the past 14 days
            df = self.get_historical_prices(days=14, interval="daily")
            
            if df.empty:
                return None
            
            # Get current price
            current_data = self.get_current_price()
            current_price = current_data.get("price", 0) if current_data else 0
            
            # Calculate weekly metrics
            today = pd.Timestamp.now().normalize()
            week_ago = today - pd.Timedelta(days=7)
            two_weeks_ago = today - pd.Timedelta(days=14)
            
            # Filter data for current week and previous week
            current_week = df[(df["timestamp"] >= week_ago) & (df["timestamp"] <= today)]
            previous_week = df[(df["timestamp"] >= two_weeks_ago) & (df["timestamp"] < week_ago)]
            
            # Calculate metrics
            if not current_week.empty and not previous_week.empty:
                current_week_open = current_week.iloc[0]["price"]
                current_week_high = current_week["price"].max()
                current_week_low = current_week["price"].min()
                current_week_close = current_price
                
                previous_week_open = previous_week.iloc[0]["price"]
                previous_week_close = previous_week.iloc[-1]["price"]
                
                weekly_change = ((current_week_close - current_week_open) / current_week_open) * 100
                weekly_volatility = current_week["price"].std() / current_week["price"].mean() * 100
                
                week_over_week = ((current_week_close - previous_week_close) / previous_week_close) * 100
                
                summary = {
                    "date": today.strftime("%Y-%m-%d"),
                    "current_price": current_price,
                    "week_open": current_week_open,
                    "week_high": current_week_high,
                    "week_low": current_week_low,
                    "weekly_change_pct": weekly_change,
                    "weekly_volatility_pct": weekly_volatility,
                    "week_over_week_pct": week_over_week,
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                print(f"Weekly ETH summary - Change: {weekly_change:.2f}%, WoW: {week_over_week:.2f}%")
                return summary
            else:
                print("Insufficient data for weekly summary")
                return None
                
        except Exception as e:
            print(f"Error generating weekly summary: {str(e)}")
            return None
    
    def save_price_data(self, data, filename="eth_price_data.json"):
        """Save price data to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Price data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving price data: {str(e)}")
            return False
    
    def load_price_data(self, filename="eth_price_data.json"):
        """Load price data from a JSON file"""
        try:
            if not os.path.exists(filename):
                print(f"File {filename} does not exist")
                return None
                
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"Price data loaded from {filename}")
            return data
        except Exception as e:
            print(f"Error loading price data: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    tracker = ETHPriceTracker()
    
    # Get current ETH price
    current_price = tracker.get_current_price()
    print(f"Current ETH data: {current_price}")
    
    # Get historical prices
    historical_prices = tracker.get_historical_prices(days=30)
    print(f"Historical data shape: {historical_prices.shape}")
    
    # Get weekly summary
    weekly_summary = tracker.get_weekly_price_summary()
    print(f"Weekly summary: {weekly_summary}")
    
    # Save data
    if current_price:
        tracker.save_price_data(current_price, "current_eth_price.json")
    
    # Note: Gas prices require an Etherscan API key
    # gas_prices = tracker.get_gas_prices()
    # print(f"Gas prices: {gas_prices}")
