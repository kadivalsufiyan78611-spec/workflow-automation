import pandas as pd
import os

def analyze_workflow_results():
    """Analyze the results of our automated workflow"""
    print("WORKFLOW RESULTS ANALYSIS")
    print("=" * 40)

    if os.path.exists("todos.csv"):
        df = pd.read_csv("todos.csv")
        print(f"✓ CSV file created successfully")
        print(f"✓ Total records: {len(df)}")
        print(f"✓ Columns: {list(df.columns)}")
        print(f"\nData Analysis:")
        print(f"- Completed tasks: {df['completed'].sum()}")
        print(f"- Pending tasks: {len(df) - df['completed'].sum()}")
        print(f"- Unique users: {df['userId'].nunique()}")
        print(f"\nSample Records:")
        print(df.head(3).to_string(index=False))
    else:
        print("✗ CSV file not found")

    if os.path.exists("workflow_automation.log"):
        print(f"\n✓ Log file created successfully")
        with open("workflow_automation.log", "r") as f:
            lines = f.readlines()
            print(f"✓ Log entries: {len(lines)}")
    else:
        print("\n✗ Log file not found")

if __name__ == "__main__":
    analyze_workflow_results()
