import os

# We removed SendGrid imports to prevent library errors
FROM_EMAIL = os.environ.get("FROM_EMAIL", "noreply@ticketbooking.com")

def send_otp_email(to_email: str, name: str, otp_code: str):
    # This now does nothing. Registration will continue instantly.
    print(f"[INTERNAL] OTP Email suppressed for user: {to_email}")
    return

def send_ticket_email(to_email: str, name: str, booking: dict):
    # This now does nothing. Booking will continue instantly.
    print(f"[INTERNAL] Ticket Email suppressed for booking: {booking.get('id')}")
    return

def _send(to_email: str, subject: str, html: str):
    # Logic removed to stop all outgoing mail attempts
    pass