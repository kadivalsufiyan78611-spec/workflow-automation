"""
Business Workflow Automation Script
Lab 22: Automating Business Workflows with Python
"""

import requests
import pandas as pd
import smtplib
import csv
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workflow_automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class WorkflowAutomation:
    """Main class for handling business workflow automation"""
    
    def __init__(self):
        self.api_url = "https://jsonplaceholder.typicode.com/todos"
        self.csv_filename = "todos.csv"
        self.data = None
        
    def fetch_api_data(self):
        """Task 1: Fetch data from public API"""
        try:
            logger.info("Starting API data fetch...")
            response = requests.get(self.api_url, timeout=30)
            response.raise_for_status()
            
            self.data = response.json()
            logger.info(f"Successfully fetched {len(self.data)} records from API")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from API: {e}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return False
    
    def save_to_csv(self):
        """Task 2: Save data to CSV file"""
        try:
            if not self.data:
                logger.error("No data available to save")
                return False
                
            logger.info("Converting data to CSV format...")
            
            df = pd.DataFrame(self.data)
            df.to_csv(self.csv_filename, index=False)
            
            if os.path.exists(self.csv_filename):
                file_size = os.path.getsize(self.csv_filename)
                logger.info(f"Successfully saved data to {self.csv_filename} (Size: {file_size} bytes)")
                return True
            else:
                logger.error("CSV file was not created")
                return False
                
        except Exception as e:
            logger.error(f"Error saving data to CSV: {e}")
            return False
    
    def send_email_with_attachment(self, sender_email, sender_password, recipient_email):
        """Task 3: Send email with CSV attachment"""
        try:
            logger.info("Preparing email with attachment...")
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Automated Workflow Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            body = f"""
            Automated Business Workflow Report
            
            This email was generated automatically by our Python workflow automation system.
            
            Report Details:
            - Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            - Data source: {self.api_url}
            - Records processed: {len(self.data) if self.data else 0}
            - File attached: {self.csv_filename}
            
            This is an automated message. Please do not reply to this email.
            
            Best regards,
            Automated Workflow System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            if os.path.exists(self.csv_filename):
                with open(self.csv_filename, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {self.csv_filename}'
                )
                msg.attach(part)
                logger.info(f"Attached file: {self.csv_filename}")
            else:
                logger.warning("CSV file not found, sending email without attachment")
            
            logger.info("Email prepared successfully (simulated send)")
            logger.info(f"Email would be sent from {sender_email} to {recipient_email}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error preparing email: {e}")
            return False
    
    def run_workflow(self, sender_email="demo@company.com", sender_password="demo_password", recipient_email="manager@company.com"):
        """Main workflow execution - chains all tasks"""
        logger.info("=" * 50)
        logger.info("STARTING AUTOMATED BUSINESS WORKFLOW")
        logger.info("=" * 50)
        
        workflow_success = True
        
        logger.info("TASK 1: Fetching data from API...")
        if not self.fetch_api_data():
            logger.error("Task 1 failed - stopping workflow")
            return False
        
        logger.info("TASK 2: Saving data to CSV...")
        if not self.save_to_csv():
            logger.error("Task 2 failed - stopping workflow")
            return False
        
        logger.info("TASK 3: Sending email with attachment...")
        if not self.send_email_with_attachment(sender_email, sender_password, recipient_email):
            logger.error("Task 3 failed")
            workflow_success = False
        
        logger.info("=" * 50)
        if workflow_success:
            logger.info("WORKFLOW COMPLETED SUCCESSFULLY")
        else:
            logger.info("WORKFLOW COMPLETED WITH ERRORS")
        logger.info("=" * 50)
        
        return workflow_success

def main():
    """Main function to run the workflow"""
    workflow = WorkflowAutomation()
    success = workflow.run_workflow()
    
    if success:
        print("\n" + "="*60)
        print("BUSINESS WORKFLOW AUTOMATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"✓ Data fetched from API")
        print(f"✓ Data saved to {workflow.csv_filename}")
        print(f"✓ Email prepared with attachment")
        print(f"✓ Check workflow_automation.log for detailed logs")
    else:
        print("\n" + "="*60)
        print("WORKFLOW COMPLETED WITH ERRORS")
        print("="*60)
        print("✗ Check workflow_automation.log for error details")

if __name__ == "__main__":
    main()
