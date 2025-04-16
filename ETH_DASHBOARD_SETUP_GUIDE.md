# ETH Investment Dashboard - Setup and Usage Guide

This comprehensive guide will walk you through setting up and using the ETH Investment Dashboard web application on Google Cloud App Engine. The dashboard provides a user-friendly interface to monitor your ETH investments, view technical analysis, manage risk, and track performance.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup and Deployment](#setup-and-deployment)
3. [Dashboard Features](#dashboard-features)
4. [User Guide](#user-guide)
5. [Customization](#customization)
6. [Troubleshooting](#troubleshooting)
7. [Security Considerations](#security-considerations)

## Prerequisites

Before you begin, ensure you have the following:

1. **Google Cloud Account**: If you don't have one, sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud SDK**: Install from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
3. **Python 3.9+**: Install from [python.org](https://python.org)
4. **Firebase Project**: For user authentication
5. **ETH Investment Script**: Already deployed to Google Cloud Functions

## Setup and Deployment

### Step 1: Configure Firebase Authentication

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select your existing project
3. Enable Google Authentication:
   - Go to Authentication > Sign-in method
   - Enable Google as a sign-in provider
4. Get your Firebase configuration:
   - Go to Project Settings > General
   - Scroll down to "Your apps" section
   - Click the web app icon (</>) to create a web app if you haven't already
   - Copy the Firebase configuration object

5. Update the Firebase configuration in `static/js/main.js`:
   ```javascript
   const firebaseConfig = {
     apiKey: "YOUR_API_KEY",
     authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
     projectId: "YOUR_PROJECT_ID",
     storageBucket: "YOUR_PROJECT_ID.appspot.com",
     messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
     appId: "YOUR_APP_ID"
   };
   ```

### Step 2: Configure Google Cloud Project

1. Create a new Google Cloud project or use an existing one:
   ```bash
   gcloud projects create [PROJECT_ID] --name="ETH Investment Dashboard"
   # or
   gcloud config set project [EXISTING_PROJECT_ID]
   ```

2. Enable required APIs:
   ```bash
   gcloud services enable appengine.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable pubsub.googleapis.com
   ```

3. Create a Cloud Storage bucket for ETH investment data:
   ```bash
   gsutil mb -l us-central1 gs://eth-investment-data-[PROJECT_ID]
   ```

4. Create a Pub/Sub topic for notifications:
   ```bash
   gcloud pubsub topics create eth-investment-notifications
   ```

### Step 3: Update Configuration

1. Edit `app.yaml` to update your project configuration:
   ```yaml
   env_variables:
     GOOGLE_CLOUD_PROJECT: "your-project-id"
     STORAGE_BUCKET: "eth-investment-data-your-project-id"
     NOTIFICATION_TOPIC: "eth-investment-notifications"
     SECRET_KEY: "generate-a-secure-random-key"
   ```

2. Generate a secure random key for the SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_hex(16))"
   ```

### Step 4: Install Dependencies

1. Create a `requirements.txt` file in the app_engine directory:
   ```
   Flask==2.0.1
   google-cloud-storage==1.42.0
   google-cloud-pubsub==2.8.0
   firebase-admin==5.0.3
   gunicorn==20.1.0
   pandas==1.3.3
   matplotlib==3.4.3
   ```

2. Install dependencies locally for testing:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5: Deploy to App Engine

1. Navigate to the app_engine directory:
   ```bash
   cd app_engine
   ```

2. Deploy the application:
   ```bash
   gcloud app deploy
   ```

3. Open the deployed application:
   ```bash
   gcloud app browse
   ```

## Dashboard Features

The ETH Investment Dashboard includes the following key features:

### Main Dashboard

- **ETH Price & Recommendation**: Current price, 24-hour change, and investment recommendation
- **Investment Chart**: Price chart with technical indicators
- **Risk Management Panel**: Stop-loss price, position sizing, and take-profit targets
- **Technical Analysis Panel**: RSI, MACD, moving averages, and trend analysis
- **Performance Tracking**: Portfolio value, trade history, and profit/loss

### Historical Analysis

- **Analysis History**: Table of past analyses with recommendations
- **Performance Charts**: Visualization of recommendation history and price trends
- **Detailed Analysis**: In-depth view of past analyses with all metrics

### Performance Tracking

- **Trade Recording**: Log of all buy/sell transactions
- **Portfolio Metrics**: ETH holdings, current value, and profit/loss
- **Performance Charts**: Visualization of holdings and value over time
- **Trade Analysis**: Detailed metrics for each trade

### Settings

- **User Settings**: Notification preferences and account information
- **Risk Management Settings**: Portfolio value, risk per trade, and exposure limits
- **Analysis Settings**: Analysis frequency and preferred timeframe
- **Display Settings**: Theme, currency, and decimal precision

## User Guide

### Getting Started

1. **Sign In**: Use your Google account to sign in to the dashboard
2. **Initial Setup**: Configure your settings:
   - Go to the Settings page
   - Enter your portfolio value
   - Set your risk tolerance
   - Configure notification preferences

### Using the Dashboard

#### Viewing ETH Analysis

The main dashboard provides a comprehensive view of your ETH investment:

1. **Current Price**: View the current ETH price and 24-hour change
2. **Recommendation**: See the current investment recommendation (Buy/Sell/Hold)
3. **Technical Indicators**: Check RSI, MACD, and moving averages
4. **Risk Management**: View recommended position size and stop-loss levels

#### Recording Trades

To record a new trade:

1. Click the "Record Trade" button in the Performance Tracking panel
2. Select the trade type (Buy/Sell)
3. Enter the price and amount
4. Add optional notes
5. Click "Record Trade"

#### Viewing Performance

To track your investment performance:

1. Go to the Performance page
2. View your ETH holdings and current value
3. Check your profit/loss for each trade
4. Analyze performance charts to see your progress over time

#### Accessing Historical Analysis

To view past analyses:

1. Go to the History page
2. Browse the table of past analyses
3. Click "Details" to view in-depth information about a specific analysis
4. Check the performance charts to see trends over time

### Customizing the Dashboard

To customize your dashboard experience:

1. Go to the Settings page
2. Adjust risk management parameters
3. Set your preferred analysis frequency
4. Choose your display theme (Light/Dark)
5. Configure notification settings

## Customization

### Modifying the Dashboard Layout

The dashboard layout is defined in the HTML templates. To modify the layout:

1. Edit the template files in the `templates` directory
2. Update the CSS styles in `static/css/styles.css`
3. Redeploy the application

### Adding New Features

To add new features to the dashboard:

1. Modify the Flask application in `main.py`
2. Add new routes and functions as needed
3. Create new templates for new pages
4. Update JavaScript functionality in `static/js/main.js`
5. Redeploy the application

### Integrating with Other Services

The dashboard can be integrated with additional services:

1. **Email Notifications**: Configure SMTP settings to send email alerts
2. **SMS Alerts**: Integrate with Twilio or similar services for SMS notifications
3. **Exchange APIs**: Connect to cryptocurrency exchanges for automated trading

## Troubleshooting

### Common Issues

#### Dashboard Not Loading

1. Check if the App Engine service is running:
   ```bash
   gcloud app services list
   ```
2. View App Engine logs:
   ```bash
   gcloud app logs tail
   ```
3. Ensure all required APIs are enabled

#### Authentication Issues

1. Verify Firebase configuration in `main.js`
2. Check Firebase Authentication console for errors
3. Ensure the domain is authorized in Firebase Authentication settings

#### Data Not Displaying

1. Check if the ETH investment script is running correctly
2. Verify Cloud Storage bucket permissions
3. Check if data files exist in the storage bucket:
   ```bash
   gsutil ls gs://eth-investment-data-[PROJECT_ID]
   ```

### Getting Support

If you encounter issues not covered in this guide:

1. Check Google Cloud documentation: [cloud.google.com/appengine/docs](https://cloud.google.com/appengine/docs)
2. Review Firebase documentation: [firebase.google.com/docs](https://firebase.google.com/docs)
3. Contact Google Cloud support if you have a support package

## Security Considerations

### Protecting User Data

1. **Authentication**: The dashboard uses Firebase Authentication for secure user login
2. **HTTPS**: All traffic is encrypted using HTTPS
3. **Secure Cookies**: Session cookies are secure and HTTP-only

### API Keys and Secrets

1. **Environment Variables**: Sensitive values are stored as environment variables
2. **Firebase Security Rules**: Implement proper security rules in Firebase
3. **IAM Permissions**: Use least privilege principle for service accounts

### Regular Updates

1. Keep dependencies updated to patch security vulnerabilities
2. Regularly update the App Engine runtime
3. Monitor Google Cloud Security Bulletins

## Conclusion

The ETH Investment Dashboard provides a powerful, user-friendly interface for monitoring and managing your ETH investments. By following this guide, you've successfully set up and deployed the dashboard to Google Cloud App Engine, integrated it with your ETH investment script, and learned how to use its features effectively.

For any questions or issues, refer to the troubleshooting section or contact support.
