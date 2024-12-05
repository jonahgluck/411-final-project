import requests

BASE_URL = "http://127.0.0.1:5000"

# 1. Create Account
def create_account(username, password):
    payload = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/create-account", json=payload)
    print(f"Create Account Response: {response.status_code}, {response.text}")
    return response

# 2. Log In
def login(username, password):
    payload = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    print(f"Login Response: {response.status_code}, {response.text}")
    return response

# 3. Update Password
def update_password(username, old_password, new_password):
    payload = {
        "username": username,
        "old_password": old_password,
        "new_password": new_password
    }
    response = requests.put(f"{BASE_URL}/update-password", json=payload)
    print(f"Update Password Response: {response.status_code}, {response.text}")
    return response

# Main Workflow
if __name__ == "__main__":
    # Step 1: Create Account
    create_response = create_account("accountN1", "CS411")
    if create_response.status_code == 201:
        # Step 2: Log In
        login_response = login("accountN1", "CS411")
        if login_response.status_code == 200:
            # Step 3: Update Password
            update_response = update_password("accountN1", "CS411", "ILOVECS411")
            if update_response.status_code == 200:
                # Verify new password works
                login("accountN1", "ILOVECS411")
            else:
                print("Failed to update password.")
        else:
            print("Login failed.")
    else:
        print("Account creation failed.")

