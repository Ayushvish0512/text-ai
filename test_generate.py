import urllib.request
import json

# Test the API with a video script prompt
url = "http://localhost:8000/generate"

# Simple prompt without special characters
prompt = "Create a 15-30 second video script with a hook about breaking news: Trump comments on Iran strikes. Include: Hook, Main content, Call to action"

payload = {
    "prompt": prompt,
    "max_length": 300
}

try:
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Generated Script:")
        print(result["response"])
except Exception as e:
    print(f"Error: {e}")

