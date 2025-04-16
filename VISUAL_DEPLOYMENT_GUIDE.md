# Visual Deployment Guide for ETH Investment Dashboard

This guide provides step-by-step visual instructions for deploying your ETH investment dashboard, designed for users with no coding experience.

## Step 1: Create a Google Cloud Account

1. Open your web browser and go to [cloud.google.com](https://cloud.google.com)
2. Click the "Get started for free" button
3. Sign in with your Google account
4. Fill in your information and add a payment method (required for verification)
5. Click "Start my free trial"

![Google Cloud Sign Up](https://storage.googleapis.com/support-kms-prod/SNP_EFFF44F8B096D7A1F641B79B9AD6D97C8968_13677480_en_v1)

## Step 2: Create a New Project

1. In the Google Cloud Console, click on the project dropdown at the top of the page
2. Click "New Project"
3. Enter "ETH Investment Dashboard" as the project name
4. Click "Create"

![Create New Project](https://cloud.google.com/static/resource-manager/img/cloud-console-create-project.png)

## Step 3: Install Google Cloud SDK

### For Windows:
1. Download the installer from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
2. Run the installer and follow the prompts
3. When installation completes, check "Start Google Cloud SDK Shell" and click "Finish"
4. In the command window that opens, type:
   ```
   gcloud init
   ```
5. Follow the prompts to log in and select your project

![Google Cloud SDK Install](https://cloud.google.com/sdk/docs/images/install-sdk-windows.png)

### For Mac:
1. Download the installer from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
2. Open the downloaded file and drag the Google Cloud SDK folder to your Applications folder
3. Open Terminal
4. Run the following command:
   ```
   ./google-cloud-sdk/install.sh
   ```
5. After installation, run:
   ```
   ./google-cloud-sdk/bin/gcloud init
   ```
6. Follow the prompts to log in and select your project

## Step 4: Enable Required APIs

1. In the Google Cloud Console, click on the navigation menu (☰)
2. Scroll down and click on "APIs & Services" > "Library"
3. Search for and enable the following APIs:
   - App Engine Admin API
   - Cloud Storage
   - Cloud Pub/Sub API

![Enable APIs](https://cloud.google.com/endpoints/docs/images/endpoints-api-library.png)

## Step 5: Set Up Firebase

1. Go to [firebase.google.com](https://firebase.google.com)
2. Click "Get started"
3. Click "Add project"
4. Select your Google Cloud project from the dropdown
5. Follow the setup steps to complete Firebase setup

![Firebase Setup](https://firebase.google.com/docs/projects/images/firebase-web-setup.png)

## Step 6: Configure Firebase Authentication

1. In the Firebase console, click on "Authentication" in the left sidebar
2. Click on the "Sign-in method" tab
3. Click on "Google" in the list of providers
4. Toggle the "Enable" switch to on
5. Enter your support email
6. Click "Save"

![Firebase Authentication](https://firebase.google.com/docs/auth/images/auth-providers.png)

## Step 7: Download the Dashboard Files

1. Create a folder on your computer called "eth-dashboard"
2. Download all the files provided in the previous messages to this folder
3. Make sure you have the following structure:
   ```
   eth-dashboard/
   ├── app_engine/
   │   ├── main.py
   │   ├── app.yaml
   │   ├── requirements.txt
   │   ├── static/
   │   │   ├── css/
   │   │   │   └── styles.css
   │   │   └── js/
   │   │       └── main.js
   │   └── templates/
   │       ├── base.html
   │       ├── dashboard.html
   │       ├── history.html
   │       ├── login.html
   │       ├── performance.html
   │       └── settings.html
   ```

## Step 8: Update Firebase Configuration

1. Open the file `app_engine/static/js/main.js` in a text editor (like Notepad)
2. Find the Firebase configuration section
3. Replace it with your Firebase configuration:
   ```javascript
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
4. Save the file

![Edit Configuration](https://www.howtogeek.com/wp-content/uploads/2021/05/notepad_open_file.png?width=1198&trim=1,1&bg-color=000&pad=1,1)

## Step 9: Update Google Cloud Project Settings

1. Open the file `app_engine/app.yaml` in a text editor
2. Update the environment variables with your project details:
   ```yaml
   env_variables:
     GOOGLE_CLOUD_PROJECT: "eth-investment-457013"
     STORAGE_BUCKET: "eth-investment-data-eth-investment-457013"
     NOTIFICATION_TOPIC: "eth-investment-notifications"
     SECRET_KEY: "your-secret-key"
   ```
3. Save the file

## Step 10: Create Requirements File

1. Create a new file in the app_engine folder called `requirements.txt`
2. Add the following content:
   ```
   Flask==2.0.1
   google-cloud-storage==1.42.0
   google-cloud-pubsub==2.8.0
   firebase-admin==5.0.3
   gunicorn==20.1.0
   pandas==1.3.3
   matplotlib==3.4.3
   ```
3. Save the file

## Step 11: Set Up Google Cloud Resources

1. Open Google Cloud SDK Shell (Windows) or Terminal (Mac)
2. Navigate to your project folder:
   ```
   cd path/to/eth-dashboard
   ```
3. Create a Cloud Storage bucket:
   ```
   gsutil mb -l us-central1 gs://eth-investment-data-eth-investment-457013
   ```
4. Create a Pub/Sub topic:
   ```
   gcloud pubsub topics create eth-investment-notifications
   ```

![Google Cloud Shell](https://cloud.google.com/shell/docs/images/cloud-shell-editor.png)

## Step 12: Deploy to App Engine

1. In Google Cloud SDK Shell or Terminal, navigate to the app_engine directory:
   ```
   cd app_engine
   ```
2. Deploy the application:
   ```
   gcloud app deploy
   ```
3. When prompted, select a region (e.g., us-central)
4. Type "Y" to confirm the deployment
5. Wait for the deployment to complete (this may take several minutes)

![App Engine Deploy](https://cloud.google.com/appengine/docs/images/deploy-success.png)

## Step 13: Open Your Dashboard

1. After deployment completes, run:
   ```
   gcloud app browse
   ```
2. Your default web browser will open with your dashboard URL
3. Sign in with your Google account
4. You'll see your ETH Investment Dashboard!

![Dashboard Login](https://firebase.google.com/docs/auth/images/auth-providers.png)

## Step 14: Set Up a Custom Domain (Optional)

1. Purchase a domain from a registrar like Google Domains, Namecheap, or GoDaddy
2. In Google Cloud Console, go to App Engine > Settings > Custom domains
3. Click "Add a Custom Domain"
4. Follow the verification process
5. Add your domain and configure the DNS settings as instructed

![Custom Domain](https://cloud.google.com/appengine/docs/images/mapping-domain.png)

## Step 15: Set Up ETH Investment Script in Cloud Functions

1. In Google Cloud Console, go to Cloud Functions
2. Click "Create Function"
3. Configure the function:
   - Name: eth-investment-analysis
   - Trigger type: Cloud Pub/Sub
   - Topic: eth-investment-notifications
   - Runtime: Python 3.9
4. Copy the ETH investment script code to the main.py editor
5. Click "Deploy"

![Cloud Functions](https://cloud.google.com/functions/docs/images/console-create-function.png)

## Step 16: Create a Scheduler for Automatic Analysis

1. In Google Cloud Console, go to Cloud Scheduler
2. Click "Create Job"
3. Configure the job:
   - Name: weekly-eth-analysis
   - Frequency: 0 9 * * 1 (runs every Monday at 9 AM)
   - Target type: Pub/Sub
   - Topic: eth-investment-notifications
   - Message: Run ETH investment analysis
4. Click "Create"

![Cloud Scheduler](https://cloud.google.com/scheduler/docs/images/create-job.png)

## Step 17: Test Your Dashboard

1. Go to your dashboard URL (e.g., https://eth-investment-457013.appspot.com)
2. Sign in with your Google account
3. Explore the different sections:
   - Main Dashboard
   - Historical Analysis
   - Performance Tracking
   - Settings
4. Try recording a test trade by clicking "Record Trade"

## Step 18: Set Up Monitoring (Optional)

1. In Google Cloud Console, go to Monitoring
2. Click "Alerting"
3. Click "Create Policy"
4. Set up alerts for:
   - App Engine uptime
   - Error rates
   - Cloud Function executions
5. Configure notification channels (email, SMS, etc.)

![Monitoring](https://cloud.google.com/monitoring/images/alerts-create-policy.png)

## Congratulations!

You've successfully deployed your ETH Investment Dashboard! Your dashboard is now running in the cloud and will automatically analyze ETH investments based on your schedule.

If you encounter any issues, refer to the troubleshooting section in the ETH_DASHBOARD_SETUP_GUIDE.md document.
