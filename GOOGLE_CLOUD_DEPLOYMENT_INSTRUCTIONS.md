# Google Cloud Deployment Instructions for ETH Investment Script

This document provides step-by-step instructions for deploying your ETH investment script to Google Cloud Platform. We've implemented two deployment options:

1. **Compute Engine VM** - Traditional virtual machine approach
2. **Cloud Functions + Cloud Scheduler** - Serverless approach

## Prerequisites

Before you begin, make sure you have:

1. A Google Cloud Platform account
2. Google Cloud SDK installed on your local machine
3. A project created in Google Cloud
4. Billing enabled for your project
5. The ETH investment script files ready for deployment

## Option 1: Compute Engine VM Deployment

This approach deploys your ETH investment script on a virtual machine that runs continuously.

### Step 1: Set Up Your Local Environment

1. Open a terminal or command prompt
2. Make sure you have the Google Cloud SDK installed:
   ```
   gcloud --version
   ```
3. If not installed, download and install it from: https://cloud.google.com/sdk/docs/install

4. Log in to your Google Cloud account:
   ```
   gcloud auth login
   ```

5. Set your project ID:
   ```
   gcloud config set project YOUR_PROJECT_ID
   ```

### Step 2: Run the Deployment Setup Script

1. Make the deployment setup script executable:
   ```
   chmod +x gcloud_deployment_setup.py
   ```

2. Run the script to generate deployment files:
   ```
   python3 gcloud_deployment_setup.py
   ```

3. This will create several files:
   - `startup-script.sh` - Script that runs when the VM starts
   - `deploy-to-gcloud.sh` - Script to create and configure the VM
   - Cloud Functions files in the `cloud-functions` directory

### Step 3: Review and Customize the Startup Script

1. Open `startup-script.sh` in a text editor
2. Customize the following sections:
   - Email notification settings (replace placeholder email addresses)
   - Cron job schedule (if you want to change from Monday 9 AM)
   - Any other settings specific to your needs

### Step 4: Deploy to Google Cloud Compute Engine

1. Make the deployment script executable:
   ```
   chmod +x deploy-to-gcloud.sh
   ```

2. Run the deployment script:
   ```
   ./deploy-to-gcloud.sh
   ```

3. The script will:
   - Create a VM instance named "eth-investment-vm"
   - Configure it with the startup script
   - Set up necessary permissions
   - Display the external IP address

### Step 5: Upload Your ETH Investment Script Files

1. Use the gcloud command to upload your script files:
   ```
   gcloud compute scp --recurse /path/to/local/script/files/* eth-investment-vm:/opt/eth-investment/ --zone=us-central1-a
   ```

2. Replace `/path/to/local/script/files/*` with the actual path to your ETH investment script files

### Step 6: Configure Email Notifications

1. Connect to your VM:
   ```
   gcloud compute ssh eth-investment-vm --zone=us-central1-a
   ```

2. Set your notification email:
   ```
   export NOTIFICATION_RECIPIENT=your-email@example.com
   ```

3. Add it to your .bashrc file for persistence:
   ```
   echo "export NOTIFICATION_RECIPIENT=your-email@example.com" >> ~/.bashrc
   ```

4. If using Gmail for sending notifications, set up app password:
   ```
   export NOTIFICATION_EMAIL=your-gmail@gmail.com
   export NOTIFICATION_PASSWORD=your-app-password
   ```

5. Add these to .bashrc as well:
   ```
   echo "export NOTIFICATION_EMAIL=your-gmail@gmail.com" >> ~/.bashrc
   echo "export NOTIFICATION_PASSWORD=your-app-password" >> ~/.bashrc
   ```

### Step 7: Test the Setup

1. While connected to the VM, run a manual analysis:
   ```
   cd /opt/eth-investment
   source venv/bin/activate
   python eth_investment_dashboard.py --run
   ```

2. Check that the analysis runs successfully and notifications are sent

## Option 2: Cloud Functions Deployment (Serverless)

This approach uses Google Cloud Functions and Cloud Scheduler for a serverless deployment.

### Step 1: Prepare Your ETH Investment Script Files

1. Make sure your ETH investment script files are in the same directory as the deployment setup script

### Step 2: Deploy to Google Cloud Functions

1. Navigate to the cloud-functions directory:
   ```
   cd cloud-functions
   ```

2. Make the deployment script executable:
   ```
   chmod +x deploy-cloud-function.sh
   ```

3. Run the deployment script:
   ```
   ./deploy-cloud-function.sh
   ```

4. The script will:
   - Create a storage bucket for your data
   - Create a Pub/Sub topic for notifications
   - Copy your ETH investment script files to the function directory
   - Deploy the Cloud Function
   - Create a Cloud Scheduler job to run weekly

### Step 3: Configure Notification Settings

1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Navigate to Cloud Functions
3. Select your function (eth-investment-analysis)
4. Go to the "Configuration" tab
5. Click "Edit"
6. Under "Runtime environment variables", add or modify:
   - NOTIFICATION_RECIPIENT: your-email@example.com
   - Any other notification settings you need

7. Click "Next" and then "Deploy" to update the function

### Step 4: Test the Cloud Function

1. Manually trigger the function:
   ```
   gcloud pubsub topics publish run-eth-analysis --message="Run ETH investment analysis"
   ```

2. Check the function logs:
   ```
   gcloud functions logs read eth-investment-analysis --region=us-central1
   ```

3. Verify that the analysis runs successfully and results are stored in the bucket

## Accessing Your Results

### For Compute Engine VM

1. Results are stored in the `/opt/eth-investment` directory on the VM
2. Log files are in `/var/log/eth-analysis.log`
3. Email notifications are sent to your configured email address

### For Cloud Functions

1. Results are stored in the Cloud Storage bucket: `eth-investment-data-YOUR_PROJECT_ID`
2. You can access them through the Google Cloud Console or using gsutil:
   ```
   gsutil ls gs://eth-investment-data-YOUR_PROJECT_ID
   ```

3. To download a specific file:
   ```
   gsutil cp gs://eth-investment-data-YOUR_PROJECT_ID/eth_analysis_YYYYMMDD.json .
   ```

## Monitoring and Maintenance

### Compute Engine VM

1. Check VM status:
   ```
   gcloud compute instances describe eth-investment-vm --zone=us-central1-a
   ```

2. View logs:
   ```
   gcloud compute ssh eth-investment-vm --zone=us-central1-a --command="sudo tail -f /var/log/eth-analysis.log"
   ```

3. Restart the VM if needed:
   ```
   gcloud compute instances stop eth-investment-vm --zone=us-central1-a
   gcloud compute instances start eth-investment-vm --zone=us-central1-a
   ```

### Cloud Functions

1. View function logs:
   ```
   gcloud functions logs read eth-investment-analysis --region=us-central1
   ```

2. Check scheduler job status:
   ```
   gcloud scheduler jobs describe weekly-eth-analysis --location=us-central1
   ```

3. Update the function if needed:
   ```
   cd cloud-functions
   ./deploy-cloud-function.sh
   ```

## Cost Management

### Compute Engine VM

1. The e2-micro instance costs approximately $6-8 per month
2. You can stop the VM when not in use to save costs:
   ```
   gcloud compute instances stop eth-investment-vm --zone=us-central1-a
   ```

3. Set up a budget alert in the Google Cloud Console

### Cloud Functions

1. Cloud Functions are billed based on execution time and resources used
2. For weekly execution, costs should be minimal (likely under $1 per month)
3. Cloud Storage costs depend on the amount of data stored
4. Set up a budget alert in the Google Cloud Console

## Troubleshooting

### Common Issues with Compute Engine VM

1. **VM not starting**:
   - Check startup script logs:
     ```
     gcloud compute ssh eth-investment-vm --zone=us-central1-a --command="sudo cat /var/log/syslog | grep startup-script"
     ```

2. **Script not running on schedule**:
   - Check cron configuration:
     ```
     gcloud compute ssh eth-investment-vm --zone=us-central1-a --command="crontab -l"
     ```

3. **Notifications not being sent**:
   - Check environment variables:
     ```
     gcloud compute ssh eth-investment-vm --zone=us-central1-a --command="env | grep NOTIFICATION"
     ```

### Common Issues with Cloud Functions

1. **Function failing to deploy**:
   - Check for Python syntax errors in your script files
   - Ensure all dependencies are listed in requirements.txt

2. **Function timing out**:
   - Increase the timeout setting in the deployment script
   - Optimize your code for faster execution

3. **Scheduler not triggering the function**:
   - Check scheduler job status:
     ```
     gcloud scheduler jobs describe weekly-eth-analysis --location=us-central1
     ```

## Security Considerations

1. **API Keys and Credentials**:
   - Store sensitive data in environment variables or Secret Manager
   - Never hardcode credentials in your script files

2. **VM Access**:
   - Limit SSH access to your IP address
   - Use strong passwords or SSH keys

3. **Data Protection**:
   - Enable Cloud Storage bucket encryption
   - Implement proper error handling to avoid exposing sensitive information

## Conclusion

Your ETH investment script is now deployed to Google Cloud Platform and will run automatically according to the schedule you've configured. The system will analyze ETH price data, generate investment recommendations, and send you notifications.

For any issues or questions, refer to the Google Cloud documentation or contact Google Cloud support.

Remember to monitor your cloud usage and costs to avoid unexpected charges.

Happy investing!
