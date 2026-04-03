# ============================================================
#  User Profile Management System — FastAPI Backend
#  Sprint 1: Auth, OTP, Secure Password Update
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import random
import string
import hashlib
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── App Setup ───────────────────────────────────────────────
app = FastAPI(
    title="User Profile Management API",
    description="Sprint 1 — Auth, OTP, Secure Password Update",
    version="1.0.0"
)

# CORS — added ONCE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Restrict to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── In-Memory Stores (replace with DB in production) ───────
# Format: { email: { name, password_hash, is_verified } }
users_db: dict = {
    "test@gmail.com": {
        "name": "Test User",
        "password_hash": hashlib.sha256("Test@1234".encode()).hexdigest(),
        "is_verified": True,
    }
}

# Format: { email: { otp, expires_at, purpose, verified } }
otp_store: dict = {}


# ─── Helper Functions ────────────────────────────────────────

def hash_password(password: str) -> str:
    """SHA-256 hash a password (use bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed


def generate_otp(length: int = 6) -> str:
    """Generate a cryptographically random numeric OTP."""
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(email: str, otp: str, purpose: str = "verification") -> bool:
    """
    OTP Trigger Logic:
    - Reads SMTP config from environment variables.
    - Falls back to console print in dev mode (no SMTP configured).
    """
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    # ── Dev Mode: print OTP to console ──
    if not smtp_host or not smtp_user:
        print(f"\n[DEV] OTP for {email} ({purpose}): {otp}\n")
        return True

    # ── Production Mode: send via SMTP ──
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = smtp_user
        msg["To"] = email
        msg["Subject"] = f"Your OTP — User Profile System"

        html_body = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;
                    padding:32px;background:#0f0f1a;border-radius:12px;color:#fff;">
            <h2 style="color:#a78bfa;">🔐 OTP Verification</h2>
            <p>Your One-Time Password for <strong>{purpose}</strong>:</p>
            <div style="font-size:36px;font-weight:bold;letter-spacing:12px;
                        color:#7c3aed;text-align:center;padding:16px 0;">{otp}</div>
            <p style="color:#94a3b8;">This OTP is valid for <strong>10 minutes</strong>.</p>
            <p style="color:#ef4444;font-size:12px;">⚠️ Do NOT share this with anyone.</p>
        </div>
        """
        msg.attach(MIMEText(html_body, "html"))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, email, msg.as_string())
        server.quit()
        return True
    except Exception as exc:
        print(f"[EMAIL ERROR] {exc}")
        return False


def validate_password_strength(password: str) -> Optional[str]:
    """Returns an error message if password is weak, else None."""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter"
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number"
    return None


# ─── Request / Response Models ───────────────────────────────

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class OTPVerifyRequest(BaseModel):
    email: str
    otp: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str
    confirm_password: str

class ResendOTPRequest(BaseModel):
    email: str


# ─── Routes ──────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def home():
    return {
        "message": "User Profile Management API is running",
        "version": "1.0.0",
        "sprint": "Sprint 1 — Auth, OTP & Secure Password Update"
    }


# ── 1. REGISTRATION API ──────────────────────────────────────
@app.post("/register", tags=["Auth"])
def register(data: RegisterRequest):
    """Register a new user and trigger OTP for email verification."""

    if not data.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if data.email in users_db:
        raise HTTPException(status_code=400, detail="Email is already registered")

    error = validate_password_strength(data.password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    # Save user (unverified until OTP confirmed)
    users_db[data.email] = {
        "name": data.name.strip(),
        "password_hash": hash_password(data.password),
        "is_verified": False,
    }

    # OTP Generation + Trigger
    otp = generate_otp()
    otp_store[data.email] = {
        "otp": otp,
        "expires_at": time.time() + 600,   # 10 minutes
        "purpose": "registration",
        "verified": False,
    }
    send_otp_email(data.email, otp, purpose="email verification")

    return {
        "success": True,
        "message": f"Registration successful! OTP sent to {data.email}",
        "dev_note": f"[DEV ONLY] OTP = {otp}",   # REMOVE in production
    }


# ── 2. LOGIN API ─────────────────────────────────────────────
@app.post("/login", tags=["Auth"])
def login(data: LoginRequest):
    """Authenticate a user with email and password."""

    user = users_db.get(data.email)

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": data.email,
            "is_verified": user.get("is_verified", False),
        },
    }


# ── 3. FORGOT PASSWORD / OTP TRIGGER ────────────────────────
@app.post("/forgot-password", tags=["OTP"])
def forgot_password(data: ForgotPasswordRequest):
    """
    OTP Trigger Logic:
    Generates OTP, stores with expiry, and sends via email.
    Does not reveal whether email is registered (security best practice).
    """
    if data.email in users_db:
        otp = generate_otp()
        otp_store[data.email] = {
            "otp": otp,
            "expires_at": time.time() + 600,
            "purpose": "password_reset",
            "verified": False,
        }
        send_otp_email(data.email, otp, purpose="password reset")
        dev_note = f"[DEV ONLY] OTP = {otp}"   # REMOVE in production
    else:
        dev_note = "[DEV] Email not registered"

    return {
        "success": True,
        "message": f"If {data.email} is registered, an OTP has been sent",
        "dev_note": dev_note,   # REMOVE in production
    }


# ── 4. OTP VERIFICATION API ──────────────────────────────────
@app.post("/verify-otp", tags=["OTP"])
def verify_otp(data: OTPVerifyRequest):
    """Verify the OTP submitted by the user."""

    stored = otp_store.get(data.email)

    if not stored:
        raise HTTPException(
            status_code=400,
            detail="No OTP found for this email. Please request a new OTP."
        )

    if time.time() > stored["expires_at"]:
        otp_store.pop(data.email, None)
        raise HTTPException(
            status_code=400,
            detail="OTP has expired. Please request a new one."
        )

    if data.otp.strip() != stored["otp"]:
        raise HTTPException(status_code=400, detail="Invalid OTP. Please try again.")

    # Mark as verified (keep entry so reset-password can proceed)
    otp_store[data.email]["verified"] = True

    # If registration OTP, mark user as verified
    if stored["purpose"] == "registration" and data.email in users_db:
        users_db[data.email]["is_verified"] = True

    return {"success": True, "message": "OTP verified successfully!"}


# ── 5. SECURE PASSWORD UPDATE (RESET) ────────────────────────
@app.post("/reset-password", tags=["Auth"])
def reset_password(data: ResetPasswordRequest):
    """
    Secure Password Update:
    - Requires OTP to have been verified first
    - Validates password strength
    - Ensures new and confirm passwords match
    """
    stored = otp_store.get(data.email)

    if not stored or not stored.get("verified"):
        raise HTTPException(
            status_code=403,
            detail="OTP verification required before resetting password."
        )

    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    error = validate_password_strength(data.new_password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    if data.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    # Update password
    users_db[data.email]["password_hash"] = hash_password(data.new_password)

    # Invalidate OTP after successful reset
    otp_store.pop(data.email, None)

    return {"success": True, "message": "Password updated successfully! You can now log in."}


# ── 6. RESEND OTP ────────────────────────────────────────────
@app.post("/resend-otp", tags=["OTP"])
def resend_otp(data: ResendOTPRequest):
    """Resend a fresh OTP to the user's email."""

    if data.email not in users_db:
        return {"success": True, "message": "If registered, a new OTP has been sent"}

    otp = generate_otp()
    # Preserve purpose from previous OTP if exists
    purpose = otp_store.get(data.email, {}).get("purpose", "verification")

    otp_store[data.email] = {
        "otp": otp,
        "expires_at": time.time() + 600,
        "purpose": purpose,
        "verified": False,
    }
    send_otp_email(data.email, otp, purpose=purpose)

    return {
        "success": True,
        "message": "New OTP sent. Valid for 10 minutes.",
        "dev_note": f"[DEV ONLY] OTP = {otp}",
    }