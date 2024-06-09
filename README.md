# User Registration and login

## Overview
This FastAPI application manages user registration and login using MongoDB for data storage. It includes API endpoints for user creation and authentication, along with HTML templates for registration and login forms.
## Features
- User Registration: Validates user input and stores user data securely in MongoDB.
- User Login: Authenticates users using bcrypt for password hashing and comparison.
- Error Handling: Custom error handling for internal errors and HTTP exceptions.

## Prerequisites
Before running the application, ensure you have the following:
- Python (3.7+ recommended)
- MongoDB installed and running locally
- Environment variables defined in .env (see .env.example)

## Usage
### 1. Clone the Repository
```
git clone https://github.com/yourusername/YourProject.git
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Run the Application
```
python main.py
```
Access the application at http://localhost:9000
Use the provided HTML forms (/register and /login) to interact with the application.

## Configuration
- MongoDB Connection: Set the MONGO_URL and MONGO_DBNAME environment variables in .env.
- Secret Key: Set the secret_key environment variable in .env.




