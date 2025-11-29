import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def log(message):
    print(f"[TEST] {message}")

def test_api():
    timestamp = int(time.time())
    email1 = f"user1_{timestamp}@example.com"
    pass1 = "password123"
    email2 = f"user2_{timestamp}@example.com"
    pass2 = "password456"

    # 1. Test Root
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            log("✅ Root endpoint working")
        else:
            log(f"❌ Root endpoint failed: {r.status_code}")
    except Exception as e:
        log(f"❌ Could not connect to server: {e}")
        return

    # 2. Register User 1
    log(f"Registering User 1: {email1}")
    r = requests.post(f"{BASE_URL}/register", json={"email": email1, "password": pass1})
    if r.status_code == 200:
        log("✅ User 1 registered")
    else:
        log(f"❌ User 1 registration failed: {r.text}")
        return

    # 3. Login User 1
    log("Logging in User 1")
    r = requests.post(f"{BASE_URL}/token", data={"username": email1, "password": pass1})
    if r.status_code == 200:
        token1 = r.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        log("✅ User 1 logged in")
    else:
        log(f"❌ User 1 login failed: {r.text}")
        return

    # 4. Shorten URL as User 1
    long_url = "https://www.google.com"
    log(f"User 1 shortening URL: {long_url}")
    r = requests.post(f"{BASE_URL}/shorten", params={"url": long_url}, headers=headers1)
    if r.status_code == 200:
        short_code1 = r.json()["short_code"]
        log(f"✅ URL shortened: {short_code1}")
    else:
        log(f"❌ URL shortening failed: {r.text}")
        return

    # 5. Get URLs as User 1
    log("User 1 fetching URLs")
    r = requests.get(f"{BASE_URL}/urls", headers=headers1)
    if r.status_code == 200:
        urls = r.json()
        if len(urls) == 1 and urls[0]["short_code"] == short_code1:
            log("✅ User 1 sees their URL")
        else:
            log(f"❌ User 1 URL list mismatch: {urls}")
    else:
        log(f"❌ Fetching URLs failed: {r.text}")

    # 6. Register User 2
    log(f"Registering User 2: {email2}")
    r = requests.post(f"{BASE_URL}/register", json={"email": email2, "password": pass2})
    if r.status_code == 200:
        log("✅ User 2 registered")
    else:
        log(f"❌ User 2 registration failed: {r.text}")
        return

    # 7. Login User 2
    log("Logging in User 2")
    r = requests.post(f"{BASE_URL}/token", data={"username": email2, "password": pass2})
    if r.status_code == 200:
        token2 = r.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        log("✅ User 2 logged in")
    else:
        log(f"❌ User 2 login failed: {r.text}")
        return

    # 8. Get URLs as User 2 (Should be empty)
    log("User 2 fetching URLs (Expect empty)")
    r = requests.get(f"{BASE_URL}/urls", headers=headers2)
    if r.status_code == 200:
        urls = r.json()
        if len(urls) == 0:
            log("✅ User 2 sees 0 URLs (Correct)")
        else:
            log(f"❌ User 2 saw URLs (Should be 0): {urls}")
    else:
        log(f"❌ Fetching URLs failed: {r.text}")

    # 9. Shorten URL as User 2
    log(f"User 2 shortening URL: {long_url}")
    r = requests.post(f"{BASE_URL}/shorten", params={"url": long_url}, headers=headers2)
    if r.status_code == 200:
        short_code2 = r.json()["short_code"]
        log(f"✅ User 2 URL shortened: {short_code2}")
    else:
        log(f"❌ URL shortening failed: {r.text}")

    # 10. Get URLs as User 2 (Should have 1)
    log("User 2 fetching URLs (Expect 1)")
    r = requests.get(f"{BASE_URL}/urls", headers=headers2)
    if r.status_code == 200:
        urls = r.json()
        if len(urls) == 1 and urls[0]["short_code"] == short_code2:
            log("✅ User 2 sees their URL")
        else:
            log(f"❌ User 2 URL list mismatch: {urls}")
    else:
        log(f"❌ Fetching URLs failed: {r.text}")
        
    # 11. Verify User 1 still only sees their own
    log("User 1 fetching URLs again (Expect 1)")
    r = requests.get(f"{BASE_URL}/urls", headers=headers1)
    if r.status_code == 200:
        urls = r.json()
        if len(urls) == 1 and urls[0]["short_code"] == short_code1:
            log("✅ User 1 still sees only their URL")
        else:
            log(f"❌ User 1 URL list mismatch (Isolation check): {urls}")
    else:
        log(f"❌ Fetching URLs failed: {r.text}")

    # 12. Test Redirect
    log(f"Testing Redirect for {short_code1}")
    r = requests.get(f"{BASE_URL}/l/{short_code1}")
    if r.status_code == 200:
        data = r.json()
        if data["original_url"] == long_url:
            log("✅ Redirect endpoint returned correct original URL")
        else:
            log(f"❌ Redirect returned wrong URL: {data}")
    else:
        log(f"❌ Redirect failed: {r.status_code}")

if __name__ == "__main__":
    test_api()
