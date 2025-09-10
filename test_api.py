import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test GET request
response = requests.get(f"{BASE_URL}/")
print("GET / response:", response.json())

# Test POST request with valid data
user_data = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
}

response = requests.post(f"{BASE_URL}/users/", json=user_data)
print("POST /users/ response:", response.json())
print("Status Code:", response.status_code)

# Test with invalid data
invalid_data = {
    "email": "john@example.com",
    "password": "securepassword123"
}

response = requests.post(f"{BASE_URL}/users/", json=invalid_data)
print("Invalid request response:", response.json())
