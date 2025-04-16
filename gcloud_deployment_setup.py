#!/usr/bin/env python3
"""
Google Cloud Deployment - Compute Engine Setup Script
----------------------------------------------------
This script helps set up a Google Cloud Compute Engine instance for the ETH investment script.
It creates the necessary startup and configuration scripts for automated deployment.

Author: Manus AI
Date: April 16, 2025
"""

import os
import argparse
import json
import subprocess
import sys

# Configuration
DEFAULT_INSTANCE_NAME = "eth-investment-vm"
DEFAULT_MACHINE_TYPE = "e2-micro"
DEFAULT_ZONE = "us-central1-a"
DEFAULT_IMAGE_FAMILY = "ubuntu-2004-lts"
DEFAULT_IMAGE_PROJECT = "ubuntu-os-cloud"

def create_startup_script():
    """Create a startup script for the VM instance"""
    script = """#!/bin/bash
# Startup script for ETH investment VM

# Update system packages
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y python3-pip python3-venv git

# Create directory for the script
mkdir -p /opt/eth-investment

# Clone the repository or download files
# git clone YOUR_REPO_URL /opt/eth-investment
# OR
# Create script files

# Create virtual environment
python3 -m venv /opt/eth-investment/venv
source /opt/eth-investment/venv/bin/activate

# Install required Python packages
pip install pandas numpy matplotlib gspread oauth2client requests

# Set up cron job for weekly analysis
(crontab -l 2>/dev/null; echo "0 9 * * 1 cd /opt/eth-investment && /opt/eth-investment/venv/bin/python eth_investment_dashboard.py --run >> /var/log/eth-analysis.log 2>&1") | crontab -

# Set up log rotation
cat > /etc/logrotate.d/eth-investment << EOL
/var/log/eth-analysis.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
}
EOL

# Create notification script
cat > /opt/eth-investment/send_notification.py << EOL
#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

def send_email_notification(subject, body, recipient):
    # Email configuration - replace with your values or use environment variables
    sender = os.environ.get("NOTIFICATION_EMAIL", "your-email@gmail.com")
    password = os.environ.get("NOTIFICATION_PASSWORD", "your-app-password")
    
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

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python send_notification.py subject body recipient")
        sys.exit(1)
        
    subject = sys.argv[1]
    body = sys.argv[2]
    recipient = sys.argv[3]
    
    send_email_notification(subject, body, recipient)
EOL

chmod +x /opt/eth-investment/send_notification.py

# Create a wrapper script to run analysis and send notification
cat > /opt/eth-investment/run_analysis_with_notification.sh << EOL
#!/bin/bash
cd /opt/eth-investment
source venv/bin/activate
python eth_investment_dashboard.py --run > analysis_output.txt
if [ $? -eq 0 ]; then
    python send_notification.py "ETH Analysis Complete" "$(cat analysis_output.txt)" "$NOTIFICATION_RECIPIENT"
else
    python send_notification.py "ETH Analysis Failed" "The ETH investment analysis script failed to run properly." "$NOTIFICATION_RECIPIENT"
fi
EOL

chmod +x /opt/eth-investment/run_analysis_with_notification.sh

# Create a health check script
cat > /opt/eth-investment/health_check.py << EOL
#!/usr/bin/env python3
import os
import time
import datetime
import sys

def check_log_file(log_file, max_age_hours=25):
    """Check if log file exists and has been updated recently"""
    if not os.path.exists(log_file):
        return False, "Log file does not exist"
        
    file_mod_time = os.path.getmtime(log_file)
    current_time = time.time()
    age_hours = (current_time - file_mod_time) / 3600
    
    if age_hours > max_age_hours:
        return False, f"Log file is too old: {age_hours:.1f} hours"
    
    return True, f"Log file is recent: {age_hours:.1f} hours old"

if __name__ == "__main__":
    log_file = "/var/log/eth-analysis.log"
    
    # Check if script should have run recently (e.g., after Monday 9 AM)
    today = datetime.datetime.now()
    day_of_week = today.weekday()  # 0 is Monday
    hour = today.hour
    
    # If it's Monday after 9 AM or any later day in the week, log should be fresh
    should_have_run = (day_of_week == 0 and hour >= 9) or day_of_week > 0
    
    if should_have_run:
        status, message = check_log_file(log_file)
        print(message)
        if not status:
            sys.exit(1)
    else:
        print("No recent run expected yet")
        
    sys.exit(0)
EOL

chmod +x /opt/eth-investment/health_check.py

# Set up a daily health check
(crontab -l 2>/dev/null; echo "0 12 * * * cd /opt/eth-investment && ./health_check.py || ./send_notification.py 'ETH Script Health Check Failed' 'The ETH investment script health check failed. Please check the VM.' '$NOTIFICATION_RECIPIENT'") | crontab -

echo "ETH investment script setup complete"
"""
    
    with open("startup-script.sh", "w") as f:
        f.write(script)
    
    print("Startup script created: startup-script.sh")
    return "startup-script.sh"

def create_deployment_script(startup_script):
    """Create a deployment script for Google Cloud"""
    script = f"""#!/bin/bash
# Google Cloud deployment script for ETH investment

# Configuration - modify these variables
INSTANCE_NAME="{DEFAULT_INSTANCE_NAME}"
MACHINE_TYPE="{DEFAULT_MACHINE_TYPE}"
ZONE="{DEFAULT_ZONE}"
PROJECT_ID=$(gcloud config get-value project)
STARTUP_SCRIPT="{startup_script}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "gcloud could not be found. Please install the Google Cloud SDK."
    exit 1
fi

# Check if project ID is set
if [ -z "$PROJECT_ID" ]; then
    echo "No project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID'"
    exit 1
fi

# Create the VM instance
echo "Creating VM instance $INSTANCE_NAME..."
gcloud compute instances create $INSTANCE_NAME \\
    --machine-type=$MACHINE_TYPE \\
    --zone=$ZONE \\
    --image-family={DEFAULT_IMAGE_FAMILY} \\
    --image-project={DEFAULT_IMAGE_PROJECT} \\
    --metadata-from-file=startup-script=$STARTUP_SCRIPT \\
    --scopes=https://www.googleapis.com/auth/cloud-platform \\
    --tags=http-server,https-server

# Get the external IP
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "VM instance created with IP: $EXTERNAL_IP"
echo "Setup is running in the background. You can check the status with:"
echo "gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo tail -f /var/log/syslog'"

echo "To upload your ETH investment script files, use:"
echo "gcloud compute scp --recurse /path/to/local/script/files/* $INSTANCE_NAME:/opt/eth-investment/ --zone=$ZONE"

echo "To set notification email, connect to the VM and run:"
echo "gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo "Then run: export NOTIFICATION_RECIPIENT=your-email@example.com"
echo "And add it to your .bashrc file for persistence"
"""
    
    with open("deploy-to-gcloud.sh", "w") as f:
        f.write(script)
    
    # Make the script executable
    os.chmod("deploy-to-gcloud.sh", 0o755)
    
    print("Deployment script created: deploy-to-gcloud.sh")
    return "deploy-to-gcloud.sh"

def create_cloud_function_files():
    """Create files for Cloud Functions deployment"""
    # Create directory for Cloud Functions
    os.makedirs("cloud-functions", exist_ok=True)
    
    # Create main.py for the Cloud Function
    main_py = """
import base64
import json
import os
import tempfile
import traceback
from google.cloud import storage
from datetime import datetime

# Import our ETH investment modules
# Note: These need to be included in the deployment package
from eth_price_tracker import ETHPriceTracker
from eth_technical_analysis import ETHTechnicalAnalysis
from eth_investment_advisor import ETHInvestmentAdvisor
from eth_risk_manager import ETHRiskManager
from eth_performance_tracker import ETHPerformanceTracker

# Configuration
BUCKET_NAME = os.environ.get('STORAGE_BUCKET', 'eth-investment-data')
CONFIG_FILE = os.environ.get('CONFIG_FILE', 'eth_config.json')
NOTIFICATION_TOPIC = os.environ.get('NOTIFICATION_TOPIC', 'eth-investment-notifications')

def run_eth_analysis(event, context):
    """
    Cloud Function to run ETH investment analysis
    
    Args:
        event (dict): Event payload
        context (google.cloud.functions.Context): Event context
    
    Returns:
        dict: Analysis results
    """
    try:
        print(f"Starting ETH investment analysis at {datetime.now().isoformat()}")
        
        # Initialize storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Download configuration if it exists
        config = {}
        config_blob = bucket.blob(CONFIG_FILE)
        if config_blob.exists():
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                config_blob.download_to_filename(temp_file.name)
                with open(temp_file.name, 'r') as f:
                    config = json.load(f)
                os.unlink(temp_file.name)
        
        # Initialize modules
        price_tracker = ETHPriceTracker()
        analyzer = ETHTechnicalAnalysis()
        advisor = ETHInvestmentAdvisor(risk_tolerance=config.get('risk_tolerance', 'medium'))
        risk_manager = ETHRiskManager(
            portfolio_value=config.get('portfolio_value', 10000),
            max_risk_per_trade=config.get('max_risk_per_trade', 0.02),
            max_portfolio_exposure=config.get('max_portfolio_exposure', 0.25)
        )
        
        # Load trade history from storage
        trades_file = 'eth_trades.json'
        trades_blob = bucket.blob(trades_file)
        trades_data = []
        if trades_blob.exists():
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                trades_blob.download_to_filename(temp_file.name)
                with open(temp_file.name, 'r') as f:
                    trades_data = json.load(f)
                os.unlink(temp_file.name)
        
        # Load decisions history from storage
        decisions_file = 'eth_decisions.json'
        decisions_blob = bucket.blob(decisions_file)
        decisions_data = []
        if decisions_blob.exists():
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                decisions_blob.download_to_filename(temp_file.name)
                with open(temp_file.name, 'r') as f:
                    decisions_data = json.load(f)
                os.unlink(temp_file.name)
        
        # Initialize performance tracker with loaded data
        performance_tracker = ETHPerformanceTracker()
        performance_tracker.trades = trades_data
        performance_tracker.decisions = decisions_data
        
        # Get current price data
        current_data = price_tracker.get_current_price()
        if not current_data:
            raise Exception("Failed to get current price data")
            
        current_price = current_data.get('price', 0)
        print(f"Current ETH Price: ${current_price:.2f}")
        
        # Get historical price data
        historical_prices = price_tracker.get_historical_prices(days=90)
        if historical_prices.empty:
            raise Exception("Failed to get historical price data")
            
        print(f"Retrieved {len(historical_prices)} days of historical data")
        
        # Perform technical analysis
        analysis_results = analyzer.analyze_price_data(historical_prices)
        if not analysis_results:
            raise Exception("Failed to perform technical analysis")
            
        print(f"Technical Analysis Recommendation: {analysis_results.get('recommendation', 'UNKNOWN')}")
        
        # Generate investment recommendation
        recommendation = advisor.generate_recommendation(analysis_results, historical_prices)
        if not recommendation:
            raise Exception("Failed to generate investment recommendation")
            
        print(f"Investment Recommendation: {recommendation.get('recommendation', 'UNKNOWN')}")
        
        # Generate risk management report
        risk_report = risk_manager.generate_risk_report(current_price, current_price, historical_prices)
        if not risk_report:
            raise Exception("Failed to generate risk management report")
        
        # Generate performance report
        performance_report = performance_tracker.generate_performance_report(current_price)
        if not performance_report:
            raise Exception("Failed to generate performance report")
        
        # Record the decision
        decision = performance_tracker.record_decision(
            recommendation.get('recommendation', 'UNKNOWN'),
            current_price,
            analysis_results
        )
        
        # Save updated decisions back to storage
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            json.dump(performance_tracker.decisions, temp_file)
            temp_file.flush()
            decisions_blob.upload_from_filename(temp_file.name)
            os.unlink(temp_file.name)
        
        # Compile results
        results = {
            'timestamp': datetime.now().isoformat(),
            'price_data': current_data,
            'analysis': analysis_results,
            'recommendation': recommendation,
            'risk_report': risk_report,
            'performance': performance_report
        }
        
        # Save results to storage
        results_file = f'eth_analysis_{datetime.now().strftime("%Y%m%d")}.json'
        results_blob = bucket.blob(results_file)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            json.dump(results, temp_file)
            temp_file.flush()
            results_blob.upload_from_filename(temp_file.name)
            os.unlink(temp_file.name)
        
        # Generate beginner-friendly summary
        summary = generate_beginner_friendly_summary(results)
        
        # Save summary to storage
        summary_file = f'eth_summary_{datetime.now().strftime("%Y%m%d")}.txt'
        summary_blob = bucket.blob(summary_file)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(summary)
            temp_file.flush()
            summary_blob.upload_from_filename(temp_file.name)
            os.unlink(temp_file.name)
        
        # Send notification (implementation depends on your notification method)
        send_notification(
            subject=f"ETH Analysis: {recommendation.get('recommendation', 'UNKNOWN')}",
            message=summary,
            results=results
        )
        
        print(f"ETH investment analysis completed successfully at {datetime.now().isoformat()}")
        return results
        
    except Exception as e:
        error_message = f"Error in ETH analysis: {str(e)}\\n{traceback.format_exc()}"
        print(error_message)
        
        # Send error notification
        try:
            send_notification(
                subject="ETH Analysis Error",
                message=error_message,
                results=None
            )
        except Exception as notify_error:
            print(f"Failed to send error notification: {str(notify_error)}")
        
        # Re-raise the exception for Cloud Functions logging
        raise

def generate_beginner_friendly_summary(results):
    """Generate a beginner-friendly summary of analysis results"""
    try:
        if not results:
            return "Error: No analysis results available"
            
        summary = []
        
        # Add header
        summary.append("=" * 60)
        summary.append("ETH INVESTMENT SUMMARY - BEGINNER'S GUIDE")
        summary.append("=" * 60)
        summary.append("")
        
        # Add current price information
        if "price_data" in results:
            price_data = results["price_data"]
            summary.append(f"Current ETH Price: ${price_data.get('price', 0):.2f}")
            
            change_24h = price_data.get('change_24h', 0)
            if change_24h > 0:
                summary.append(f"24-hour Change: 📈 +{change_24h:.2f}% (Up)")
            else:
                summary.append(f"24-hour Change: 📉 {change_24h:.2f}% (Down)")
                
            summary.append("")
        
        # Add recommendation
        if "recommendation" in results:
            recommendation = results["recommendation"]
            rec_text = recommendation.get("recommendation", "UNKNOWN")
            
            summary.append("WHAT SHOULD YOU DO?")
            summary.append("-" * 60)
            
            if rec_text == "STRONG BUY":
                summary.append("🟢 STRONG BUY - Technical indicators strongly suggest buying ETH now")
            elif rec_text == "BUY":
                summary.append("🟢 BUY - Technical indicators suggest buying ETH now")
            elif rec_text == "HOLD":
                summary.append("🟡 HOLD - Technical indicators suggest holding your current position")
            elif rec_text == "SELL":
                summary.append("🔴 SELL - Technical indicators suggest selling ETH now")
            elif rec_text == "STRONG SELL":
                summary.append("🔴 STRONG SELL - Technical indicators strongly suggest selling ETH now")
            else:
                summary.append(f"⚪ {rec_text} - Please check the detailed analysis")
            
            summary.append("")
            summary.append("Recommended Action:")
            summary.append(recommendation.get("action", "No specific action recommended"))
            summary.append("")
            
            # Add explanation in simple terms
            summary.append("WHY THIS RECOMMENDATION?")
            summary.append("-" * 60)
            
            for explanation in recommendation.get("explanations", []):
                if explanation:
                    summary.append(f"• {explanation}")
            
            summary.append("")
        
        # Add risk management in simple terms
        if "risk_report" in results:
            risk_report = results["risk_report"]
            
            summary.append("RISK MANAGEMENT")
            summary.append("-" * 60)
            
            # Stop-loss
            if "stop_loss" in risk_report:
                stop_loss = risk_report["stop_loss"]
                recommended_method = stop_loss.get("recommended_method", "")
                
                if recommended_method and recommended_method in stop_loss.get("methods", {}):
                    stop_price = stop_loss["methods"][recommended_method].get("stop_price", 0)
                    
                    summary.append(f"Stop-Loss Price: ${stop_price:.2f}")
                    summary.append("(This is the price at which you should sell to limit potential losses)")
                    summary.append("")
            
            # Position size
            if "position_size" in risk_report:
                position_size = risk_report["position_size"]
                
                summary.append("If you decide to buy ETH:")
                summary.append(f"• Recommended Amount: {position_size.get('position_size_coins', 0):.4f} ETH")
                summary.append(f"• Approximate Cost: ${position_size.get('position_size_dollars', 0):.2f}")
                summary.append(f"• This represents {position_size.get('portfolio_percentage', 0) * 100:.1f}% of your portfolio")
                summary.append("")
        
        # Add performance summary
        if "performance" in results and "portfolio" in results["performance"]:
            portfolio = results["performance"]["portfolio"]
            
            summary.append("YOUR PORTFOLIO PERFORMANCE")
            summary.append("-" * 60)
            
            eth_balance = portfolio.get('eth_balance', 0)
            if eth_balance > 0:
                summary.append(f"Current ETH Holdings: {eth_balance:.4f} ETH (${portfolio.get('current_value', 0):.2f})")
                
                total_pl = portfolio.get('total_pl', 0)
                roi = portfolio.get('roi', 0) * 100
                
                if total_pl >= 0:
                    summary.append(f"Total Profit: ${total_pl:.2f} (ROI: {roi:.1f}%)")
                else:
                    summary.append(f"Total Loss: ${total_pl:.2f} (ROI: {roi:.1f}%)")
            else:
                summary.append("You don't have any ETH holdings recorded yet.")
                summary.append("Use this tool to track your investments once you start buying ETH.")
            
            summary.append("")
        
        # Add footer with next steps
        summary.append("NEXT STEPS")
        summary.append("-" * 60)
        summary.append("1. Review the recommendation and decide if you want to take action")
        summary.append("2. If buying, consider using the recommended position size")
        summary.append("3. If selling, consider the tax implications of your sale")
        summary.append("4. Always set a stop-loss to protect your investment")
        summary.append("5. Check back next week for an updated analysis")
        summary.append("")
        
        # Add disclaimer
        summary.append("DISCLAIMER")
        summary.append("-" * 60)
        summary.append("This is an automated analysis based on technical indicators.")
        summary.append("It should not be considered financial advice.")
        summary.append("Always do your own research before making investment decisions.")
        summary.append("=" * 60)
        
        return "\\n".join(summary)
    except Exception as e:
        print(f"Error generating beginner-friendly summary: {str(e)}")
        return f"Error generating summary: {str(e)}"

def send_notification(subject, message, results=None):
    """
    Send notification with analysis results
    
    This is a placeholder function. Implement your preferred notification method:
    - Pub/Sub
    - SendGrid
    - SMTP email
    - Twilio SMS
    - etc.
    """
    # Example using Pub/Sub (you would need to set up a Pub/Sub topic and subscriber)
    try:
        from google.cloud import pubsub_v1
        
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(
            os.environ.get('PROJECT_ID', 'your-project-id'),
            NOTIFICATION_TOPIC
        )
        
        # Create message data
        data = {
            'subject': subject,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add results if available
        if results:
            data['results'] = results
        
        # Convert to JSON and publish
        data_bytes = json.dumps(data).encode('utf-8')
        publisher.publish(topic_path, data=data_bytes)
        
        print(f"Notification sent to topic: {NOTIFICATION_TOPIC}")
        return True
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return False
"""
    
    with open(os.path.join("cloud-functions", "main.py"), "w") as f:
        f.write(main_py)
    
    # Create requirements.txt
    requirements = """
google-cloud-storage>=2.0.0
google-cloud-pubsub>=2.0.0
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
gspread>=5.0.0
oauth2client>=4.1.3
requests>=2.25.0
"""
    
    with open(os.path.join("cloud-functions", "requirements.txt"), "w") as f:
        f.write(requirements)
    
    # Create deployment script for Cloud Functions
    deploy_script = """#!/bin/bash
# Deploy ETH investment script to Google Cloud Functions

# Configuration - modify these variables
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
FUNCTION_NAME="eth-investment-analysis"
BUCKET_NAME="eth-investment-data-$PROJECT_ID"
TOPIC_NAME="eth-investment-notifications"
SCHEDULE="0 9 * * 1"  # Every Monday at 9 AM

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "gcloud could not be found. Please install the Google Cloud SDK."
    exit 1
fi

# Check if project ID is set
if [ -z "$PROJECT_ID" ]; then
    echo "No project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID'"
    exit 1
fi

# Create storage bucket if it doesn't exist
if ! gsutil ls -b gs://$BUCKET_NAME &> /dev/null; then
    echo "Creating storage bucket: $BUCKET_NAME"
    gsutil mb -l $REGION gs://$BUCKET_NAME
else
    echo "Storage bucket already exists: $BUCKET_NAME"
fi

# Create Pub/Sub topic if it doesn't exist
if ! gcloud pubsub topics describe $TOPIC_NAME &> /dev/null; then
    echo "Creating Pub/Sub topic: $TOPIC_NAME"
    gcloud pubsub topics create $TOPIC_NAME
else
    echo "Pub/Sub topic already exists: $TOPIC_NAME"
fi

# Copy ETH investment script files to the cloud function directory
echo "Copying ETH investment script files to cloud function directory..."
cp ../eth_*.py cloud-functions/

# Deploy the Cloud Function
echo "Deploying Cloud Function: $FUNCTION_NAME"
gcloud functions deploy $FUNCTION_NAME \\
    --region=$REGION \\
    --runtime=python39 \\
    --source=cloud-functions \\
    --entry-point=run_eth_analysis \\
    --trigger-topic=run-eth-analysis \\
    --memory=512MB \\
    --timeout=540s \\
    --set-env-vars=STORAGE_BUCKET=$BUCKET_NAME,NOTIFICATION_TOPIC=$TOPIC_NAME,PROJECT_ID=$PROJECT_ID

# Create Cloud Scheduler job
JOB_NAME="weekly-eth-analysis"
if ! gcloud scheduler jobs describe $JOB_NAME --location=$REGION &> /dev/null; then
    echo "Creating Cloud Scheduler job: $JOB_NAME"
    gcloud scheduler jobs create pubsub $JOB_NAME \\
        --location=$REGION \\
        --schedule="$SCHEDULE" \\
        --topic=run-eth-analysis \\
        --message-body="Run ETH investment analysis" \\
        --time-zone="UTC"
else
    echo "Cloud Scheduler job already exists: $JOB_NAME"
    echo "Updating Cloud Scheduler job: $JOB_NAME"
    gcloud scheduler jobs update pubsub $JOB_NAME \\
        --location=$REGION \\
        --schedule="$SCHEDULE" \\
        --topic=run-eth-analysis \\
        --message-body="Run ETH investment analysis" \\
        --time-zone="UTC"
fi

echo "Deployment complete!"
echo "Your ETH investment script will run every Monday at 9 AM UTC."
echo "Results will be stored in the bucket: $BUCKET_NAME"
echo "Notifications will be published to the topic: $TOPIC_NAME"
echo ""
echo "To manually trigger the analysis, run:"
echo "gcloud pubsub topics publish run-eth-analysis --message='Run ETH investment analysis'"
echo ""
echo "To view the Cloud Function logs, run:"
echo "gcloud functions logs read $FUNCTION_NAME --region=$REGION"
"""
    
    with open(os.path.join("cloud-functions", "deploy-cloud-function.sh"), "w") as f:
        f.write(deploy_script)
    
    # Make the script executable
    os.chmod(os.path.join("cloud-functions", "deploy-cloud-function.sh"), 0o755)
    
    print("Cloud Functions files created in the 'cloud-functions' directory")
    return "cloud-functions"

def create_notification_subscriber():
    """Create a notification subscriber script"""
    script = """#!/usr/bin/env python3
"""
    
    with open("notification-subscriber.py", "w") as f:
        f.write(script)
    
    print("Notification subscriber script created: notification-subscriber.py")
    return "notification-subscriber.py"

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Google Cloud Deployment Setup for ETH Investment Script")
    parser.add_argument("--instance-name", default=DEFAULT_INSTANCE_NAME, help="Name for the VM instance")
    parser.add_argument("--machine-type", default=DEFAULT_MACHINE_TYPE, help="Machine type for the VM instance")
    parser.add_argument("--zone", default=DEFAULT_ZONE, help="Zone for the VM instance")
    args = parser.parse_args()
    
    print("Creating Google Cloud deployment files for ETH investment script...")
    
    # Create startup script
    startup_script = create_startup_script()
    
    # Create deployment script
    deployment_script = create_deployment_script(startup_script)
    
    # Create Cloud Function files
    cloud_function_dir = create_cloud_function_files()
    
    # Create notification subscriber
    notification_subscriber = create_notification_subscriber()
    
    print("\nDeployment files created successfully!")
    print("\nTo deploy to Google Cloud Compute Engine:")
    print(f"1. Review and modify the startup script: {startup_script}")
    print(f"2. Run the deployment script: ./{deployment_script}")
    print("\nTo deploy to Google Cloud Functions:")
    print(f"1. Review and modify the Cloud Function files in: {cloud_function_dir}")
    print(f"2. Run the deployment script: ./{cloud_function_dir}/deploy-cloud-function.sh")
    print("\nFor more information, refer to the ETH_CLOUD_DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
