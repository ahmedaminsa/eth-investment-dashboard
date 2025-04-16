#!/usr/bin/env python3
"""
ETH Performance Tracker Module
------------------------------
This module implements performance tracking for ETH investments.
It provides profit/loss tracking, performance metrics, and historical decision evaluation.

Author: Manus AI
Date: April 16, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import matplotlib.pyplot as plt

class ETHPerformanceTracker:
    """Class for tracking ETH investment performance"""
    
    def __init__(self, trades_file="eth_trades.json", decisions_file="eth_decisions.json"):
        """
        Initialize the performance tracker
        
        Args:
            trades_file (str): File to store trade data
            decisions_file (str): File to store decision history
        """
        self.trades_file = trades_file
        self.decisions_file = decisions_file
        self.trades = self._load_trades()
        self.decisions = self._load_decisions()
    
    def _load_trades(self):
        """Load trades from file"""
        try:
            if os.path.exists(self.trades_file):
                with open(self.trades_file, 'r') as f:
                    trades = json.load(f)
                print(f"Loaded {len(trades)} trades from {self.trades_file}")
                return trades
            else:
                print(f"No trades file found at {self.trades_file}, starting with empty trades list")
                return []
        except Exception as e:
            print(f"Error loading trades: {str(e)}")
            return []
    
    def _load_decisions(self):
        """Load decisions from file"""
        try:
            if os.path.exists(self.decisions_file):
                with open(self.decisions_file, 'r') as f:
                    decisions = json.load(f)
                print(f"Loaded {len(decisions)} decisions from {self.decisions_file}")
                return decisions
            else:
                print(f"No decisions file found at {self.decisions_file}, starting with empty decisions list")
                return []
        except Exception as e:
            print(f"Error loading decisions: {str(e)}")
            return []
    
    def _save_trades(self):
        """Save trades to file"""
        try:
            with open(self.trades_file, 'w') as f:
                json.dump(self.trades, f, indent=4)
            print(f"Saved {len(self.trades)} trades to {self.trades_file}")
            return True
        except Exception as e:
            print(f"Error saving trades: {str(e)}")
            return False
    
    def _save_decisions(self):
        """Save decisions to file"""
        try:
            with open(self.decisions_file, 'w') as f:
                json.dump(self.decisions, f, indent=4)
            print(f"Saved {len(self.decisions)} decisions to {self.decisions_file}")
            return True
        except Exception as e:
            print(f"Error saving decisions: {str(e)}")
            return False
    
    def record_trade(self, trade_type, price, amount, date=None, notes=""):
        """
        Record a new trade
        
        Args:
            trade_type (str): Type of trade (buy, sell)
            price (float): Price of ETH at trade
            amount (float): Amount of ETH traded
            date (str): Date of trade (defaults to current date)
            notes (str): Additional notes about the trade
            
        Returns:
            dict: The recorded trade
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            trade = {
                "id": len(self.trades) + 1,
                "date": date,
                "type": trade_type.lower(),
                "price": price,
                "amount": amount,
                "value": price * amount,
                "notes": notes
            }
            
            self.trades.append(trade)
            self._save_trades()
            
            print(f"Recorded {trade_type} trade of {amount} ETH at ${price:.2f}")
            return trade
        except Exception as e:
            print(f"Error recording trade: {str(e)}")
            return None
    
    def record_decision(self, recommendation, price, analysis_data, date=None):
        """
        Record an investment decision
        
        Args:
            recommendation (str): Investment recommendation (BUY, SELL, HOLD)
            price (float): Current ETH price
            analysis_data (dict): Technical analysis data
            date (str): Date of decision (defaults to current date)
            
        Returns:
            dict: The recorded decision
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            decision = {
                "id": len(self.decisions) + 1,
                "date": date,
                "recommendation": recommendation,
                "price": price,
                "analysis": analysis_data
            }
            
            self.decisions.append(decision)
            self._save_decisions()
            
            print(f"Recorded {recommendation} decision at ${price:.2f}")
            return decision
        except Exception as e:
            print(f"Error recording decision: {str(e)}")
            return None
    
    def calculate_portfolio_value(self, current_price):
        """
        Calculate current portfolio value based on trade history
        
        Args:
            current_price (float): Current ETH price
            
        Returns:
            dict: Portfolio value details
        """
        try:
            # Calculate net ETH holdings
            eth_balance = 0
            total_invested = 0
            total_withdrawn = 0
            
            for trade in self.trades:
                if trade["type"] == "buy":
                    eth_balance += trade["amount"]
                    total_invested += trade["value"]
                elif trade["type"] == "sell":
                    eth_balance -= trade["amount"]
                    total_withdrawn += trade["value"]
            
            # Calculate current value
            current_value = eth_balance * current_price
            
            # Calculate profit/loss
            realized_pl = total_withdrawn - total_invested
            unrealized_pl = current_value - (total_invested - total_withdrawn)
            total_pl = realized_pl + unrealized_pl
            
            # Calculate ROI
            if total_invested > 0:
                roi = total_pl / total_invested
            else:
                roi = 0
                
            result = {
                "eth_balance": eth_balance,
                "total_invested": total_invested,
                "total_withdrawn": total_withdrawn,
                "current_value": current_value,
                "realized_pl": realized_pl,
                "unrealized_pl": unrealized_pl,
                "total_pl": total_pl,
                "roi": roi,
                "current_price": current_price,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return result
        except Exception as e:
            print(f"Error calculating portfolio value: {str(e)}")
            return None
    
    def calculate_performance_metrics(self, current_price, benchmark_return=0.08):
        """
        Calculate detailed performance metrics
        
        Args:
            current_price (float): Current ETH price
            benchmark_return (float): Annual benchmark return for comparison (default: 8%)
            
        Returns:
            dict: Performance metrics
        """
        try:
            # Get portfolio value
            portfolio = self.calculate_portfolio_value(current_price)
            
            if not portfolio:
                return None
                
            # Get trade history as DataFrame
            if not self.trades:
                return {
                    "error": "No trade history available for performance calculation"
                }
                
            trades_df = pd.DataFrame(self.trades)
            trades_df["date"] = pd.to_datetime(trades_df["date"])
            trades_df = trades_df.sort_values("date")
            
            # Calculate metrics
            metrics = {}
            
            # 1. Basic metrics
            metrics["total_trades"] = len(self.trades)
            metrics["buy_trades"] = len(trades_df[trades_df["type"] == "buy"])
            metrics["sell_trades"] = len(trades_df[trades_df["type"] == "sell"])
            
            # 2. Profit/Loss metrics
            metrics["realized_pl"] = portfolio["realized_pl"]
            metrics["unrealized_pl"] = portfolio["unrealized_pl"]
            metrics["total_pl"] = portfolio["total_pl"]
            metrics["roi"] = portfolio["roi"]
            metrics["roi_percentage"] = portfolio["roi"] * 100
            
            # 3. Time-based metrics
            if len(trades_df) > 0:
                first_trade_date = trades_df["date"].min()
                last_trade_date = trades_df["date"].max()
                days_invested = (datetime.now() - first_trade_date).days
                
                metrics["first_trade_date"] = first_trade_date.strftime("%Y-%m-%d")
                metrics["last_trade_date"] = last_trade_date.strftime("%Y-%m-%d")
                metrics["days_invested"] = days_invested
                
                # Annualized return
                if days_invested > 0:
                    annualized_return = (1 + portfolio["roi"]) ** (365 / days_invested) - 1
                    metrics["annualized_return"] = annualized_return
                    metrics["annualized_return_percentage"] = annualized_return * 100
                    
                    # Compare to benchmark
                    metrics["benchmark_return"] = benchmark_return
                    metrics["benchmark_return_percentage"] = benchmark_return * 100
                    metrics["excess_return"] = annualized_return - benchmark_return
                    metrics["excess_return_percentage"] = metrics["excess_return"] * 100
            
            # 4. Risk metrics
            if len(trades_df) > 1:
                # Calculate daily returns if we have enough data
                if len(trades_df) >= 30:
                    # Create a price history from trades
                    price_history = []
                    
                    for trade in self.trades:
                        price_history.append({
                            "date": trade["date"],
                            "price": trade["price"]
                        })
                    
                    price_df = pd.DataFrame(price_history)
                    price_df["date"] = pd.to_datetime(price_df["date"])
                    price_df = price_df.sort_values("date")
                    
                    # Calculate daily returns
                    price_df["return"] = price_df["price"].pct_change()
                    
                    # Calculate volatility (standard deviation of returns)
                    volatility = price_df["return"].std()
                    annualized_volatility = volatility * (252 ** 0.5)  # Annualize using trading days
                    
                    metrics["volatility"] = volatility
                    metrics["annualized_volatility"] = annualized_volatility
                    
                    # Calculate Sharpe Ratio (assuming risk-free rate of 0.02)
                    risk_free_rate = 0.02
                    if annualized_volatility > 0:
                        sharpe_ratio = (metrics.get("annualized_return", 0) - risk_free_rate) / annualized_volatility
                        metrics["sharpe_ratio"] = sharpe_ratio
                    
                    # Calculate maximum drawdown
                    price_df["cummax"] = price_df["price"].cummax()
                    price_df["drawdown"] = (price_df["price"] - price_df["cummax"]) / price_df["cummax"]
                    max_drawdown = price_df["drawdown"].min()
                    
                    metrics["max_drawdown"] = max_drawdown
                    metrics["max_drawdown_percentage"] = max_drawdown * 100
            
            # 5. Decision effectiveness (if we have decisions)
            if self.decisions:
                decisions_df = pd.DataFrame(self.decisions)
                decisions_df["date"] = pd.to_datetime(decisions_df["date"])
                decisions_df = decisions_df.sort_values("date")
                
                # Count recommendations by type
                recommendation_counts = decisions_df["recommendation"].value_counts().to_dict()
                metrics["recommendation_counts"] = recommendation_counts
                
                # Evaluate decision accuracy (simplified)
                correct_decisions = 0
                total_evaluated = 0
                
                for i in range(len(decisions_df) - 1):
                    current_decision = decisions_df.iloc[i]
                    next_decision = decisions_df.iloc[i + 1]
                    
                    price_change = (next_decision["price"] - current_decision["price"]) / current_decision["price"]
                    
                    # Evaluate if recommendation was correct
                    if (current_decision["recommendation"] == "BUY" and price_change > 0.02) or \
                       (current_decision["recommendation"] == "SELL" and price_change < -0.02) or \
                       (current_decision["recommendation"] == "HOLD" and abs(price_change) < 0.05):
                        correct_decisions += 1
                    
                    total_evaluated += 1
                
                if total_evaluated > 0:
                    decision_accuracy = correct_decisions / total_evaluated
                    metrics["decision_accuracy"] = decision_accuracy
                    metrics["decision_accuracy_percentage"] = decision_accuracy * 100
            
            return metrics
        except Exception as e:
            print(f"Error calculating performance metrics: {str(e)}")
            return None
    
    def evaluate_decision_history(self, current_price):
        """
        Evaluate the effectiveness of past investment decisions
        
        Args:
            current_price (float): Current ETH price
            
        Returns:
            dict: Decision evaluation results
        """
        try:
            if not self.decisions:
                return {
                    "error": "No decision history available for evaluation"
                }
                
            decisions_df = pd.DataFrame(self.decisions)
            decisions_df["date"] = pd.to_datetime(decisions_df["date"])
            decisions_df = decisions_df.sort_values("date")
            
            # Add price change information
            decisions_df["next_price"] = decisions_df["price"].shift(-1)
            decisions_df["price_change"] = decisions_df["next_price"] - decisions_df["price"]
            decisions_df["price_change_pct"] = decisions_df["price_change"] / decisions_df["price"]
            
            # For the last decision, use current price
            if len(decisions_df) > 0:
                decisions_df.loc[decisions_df.index[-1], "next_price"] = current_price
                decisions_df.loc[decisions_df.index[-1], "price_change"] = current_price - decisions_df.iloc[-1]["price"]
                decisions_df.loc[decisions_df.index[-1], "price_change_pct"] = decisions_df.iloc[-1]["price_change"] / decisions_df.iloc[-1]["price"]
            
            # Evaluate each decision
            evaluation_results = []
            
            for i, decision in decisions_df.it
(Content truncated due to size limit. Use line ranges to read in chunks)