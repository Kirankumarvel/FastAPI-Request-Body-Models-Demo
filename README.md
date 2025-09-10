# FastAPI Pydantic Request Body Demo

A FastAPI application demonstrating the use of Pydantic models as request bodies for POST endpoints with automatic validation and response modeling.

---

## 🚀 Features

- **FastAPI** framework with automatic OpenAPI documentation (`/docs` and `/redoc`)
- **Pydantic models** for request body validation and response modeling
- Response model filtering for security (exclude sensitive fields)
- Automatic HTTP status code handling
- Input validation before function execution
- Python 3.7+ compatibility
- Virtual environment setup instructions

---

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

---

## 🛠️ Installation & Setup

### 1. Create Project Structure

```bash
# Create project directory
mkdir fastapi-request-body-demo
cd fastapi-request-body-demo

# Create necessary files
touch main.py models.py requirements.txt .gitignore
```

## 📥 Clone the Repository

To get started, clone the repository to your local machine using the following command (replace with your desired repo if needed):

```bash
git clone https://github.com/Kirankumarvel/FastAPI-Pydantic-Models-Demo.git
cd FastAPI-Pydantic-Models-Demo
```

### 2. Add Content to Files

**`models.py`**
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    join_date: datetime

    class Config:
        from_attributes = True
```

**`main.py`**
```python
from fastapi import FastAPI, status
from datetime import datetime
from models import UserCreate, UserOut

app = FastAPI()

# In-memory "database" for demonstration
fake_db = []

@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """
    Create a new user with validated request body.
    """
    db_user = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "join_date": datetime.now(),
        "hashed_password": f"hashed_{user_data.password}" 
    }
    fake_db.append(db_user)
    return db_user

@app.get("/")
async def root():
    return {"message": "FastAPI Server is running!"}

@app.get("/users/")
async def get_all_users():
    return fake_db
```

**`requirements.txt`**
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-extra-types==0.7.0
```

**`.gitignore`**
```
venv/
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.vscode/
.idea/
*.swp
*.swo
.DS_Store
Thumbs.db
```

---

## 3. Set Up Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 4. Run the FastAPI Server

```bash
uvicorn main:app --reload --reload-exclude venv
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
...
```

---

## 5. Test the API

### Method 1: Using Browser

- Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (should show a welcome message)
- Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)
- Redoc docs: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Method 2: Using curl

```bash
# Test GET endpoint
curl http://127.0.0.1:8000/

# Test POST endpoint with valid data
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "email": "john@example.com", "password": "securepassword123", "full_name": "John Doe"}'

# Test with missing required field (should show error)
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "securepassword123"}'

# Test with invalid email (should show error)
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "email": "invalid-email", "password": "securepassword123"}'

# View all users
curl http://127.0.0.1:8000/users/
```

### Method 3: Using Python `requests`

**Create a test script `test_api.py`:**
```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Test GET request
r = requests.get(f"{BASE_URL}/")
print("GET / response:", r.json())

# Test POST request with valid data
user_data = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
}
r = requests.post(f"{BASE_URL}/users/", json=user_data)
print("POST /users/ response:", r.json())
print("Status Code:", r.status_code)
```
Run with:
```bash
python test_api.py
```

---

## 📡 API Endpoints

- **POST `/users/`**  
  Create a new user with validated request body data.

  **Request Body Example:**
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }
  ```
  **Response Example:**
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "join_date": "2025-09-10T06:05:34.000000"
  }
  ```
  **Status Code:** `201 Created`

---

## 🎯 Key Concept: Request Body Models

- **Declaration:** Use Pydantic models as function parameters.
- **Validation:** FastAPI validates request body before function execution.
- **Docs:** OpenAPI schema generated automatically.
- **Error Handling:** Descriptive errors for validation failures.
- **Response Filtering:** `response_model` controls output data.

---

## 📁 Project Structure

```
fastapi-request-body-demo/
├── venv/             # Virtual environment (ignored by git)
├── main.py           # Main application file
├── models.py         # Pydantic model definitions
├── requirements.txt  # Project dependencies
├── .gitignore        # Git ignore file
└── test_api.py       # (optional) test script
```

---

## 🧪 Troubleshooting

**ModuleNotFoundError:**  
- Make sure you are in the project directory and the virtual environment is activated.

**Port already in use:**  
- Use a different port:  
  `uvicorn main:app --reload --port 8001`

**EmailStr validation errors:**  
- Ensure `pydantic-extra-types` is installed.

**Import errors:**  
- Check you installed all dependencies and are running from the project directory.

---

## 📚 Learning Resources

- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic Models](https://docs.pydantic.dev/)
- [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- FastAPI team for seamless request body handling
- Pydantic team for robust validation library
- Uvicorn team for the ASGI server
- Python community for ongoing support

---

This step-by-step guide should help you set up and execute the FastAPI project without confusion. The server will run on [http://127.0.0.1:8000](http://127.0.0.1:8000) and you can test it using curl, browser, or the interactive documentation!
