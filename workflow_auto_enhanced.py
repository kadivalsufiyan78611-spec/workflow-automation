"""
Enhanced Business Workflow Automation Script
Lab 22: Automating Business Workflows with Python
"""

import requests
import pandas as pd
import smtplib
import json
import logging
import os
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EnhancedWorkflowAutomation:
    """Enhanced workflow automation with better error handling and configuration"""

    def __init__(self, config=None):
        self.config = {
            'api_url': 'https://jsonplaceholder.typicode.com/todos',
            'csv_filename': 'todos_enhanced.csv',
            'log_filename': 'workflow_enhanced.log',
            'max_retries': 3,
            'timeout': 30
        }

        if config:
            self.config.update(config)

        self.setup_logging()
        self.data = None
        self.workflow_stats = {
            'start_time': None,
            'end_time': None,
            'records_processed': 0,
            'errors': []
        }

    def setup_logging(self):
        """Setup enhanced logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config['log_filename']),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def fetch_api_data_with_retry(self):
        """Fetch data from API with retry mechanism"""
        self.logger.info("Starting API data fetch with retry mechanism...")

        for attempt in range(self.config['max_retries']):
            try:
                self.logger.info(f"Attempt {attempt + 1} of {self.config['max_retries']}")

                response = requests.get(
                    self.config['api_url'],
                    timeout=self.config['timeout']
                )
                response.raise_for_status()

                self.data = response.json()
                self.workflow_stats['records_processed'] = len(self.data)

                self.logger.info(f"Successfully fetched {len(self.data)} records")
                return True

            except requests.exceptions.RequestException as e:
                error_msg = f"Attempt {attempt + 1} failed: {e}"
                self.logger.warning(error_msg)
                self.workflow_stats['errors'].append(error_msg)

                if attempt == self.config['max_retries'] - 1:
                    self.logger.error("All retry attempts failed")
                    return False

        return False

    def validate_and_clean_data(self):
        """Validate and clean the fetched data"""
        if not self.data:
            self.logger.error("No data to validate")
            return False

        self.logger.info("Validating and cleaning data...")

        try:
            df = pd.DataFrame(self.data)
            required_columns = ['userId', 'id', 'title', 'completed']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                self.logger.error(f"Missing required columns: {missing_columns}")
                return False

            original_count = len(df)
            df = df.drop_duplicates(subset=['id'])
            df = df.dropna(subset=['userId', 'id', 'title'])
            cleaned_count = len(df)

            if cleaned_count != original_count:
                self.logger.info(f"Data cleaned: {original_count} -> {cleaned_count} records")

            self.data = df.to_dict('records')
            self.workflow_stats['records_processed'] = len(self.data)
            self.logger.info("Data validation and cleaning completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error during data validation: {e}")
            return False

    def save_to_csv_enhanced(self):
        """Enhanced CSV saving with additional metadata"""
        try:
            if not self.data:
                self.logger.error("No data available to save")
                return False

            self.logger.info("Saving data to CSV with metadata...")
            df = pd.DataFrame(self.data)
            df['processed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['workflow_version'] = 'enhanced_v1.0'
            df.to_csv(self.config['csv_filename'], index=False)

            if os.path.exists(self.config['csv_filename']):
                file_size = os.path.getsize(self.config['csv_filename'])
                self.logger.info(f"CSV saved successfully: {self.config['csv_filename']} ({file_size} bytes)")

                summary = {
                    'filename': self.config['csv_filename'],
                    'records': len(self.data),
                    'file_size_bytes': file_size,
                    'created_date': datetime.now().isoformat(),
                    'columns': list(df.columns)
                }

                with open('workflow_summary.json', 'w') as f:
                    json.dump(summary, f, indent=2)

                return True
            else:
                self.logger.error("CSV file was not created")
                return False

        except Exception as e:
            self.logger.error(f"Error saving CSV: {e}")
            return False

    def generate_workflow_report(self):
        """Generate a comprehensive workflow report"""
        try:
            self.logger.info("Generating workflow report...")

            report = {
                'workflow_execution': {
                    'start_time': self.workflow_stats['start_time'],
                    'end_time': self.workflow_stats['end_time'],
                    'duration_seconds': None,
                    'status': 'completed' if not self.workflow_stats['errors'] else 'completed_with_errors'
                },
                'data_processing': {
                    'source_api': self.config['api_url'],
                    'records_processed': self.workflow_stats['records_processed'],
                    'output_file': self.config['csv_filename']
                },
                'errors': self.workflow_stats['errors']
            }

            if self.workflow_stats['start_time'] and self.workflow_stats['end_time']:
                duration = self.workflow_stats['end_time'] - self.workflow_stats['start_time']
                report['workflow_execution']['duration_seconds'] = duration.total_seconds()

            with open('workflow_report.json', 'w') as f:
                json.dump(report, f, indent=2, default=str)

            self.logger.info("Workflow report generated: workflow_report.json")
            return True

        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return False

    def run_enhanced_workflow(self):
        """Run the complete enhanced workflow"""
        self.workflow_stats['start_time'] = datetime.now()

        self.logger.info("=" * 60)
        self.logger.info("STARTING ENHANCED BUSINESS WORKFLOW AUTOMATION")
        self.logger.info("=" * 60)

        success_count = 0
        total_tasks = 4

        self.logger.info("TASK 1: Fetching data from API (with retry)...")
        if self.fetch_api_data_with_retry():
            success_count += 1
            self.logger.info("✓ Task 1 completed successfully")
        else:
            self.logger.error("✗ Task 1 failed")

        self.logger.info("TASK 2: Validating and cleaning data...")
        if self.validate_and_clean_data():
            success_count += 1
            self.logger.info("✓ Task 2 completed successfully")
        else:
            self.logger.error("✗ Task 2 failed")

        self.logger.info("TASK 3: Saving data to CSV (enhanced)...")
        if self.save_to_csv_enhanced():
            success_count += 1
            self.logger.info("✓ Task 3 completed successfully")
        else:
            self.logger.error("✗ Task 3 failed")

        self.logger.info("TASK 4: Generating workflow report...")
        if self.generate_workflow_report():
            success_count += 1
            self.logger.info("✓ Task 4 completed successfully")
        else:
            self.logger.error("✗ Task 4 failed")

        self.workflow_stats['end_time'] = datetime.now()
        self.logger.info("=" * 60)
        self.logger.info(f"ENHANCED WORKFLOW COMPLETED: {success_count}/{total_tasks} tasks successful")
        self.logger.info("=" * 60)

        return success_count == total_tasks

def main():
    """Main function for enhanced workflow"""
    print("Enhanced Business Workflow Automation")
    print("=" * 40)

    workflow = EnhancedWorkflowAutomation()
    success = workflow.run_enhanced_workflow()

    print(f"\nWorkflow Status: {'SUCCESS' if success else 'PARTIAL SUCCESS'}")
    print(f"Records Processed: {workflow.workflow_stats['records_processed']}")
    print(f"Errors Encountered: {len(workflow.workflow_stats['errors'])}")

    print(f"\nGenerated Files:")
    files_to_check = [
        workflow.config['csv_filename'],
        'workflow_summary.json',
        'workflow_report.json',
        workflow.config['log_filename']
    ]

    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ {filename} ({size} bytes)")
        else:
            print(f"✗ {filename} (not found)")

if __name__ == "__main__":
    main()
