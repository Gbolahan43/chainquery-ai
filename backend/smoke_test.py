"""
ChainQuery AI - Automated Smoke Test
Tests both Guest and Authenticated user flows
"""
import requests
import uuid

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_guest_flow():
    print("🧪 Testing Guest Flow...")
    session_id = str(uuid.uuid4())
    
    # 1. Generate
    payload = {
        "user_input": "Test query for guest",
        "chain": "solana",
        "session_id": session_id
    }
    res = requests.post(f"{BASE_URL}/generate", json=payload)
    assert res.status_code == 200, f"Generate Failed: {res.text}"
    print("   ✅ Generate OK")

    # 2. History
    res = requests.get(f"{BASE_URL}/history", params={"session_id": session_id})
    data = res.json()
    assert len(data) > 0, "History is empty"
    assert data[0]["user_input"] == "Test query for guest"
    print("   ✅ History OK")

def test_auth_flow():
    print("\n🧪 Testing Auth Flow...")
    email = f"auto_test_{uuid.uuid4()}@test.com"
    password = "password123"

    # 1. Signup
    res = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email, "password": password, "full_name": "Test Bot"
    })
    assert res.status_code == 200, f"Signup Failed: {res.text}"
    token = res.json()["access_token"]
    print("   ✅ Signup OK")

    # 2. Protected Generate
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "user_input": "Test query for AUTH user",
        "chain": "solana",
        "session_id": "ignored_for_auth"
    }
    res = requests.post(f"{BASE_URL}/generate", json=payload, headers=headers)
    assert res.status_code == 200, f"Protected Generate Failed: {res.text}"
    print("   ✅ Protected Generate OK")

if __name__ == "__main__":
    try:
        test_guest_flow()
        test_auth_flow()
        print("\n🎉 ALL SYSTEMS GO! READY FOR DEMO.")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
