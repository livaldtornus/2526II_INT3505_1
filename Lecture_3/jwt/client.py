import requests

BASE_URL = "http://localhost:5005"

def login(username, password):
    print(f"\n--- Logging in as {username} ---")
    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json().get("token")
        print("Login successful. Received token:", token)
        return token
    else:
        print("Login failed:", response.status_code, response.json())
        return None

def access_protected(token):
    print("\n--- Accessing protected route ---")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print("Status:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    # 1. Valid login
    token_alice = login("alice", "password123")
    
    # 2. Access protected route with valid token
    if token_alice:
        access_protected(token_alice)
        
    # 3. Invalid login
    login("bob", "wrongpass")

    # 4. Access without token
    access_protected(None)

    # 5. Access with invalid token
    access_protected("invalid.token.here")
