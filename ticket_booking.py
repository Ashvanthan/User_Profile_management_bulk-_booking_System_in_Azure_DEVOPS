from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Fake database
tickets = []

class Booking(BaseModel):
    user_id: str
    event_name: str
    seat_number: int


@app.post("/book-ticket")
def book_ticket(booking: Booking):

    ticket = {
        "user_id": booking.user_id,
        "event_name": booking.event_name,
        "seat_number": booking.seat_number
    }

    tickets.append(ticket)

    return {
        "message": "Ticket booked successfully",
        "ticket": ticket
    }