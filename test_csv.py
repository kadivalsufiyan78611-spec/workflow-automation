import pandas as pd
import requests

def test_csv_creation():
    try:
        url = "https://jsonplaceholder.typicode.com/todos"
        response = requests.get(url)
        data = response.json()
        
        df = pd.DataFrame(data[:5])
        df.to_csv("test_todos.csv", index=False)
        
        print("CSV Test Successful!")
        print("Created test_todos.csv with sample data")
        
        print("\nCSV Content Preview:")
        print(df.head())
        
    except Exception as e:
        print(f"CSV Test Failed: {e}")

if __name__ == "__main__":
    test_csv_creation()
