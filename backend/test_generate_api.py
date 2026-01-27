"""
Quick test to verify the /generate endpoint works
"""
import requests
import json

def test_generate():
    url = "http://127.0.0.1:8000/api/v1/generate"
    
    payload = {
        "user_input": "Show top 10 SOL holders",
        "chain": "solana",
        "session_id": "test-session-123"
    }
    
    print("🚀 Testing /generate endpoint...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received!")
            print(f"   - ID: {data.get('id')}")
            print(f"   - User Input: {data.get('user_input')}")
            print(f"   - SQL Output: {data.get('sql_output')[:100] if data.get('sql_output') else None}...")
            print(f"   - Error: {data.get('error_message')}")
            print(f"   - Chain: {data.get('chain')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (LLM taking too long)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_generate()
