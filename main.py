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
    # Simulate saving to database
    db_user = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "join_date": datetime.now(),
        "hashed_password": f"hashed_{user_data.password}" 
    }
    fake_db.append(db_user)
    
    # Return user data (filtered by UserOut response_model)
    return db_user

# Add a simple GET endpoint to check if server is running
@app.get("/")
async def root():
    return {"message": "FastAPI Server is running!"}

# Add endpoint to see all users (for testing)
@app.get("/users/")
async def get_all_users():
    return fake_db
