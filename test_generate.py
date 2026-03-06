import requests
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n=== Testing Health Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_generate():
    print("\n=== Testing Generate Endpoint ===")
    test_cases = [
        {"text": "Hello, how are", "max_length": 20},
        {"text": "The weather today is", "max_length": 30},
        {"text": "Once upon a time", "max_length": 50}
    ]
    
    for i, payload in enumerate(test_cases, 1):
        print(f"\nTest {i}: {payload['text']}")
        try:
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/generate",
                json=payload,
                timeout=60
            )
            elapsed = time.time() - start
            
            print(f"Status: {response.status_code}")
            print(f"Time: {elapsed:.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data.get('response', '')[:100]}...")
            else:
                print(f"Error: {response.json()}")
                
        except Exception as e:
            print(f"Error: {e}")

def test_error_handling():
    print("\n=== Testing Error Handling ===")
    
    # Empty text
    print("\nTest: Empty text")
    response = requests.post(f"{BASE_URL}/generate", json={"text": ""})
    print(f"Status: {response.status_code} (expected 400)")
    print(f"Response: {response.json()}")
    
    # Missing text field
    print("\nTest: Missing text field")
    response = requests.post(f"{BASE_URL}/generate", json={"max_length": 10})
    print(f"Status: {response.status_code} (expected 400)")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("=" * 50)
    print("Tiny LLM API Test Suite")
    print("=" * 50)
    
    if test_health():
        test_generate()
        test_error_handling()
    else:
        print("\nHealth check failed. Is the server running?")
        print("Start with: python app.py")
