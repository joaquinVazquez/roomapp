import requests

BASE_URL = "http://127.0.0.1:8000"

def login(email, password):
    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": email,
            "password": password
        }
    )

    if response.status_code != 200:
        print("Error login:", response.json())
        return None

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }