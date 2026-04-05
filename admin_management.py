from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

admins = {
    "admin1": {"name": "John", "flagged": False, "active": True},
    "admin2": {"name": "Alice", "flagged": False, "active": True}
}

privileged_admins = ["superadmin"]


class FlagRequest(BaseModel):
    admin_id: str


class ActionRequest(BaseModel):
    privileged_admin_id: str
    admin_id: str


@app.post("/flag-admin")
def flag_admin(request: FlagRequest):
    if request.admin_id not in admins:
        raise HTTPException(status_code=404, detail="Admin not found")

    admins[request.admin_id]["flagged"] = True

    return {
        "message": f"{request.admin_id} has been flagged for review",
        "admin_status": admins[request.admin_id]
    }


@app.post("/validate-admin")
def validate_admin(request: ActionRequest):

    if request.privileged_admin_id not in privileged_admins:
        raise HTTPException(status_code=403, detail="Not a privileged admin")

    if request.admin_id not in admins:
        raise HTTPException(status_code=404, detail="Admin not found")

    if not admins[request.admin_id]["flagged"]:
        return {"message": "Admin is not flagged"}

    return {
        "message": f"Flag validated for {request.admin_id}",
        "admin_status": admins[request.admin_id]
    }


@app.post("/deactivate-admin")
def deactivate_admin(request: ActionRequest):

    if request.privileged_admin_id not in privileged_admins:
        raise HTTPException(status_code=403, detail="Not authorized")

    if request.admin_id not in admins:
        raise HTTPException(status_code=404, detail="Admin not found")

    if not admins[request.admin_id]["flagged"]:
        return {"message": "Admin must be flagged before deactivation"}

    admins[request.admin_id]["active"] = False

    return {
        "message": f"{request.admin_id} has been deactivated",
        "admin_status": admins[request.admin_id]
    }