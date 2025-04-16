# Cloud-Only Deployment Guide for ETH Investment Dashboard

This guide will walk you through deploying your ETH investment dashboard entirely in Google Cloud, without requiring any local setup on your computer. Everything will be done through your web browser.

## Step 1: Create a Google Cloud Account

1. Open your web browser and go to [cloud.google.com](https://cloud.google.com)
2. Click the "Get started for free" button
3. Sign in with your Google account
4. Fill in your information and add a payment method (required for verification)
5. Click "Start my free trial"

## Step 2: Create a New Project

1. In the Google Cloud Console, click on the project dropdown at the top of the page
2. Click "New Project"
3. Enter "ETH Investment Dashboard" as the project name
4. Click "Create"
5. Wait for the project to be created, then select it from the project dropdown

## Step 3: Enable Required APIs

1. In the Google Cloud Console, click on the navigation menu (☰)
2. Scroll down and click on "APIs & Services" > "Library"
3. Search for and enable the following APIs (click each one and click "Enable"):
   - App Engine Admin API
   - Cloud Storage
   - Cloud Pub/Sub API
   - Cloud Build API
   - Cloud Functions API

## Step 4: Open Cloud Shell

1. Click the Cloud Shell icon (>_) in the top-right corner of the Google Cloud Console
2. This opens a terminal directly in your browser
3. Wait for Cloud Shell to initialize

## Step 5: Create Project Directory Structure

In Cloud Shell, run the following commands to create the necessary directory structure:

```bash
mkdir -p eth-dashboard/app_engine/static/css eth-dashboard/app_engine/static/js eth-dashboard/app_engine/templates
cd eth-dashboard
```

## Step 6: Create Main Application File

1. In Cloud Shell, run:
```bash
nano app_engine/main.py
```

2. Copy and paste the following code:

```python
import os
import json
import datetime
import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from google.cloud import storage, pubsub_v1

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Initialize Firebase Admin
try:
    firebase_admin.initialize_app()
except ValueError:
    # Already initialized
    pass

# Initialize Google Cloud clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

# Constants
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')
STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET')
NOTIFICATION_TOPIC = os.environ.get('NOTIFICATION_TOPIC')

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('history.html')

@app.route('/performance')
def performance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Mock data for demonstration
    trades = [
        {
            'date': '2025-04-01',
            'type': 'buy',
            'price': 3500.00,
            'amount': 0.5,
            'notes': 'Initial investment'
        },
        {
            'date': '2025-04-08',
            'type': 'buy',
            'price': 3300.00,
            'amount': 0.3,
            'notes': 'Buying the dip'
        }
    ]
    
    current_price = 3800.00  # This would be fetched from an API in production
    now = datetime.datetime.now()
    
    return render_template('performance.html', trades=trades, current_price=current_price, now=now)

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Mock user data for demonstration
    user = {
        'name': 'Demo User',
        'email': 'demo@example.com'
    }
    
    return render_template('settings.html', user=user)

# API Routes
@app.route('/api/auth', methods=['POST'])
def authenticate():
    data = request.json
    id_token = data.get('idToken')
    
    try:
        # Verify Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        
        # Set session
        session['user_id'] = user_id
        session['email'] = decoded_token.get('email', '')
        session['name'] = decoded_token.get('name', '')
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/analysis/run', methods=['POST'])
def run_analysis():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        # Publish message to trigger Cloud Function
        topic_path = publisher.topic_path(PROJECT_ID, NOTIFICATION_TOPIC)
        message = json.dumps({'action': 'run_analysis', 'user_id': session['user_id']}).encode('utf-8')
        publisher.publish(topic_path, data=message)
        
        return jsonify({'success': True, 'message': 'Analysis started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/trades', methods=['POST'])
def record_trade():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    data = request.json
    
    # Validate data
    required_fields = ['type', 'price', 'amount', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing required field: {field}'})
    
    try:
        # In production, this would save to Cloud Storage or Firestore
        # For demo, we'll just return success
        return jsonify({'success': True, 'message': 'Trade recorded'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/trades/clear', methods=['POST'])
def clear_trades():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        # In production, this would delete from Cloud Storage or Firestore
        # For demo, we'll just return success
        return jsonify({'success': True, 'message': 'Trades cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
```

3. Press Ctrl+X, then Y, then Enter to save the file

## Step 7: Create App Engine Configuration

1. In Cloud Shell, run:
```bash
nano app_engine/app.yaml
```

2. Copy and paste the following code:

```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT main:app

env_variables:
  GOOGLE_CLOUD_PROJECT: "eth-investment-457013"
  STORAGE_BUCKET: "eth-investment-data-eth-investment-457013"
  NOTIFICATION_TOPIC: "eth-investment-notifications"
  SECRET_KEY: "change-this-to-a-secure-secret-key-in-production"

handlers:
- url: /static
  static_dir: static
  secure: always

- url: /.*
  script: auto
  secure: always
```

3. Replace "eth-investment-457013" with your actual project ID
4. Press Ctrl+X, then Y, then Enter to save the file

## Step 8: Create Requirements File

1. In Cloud Shell, run:
```bash
nano app_engine/requirements.txt
```

2. Copy and paste the following:

```
Flask==2.0.1
google-cloud-storage==1.42.0
google-cloud-pubsub==2.8.0
firebase-admin==5.0.3
gunicorn==20.1.0
pandas==1.3.3
matplotlib==3.4.3
```

3. Press Ctrl+X, then Y, then Enter to save the file

## Step 9: Create HTML Templates

### Base Template

1. In Cloud Shell, run:
```bash
nano app_engine/templates/base.html
```

2. Copy and paste the following code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ETH Investment Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav id="sidebar" class="col-md-3 col-lg-2 d-md-block bg-dark sidebar collapse">
                <div class="position-sticky pt-3">
                    <div class="text-center mb-4">
                        <h4 class="text-white">ETH Investment</h4>
                        <p class="text-muted">Dashboard</p>
                    </div>
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link" href="/">
                                <i class="bi bi-speedometer2 me-2"></i>
                                Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/history">
                                <i class="bi bi-clock-history me-2"></i>
                                Analysis History
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/performance">
                                <i class="bi bi-graph-up me-2"></i>
                                Performance
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/settings">
                                <i class="bi bi-gear me-2"></i>
                                Settings
                            </a>
                        </li>
                        <li class="nav-item mt-5">
                            <a class="nav-link" href="#" id="logoutBtn">
                                <i class="bi bi-box-arrow-right me-2"></i>
                                Logout
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">ETH Investment Dashboard</h1>
                    <div class="btn-toolbar mb-2 mb-md-0">
                        <button type="button" class="btn btn-primary me-2" id="runAnalysisBtn">
                            <i class="bi bi-play-fill me-1"></i>
                            Run Analysis Now
                        </button>
                    </div>
                </div>

                {% block content %}{% endblock %}
            </main>
        </div>
    </div>

    <!-- Firebase -->
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-analytics-compat.js"></script>
    
    <!-- Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="/static/js/main.js"></script>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

3. Press Ctrl+X, then Y, then Enter to save the file

### Login Template

1. In Cloud Shell, run:
```bash
nano app_engine/templates/login.html
```

2. Copy and paste the following code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - ETH Investment Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body class="bg-light">
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-md-6 col-lg-4">
                <div class="card shadow">
                    <div class="card-body p-5">
                        <div class="text-center mb-4">
                            <i class="bi bi-currency-ethereum display-1 text-primary"></i>
                            <h2 class="mt-3">ETH Investment</h2>
                            <p class="text-muted">Dashboard Login</p>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary" id="googleSignInBtn">
                                <i class="bi bi-google me-2"></i>
                                Sign in with Google
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Firebase -->
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-auth-compat.js"></script>
    
    <!-- Custom JS -->
    <script src="/static/js/main.js"></script>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize Firebase Authentication
            initFirebase();
            
            // Set up Google Sign-In button
            const googleSignInBtn = document.getElementById('googleSignInBtn');
            if (googleSignInBtn) {
                googleSignInBtn.addEventListener('click', function() {
                    const provider = new firebase.auth.GoogleAuthProvider();
                    firebase.auth().signInWithPopup(provider)
                        .then((result) => {
                            // Get ID token
                            return result.user.getIdToken();
                        })
                        .then((idToken) => {
                            // Send token to backend
                            return fetch('/api/auth', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ idToken: idToken })
                            });
                        })
                        .then((response) => response.json())
                        .then((data) => {
                            if (data.success) {
                                window.location.href = '/';
                            } else {
                                alert('Authentication failed: ' + data.error);
                            }
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                            alert('Authentication failed. Please try again.');
                        });
                });
            }
        });
    </script>
</body>
</html>
```

3. Press Ctrl+X, then Y, then Enter to save the file

### Dashboard Template

1. In Cloud Shell, run:
```bash
nano app_engine/templates/dashboard.html
```

2. Copy and paste the following code:

```html
{% extends "base.html" %}

{% block content %}
<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="card-title mb-0">
                    <i class="bi bi-currency-exchange me-2"></i>ETH Price & Recommendation
                </h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h2 class="mb-0">$3,800.25</h2>
                        <p class="text-success">
                            <i class="bi bi-arrow-up"></i> +2.5% (24h)
                        </p>
                        <div class="mt-3">
                            <span class="badge bg-success p-2">BUY</span>
                            <p class="mt-2">Strong buy signal based on technical indicators and market sentiment.</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="d-flex flex-column h-100 justify-content-between">
                            <div>
                                <p class="mb-1">Next Support</p>
                                <h5>$3,650.00</h5>
                            </div>
                            <div>
                                <p class="mb-1">Next Resistance</p>
                                <h5>$4,000.00</h5>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="card-title mb-0">
                    <i class="bi bi-shield-check me-2"></i>Risk Management
                </h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <p class="mb-1">Recommended Position Size</p>
                        <h5>0.25 ETH ($950.06)</h5>
                        <p class="text-muted small">Based on 1% risk per trade</p>
                        
                        <p class="mb-1 mt-3">Stop Loss Price</p>
                        <h5 class="text-danger">$3,650.00</h5>
                        <p class="text-muted small">4% below entry price</p>
                    </div>
                    <div class="col-md-6">
                        <p class="mb-1">Take Profit Targets</p>
                        <div class="d-flex justify-content-between mb-2">
                            <span>Target 1 (1:1)</span>
                            <span class="text-success">$3,950.00</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span>Target 2 (1:2)</span>
                            <span class="text-success">$4,100.00</span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span>Target 3 (1:3)</span>
                            <span class="text-success">$4,250.00</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row mb-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="card-title mb-0">
                    <i class="bi bi-graph-up me-2"></i>ETH Price Chart
                </h5>
            </div>
            <div class="card-body">
                <canvas id="priceChart" height="300"></canvas>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="card-title mb-0">
                    <i class="bi bi-bar-chart me-2"></i>Technical Analysis
                </h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h6>RSI (14)</h6>
                        <div class="progress mb-3" style="height: 20px;">
                            <div class="progress-bar" role="progressbar" style="width: 65%;" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100">65</div>
                        </div>
                        
                        <h6>MACD</h6>
                        <p class="text-success">Bullish Crossover</p>
                        
                        <h6>Moving Averages</h6>
                        <p>Price above MA50 and MA200</p>
                    </div>
                    <div class="col-md-6">
                        <h6>Trend Analysis</h6>
                        <div class="d-flex justify-content-between mb-2">
                            <span>Short-term</span>
                            <span class="text-success">Bullish</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span>Medium-term</span>
                            <span class="text-success">Bullish</span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span>Long-term</span>
                            <span class="text-success">Bullish</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">
                    <i class="bi bi-wallet2 me-2"></i>Performance Tracking
                </h5>
                <a href="/performance" class="btn btn-sm btn-light">View Details</a>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <p class="mb-1">ETH Holdings</p>
                        <h5>0.8 ETH</h5>
                        <p class="text-muted small">$3,040.20 at current price</p>
                        
                        <p class="mb-1 mt-3">Unrealized P/L</p>
                        <h5 class="text-success">+$240.20 (+8.6%)</h5>
                    </div>
                    <div class="col-md-6">
                        <p class="mb-1">Last Trade</p>
                        <h5>Buy 0.3 ETH @ $3,300.00</h5>
                        <p class="text-muted small">April 8, 2025</p>
                        
                        <button class="btn btn-primary mt-3" data-bs-toggle="modal" data-bs-target="#recordTradeModal">
                            <i class="bi bi-plus-circle me-2"></i>Record Trade
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Record Trade Modal -->
<div class="modal fade" id="recordTradeModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Record ETH Trade</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="recordTradeForm">
                    <div class="mb-3">
                        <label class="form-label">Trade Type</label>
                        <div class="btn-group w-100" role="group">
                            <input type="radio" class="btn-check" name="tradeType" id="typeBuy" value="buy" checked>
                            <label class="btn btn-outline-success" for="typeBuy">Buy</label>
                            <input type="radio" class="btn-check" name="tradeType" id="typeSell" value="sell">
                            <label class="btn btn-outline-danger" for="typeSell">Sell</label>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="tradePrice" class="form-label">Price (USD)</label>
                        <div class="input-group">
                            <span class="input-group-text">$</span>
                            <input type="number" class="form-control" id="tradePrice" step="0.01" min="0" required value="3800.25">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="tradeAmount" class="form-label">Amount (ETH)</label>
                        <input type="number" class="form-control" id="tradeAmount" step="0.0001" min="0.0001" required>
                    </div>
                    <div class="mb-3">
                        <label for="tradeDate" class="form-label">Date</label>
                        <input type="date" class="form-control" id="tradeDate" required>
                    </div>
                    <div class="mb-3">
                        <label for="tradeNotes" class="form-label">Notes (Optional)</label>
                        <textarea class="form-control" id="tradeNotes" rows="2"></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" id="submitTradeBtn">Record Trade</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Price Chart
        const priceChartEl = document.getElementById('priceChart');
        if (priceChartEl) {
            const ctx = priceChartEl.getContext('2d');
            
            // Sample data - would be replaced with real data in production
            const labels = ['Apr 1', 'Apr 2', 'Apr 3', 'Apr 4', 'Apr 5', 'Apr 6', 'Apr 7', 'Apr 8', 'Apr 9', 'Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 15', 'Apr 16'];
            const prices = [3600, 3550, 3500, 3450, 3400, 3450, 3500, 3550, 3600, 3650, 3700, 3750, 3800, 3750, 3800, 3850];
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'ETH Price (USD)',
                            data: prices,
                            borderColor: '#3498db',
                            backgroundColor: 'rgba(52, 152, 219, 0.1)',
                            borderWidth: 2,
                            tension: 0.1,
                            fill: true
                        },
                        {
                            label: 'MA50',
                            data: prices.map(p => p * 0.95), // Simplified for demo
                            borderColor: '#2ecc71',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            tension: 0.1,
                            fill: false
                        },
                        {
                            label: 'MA200',
                            data: prices.map(p => p * 0.9), // Simplified for demo
                            borderColor: '#e74c3c',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            tension: 0.1,
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        }
        
        // Record Trade Form
        const submitTradeBtn = document.getElementById('submitTradeBtn');
        if (submitTradeBtn) {
            submitTradeBtn.addEventListener('click', function() {
                recordTrade();
            });
        }
        
        // Set default date to today
        const tradeDateInput = document.getElementById('tradeDate');
        if (tradeDateInput) {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            tradeDateInput.value = `${yyyy}-${mm}-${dd}`;
        }
        
        // Run Analysis Button
        const runAnalysisBtn = document.getElementById('runAnalysisBtn');
        if (runAnalysisBtn) {
            runAnalysisBtn.addEventListener('click', function() {
                runAnalysis();
            });
        }
    });
    
    function recordTrade() {
        const form = document.getElementById('recordTradeForm');
        const btn = document.getElementById('submitTradeBtn');
        
        // Get form values
        const tradeType = document.querySelector('input[name="tradeType"]:checked').value;
        const price = document.getElementById('tradePrice').value;
        const amount = document.getElementById('tradeAmount').value;
        const date = document.getElementById('tradeDate').value;
        const notes = document.getElementById('tradeNotes').value;

        // Validate form
        if (!price || !amount || !date) {
            alert('Please fill in all required fields.');
            return;
        }

        // Disable button and show loading state
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Recording...';

        // Send API request
        fetch('/api/trades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: tradeType,
                price: parseFloat(price),
                amount: parseFloat(amount),
                date: date,
                notes: notes
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Trade recorded successfully!');
                // Close modal and reload page
                const modal = bootstrap.Modal.getInstance(document.getElementById('recordTradeModal'));
                modal.hide();
                window.location.reload();
            } else {
                alert('Error: ' + data.error);
                btn.disabled = false;
                btn.innerHTML = 'Record Trade';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while recording the trade.');
            btn.disabled = false;
            btn.innerHTML = 'Record Trade';
        });
    }
    
    function runAnalysis() {
        const btn = document.getElementById('runAnalysisBtn');
        
        // Disable button and show loading state
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Running...';

        // Send API request
        fetch('/api/analysis/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Analysis started! Results will be available shortly.');
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                alert('Error: ' + data.error);
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-play-fill me-1"></i>Run Analysis Now';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while starting the analysis.');
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-play-fill me-1"></i>Run Analysis Now';
        });
    }
</script>
{% endblock %}
```

3. Press Ctrl+X, then Y, then Enter to save the file

## Step 10: Create CSS Styles

1. In Cloud Shell, run:
```bash
nano app_engine/static/css/styles.css
```

2. Copy and paste the following code:

```css
/* Main layout */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    padding: 48px 0 0;
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.sidebar .nav-link {
    color: #adb5bd;
    padding: 0.75rem 1rem;
    margin-bottom: 0.2rem;
    border-radius: 0.25rem;
}

.sidebar .nav-link:hover {
    color: #fff;
    background-color: rgba(255, 255, 255, 0.1);
}

.sidebar .nav-link.active {
    color: #fff;
    background-color: rgba(255, 255, 255, 0.2);
}

.sidebar .nav-link i {
    margin-right: 0.5rem;
}

/* Cards */
.card {
    border-radius: 0.5rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    margin-bottom: 1.5rem;
}

.card-header {
    border-top-left-radius: 0.5rem !important;
    border-top-right-radius: 0.5rem !important;
    padding: 0.75rem 1.25rem;
}

/* Dark mode */
.dark-mode {
    background-color: #121212;
    color: #e0e0e0;
}

.dark-mode .card {
    background-color: #1e1e1e;
    border-color: #333;
}

.dark-mode .card-header {
    background-color: #2c2c2c;
    border-color: #333;
}

.dark-mode .table {
    color: #e0e0e0;
}

.dark-mode .table-hover tbody tr:hover {
    color: #fff;
    background-color: rgba(255, 255, 255, 0.075);
}

.dark-mode .modal-content {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

/* Responsive */
@media (max-width: 767.98px) {
    .sidebar {
        position: static;
        height: auto;
        padding-top: 0;
    }
    
    main {
        margin-left: 0 !important;
    }
}

/* Login page */
.login-page {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

/* Utilities */
.text-success {
    color: #2ecc71 !important;
}

.text-danger {
    color: #e74c3c !important;
}

.bg-primary {
    background-color: #3498db !important;
}

.btn-primary {
    background-color: #3498db;
    border-color: #3498db;
}

.btn-primary:hover {
    background-color: #2980b9;
    border-color: #2980b9;
}
```

3. Press Ctrl+X, then Y, then Enter to save the file

## Step 11: Create JavaScript File

1. In Cloud Shell, run:
```bash
nano app_engine/static/js/main.js
```

2. Copy and paste the following code:

```javascript
// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD_BF6zt4-I8HUwe3Gg3WJ6RkaDaoaxfZU",
  authDomain: "eth-investment-2a09d.firebaseapp.com",
  projectId: "eth-investment-2a09d",
  storageBucket: "eth-investment-2a09d.firebasestorage.app",
  messagingSenderId: "468606711281",
  appId: "1:468606711281:web:41e64e61b2bec0b25f8050",
  measurementId: "G-02JLT7LXKZ"
};

// Initialize Firebase
function initFirebase() {
    if (typeof firebase !== 'undefined' && !firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
        
        // Set up authentication state change listener
        firebase.auth().onAuthStateChanged(function(user) {
            if (user && window.location.pathname === '/login') {
                // User is signed in and on login page, redirect to dashboard
                window.location.href = '/';
            } else if (!user && window.location.pathname !== '/login') {
                // User is not signed in and not on login page, redirect to login
                window.location.href = '/login';
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Firebase
    initFirebase();
    
    // Set up logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Sign out from Firebase
            firebase.auth().signOut()
                .then(() => {
                    // Call backend logout endpoint
                    return fetch('/api/logout', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                })
                .then(() => {
                    // Redirect to login page
                    window.location.href = '/login';
                })
                .catch((error) => {
                    console.error('Error signing out:', error);
                });
        });
    }
    
    // Check for dark mode preference
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
});
```

3. Update the Firebase configuration with your own values
4. Press Ctrl+X, then Y, then Enter to save the file

## Step 12: Set Up Firebase in Google Cloud Console

1. Open a new browser tab and go to [firebase.google.com](https://firebase.google.com)
2. Click "Get started"
3. Click "Add project"
4. Select your Google Cloud project from the dropdown
5. Follow the setup steps to complete Firebase setup
6. Go to Authentication > Sign-in method
7. Enable Google as a sign-in provider
8. Add your App Engine domain to the authorized domains:
   - Your domain will be: [PROJECT-ID].appspot.com

## Step 13: Create Cloud Storage Bucket

1. In Cloud Shell, run:
```bash
gsutil mb -l us-central1 gs://eth-investment-data-[PROJECT-ID]
```

Replace [PROJECT-ID] with your actual project ID

## Step 14: Create Pub/Sub Topic

1. In Cloud Shell, run:
```bash
gcloud pubsub topics create eth-investment-notifications
```

## Step 15: Deploy to App Engine

1. In Cloud Shell, navigate to the app_engine directory:
```bash
cd app_engine
```

2. Deploy the application:
```bash
gcloud app deploy
```

3. When prompted, select a region (e.g., us-central)
4. Type "Y" to confirm the deployment
5. Wait for the deployment to complete (this may take several minutes)

## Step 16: Open Your Dashboard

1. After deployment completes, run:
```bash
gcloud app browse
```

2. Your default web browser will open with your dashboard URL
3. Sign in with your Google account
4. You'll see your ETH Investment Dashboard!

## Step 17: Create ETH Investment Analysis Function

1. In the Google Cloud Console, go to Cloud Functions
2. Click "Create Function"
3. Configure the function:
   - Name: eth-investment-analysis
   - Trigger type: Cloud Pub/Sub
   - Topic: eth-investment-notifications
   - Runtime: Python 3.9
   - Entry point: run_analysis
4. In the inline editor, paste the ETH investment script code
5. Click "Deploy"

## Step 18: Create a Scheduler for Automatic Analysis

1. In the Google Cloud Console, go to Cloud Scheduler
2. Click "Create Job"
3. Configure the job:
   - Name: weekly-eth-analysis
   - Frequency: 0 9 * * 1 (runs every Monday at 9 AM)
   - Target type: Pub/Sub
   - Topic: eth-investment-notifications
   - Message: {"action": "run_analysis"}
4. Click "Create"

## Congratulations!

You've successfully deployed your ETH Investment Dashboard entirely in Google Cloud without any local setup! Your dashboard is now running in the cloud and will automatically analyze ETH investments based on your schedule.

## Next Steps

1. **Customize Your Dashboard**: Edit the HTML templates and CSS to match your preferences
2. **Add Real Data**: Modify the Cloud Function to fetch real ETH data from APIs
3. **Set Up Monitoring**: Configure alerts for your App Engine application
4. **Add a Custom Domain**: Configure a custom domain for your dashboard
