from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

records = []
admin_warnings = {}

class Record(BaseModel):
    adminId: str
    name: str
    email: EmailStr
    phone: str


@app.post("/addRecord")
def add_record(record: Record):

    for r in records:
        if r["email"] == record.email or r["phone"] == record.phone:

            if record.adminId not in admin_warnings:
                admin_warnings[record.adminId] = 0

            admin_warnings[record.adminId] += 1

            if admin_warnings[record.adminId] >= 3:
                return {
                    "message": "Duplicate record detected. Admin flagged!",
                    "adminFlagged": True
                }

            return {
                "message": "Duplicate record detected",
                "warnings": admin_warnings[record.adminId]
            }

    records.append(record.dict())

    return {
        "message": "Record added successfully",
        "data": records
    }