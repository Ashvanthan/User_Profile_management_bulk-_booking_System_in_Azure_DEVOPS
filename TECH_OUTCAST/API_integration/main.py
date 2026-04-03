from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS setup
origins = [
    "*",  # allow all origins (for testing). Later, restrict to your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],     # allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],     # allow all headers
)

# Request model
class ForgotPasswordRequest(BaseModel):
    email: str

# Forgot Password API
@app.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    email = data.email
    # Normally check email in DB and send OTP
    return {
        "success": True,
        "message": f"OTP sent to {email}"
    }

# Test route
@app.get("/")
def home():
    return {"message": "API running"}




# CORS (allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class LoginRequest(BaseModel):
    email: str
    password: str

# Dummy login API
@app.post("/login")
def login_api(data: LoginRequest):
    # Dummy user check
    if data.email == "test@gmail.com" and data.password == "123456":
        return {"success": True, "message": "Login successful"}
    else:
        return {"success": False, "message": "Invalid credentials"}
    


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OTP model
class OTPRequest(BaseModel):
    email: str
    otp: str

@app.post("/verify-otp")
def verify_otp(data: OTPRequest):
    # For testing, assume OTP is always "123456"
    if data.otp == "123456":
        return {"success": True, "message": "OTP verified successfully!"}
    else:
        return {"success": False, "message": "Invalid OTP"}