import requests
import time
import sys

def test_server(url, max_retries=5):
    """Test if the server is running and accessible"""
    print(f"Testing server at {url}...")
    
    for i in range(max_retries):
        try:
            response = requests.get(url)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return True
        except requests.exceptions.ConnectionError:
            print(f"Connection failed. Retry {i+1}/{max_retries}...")
            time.sleep(2)
    
    print("Server is not responding after maximum retries.")
    return False

if __name__ == "__main__":
    # Test the root endpoint (HTML page)
    test_server("http://localhost:8000/")
    
    # Test the API endpoints
    test_server("http://localhost:8000/api/players/")
    test_server("http://localhost:8000/api/saves/")