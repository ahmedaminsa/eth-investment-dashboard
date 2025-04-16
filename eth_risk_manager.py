#!/usr/bin/env python3
"""
ETH Risk Management Module
--------------------------
This module implements risk management features for ETH investments.
It provides stop-loss calculation, position sizing, and portfolio exposure limits.

Author: Manus AI
Date: April 16, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class ETHRiskManager:
    """Class for managing risk in ETH investments"""
    
    def __init__(self, portfolio_value=10000, max_risk_per_trade=0.02, max_portfolio_exposure=0.25):
        """
        Initialize the risk manager
        
        Args:
            portfolio_value (float): Total portfolio value in USD
            max_risk_per_trade (float): Maximum risk per trade as a fraction (0.02 = 2%)
            max_portfolio_exposure (float): Maximum portfolio exposure to ETH as a fraction (0.25 = 25%)
        """
        self.portfolio_value = portfolio_value
        self.max_risk_per_trade = max_risk_per_trade
        self.max_portfolio_exposure = max_portfolio_exposure
    
    def update_portfolio_value(self, portfolio_value):
        """
        Update the portfolio value
        
        Args:
            portfolio_value (float): New portfolio value in USD
        """
        self.portfolio_value = portfolio_value
        print(f"Portfolio value updated to ${portfolio_value:.2f}")
    
    def calculate_position_size(self, entry_price, stop_loss_price):
        """
        Calculate optimal position size based on risk parameters
        
        Args:
            entry_price (float): Entry price for ETH
            stop_loss_price (float): Stop-loss price for ETH
            
        Returns:
            dict: Position sizing details
        """
        try:
            # Calculate risk amount in dollars
            risk_amount = self.portfolio_value * self.max_risk_per_trade
            
            # Calculate risk per coin
            if entry_price <= stop_loss_price:
                print("Error: Entry price must be greater than stop-loss price for long positions")
                return None
                
            risk_per_coin = entry_price - stop_loss_price
            
            # Calculate position size in coins
            position_size_coins = risk_amount / risk_per_coin
            
            # Calculate position size in dollars
            position_size_dollars = position_size_coins * entry_price
            
            # Check if position size exceeds maximum portfolio exposure
            max_position_dollars = self.portfolio_value * self.max_portfolio_exposure
            
            if position_size_dollars > max_position_dollars:
                # Adjust position size to respect maximum exposure
                position_size_dollars = max_position_dollars
                position_size_coins = position_size_dollars / entry_price
                actual_risk_amount = position_size_coins * risk_per_coin
                actual_risk_percentage = actual_risk_amount / self.portfolio_value
                
                explanation = (
                    f"Position size was reduced from ${risk_amount / self.max_risk_per_trade:.2f} "
                    f"to ${position_size_dollars:.2f} to respect the maximum portfolio "
                    f"exposure limit of {self.max_portfolio_exposure * 100:.1f}%. "
                    f"This results in an actual risk of ${actual_risk_amount:.2f} "
                    f"({actual_risk_percentage * 100:.2f}% of portfolio)."
                )
            else:
                explanation = (
                    f"Position size of ${position_size_dollars:.2f} respects the maximum "
                    f"risk per trade of {self.max_risk_per_trade * 100:.1f}% (${risk_amount:.2f}) "
                    f"and is within the maximum portfolio exposure limit of "
                    f"{self.max_portfolio_exposure * 100:.1f}% (${max_position_dollars:.2f})."
                )
            
            # Calculate percentage of portfolio
            portfolio_percentage = position_size_dollars / self.portfolio_value
            
            result = {
                "position_size_coins": position_size_coins,
                "position_size_dollars": position_size_dollars,
                "risk_amount": risk_amount,
                "risk_per_coin": risk_per_coin,
                "portfolio_percentage": portfolio_percentage,
                "max_position_dollars": max_position_dollars,
                "explanation": explanation
            }
            
            return result
            
        except Exception as e:
            print(f"Error calculating position size: {str(e)}")
            return None
    
    def calculate_stop_loss(self, entry_price, historical_prices=None, atr_multiplier=2.0, fixed_percentage=0.05):
        """
        Calculate stop-loss price based on various methods
        
        Args:
            entry_price (float): Entry price for ETH
            historical_prices (DataFrame): Historical price data for ATR calculation
            atr_multiplier (float): Multiplier for ATR-based stop-loss
            fixed_percentage (float): Fixed percentage for simple stop-loss
            
        Returns:
            dict: Stop-loss details with multiple methods
        """
        try:
            results = {
                "entry_price": entry_price,
                "methods": {}
            }
            
            # Method 1: Fixed percentage stop-loss
            fixed_stop = entry_price * (1 - fixed_percentage)
            fixed_risk = entry_price - fixed_stop
            fixed_risk_percentage = fixed_risk / entry_price
            
            results["methods"]["fixed_percentage"] = {
                "stop_price": fixed_stop,
                "risk_amount": fixed_risk,
                "risk_percentage": fixed_risk_percentage,
                "explanation": f"Fixed {fixed_percentage * 100:.1f}% stop-loss below entry price"
            }
            
            # Method 2: ATR-based stop-loss (if historical data is available)
            if historical_prices is not None and not historical_prices.empty and len(historical_prices) >= 14:
                # Calculate ATR (Average True Range)
                high = historical_prices["price"].rolling(window=2).max()
                low = historical_prices["price"].rolling(window=2).min()
                close = historical_prices["price"]
                
                # Calculate True Range
                tr1 = high - low
                tr2 = abs(high - close.shift())
                tr3 = abs(low - close.shift())
                
                true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
                atr = true_range.rolling(window=14).mean().iloc[-1]
                
                # Calculate ATR-based stop-loss
                atr_stop = entry_price - (atr * atr_multiplier)
                atr_risk = entry_price - atr_stop
                atr_risk_percentage = atr_risk / entry_price
                
                results["methods"]["atr_based"] = {
                    "stop_price": atr_stop,
                    "risk_amount": atr_risk,
                    "risk_percentage": atr_risk_percentage,
                    "atr_value": atr,
                    "explanation": f"ATR-based stop-loss {atr_multiplier} x ATR (${atr:.2f}) below entry price"
                }
                
                # Method 3: Support-based stop-loss (if we have enough data)
                if len(historical_prices) >= 30:
                    # Find recent lows as potential support levels
                    window = 5  # Window for local minimum detection
                    support_levels = []
                    
                    for i in range(window, len(historical_prices) - window):
                        if all(historical_prices["price"].iloc[i] <= historical_prices["price"].iloc[i-window:i]) and \
                           all(historical_prices["price"].iloc[i] <= historical_prices["price"].iloc[i+1:i+window+1]):
                            support_levels.append(historical_prices["price"].iloc[i])
                    
                    # Filter support levels below entry price
                    valid_supports = [s for s in support_levels if s < entry_price]
                    
                    if valid_supports:
                        # Find closest support level below entry price
                        closest_support = max(valid_supports)
                        support_risk = entry_price - closest_support
                        support_risk_percentage = support_risk / entry_price
                        
                        results["methods"]["support_based"] = {
                            "stop_price": closest_support,
                            "risk_amount": support_risk,
                            "risk_percentage": support_risk_percentage,
                            "explanation": f"Support-based stop-loss at nearest support level (${closest_support:.2f})"
                        }
            
            # Determine recommended stop-loss method
            if "atr_based" in results["methods"] and results["methods"]["atr_based"]["risk_percentage"] <= 0.1:
                # ATR-based is preferred if risk is reasonable
                results["recommended_method"] = "atr_based"
            elif "support_based" in results["methods"] and results["methods"]["support_based"]["risk_percentage"] <= 0.1:
                # Support-based is next preference if risk is reasonable
                results["recommended_method"] = "support_based"
            else:
                # Fixed percentage is the fallback
                results["recommended_method"] = "fixed_percentage"
                
            # Get the recommended stop-loss price
            recommended_stop = results["methods"][results["recommended_method"]]["stop_price"]
            results["recommended_stop_price"] = recommended_stop
            
            return results
            
        except Exception as e:
            print(f"Error calculating stop-loss: {str(e)}")
            return {
                "entry_price": entry_price,
                "methods": {
                    "fixed_percentage": {
                        "stop_price": entry_price * (1 - fixed_percentage),
                        "risk_amount": entry_price * fixed_percentage,
                        "risk_percentage": fixed_percentage,
                        "explanation": f"Fixed {fixed_percentage * 100:.1f}% stop-loss below entry price (fallback due to error)"
                    }
                },
                "recommended_method": "fixed_percentage",
                "recommended_stop_price": entry_price * (1 - fixed_percentage),
                "error": str(e)
            }
    
    def calculate_take_profit_targets(self, entry_price, stop_loss_price, risk_reward_ratios=[1.5, 2.5, 3.5]):
        """
        Calculate take-profit targets based on risk-reward ratios
        
        Args:
            entry_price (float): Entry price for ETH
            stop_loss_price (float): Stop-loss price for ETH
            risk_reward_ratios (list): List of risk-reward ratios for targets
            
        Returns:
            dict: Take-profit targets
        """
        try:
            # Calculate risk amount
            risk = entry_price - stop_loss_price
            
            # Calculate targets
            targets = []
            
            for ratio in risk_reward_ratios:
                target_price = entry_price + (risk * ratio)
                profit = target_price - entry_price
                profit_percentage = profit / entry_price
                
                targets.append({
                    "risk_reward_ratio": ratio,
                    "target_price": target_price,
                    "profit_amount": profit,
                    "profit_percentage": profit_percentage,
                    "explanation": f"{ratio}R target (R = ${risk:.2f})"
                })
            
            result = {
                "entry_price": entry_price,
                "stop_loss_price": stop_loss_price,
                "risk_amount": risk,
                "risk_percentage": risk / entry_price,
                "targets": targets
            }
            
            return result
            
        except Exception as e:
            print(f"Error calculating take-profit targets: {str(e)}")
            return None
    
    def calculate_trailing_stop(self, entry_price, current_price, initial_stop_price, trail_percentage=0.5):
        """
        Calculate trailing stop-loss price
        
        Args:
            entry_price (float): Entry price for ETH
            current_price (float): Current price for ETH
            initial_stop_price (float): Initial stop-loss price
            trail_percentage (float): Trailing percentage (0.5 = 0.5%)
            
        Returns:
            dict: Trailing stop details
        """
        try:
            # Only adjust stop if in profit
            if current_price <= entry_price:
                return {
                    "entry_price": entry_price,
                    "current_price": current_price,
                    "trailing_stop_price": initial_stop_price,
                    "is_adjusted": False,
                    "explanation": "Price has not moved above entry point, using initial stop-loss"
                }
            
            # Calculate trailing stop based on highest price
            trail_amount = current_price * (trail_percentage / 100)
            trailing_stop = current_price - trail_amount
            
            # Only use trailing stop if it's higher than the initial stop
            if trailing_stop > initial_stop_price:
                explanation = (
                    f"Trailing stop adjusted to ${trailing_stop:.2f}, which is {trail_percentage}% "
                    f"below the current price of ${current_price:.2f}"
                )
                is_adjusted = True
            else:
                trailing_stop = initial_stop_price
                explanation = "Trailing stop would be lower than initial stop-loss, keeping initial stop"
                is_adjusted = False
            
            result = {
                "entry_price": entry_price,
                "current_price": current_price,
                "initial_stop_price": initial_stop_price,
                "trailing_stop_price": trailing_stop,
                "trail_percentage": trail_percentage,
                "trail_amount": trail_amount,
                "is_adjusted": is_adjusted,
                "explanation": explanation
            }
            
            return result
            
        except Exception as e:
            print(f"Error calculating trailing stop: {str(e)}")
            return None
    
    def calculate_portfolio_exposure(self, eth_holdings, eth_price):
        """
        Calculate current portfolio exposure to ETH
        
        Args:
            eth_holdings (float): Current ETH holdings in coins
            eth_price (float): Current ETH price in USD
            
        Returns:
            dict: Portfolio exposure details
        """
        try:
            # Calculate ETH value
            eth_value = eth_holdings * eth_price
            
            # Calculate exposure percentage
            exposure_percentage = eth_value / self.portfolio_value
            
            # Determine if exposure exceeds limit
            exceeds_limit = exposure_percentage > self.max_portfolio_exposure
            
            # Calculate adjustment if needed
            if exceeds_limit:
                max_eth_value = self.portfolio_value * self.max_portfolio_exposure
                max_eth_holdings = max_eth_value / eth_price
                adjustment_needed = eth_holdings - max_eth_holdings
                
                expl
(Content truncated due to size limit. Use line ranges to read in chunks)