# Step-by-Step Guide to Deploy ETH Investment Dashboard

This guide will walk you through deploying your ETH Investment Dashboard to Google Cloud App Engine with your Firebase configuration.

## Step 1: Set Up Your Local Environment

1. Create a new directory for your project:
```bash
mkdir eth-dashboard
cd eth-dashboard
```

2. Download the dashboard files:
   - Create subdirectories:
```bash
mkdir -p app_engine/static/css app_engine/static/js app_engine/templates
```

3. Copy the main.py and app.yaml files to the app_engine directory
   - These were provided in the previous message

## Step 2: Update Firebase Configuration

1. Open the file `app_engine/static/js/main.js`
2. Replace the Firebase configuration with your own:
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
```

## Step 3: Update Google Cloud Project Settings

1. Open the file `app_engine/app.yaml`
2. Update the environment variables with your project details:
```yaml
env_variables:
  GOOGLE_CLOUD_PROJECT: "eth-investment-457013"
  STORAGE_BUCKET: "eth-investment-data-eth-investment-457013"
  NOTIFICATION_TOPIC: "eth-investment-notifications"
  SECRET_KEY: "generate-a-secure-random-key"
```

## Step 4: Set Up Google Cloud Resources

1. Install Google Cloud SDK if you haven't already
2. Initialize the SDK and authenticate:
```bash
gcloud init
# Select your project: eth-investment-457013
```

3. Enable required APIs:
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable pubsub.googleapis.com
```

4. Create a Cloud Storage bucket:
```bash
gsutil mb -l us-central1 gs://eth-investment-data-eth-investment-457013
```

5. Create a Pub/Sub topic:
```bash
gcloud pubsub topics create eth-investment-notifications
```

## Step 5: Configure Firebase Authentication

1. Go to the Firebase Console: https://console.firebase.google.com/
2. Select your project: eth-investment-2a09d
3. Go to Authentication > Sign-in method
4. Enable Google as a sign-in provider
5. Add your App Engine domain to the authorized domains:
   - Your domain will be: eth-investment-457013.appspot.com

## Step 6: Create Requirements File

1. Create a file `app_engine/requirements.txt` with the following content:
```
Flask==2.0.1
google-cloud-storage==1.42.0
google-cloud-pubsub==2.8.0
firebase-admin==5.0.3
gunicorn==20.1.0
pandas==1.3.3
matplotlib==3.4.3
```

## Step 7: Deploy to App Engine

1. Navigate to the app_engine directory:
```bash
cd app_engine
```

2. Deploy the application:
```bash
gcloud app deploy
```

3. When prompted, select a region (e.g., us-central)
4. Confirm the deployment

5. Once deployed, open the application:
```bash
gcloud app browse
```

## Step 8: Set Up ETH Investment Script in Cloud Functions

1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Navigate to Cloud Functions
3. Create a new function:
   - Name: eth-investment-analysis
   - Trigger: Pub/Sub
   - Topic: eth-investment-notifications
   - Runtime: Python 3.9
   - Entry point: run_analysis
   - Copy the ETH investment script code

4. Create a Cloud Scheduler job to run weekly:
   - Name: weekly-eth-analysis
   - Frequency: 0 9 * * 1 (Monday at 9 AM)
   - Target: Pub/Sub
   - Topic: eth-investment-notifications
   - Message: Run ETH investment analysis

## Step 9: Test the Dashboard

1. Open your dashboard at: https://eth-investment-457013.appspot.com
2. Sign in with your Google account
3. Configure your settings:
   - Go to the Settings page
   - Enter your portfolio value
   - Set your risk tolerance
   - Configure notification preferences

4. Trigger a manual analysis:
   - On the main dashboard, click "Run Analysis Now"
   - Wait for the analysis to complete (this may take a few minutes)

5. Record a test trade:
   - Click "Record Trade"
   - Enter the details of a test trade
   - Click "Record Trade" to save

## Step 10: Monitor and Maintain

1. Set up monitoring:
   - Go to Google Cloud Console > Monitoring
   - Create alerts for App Engine and Cloud Functions

2. Check logs regularly:
```bash
gcloud app logs tail
```

3. Update the application as needed:
   - Make changes locally
   - Test thoroughly
   - Redeploy using `gcloud app deploy`

## Troubleshooting

If you encounter issues:

1. Check App Engine logs:
```bash
gcloud app logs tail
```

2. Verify Firebase authentication is working:
   - Check Firebase Console > Authentication > Users
   - Ensure your domain is in the authorized domains list

3. Check Cloud Storage permissions:
```bash
gsutil ls gs://eth-investment-data-eth-investment-457013
```

4. Verify Cloud Functions are running:
```bash
gcloud functions logs read eth-investment-analysis
```

Congratulations! You've successfully deployed your ETH Investment Dashboard to Google Cloud App Engine with Firebase authentication.
