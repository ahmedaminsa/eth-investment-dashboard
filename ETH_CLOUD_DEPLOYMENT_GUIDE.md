# Cloud Deployment Guide for ETH Investment Script

This guide explains how to deploy the ETH investment script to various cloud services for automated execution.

## Table of Contents

1. [Introduction](#introduction)
2. [Cloud Deployment Options](#cloud-deployment-options)
3. [AWS Deployment](#aws-deployment)
4. [Google Cloud Deployment](#google-cloud-deployment)
5. [Azure Deployment](#azure-deployment)
6. [Digital Ocean Deployment](#digital-ocean-deployment)
7. [Scheduling and Automation](#scheduling-and-automation)
8. [Security Considerations](#security-considerations)
9. [Cost Optimization](#cost-optimization)
10. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Introduction

Deploying the ETH investment script to a cloud service offers several advantages:

- **24/7 Operation**: The script can run automatically without your local computer being on
- **Reliability**: Cloud providers offer high uptime and reliability
- **Scalability**: Easily scale resources as your needs grow
- **Automation**: Schedule regular analysis and receive notifications
- **Security**: Protect your investment data with cloud security features

This guide covers multiple cloud deployment options, allowing you to choose the one that best fits your needs and budget.

## Cloud Deployment Options

Here are the main cloud providers you can use to deploy the ETH investment script:

### AWS (Amazon Web Services)
- **Pros**: Extensive services, high reliability, good free tier
- **Cons**: Can be complex for beginners
- **Cost**: Free tier available, then pay-as-you-go
- **Best for**: Long-term, scalable deployments

### Google Cloud Platform
- **Pros**: User-friendly, good integration with Google Sheets
- **Cons**: Free tier is more limited than AWS
- **Cost**: Free credits for new users, then pay-as-you-go
- **Best for**: Users already using Google services

### Microsoft Azure
- **Pros**: Good Windows integration, comprehensive services
- **Cons**: Interface can be complex
- **Cost**: Free credits for new users, then pay-as-you-go
- **Best for**: Users familiar with Microsoft ecosystem

### Digital Ocean
- **Pros**: Simple pricing, user-friendly
- **Cons**: Fewer services than major providers
- **Cost**: Starting at $5/month for basic droplets
- **Best for**: Beginners looking for simplicity

### Heroku
- **Pros**: Very easy to deploy, good for beginners
- **Cons**: Limited free tier, can get expensive
- **Cost**: Free tier available, paid tiers start at $7/month
- **Best for**: Quick deployment with minimal setup

## AWS Deployment

### Prerequisites
- AWS account
- AWS CLI installed locally
- Basic understanding of AWS services

### Step 1: Set Up an EC2 Instance

1. Log in to the AWS Management Console
2. Navigate to EC2 service
3. Click "Launch Instance"
4. Choose an Amazon Machine Image (AMI)
   - Recommended: Amazon Linux 2 or Ubuntu Server 20.04
5. Choose an instance type
   - Recommended: t2.micro (eligible for free tier)
6. Configure instance details (default settings are fine for basic use)
7. Add storage (default 8GB is sufficient)
8. Add tags (optional)
9. Configure security group
   - Allow SSH access from your IP address
10. Review and launch
11. Create or select an existing key pair for SSH access
12. Launch instance

### Step 2: Connect to Your Instance

```bash
ssh -i /path/to/your-key.pem ec2-user@your-instance-public-dns
```

For Ubuntu:
```bash
ssh -i /path/to/your-key.pem ubuntu@your-instance-public-dns
```

### Step 3: Set Up the Environment

```bash
# Update system packages
sudo yum update -y  # For Amazon Linux
# OR
sudo apt update && sudo apt upgrade -y  # For Ubuntu

# Install Python and pip
sudo yum install python3 python3-pip -y  # For Amazon Linux
# OR
sudo apt install python3 python3-pip -y  # For Ubuntu

# Install required packages
pip3 install pandas numpy matplotlib gspread oauth2client requests
```

### Step 4: Upload the Script Files

Use SCP to upload your script files:

```bash
scp -i /path/to/your-key.pem /path/to/local/script/files/* ec2-user@your-instance-public-dns:~/eth_investment_script/
```

For Ubuntu:
```bash
scp -i /path/to/your-key.pem /path/to/local/script/files/* ubuntu@your-instance-public-dns:~/eth_investment_script/
```

### Step 5: Set Up Scheduled Execution

Create a cron job to run the script automatically:

```bash
# Open crontab editor
crontab -e

# Add a line to run the script weekly (e.g., every Monday at 9 AM)
0 9 * * 1 cd ~/eth_investment_script && python3 eth_investment_dashboard.py --run >> ~/eth_analysis_log.txt 2>&1
```

### Step 6: Set Up Email Notifications (Optional)

Install and configure the `mailutils` package:

```bash
sudo yum install mailx -y  # For Amazon Linux
# OR
sudo apt install mailutils -y  # For Ubuntu
```

Modify your cron job to send email notifications:

```bash
0 9 * * 1 cd ~/eth_investment_script && python3 eth_investment_dashboard.py --run | mail -s "ETH Weekly Analysis" your-email@example.com
```

## Google Cloud Deployment

### Prerequisites
- Google Cloud Platform account
- Google Cloud SDK installed locally
- Basic understanding of Google Cloud services

### Step 1: Create a Compute Engine Instance

1. Go to the Google Cloud Console
2. Navigate to Compute Engine > VM instances
3. Click "Create Instance"
4. Configure your instance:
   - Name: eth-investment-script
   - Region: Choose one close to you
   - Machine type: e2-micro (lowest cost)
   - Boot disk: Ubuntu 20.04 LTS
   - Allow HTTP/HTTPS traffic if needed
5. Click "Create"

### Step 2: Connect to Your Instance

Click the "SSH" button next to your instance in the Google Cloud Console, or use gcloud:

```bash
gcloud compute ssh eth-investment-script
```

### Step 3: Set Up the Environment

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install required packages
pip3 install pandas numpy matplotlib gspread oauth2client requests
```

### Step 4: Upload the Script Files

Use gcloud SCP to upload your script files:

```bash
gcloud compute scp --recurse /path/to/local/script/files/* eth-investment-script:~/eth_investment_script/
```

### Step 5: Set Up Scheduled Execution

Create a cron job to run the script automatically:

```bash
# Open crontab editor
crontab -e

# Add a line to run the script weekly (e.g., every Monday at 9 AM)
0 9 * * 1 cd ~/eth_investment_script && python3 eth_investment_dashboard.py --run >> ~/eth_analysis_log.txt 2>&1
```

### Step 6: Set Up Cloud Functions for Notifications (Optional)

1. Create a new Cloud Function
2. Set the trigger to HTTP
3. Write a function to send email notifications using the Gmail API
4. Modify your script to call this function after analysis

## Azure Deployment

### Prerequisites
- Microsoft Azure account
- Azure CLI installed locally
- Basic understanding of Azure services

### Step 1: Create a Virtual Machine

1. Go to the Azure Portal
2. Navigate to Virtual Machines
3. Click "Add" > "Virtual machine"
4. Configure your VM:
   - Resource group: Create new or select existing
   - VM name: eth-investment-script
   - Region: Choose one close to you
   - Image: Ubuntu Server 20.04 LTS
   - Size: Standard_B1s (lowest cost)
   - Authentication: Password or SSH key
5. Review and create

### Step 2: Connect to Your VM

```bash
ssh your-username@your-vm-public-ip
```

### Step 3: Set Up the Environment

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install required packages
pip3 install pandas numpy matplotlib gspread oauth2client requests
```

### Step 4: Upload the Script Files

Use SCP to upload your script files:

```bash
scp -r /path/to/local/script/files/* your-username@your-vm-public-ip:~/eth_investment_script/
```

### Step 5: Set Up Scheduled Execution

Create a cron job to run the script automatically:

```bash
# Open crontab editor
crontab -e

# Add a line to run the script weekly (e.g., every Monday at 9 AM)
0 9 * * 1 cd ~/eth_investment_script && python3 eth_investment_dashboard.py --run >> ~/eth_analysis_log.txt 2>&1
```

## Digital Ocean Deployment

### Prerequisites
- Digital Ocean account
- Basic understanding of Linux

### Step 1: Create a Droplet

1. Log in to Digital Ocean
2. Click "Create" > "Droplets"
3. Choose an image: Ubuntu 20.04
4. Choose a plan: Basic ($5/mo)
5. Choose a datacenter region close to you
6. Add your SSH key or create a password
7. Click "Create Droplet"

### Step 2: Connect to Your Droplet

```bash
ssh root@your-droplet-ip
```

### Step 3: Set Up the Environment

```bash
# Update system packages
apt update && apt upgrade -y

# Install Python and pip
apt install python3 python3-pip -y

# Install required packages
pip3 install pandas numpy matplotlib gspread oauth2client requests
```

### Step 4: Upload the Script Files

Use SCP to upload your script files:

```bash
scp -r /path/to/local/script/files/* root@your-droplet-ip:~/eth_investment_script/
```

### Step 5: Set Up Scheduled Execution

Create a cron job to run the script automatically:

```bash
# Open crontab editor
crontab -e

# Add a line to run the script weekly (e.g., every Monday at 9 AM)
0 9 * * 1 cd ~/eth_investment_script && python3 eth_investment_dashboard.py --run >> ~/eth_analysis_log.txt 2>&1
```

## Scheduling and Automation

### Cron Job Syntax

The basic syntax for cron jobs is:

```
* * * * * command-to-execute
```

Where the five asterisks represent:
1. Minute (0-59)
2. Hour (0-23)
3. Day of month (1-31)
4. Month (1-12)
5. Day of week (0-6, where 0 is Sunday)

Common examples:

- Every day at midnight: `0 0 * * *`
- Every Monday at 9 AM: `0 9 * * 1`
- Every hour: `0 * * * *`
- Every 15 minutes: `*/15 * * * *`

### Automating Analysis and Notifications

To fully automate your ETH investment script, consider:

1. **Scheduled Analysis**: Run weekly analysis using cron
2. **Email Notifications**: Send results via email
3. **SMS Alerts**: For urgent buy/sell signals
4. **Dashboard Updates**: Automatically update Google Sheets
5. **Log Rotation**: Manage log files to prevent disk space issues

Example script for email notifications:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(subject, body, recipient):
    # Email configuration
    sender = "your-email@gmail.com"
    password = "your-app-password"  # Use app password for Gmail
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    
    # Add body
    message.attach(MIMEText(body, "plain"))
    
    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(message)
        
    print(f"Email notification sent to {recipient}")
```

## Security Considerations

When deploying your ETH investment script to the cloud, consider these security measures:

### API Keys and Credentials

- **Never hardcode credentials** in your script files
- Use environment variables or secure storage services:
  - AWS: AWS Secrets Manager
  - Google Cloud: Secret Manager
  - Azure: Key Vault
  - Digital Ocean: Environment variables

Example using environment variables:

```python
import os

api_key = os.environ.get("CRYPTO_API_KEY")
api_secret = os.environ.get("CRYPTO_API_SECRET")
```

### Network Security

- Restrict SSH access to your IP address only
- Use a firewall to block unnecessary ports
- Enable HTTPS for any web interfaces
- Consider using a VPN for additional security

### Data Protection

- Encrypt sensitive data at rest
- Regularly backup your data
- Implement proper error handling to avoid exposing sensitive information in logs

## Cost Optimization

Cloud services can be cost-effective if managed properly:

### Choosing the Right Instance Type

- For this script, a micro instance is usually sufficient
- AWS t2.micro, Google Cloud e2-micro, or Azure B1s are good options
- These typically fall within free tiers or cost $5-10 per month

### Using Spot Instances/Preemptible VMs

- AWS Spot Instances or Google Cloud Preemptible VMs can reduce costs by 70-90%
- These are suitable for non-critical workloads that can handle interruptions
- Not recommended if you need guaranteed availability

### Scheduling VM Uptime

If your script only runs weekly, you can:

1. Use cloud functions/lambdas instead of VMs
2. Script VM startup/shutdown to run only when needed
3. Use serverless options where available

### Monitoring Costs

- Set up billing alerts to avoid unexpected charges
- Regularly review your usage and adjust resources as needed
- Consider reserved instances for long-term use

## Monitoring and Maintenance

### Logging

Implement comprehensive logging to track script execution:

```python
import logging

# Configure logging
logging.basicConfig(
    filename='eth_investment.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example usage
logging.info("Starting ETH analysis")
logging.error("Error fetching price data: {str(e)}")
```

### Monitoring Script Health

Create a simple health check script:

```python
import requests
import time
import smtplib
from email.mime.text import MIMEText

def check_script_health():
    # Check if log file has been updated recently
    try:
        with open('eth_analysis_log.txt', 'r') as f:
            last_line = f.readlines()[-1]
            # Parse timestamp from last line
            # Check if it's within expected timeframe
            # Send alert if not
    except Exception as e:
        send_alert(f"ETH script health check failed: {str(e)}")

def send_alert(message):
    # Send email or SMS alert
    pass

# Run health check
check_script_health()
```

### Updating the Script

Regularly update your script and dependencies:

1. Set up a development environment for testing updates
2. Use version control (Git) to track changes
3. Implement a proper deployment pipeline
4. Test thoroughly before deploying to production

## Conclusion

Deploying your ETH investment script to the cloud provides reliability, automation, and peace of mind. By following this guide, you can set up a robust cloud deployment that runs your script automatically and notifies you of investment opportunities.

Remember to:
- Choose the cloud provider that best fits your needs and budget
- Implement proper security measures to protect your data
- Monitor costs to avoid unexpected charges
- Set up logging and monitoring to ensure your script runs properly

With these steps in place, your ETH investment script will run reliably in the cloud, helping you make informed investment decisions without manual intervention.
