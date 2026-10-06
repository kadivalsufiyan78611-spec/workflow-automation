import requests
import json

def test_api():
    try:
        url = "https://jsonplaceholder.typicode.com/todos"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"API Test Successful!")
        print(f"Fetched {len(data)} records")
        print(f"Sample record: {json.dumps(data[0], indent=2)}")
        
    except Exception as e:
        print(f"API Test Failed: {e}")

if __name__ == "__main__":
    test_api()
