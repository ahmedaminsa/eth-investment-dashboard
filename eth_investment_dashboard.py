#!/usr/bin/env python3
"""
ETH Investment Dashboard - Main Interface
-----------------------------------------
This module provides a user-friendly interface for the ETH investment script.
It integrates all components and provides a simple dashboard for beginners.

Author: Manus AI
Date: April 16, 2025
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Import our custom modules
from eth_price_tracker import ETHPriceTracker
from eth_technical_analysis import ETHTechnicalAnalysis
from eth_investment_advisor import ETHInvestmentAdvisor
from eth_risk_manager import ETHRiskManager
from eth_performance_tracker import ETHPerformanceTracker

class ETHInvestmentDashboard:
    """Main dashboard class for ETH investment script"""
    
    def __init__(self, config_file="eth_config.json"):
        """
        Initialize the dashboard
        
        Args:
            config_file (str): Configuration file path
        """
        self.config_file = config_file
        self.config = self._load_config()
        
        # Initialize modules
        self.price_tracker = ETHPriceTracker()
        self.analyzer = ETHTechnicalAnalysis()
        self.advisor = ETHInvestmentAdvisor(risk_tolerance=self.config.get("risk_tolerance", "medium"))
        self.risk_manager = ETHRiskManager(
            portfolio_value=self.config.get("portfolio_value", 10000),
            max_risk_per_trade=self.config.get("max_risk_per_trade", 0.02),
            max_portfolio_exposure=self.config.get("max_portfolio_exposure", 0.25)
        )
        self.performance_tracker = ETHPerformanceTracker()
        
        # Google Sheets integration
        self.sheets_enabled = self.config.get("google_sheets_enabled", False)
        self.sheet_id = self.config.get("google_sheet_id", "")
        self.credentials_file = self.config.get("google_credentials_file", "")
        self.gc = None
        self.sheet = None
        
        if self.sheets_enabled:
            self._setup_google_sheets()
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                print(f"Loaded configuration from {self.config_file}")
                return config
            else:
                print(f"No configuration file found at {self.config_file}, using defaults")
                # Create default configuration
                default_config = {
                    "portfolio_value": 10000,
                    "risk_tolerance": "medium",
                    "max_risk_per_trade": 0.02,
                    "max_portfolio_exposure": 0.25,
                    "analysis_frequency": "weekly",
                    "analysis_day": "Monday",
                    "google_sheets_enabled": False,
                    "google_sheet_id": "",
                    "google_credentials_file": "",
                    "save_charts": True,
                    "charts_directory": "charts",
                    "data_directory": "data"
                }
                
                # Save default configuration
                self._save_config(default_config)
                return default_config
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            return {}
    
    def _save_config(self, config=None):
        """Save configuration to file"""
        try:
            if config is None:
                config = self.config
                
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"Saved configuration to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
            return False
    
    def update_config(self, key, value):
        """
        Update a configuration value
        
        Args:
            key (str): Configuration key
            value: New value
            
        Returns:
            bool: Success status
        """
        try:
            self.config[key] = value
            
            # Update relevant module settings
            if key == "risk_tolerance":
                self.advisor.set_risk_tolerance(value)
            elif key == "portfolio_value":
                self.risk_manager.update_portfolio_value(value)
            elif key == "max_risk_per_trade":
                self.risk_manager.max_risk_per_trade = value
            elif key == "max_portfolio_exposure":
                self.risk_manager.max_portfolio_exposure = value
            
            # Save updated configuration
            self._save_config()
            print(f"Updated configuration: {key} = {value}")
            return True
        except Exception as e:
            print(f"Error updating configuration: {str(e)}")
            return False
    
    def _setup_google_sheets(self):
        """Set up Google Sheets integration"""
        try:
            if not self.sheets_enabled or not self.sheet_id or not self.credentials_file:
                print("Google Sheets integration is not properly configured")
                return False
                
            if not os.path.exists(self.credentials_file):
                print(f"Google credentials file not found: {self.credentials_file}")
                return False
                
            # Set up credentials
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
            self.gc = gspread.authorize(credentials)
            
            # Open the spreadsheet
            try:
                self.sheet = self.gc.open_by_key(self.sheet_id)
                print(f"Connected to Google Sheet: {self.sheet.title}")
                
                # Check if required worksheets exist, create if not
                worksheet_names = [ws.title for ws in self.sheet.worksheets()]
                
                required_worksheets = [
                    "Dashboard", "Price Data", "Technical Analysis", 
                    "Recommendations", "Risk Management", "Performance"
                ]
                
                for ws_name in required_worksheets:
                    if ws_name not in worksheet_names:
                        self.sheet.add_worksheet(title=ws_name, rows=1000, cols=20)
                        print(f"Created worksheet: {ws_name}")
                
                return True
            except Exception as e:
                print(f"Error opening Google Sheet: {str(e)}")
                return False
        except Exception as e:
            print(f"Error setting up Google Sheets: {str(e)}")
            return False
    
    def update_google_sheets(self, data):
        """
        Update Google Sheets with latest data
        
        Args:
            data (dict): Data to update in sheets
            
        Returns:
            bool: Success status
        """
        try:
            if not self.sheets_enabled or not self.sheet:
                print("Google Sheets integration is not enabled or properly set up")
                return False
                
            # Update Price Data worksheet
            if "price_data" in data:
                price_data = data["price_data"]
                ws = self.sheet.worksheet("Price Data")
                
                # Clear existing data
                ws.clear()
                
                # Set headers
                headers = ["Date", "Price", "24h Change", "Market Cap", "Volume"]
                ws.append_row(headers)
                
                # Add current price data
                current_row = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    price_data.get("price", 0),
                    f"{price_data.get('change_24h', 0):.2f}%",
                    price_data.get("market_cap", 0),
                    price_data.get("volume_24h", 0)
                ]
                ws.append_row(current_row)
                
                print("Updated Price Data worksheet")
            
            # Update Technical Analysis worksheet
            if "analysis" in data:
                analysis = data["analysis"]
                ws = self.sheet.worksheet("Technical Analysis")
                
                # Clear existing data
                ws.clear()
                
                # Set headers
                headers = ["Indicator", "Value", "Signal"]
                ws.append_row(headers)
                
                # Add indicators
                ws.append_row(["RSI", f"{analysis.get('rsi', 0):.2f}", "Oversold" if analysis.get('rsi', 50) < 30 else "Overbought" if analysis.get('rsi', 50) > 70 else "Neutral"])
                ws.append_row(["MACD", "N/A", analysis.get('macd_signal', 'neutral').upper()])
                ws.append_row(["Golden Cross", "N/A", "YES" if analysis.get('golden_cross', False) else "NO"])
                ws.append_row(["Death Cross", "N/A", "YES" if analysis.get('death_cross', False) else "NO"])
                
                # Add support/resistance levels
                support_levels = analysis.get('support_levels', [])
                resistance_levels = analysis.get('resistance_levels', [])
                
                if support_levels:
                    ws.append_row(["Support Levels", ", ".join([f"${level:.2f}" for level in support_levels]), ""])
                
                if resistance_levels:
                    ws.append_row(["Resistance Levels", ", ".join([f"${level:.2f}" for level in resistance_levels]), ""])
                
                print("Updated Technical Analysis worksheet")
            
            # Update Recommendations worksheet
            if "recommendation" in data:
                recommendation = data["recommendation"]
                ws = self.sheet.worksheet("Recommendations")
                
                # Add new recommendation at the top
                new_row = [
                    datetime.now().strftime("%Y-%m-%d"),
                    recommendation.get("price", 0),
                    recommendation.get("recommendation", ""),
                    recommendation.get("action", "")
                ]
                
                # Get existing data
                existing_data = ws.get_all_values()
                
                if not existing_data or existing_data[0] != ["Date", "Price", "Recommendation", "Action"]:
                    # Set headers if sheet is empty or headers don't match
                    ws.clear()
                    ws.append_row(["Date", "Price", "Recommendation", "Action"])
                    ws.append_row(new_row)
                else:
                    # Insert new row after header
                    ws.insert_row(new_row, 2)
                
                # Limit to 100 rows
                if len(existing_data) > 100:
                    ws.delete_rows(101, len(existing_data))
                
                print("Updated Recommendations worksheet")
            
            # Update Risk Management worksheet
            if "risk_report" in data:
                risk_report = data["risk_report"]
                ws = self.sheet.worksheet("Risk Management")
                
                # Clear existing data
                ws.clear()
                
                # Set headers
                headers = ["Parameter", "Value", "Notes"]
                ws.append_row(headers)
                
                # Add risk management data
                if "stop_loss" in risk_report:
                    stop_loss = risk_report["stop_loss"]
                    recommended_method = stop_loss.get("recommended_method", "")
                    if recommended_method and recommended_method in stop_loss.get("methods", {}):
                        stop_price = stop_loss["methods"][recommended_method].get("stop_price", 0)
                        explanation = stop_loss["methods"][recommended_method].get("explanation", "")
                        ws.append_row(["Recommended Stop-Loss", f"${stop_price:.2f}", explanation])
                
                if "position_size" in risk_report:
                    position_size = risk_report["position_size"]
                    ws.append_row(["Recommended Position", f"{position_size.get('position_size_coins', 0):.4f} ETH", ""])
                    ws.append_row(["Position Value", f"${position_size.get('position_size_dollars', 0):.2f}", ""])
                    ws.append_row(["Risk Amount", f"${position_size.get('risk_amount', 0):.2f}", ""])
                    ws.append_row(["Portfolio %", f"{position_size.get('portfolio_percentage', 0) * 100:.2f}%", ""])
                
                if "take_profit" in risk_report:
                    take_profit = risk_report["take_profit"]
                    targets = take_profit.get("targets", [])
                    
                    for i, target in enumerate(targets):
                        ws.append_row([
                            f"Take-Profit Target {i+1}",
                            f"${target.get('target_price', 0):.2f}",
                            f"{target.get('profit_percentage', 0) * 100:.2f}% profit"
                        ])
                
                print("Updated Risk Management worksheet")
            
            # Update Performance worksheet
            if "performance" in data:
                performance = data["performance"]
                ws = self.sheet.worksheet("Performance")
                
                # Clear existing data
                ws.clear()
                
                # Set headers
                headers = ["Metric", "Value"]
                ws.append_row(headers)
                
                # Add portfolio data
                if "portfolio" in performance:
                    portfolio = performance["portfolio"]
                    ws.append_row(["ETH Balance", f"{portfolio.get('eth_balance', 0):.4f} ETH"])
                    ws.append_row(["Current Value", f"${portfolio.get('current_value', 0):.2f}"])
                    ws.append_row(["Total Invested", f"${portfolio.get('total_invested', 0):.2f}"])
                    ws.append_row(["Total Withdrawn", f"${portfolio.get('total_withdrawn', 0):.2f}"])
                    ws.append_row(["Realized P/L", f"${portfolio.get('realized_pl', 0):.2f}"])
                    ws.append_row(["Unrealized P/L", f"${portfolio.get('unrealized_pl', 0):.2f}"])
                    ws.append_row(["Total P/L", f"${portfolio.get('total_pl', 0):.2f}"])
                    ws.append_row(["ROI", f"{portfolio.get('roi', 0) * 100:.2f}%"])
                
                # Add performance metrics
                if "metrics" in performance:
                    metrics = performance["metrics"]
                    ws.append_row(["", ""])  # Empty row for separation
                    ws.append_row(["Performance Metrics", ""])
                    
                    if "annualized_return_percentage" in metrics:
                        ws.append_row(["Annualized Return", f"{metrics['annualized_return_percentage']:.2f}%"])
                    
                    if "sharpe_ratio" in metrics:
                        ws.append_row(["Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}"])
                    
                    if "max_drawdown_percentage" in metrics:
                        ws.append_row(["Maximum Drawdown", f"{metrics['max_drawdown_percentage']:.2f}%"])
                
                # 
(Content truncated due to size limit. Use line ranges to read in chunks)