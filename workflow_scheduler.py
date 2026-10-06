"""
Workflow Scheduler for Business Automation
Lab 22: Automating Business Workflows with Python
"""

import time
import schedule
import subprocess
import logging
from datetime import datetime
import os

class WorkflowScheduler:
    """Simple scheduler for running workflow automation"""

    def __init__(self):
        self.setup_logging()
        self.workflow_script = "workflow_auto.py"
        self.run_count = 0

    def setup_logging(self):
        """Setup logging for scheduler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SCHEDULER - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def run_workflow(self):
        """Execute the workflow script"""
        self.run_count += 1
        self.logger.info(f"Starting scheduled workflow run #{self.run_count}")

        try:
            result = subprocess.run(
                ['python3', self.workflow_script],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.logger.info(f"Workflow run #{self.run_count} completed successfully")
            else:
                self.logger.error(f"Workflow run #{self.run_count} failed with return code {result.returncode}")
                self.logger.error(f"Error output: {result.stderr}")

        except subprocess.TimeoutExpired:
            self.logger.error(f"Workflow run #{self.run_count} timed out")
        except Exception as e:
            self.logger.error(f"Error running workflow #{self.run_count}: {e}")

    def start_scheduler(self, interval_minutes=30):
        """Start the workflow scheduler"""
        self.logger.info(f"Starting workflow scheduler (interval: {interval_minutes} minutes)")
        schedule.every(interval_minutes).minutes.do(self.run_workflow)
        self.logger.info("Running initial workflow execution...")
        self.run_workflow()

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")

def main():
    """Main function for scheduler"""
    print("Business Workflow Scheduler")
    print("=" * 30)
    print("This scheduler will run the workflow automation every 30 minutes")
    print("Press Ctrl+C to stop the scheduler")
    print()

    scheduler = WorkflowScheduler()

    if not os.path.exists(scheduler.workflow_script):
        print(f"Error: {scheduler.workflow_script} not found!")
        print("Please ensure the workflow script is in the current directory")
        return

    scheduler.start_scheduler(interval_minutes=30)

if __name__ == "__main__":
    main()
