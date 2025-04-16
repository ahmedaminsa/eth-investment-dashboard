#!/usr/bin/env python3
"""
ETH Investment Dashboard - App Engine Web Application
----------------------------------------------------
This is the main application file for the ETH Investment Dashboard web application.
It provides a user interface to view ETH investment data and analysis results.

Author: Manus AI
Date: April 16, 2025
"""

import os
import json
import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from google.cloud import storage
from google.cloud import pubsub_v1
import google.oauth2.id_token
from google.auth.transport import requests as google_requests
import tempfile
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Google Cloud configuration
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'your-project-id')
BUCKET_NAME = os.environ.get('STORAGE_BUCKET', 'eth-investment-data')
TOPIC_NAME = os.environ.get('NOTIFICATION_TOPIC', 'eth-investment-notifications')

# Initialize Google Cloud clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()
firebase_request_adapter = google_requests.Request()

# Helper functions
def get_current_user():
    """Get the current user from the session"""
    id_token = session.get('id_token')
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            return claims
        except ValueError as exc:
            logger.error(f"Error verifying token: {exc}")
            return None
    return None

def get_latest_analysis():
    """Get the latest ETH analysis results from Cloud Storage"""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Find the latest analysis file
        blobs = list(bucket.list_blobs(prefix='eth_analysis_'))
        if not blobs:
            logger.warning("No analysis files found in bucket")
            return None
            
        # Sort by name (which includes date) in descending order
        blobs.sort(key=lambda x: x.name, reverse=True)
        latest_blob = blobs[0]
        
        # Download the latest analysis
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            latest_blob.download_to_filename(temp_file.name)
            with open(temp_file.name, 'r') as f:
                analysis = json.load(f)
            os.unlink(temp_file.name)
            
        return analysis
    except Exception as e:
        logger.error(f"Error getting latest analysis: {e}")
        return None

def get_historical_analyses(limit=10):
    """Get historical ETH analyses from Cloud Storage"""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Find all analysis files
        blobs = list(bucket.list_blobs(prefix='eth_analysis_'))
        if not blobs:
            logger.warning("No analysis files found in bucket")
            return []
            
        # Sort by name (which includes date) in descending order
        blobs.sort(key=lambda x: x.name, reverse=True)
        
        # Limit the number of analyses
        blobs = blobs[:limit]
        
        # Download and parse each analysis
        analyses = []
        for blob in blobs:
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                blob.download_to_filename(temp_file.name)
                with open(temp_file.name, 'r') as f:
                    analysis = json.load(f)
                os.unlink(temp_file.name)
                analyses.append(analysis)
                
        return analyses
    except Exception as e:
        logger.error(f"Error getting historical analyses: {e}")
        return []

def get_trade_history():
    """Get ETH trade history from Cloud Storage"""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        trades_blob = bucket.blob('eth_trades.json')
        
        if not trades_blob.exists():
            logger.warning("No trade history found in bucket")
            return []
            
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            trades_blob.download_to_filename(temp_file.name)
            with open(temp_file.name, 'r') as f:
                trades = json.load(f)
            os.unlink(temp_file.name)
            
        return trades
    except Exception as e:
        logger.error(f"Error getting trade history: {e}")
        return []

def generate_price_chart(historical_prices):
    """Generate a price chart with technical indicators"""
    try:
        # Convert to DataFrame if it's a list
        if isinstance(historical_prices, list):
            df = pd.DataFrame(historical_prices)
        else:
            df = historical_prices
            
        # Ensure we have the required columns
        if 'date' not in df.columns or 'price' not in df.columns:
            logger.error("Historical prices data missing required columns")
            return None
            
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot the price
        ax.plot(df['date'], df['price'], label='ETH Price', color='#3498db')
        
        # Add moving averages if available
        if 'ma50' in df.columns:
            ax.plot(df['date'], df['ma50'], label='50-day MA', color='#2ecc71', linestyle='--')
        if 'ma200' in df.columns:
            ax.plot(df['date'], df['ma200'], label='200-day MA', color='#e74c3c', linestyle='--')
            
        # Set labels and title
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.set_title('ETH Price Chart')
        
        # Add grid and legend
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Tight layout
        plt.tight_layout()
        
        # Convert plot to base64 encoded image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close(fig)
        
        return image_base64
    except Exception as e:
        logger.error(f"Error generating price chart: {e}")
        return None

def trigger_analysis():
    """Trigger a new ETH analysis via Pub/Sub"""
    try:
        topic_path = publisher.topic_path(PROJECT_ID, 'run-eth-analysis')
        message = 'Run ETH investment analysis'
        data = message.encode('utf-8')
        future = publisher.publish(topic_path, data=data)
        message_id = future.result()
        logger.info(f"Published message to {topic_path} with ID: {message_id}")
        return True
    except Exception as e:
        logger.error(f"Error triggering analysis: {e}")
        return False

def record_trade(trade_type, price, amount, notes=""):
    """Record a new trade in Cloud Storage"""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        trades_blob = bucket.blob('eth_trades.json')
        
        # Get existing trades
        trades = []
        if trades_blob.exists():
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                trades_blob.download_to_filename(temp_file.name)
                with open(temp_file.name, 'r') as f:
                    trades = json.load(f)
                os.unlink(temp_file.name)
        
        # Create new trade
        new_trade = {
            'type': trade_type,
            'price': float(price),
            'amount': float(amount),
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.datetime.now().isoformat(),
            'notes': notes
        }
        
        # Add to trades list
        trades.append(new_trade)
        
        # Save updated trades
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            json.dump(trades, temp_file)
            temp_file.flush()
            trades_blob.upload_from_filename(temp_file.name)
            os.unlink(temp_file.name)
            
        return True
    except Exception as e:
        logger.error(f"Error recording trade: {e}")
        return False

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    # Get latest analysis
    analysis = get_latest_analysis()
    
    # Get trade history
    trades = get_trade_history()
    
    # Generate price chart if we have historical prices
    price_chart = None
    if analysis and 'historical_prices' in analysis:
        price_chart = generate_price_chart(analysis['historical_prices'])
    
    return render_template(
        'dashboard.html',
        user=user,
        analysis=analysis,
        trades=trades,
        price_chart=price_chart
    )

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/sessionLogin', methods=['POST'])
def session_login():
    """Handle login with Firebase ID token"""
    id_token = request.json.get('idToken')
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            session['id_token'] = id_token
            return jsonify({'success': True}), 200
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 401
    return jsonify({'error': 'No ID token provided'}), 400

@app.route('/history')
def history():
    """Historical analysis page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    # Get historical analyses
    analyses = get_historical_analyses()
    
    return render_template(
        'history.html',
        user=user,
        analyses=analyses
    )

@app.route('/performance')
def performance():
    """Performance tracking page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    # Get trade history
    trades = get_trade_history()
    
    # Get latest analysis for current price
    analysis = get_latest_analysis()
    current_price = 0
    if analysis and 'price_data' in analysis and 'price' in analysis['price_data']:
        current_price = analysis['price_data']['price']
    
    return render_template(
        'performance.html',
        user=user,
        trades=trades,
        current_price=current_price
    )

@app.route('/settings')
def settings():
    """Settings page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    return render_template(
        'settings.html',
        user=user
    )

@app.route('/api/analysis/latest')
def api_latest_analysis():
    """API endpoint for latest analysis"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    analysis = get_latest_analysis()
    if not analysis:
        return jsonify({'error': 'No analysis found'}), 404
        
    return jsonify(analysis)

@app.route('/api/analysis/trigger', methods=['POST'])
def api_trigger_analysis():
    """API endpoint to trigger a new analysis"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    success = trigger_analysis()
    if not success:
        return jsonify({'error': 'Failed to trigger analysis'}), 500
        
    return jsonify({'success': True, 'message': 'Analysis triggered successfully'})

@app.route('/api/trades', methods=['GET'])
def api_get_trades():
    """API endpoint to get trade history"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    trades = get_trade_history()
    return jsonify(trades)

@app.route('/api/trades', methods=['POST'])
def api_record_trade():
    """API endpoint to record a new trade"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    if not data or 'type' not in data or 'price' not in data or 'amount' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
        
    success = record_trade(
        data['type'],
        data['price'],
        data['amount'],
        data.get('notes', '')
    )
    
    if not success:
        return jsonify({'error': 'Failed to record trade'}), 500
        
    return jsonify({'success': True, 'message': 'Trade recorded successfully'})

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host='127.0.0.1', port=8080, debug=True)
