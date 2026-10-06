"""
Simple Workflow Scheduler (Demo Version)
Lab 22: Automating Business Workflows with Python
"""

import time
import subprocess
import logging
from datetime import datetime

def run_workflow_demo():
    """Demonstrate running workflow multiple times"""
    print("WORKFLOW SCHEDULER DEMONSTRATION")
    print("=" * 40)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    for run_number in range(1, 4):
        logger.info(f"Starting workflow run #{run_number}")

        try:
            result = subprocess.run(
                ['python3', 'workflow_auto.py'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info(f"Run #{run_number} completed successfully")
            else:
                logger.error(f"Run #{run_number} failed")

            if run_number < 3:
                logger.info("Waiting 30 seconds before next run...")
                time.sleep(30)

        except Exception as e:
            logger.error(f"Error in run #{run_number}: {e}")

    logger.info("Scheduler demonstration completed")

if __name__ == "__main__":
    run_workflow_demo()
