#!/usr/bin/env python3
"""
ETH Investment Script - Test Suite
---------------------------------
This module tests the functionality of the ETH investment script components.
It validates the integration of all modules and ensures proper functionality.

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
import unittest

# Import our custom modules
from eth_price_tracker import ETHPriceTracker
from eth_technical_analysis import ETHTechnicalAnalysis
from eth_investment_advisor import ETHInvestmentAdvisor
from eth_risk_manager import ETHRiskManager
from eth_performance_tracker import ETHPerformanceTracker
from eth_investment_dashboard import ETHInvestmentDashboard

class ETHInvestmentScriptTest(unittest.TestCase):
    """Test suite for ETH investment script"""
    
    def setUp(self):
        """Set up test environment"""
        print("\nSetting up test environment...")
        
        # Create test directories
        self.test_data_dir = "test_data"
        self.test_charts_dir = "test_charts"
        
        if not os.path.exists(self.test_data_dir):
            os.makedirs(self.test_data_dir)
            
        if not os.path.exists(self.test_charts_dir):
            os.makedirs(self.test_charts_dir)
            
        # Initialize modules
        self.price_tracker = ETHPriceTracker()
        self.analyzer = ETHTechnicalAnalysis()
        self.advisor = ETHInvestmentAdvisor(risk_tolerance="medium")
        self.risk_manager = ETHRiskManager(portfolio_value=10000)
        self.performance_tracker = ETHPerformanceTracker(
            trades_file=os.path.join(self.test_data_dir, "test_trades.json"),
            decisions_file=os.path.join(self.test_data_dir, "test_decisions.json")
        )
        
        # Create test config
        self.test_config = {
            "portfolio_value": 10000,
            "risk_tolerance": "medium",
            "max_risk_per_trade": 0.02,
            "max_portfolio_exposure": 0.25,
            "analysis_frequency": "weekly",
            "analysis_day": "Monday",
            "google_sheets_enabled": False,
            "save_charts": True,
            "charts_directory": self.test_charts_dir,
            "data_directory": self.test_data_dir
        }
        
        # Save test config
        with open(os.path.join(self.test_data_dir, "test_config.json"), 'w') as f:
            json.dump(self.test_config, f, indent=4)
            
        # Initialize dashboard with test config
        self.dashboard = ETHInvestmentDashboard(
            config_file=os.path.join(self.test_data_dir, "test_config.json")
        )
        
        print("Test environment set up successfully")
    
    def tearDown(self):
        """Clean up after tests"""
        print("\nCleaning up test environment...")
        
        # Clean up is optional - you might want to keep test files for inspection
        # Uncomment the following lines to clean up test files
        
        # import shutil
        # if os.path.exists(self.test_data_dir):
        #     shutil.rmtree(self.test_data_dir)
        # if os.path.exists(self.test_charts_dir):
        #     shutil.rmtree(self.test_charts_dir)
            
        print("Test environment cleaned up")
    
    def test_price_tracker(self):
        """Test ETH price tracker functionality"""
        print("\nTesting ETH price tracker...")
        
        # Test current price
        current_data = self.price_tracker.get_current_price()
        self.assertIsNotNone(current_data, "Failed to get current price data")
        self.assertIn("price", current_data, "Price data missing from current data")
        self.assertGreater(current_data["price"], 0, "Price should be greater than 0")
        
        print(f"Current ETH price: ${current_data['price']:.2f}")
        
        # Test historical prices
        historical_prices = self.price_tracker.get_historical_prices(days=30)
        self.assertFalse(historical_prices.empty, "Failed to get historical price data")
        self.assertGreaterEqual(len(historical_prices), 25, "Should have at least 25 days of data")
        
        print(f"Retrieved {len(historical_prices)} days of historical data")
        
        # Test gas price data
        gas_data = self.price_tracker.get_gas_prices()
        self.assertIsNotNone(gas_data, "Failed to get gas price data")
        
        if gas_data:
            print(f"Current gas prices: Safe: {gas_data.get('SafeGasPrice')} gwei, " +
                  f"Proposed: {gas_data.get('ProposeGasPrice')} gwei, " +
                  f"Fast: {gas_data.get('FastGasPrice')} gwei")
        
        print("ETH price tracker tests passed")
    
    def test_technical_analysis(self):
        """Test technical analysis functionality"""
        print("\nTesting technical analysis...")
        
        # Get historical prices for analysis
        historical_prices = self.price_tracker.get_historical_prices(days=90)
        self.assertFalse(historical_prices.empty, "Failed to get historical price data for analysis")
        
        # Perform analysis
        analysis_results = self.analyzer.analyze_price_data(historical_prices)
        self.assertIsNotNone(analysis_results, "Failed to perform technical analysis")
        self.assertIn("rsi", analysis_results, "RSI missing from analysis results")
        self.assertIn("macd_signal", analysis_results, "MACD signal missing from analysis results")
        
        print(f"RSI: {analysis_results.get('rsi', 0):.2f}")
        print(f"MACD Signal: {analysis_results.get('macd_signal', 'unknown')}")
        print(f"Golden Cross: {analysis_results.get('golden_cross', False)}")
        print(f"Death Cross: {analysis_results.get('death_cross', False)}")
        
        # Test chart generation
        chart_path = os.path.join(self.test_charts_dir, "test_price_chart.png")
        chart_result = self.analyzer.plot_price_chart(historical_prices, save_path=chart_path)
        self.assertTrue(chart_result, "Failed to generate price chart")
        self.assertTrue(os.path.exists(chart_path), "Price chart file not created")
        
        print(f"Price chart saved to {chart_path}")
        print("Technical analysis tests passed")
    
    def test_investment_advisor(self):
        """Test investment advisor functionality"""
        print("\nTesting investment advisor...")
        
        # Get data for recommendation
        historical_prices = self.price_tracker.get_historical_prices(days=90)
        analysis_results = self.analyzer.analyze_price_data(historical_prices)
        
        # Generate recommendation
        recommendation = self.advisor.generate_recommendation(analysis_results, historical_prices)
        self.assertIsNotNone(recommendation, "Failed to generate investment recommendation")
        self.assertIn("recommendation", recommendation, "Recommendation missing from results")
        self.assertIn("action", recommendation, "Action missing from recommendation")
        
        print(f"Investment Recommendation: {recommendation.get('recommendation', 'UNKNOWN')}")
        print(f"Recommended Action: {recommendation.get('action', 'UNKNOWN')}")
        
        # Test saving recommendation
        rec_path = os.path.join(self.test_data_dir, "test_recommendation.json")
        save_result = self.advisor.save_recommendation(recommendation, rec_path)
        self.assertTrue(save_result, "Failed to save recommendation")
        self.assertTrue(os.path.exists(rec_path), "Recommendation file not created")
        
        # Test loading recommendation
        loaded_rec = self.advisor.load_recommendation(rec_path)
        self.assertIsNotNone(loaded_rec, "Failed to load recommendation")
        self.assertEqual(loaded_rec["recommendation"], recommendation["recommendation"], 
                         "Loaded recommendation doesn't match original")
        
        print("Investment advisor tests passed")
    
    def test_risk_manager(self):
        """Test risk manager functionality"""
        print("\nTesting risk manager...")
        
        # Get current price
        current_data = self.price_tracker.get_current_price()
        current_price = current_data.get("price", 0)
        
        # Set a sample entry price (e.g., slightly below current price)
        entry_price = current_price * 0.98
        
        # Get historical prices for ATR calculation
        historical_prices = self.price_tracker.get_historical_prices(days=30)
        
        # Test stop-loss calculation
        stop_loss = self.risk_manager.calculate_stop_loss(entry_price, historical_prices)
        self.assertIsNotNone(stop_loss, "Failed to calculate stop-loss")
        self.assertIn("recommended_stop_price", stop_loss, "Recommended stop price missing")
        
        print(f"Entry Price: ${entry_price:.2f}")
        print(f"Recommended Stop-Loss: ${stop_loss['recommended_stop_price']:.2f}")
        
        # Test position size calculation
        position_size = self.risk_manager.calculate_position_size(entry_price, stop_loss["recommended_stop_price"])
        self.assertIsNotNone(position_size, "Failed to calculate position size")
        self.assertIn("position_size_coins", position_size, "Position size in coins missing")
        
        print(f"Recommended Position: {position_size['position_size_coins']:.4f} ETH")
        print(f"Position Value: ${position_size['position_size_dollars']:.2f}")
        
        # Test take-profit targets
        take_profit = self.risk_manager.calculate_take_profit_targets(entry_price, stop_loss["recommended_stop_price"])
        self.assertIsNotNone(take_profit, "Failed to calculate take-profit targets")
        self.assertIn("targets", take_profit, "Targets missing from take-profit results")
        self.assertGreater(len(take_profit["targets"]), 0, "No take-profit targets generated")
        
        print("Take-Profit Targets:")
        for i, target in enumerate(take_profit["targets"]):
            print(f"Target {i+1}: ${target['target_price']:.2f} ({target['profit_percentage'] * 100:.2f}% profit)")
        
        # Test risk report generation
        risk_report = self.risk_manager.generate_risk_report(entry_price, current_price, historical_prices)
        self.assertIsNotNone(risk_report, "Failed to generate risk report")
        
        # Test saving risk report
        report_path = os.path.join(self.test_data_dir, "test_risk_report.json")
        save_result = self.risk_manager.save_risk_report(risk_report, report_path)
        self.assertTrue(save_result, "Failed to save risk report")
        self.assertTrue(os.path.exists(report_path), "Risk report file not created")
        
        print("Risk manager tests passed")
    
    def test_performance_tracker(self):
        """Test performance tracker functionality"""
        print("\nTesting performance tracker...")
        
        # Get current price
        current_data = self.price_tracker.get_current_price()
        current_price = current_data.get("price", 0)
        
        # Test trade recording
        trade1 = self.performance_tracker.record_trade("buy", current_price * 0.9, 1.0, 
                                                      (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"), 
                                                      "Test buy trade")
        self.assertIsNotNone(trade1, "Failed to record buy trade")
        
        trade2 = self.performance_tracker.record_trade("sell", current_price, 0.5, 
                                                      datetime.now().strftime("%Y-%m-%d"), 
                                                      "Test sell trade")
        self.assertIsNotNone(trade2, "Failed to record sell trade")
        
        # Test decision recording
        decision = self.performance_tracker.record_decision("BUY", current_price, {"rsi": 30}, 
                                                          datetime.now().strftime("%Y-%m-%d"))
        self.assertIsNotNone(decision, "Failed to record decision")
        
        # Test portfolio value calculation
        portfolio = self.performance_tracker.calculate_portfolio_value(current_price)
        self.assertIsNotNone(portfolio, "Failed to calculate portfolio value")
        self.assertIn("eth_balance", portfolio, "ETH balance missing from portfolio")
        
        print(f"ETH Balance: {portfolio['eth_balance']:.4f} ETH")
        print(f"Current Value: ${portfolio['current_value']:.2f}")
        
        # Test performance metrics
        metrics = self.performance_tracker.calculate_performance_metrics(current_price)
        self.assertIsNotNone(metrics, "Failed to calculate performance metrics")
        
        # Test decision evaluation
        evaluation = self.performance_tracker.evaluate_decision_history(current_price)
        self.assertIsNotNone(evaluation, "Failed to evaluate decision history")
        
        # Test performance report
        performance_report = self.performance_tracker.generate_performance_report(current_price)
        self.assertIsNotNone(performance_report, "Failed to generate performance report")
        
        # Test saving performance report
        report_path = os.path.join(self.test_data_dir, "test_performance_report.json")
        save_result = self.performance_tracker.save_performance_report(performance_report, report_path)
        self.assertTrue(save_result, "Failed to save performance report")
        self.assertTrue(os.path.exists(report_path), "Performance report file not created")
        
        # Test performance chart
        chart_path = os.path.join(self.test_charts_dir, "test_performance_chart.png")
        chart_result = self.performance_tracker.plot_performance_chart(save_path=chart_path)
        self.assertTrue(chart_result, "Failed to generate performance chart")
        self.assertTrue(os.path.exists(chart_path), "Performance chart file not created")
        
        print("Performance tracker tests passed")
    
    def test_dashboard(self):
        """Test dashboard functionality"""
        print("\nTesting dashboard...")
        
        # Test manual run
        results = self.dashboard.run_weekly_analysis()
        self.assertIsNotNone(results, "Failed to run weekly analysis")
        self.assertIn("price_data", results, "Price data missing from results")
        self.assertIn("analysis", results, "Analysis missing from results")
        self.assertIn("recommendation", results, "Recommendation missing from results")
        
        # Test beginner-friendly summary
        summary = self.dashboard.generate_beginner_friendly_summary(results)
        self.assertIsNotNone(summary, "Failed to generate beginner-friendly summary")
        self.assertGreater(len(summary), 500, "Summary seems too short")
        
        # Save summary for inspection
        summary_path = os.path.join(self.test_data_dir, "test_summary.txt")
        with open(summary_path, 'w') as f:
            f.write(summary)
            
        print(f"Beginner-friendly summary saved to {summary_path}")
        
        # Test trade recording through dashboard
        current_data = self.price_tracker.get_current_price()
        current_price = current_data.get("price", 0)
        
        trade = self.dashboard.record_trade("buy", current_price, 0.1, "Test trade through dashboard")
        self.assertIsNotNone(trade, "Failed to record trade through dashboard")
        
        print("Dashboard tests passed")
    
    def test_full_integration(self):
        """Test full integration of all components"""
        print("\nTesting full integration...")
        
        # This test simulates a complete workflow
        
        # 1. Get current price data
        current_data = self.price_tracker.get_current_price()
        current_price = current_data.get("price", 0)
        
       
(Content truncated due to size limit. Use line ranges to read in chunks)