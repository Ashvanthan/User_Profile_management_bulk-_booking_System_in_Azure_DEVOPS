'''import azure.functions as func
import json, uuid, random, sys, os, asyncio
from datetime import datetime
from azure.cosmos import exceptions

# Helper imports from your shared folder
from shared.cosmos_helper import get_container
from shared.auth_helper import hash_password, verify_password, create_token, require_role
from shared.email_helper import send_otp_email, send_ticket_email

# Initialize the V2 App - This MUST be at the root
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
HEADERS = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

# ─── 1. REGISTER & OTP ───
@app.route(route="register", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        name = body.get("name", "").strip()
        otp_code = str(random.randint(100000, 999999))
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        
        user_doc = {
            "id": user_id, "email": email, "name": name,
            "passwordHash": hash_password(body.get("password")),
            "role": body.get("role", "user"), "isEmailVerified": False,
            "otpCode": hash_password(otp_code), 
            "otpExpiry": (datetime.utcnow().timestamp() + 300),
            "createdAt": datetime.utcnow().isoformat()
        }
        get_container("users").create_item(body=user_doc)
        send_otp_email(email, name, otp_code)
        return func.HttpResponse(json.dumps({"message": "OTP Sent", "userId": user_id}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 2. LOGIN ───
@app.route(route="login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        users = get_container("users")
        results = list(users.query_items("SELECT * FROM c WHERE c.email = @e", [{"name":"@e","value":body.get("email")}], True))
        if not results or not verify_password(body.get("password"), results[0]['passwordHash']):
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)
        user = results[0]
        token = create_token(user['id'], user['email'], user['role'])
        return func.HttpResponse(json.dumps({"token": token, "user": {"name":user['name'], "role":user['role']}}), headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 3. MOVIES & THEATERS ───
@app.route(route="getMovies", methods=["GET"])
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    movies = list(get_container("movies").read_all_items())
    return func.HttpResponse(json.dumps({"movies": movies}), headers=HEADERS)

@app.route(route="addMovie", methods=["POST"])
def add_movie(req: func.HttpRequest) -> func.HttpResponse:
    require_role(req, ["admin", "superadmin"])
    body = req.get_json()
    body["id"] = str(uuid.uuid4())
    get_container("movies").create_item(body)
    return func.HttpResponse(json.dumps({"message": "Movie Added"}), status_code=201, headers=HEADERS)

# ─── 4. BOOKINGS ───
@app.route(route="bookTicket", methods=["POST"])
def book_ticket(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    body["id"] = str(uuid.uuid4())
    body["status"] = "confirmed"
    get_container("bookings").create_item(body)
    return func.HttpResponse(json.dumps({"message": "Booking Success"}), status_code=201, headers=HEADERS)'''


'''import azure.functions as func
import json, uuid, random, sys, os, asyncio
from datetime import datetime
from azure.cosmos import exceptions

# Helper imports from your shared folder
from shared.cosmos_helper import get_container
from shared.auth_helper import hash_password, verify_password, create_token, require_role
from shared.email_helper import send_otp_email, send_ticket_email

# Initialize the V2 App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
HEADERS = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

# ─── 1. REGISTER (Auto-Verified) ───
@app.route(route="register", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        name = body.get("name", "").strip()
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        
        user_doc = {
            "id": user_id, 
            "email": email, 
            "name": name,
            "passwordHash": hash_password(body.get("password")),
            "role": body.get("role", "user"), 
            "isEmailVerified": True, # Auto-set to True
            "createdAt": datetime.utcnow().isoformat()
        }
        
        get_container("users").create_item(body=user_doc)
        
        # We no longer call send_otp_email here.
        return func.HttpResponse(json.dumps({"message": "Registration Successful", "userId": user_id}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 2. LOGIN ───
@app.route(route="login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        users = get_container("users")
        results = list(users.query_items("SELECT * FROM c WHERE c.email = @e", [{"name":"@e","value":body.get("email")}], True))
        
        if not results or not verify_password(body.get("password"), results[0]['passwordHash']):
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)
        
        user = results[0]
        token = create_token(user['id'], user['email'], user['role'])
        return func.HttpResponse(json.dumps({"token": token, "user": {"name":user['name'], "role":user['role']}}), headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 3. MOVIES & THEATERS ───
@app.route(route="getMovies", methods=["GET"])
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    movies = list(get_container("movies").read_all_items())
    return func.HttpResponse(json.dumps({"movies": movies}), headers=HEADERS)

@app.route(route="addMovie", methods=["POST"])
def add_movie(req: func.HttpRequest) -> func.HttpResponse:
    require_role(req, ["admin", "superadmin"])
    body = req.get_json()
    body["id"] = str(uuid.uuid4())
    get_container("movies").create_item(body)
    return func.HttpResponse(json.dumps({"message": "Movie Added"}), status_code=201, headers=HEADERS)

# ─── 4. BOOKINGS ───
@app.route(route="bookTicket", methods=["POST"])
def book_ticket(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    body["id"] = str(uuid.uuid4())
    body["status"] = "confirmed"
    get_container("bookings").create_item(body)
    # Note: send_ticket_email in shared/email_helper.py is now a mock function and won't send actual mail.
    return func.HttpResponse(json.dumps({"message": "Booking Success"}), status_code=201, headers=HEADERS)'''


'''import azure.functions as func
import json, uuid, sys, os
from datetime import datetime
from azure.cosmos import exceptions

# Helper imports
from shared.cosmos_helper import get_container
from shared.auth_helper import hash_password, verify_password, create_token, require_role
from shared.email_helper import send_otp_email, send_ticket_email

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
HEADERS = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

# ─── 1. REGISTER (CLEAN VERSION) ───
@app.route(route="register", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        name = body.get("name", "").strip()
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        
        user_doc = {
            "id": user_id, 
            "email": email, 
            "name": name,
            "passwordHash": hash_password(body.get("password")),
            "role": body.get("role", "user"), 
            "isEmailVerified": True,  # USER IS NOW AUTO-VERIFIED
            "createdAt": datetime.utcnow().isoformat()
        }
        
        get_container("users").create_item(body=user_doc)
        
        # We return 201 immediately. No OTP generation.
        return func.HttpResponse(
            json.dumps({"message": "Registration Successful", "userId": user_id}), 
            status_code=201, 
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 2. LOGIN ───
@app.route(route="login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        users = get_container("users")
        results = list(users.query_items(
            "SELECT * FROM c WHERE c.email = @e", 
            [{"name":"@e","value":body.get("email")}], 
            True
        ))
        
        if not results or not verify_password(body.get("password"), results[0]['passwordHash']):
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)
        
        user = results[0]
        token = create_token(user['id'], user['email'], user['role'])
        return func.HttpResponse(
            json.dumps({"token": token, "user": {"name":user['name'], "role":user['role']}}), 
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 3. MOVIES ───
@app.route(route="getMovies", methods=["GET"])
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    movies = list(get_container("movies").read_all_items())
    return func.HttpResponse(json.dumps({"movies": movies}), headers=HEADERS)

@app.route(route="addMovie", methods=["POST"])
def add_movie(req: func.HttpRequest) -> func.HttpResponse:
    require_role(req, ["admin", "superadmin"])
    body = req.get_json()
    body["id"] = str(uuid.uuid4())
    get_container("movies").create_item(body)
    return func.HttpResponse(json.dumps({"message": "Movie Added"}), status_code=201, headers=HEADERS)

# ─── 4. BOOKINGS ───
@app.route(route="bookTicket", methods=["POST"])
def book_ticket(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    body["id"] = str(uuid.uuid4())
    body["status"] = "confirmed"
    get_container("bookings").create_item(body)
    return func.HttpResponse(json.dumps({"message": "Booking Success"}), status_code=201, headers=HEADERS)'''

'''import azure.functions as func
import json, uuid, sys, os
from datetime import datetime
from azure.cosmos import exceptions

# Helper imports
from shared.cosmos_helper import get_container
from shared.auth_helper import hash_password, verify_password, create_token, require_role
from shared.email_helper import send_otp_email, send_ticket_email

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
HEADERS = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

# ─── 1. REGISTER ───
@app.route(route="register", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        name = body.get("name", "").strip()
        password = body.get("password") # PLAIN TEXT
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        
        user_doc = {
            "id": user_id, 
            "email": email, 
            "name": name,
            "passwordHash": password, # STORING PLAIN TEXT DIRECTLY
            "role": body.get("role", "user"), 
            "isEmailVerified": True,
            "createdAt": datetime.utcnow().isoformat()
        }
        
        get_container("users").create_item(body=user_doc)
        
        return func.HttpResponse(
            json.dumps({"message": "Registration Successful", "userId": user_id}), 
            status_code=201, 
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 2. LOGIN (DIRECT COMPARISON FIX) ───
@app.route(route="login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        password = body.get("password")

        users = get_container("users")
        results = list(users.query_items(
            "SELECT * FROM c WHERE c.email = @e", 
            [{"name":"@e","value": email}], 
            True
        ))
        
        # 1. Check if user exists
        if not results:
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)
        
        user = results[0]

        # 2. DIRECT STRING COMPARISON (Avoids all bcrypt/encoding issues)
        if str(password) != str(user.get("passwordHash")):
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)
        
        # 3. Generate Token
        token = create_token(user['id'], user['email'], user['role'])
        
        return func.HttpResponse(
            json.dumps({
                "token": token, 
                "user": {"name": user['name'], "role": user['role']}
            }), 
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 3. MOVIES ───
@app.route(route="getMovies", methods=["GET"])
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    try:
        movies = list(get_container("movies").read_all_items())
        return func.HttpResponse(json.dumps({"movies": movies}), headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

@app.route(route="addMovie", methods=["POST"])
def add_movie(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        get_container("movies").create_item(body)
        return func.HttpResponse(json.dumps({"message": "Movie Added"}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 4. BOOKINGS ───
@app.route(route="bookTicket", methods=["POST"])
def book_ticket(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        body["status"] = "confirmed"
        get_container("bookings").create_item(body)
        return func.HttpResponse(json.dumps({"message": "Booking Success"}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)'''

'''import azure.functions as func
import json, uuid, sys, os
from datetime import datetime
from azure.cosmos import exceptions

# Helper imports from your shared folder
from shared.cosmos_helper import get_container
from shared.auth_helper import create_token, require_role

# Initialize the V2 App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
HEADERS = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

# ─── 1. REGISTER ───
@app.route(route="register", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        name = body.get("name", "").strip()
        password = body.get("password") # Plain text from request
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        
        user_doc = {
            "id": user_id, 
            "email": email, 
            "name": name,
            "passwordHash": password,  # Storing plain text password
            "role": body.get("role", "user"), 
            "isEmailVerified": True,    # Auto-verified
            "createdAt": datetime.utcnow().isoformat()
        }
        
        get_container("users").create_item(body=user_doc)
        
        return func.HttpResponse(
            json.dumps({"message": "Registration Successful", "userId": user_id}), 
            status_code=201, 
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 2. LOGIN (Direct Comparison Fix) ───
@app.route(route="login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        input_password = str(body.get("password"))

        users = get_container("users")
        # Find user by email
        results = list(users.query_items(
            "SELECT * FROM c WHERE c.email = @e", 
            [{"name":"@e","value": email}], 
            True
        ))
        
        # Check if user exists
        if not results:
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)
        
        user = results[0]
        stored_password = str(user.get("passwordHash"))

        # DIRECT PLAIN TEXT COMPARISON
        if input_password != stored_password:
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)
        
        # Generate JWT Token
        token = create_token(user['id'], user['email'], user['role'])
        
        return func.HttpResponse(
            json.dumps({
                "token": token, 
                "user": {"name": user['name'], "role": user['role']}
            }), 
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 3. MOVIES ───
@app.route(route="getMovies", methods=["GET"])
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    try:
        movies = list(get_container("movies").read_all_items())
        return func.HttpResponse(json.dumps({"movies": movies}), headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

@app.route(route="addMovie", methods=["POST"])
def add_movie(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        get_container("movies").create_item(body)
        return func.HttpResponse(json.dumps({"message": "Movie Added"}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

# ─── 4. BOOKINGS ───
@app.route(route="bookTicket", methods=["POST"])
def book_ticket(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        body["status"] = "confirmed"
        get_container("bookings").create_item(body)
        return func.HttpResponse(json.dumps({"message": "Booking Success"}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)'''

'''import azure.functions as func
import json, uuid, sys, os
from datetime import datetime
from azure.cosmos import exceptions

# Helper imports from your shared folder
from shared.cosmos_helper import get_container
from shared.auth_helper import create_token, require_role

# Initialize the V2 App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
HEADERS = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

# ─── 1. REGISTER ───
@app.route(route="register", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        name = body.get("name", "").strip()
        password = body.get("password")  # Plain text from request
        user_id = f"usr_{uuid.uuid4().hex[:12]}"

        user_doc = {
            "id": user_id,
            "email": email,
            "name": name,
            "passwordHash": password,  # Storing plain text password
            "role": body.get("role", "user"),
            "isEmailVerified": True,   # Auto-verified
            "createdAt": datetime.utcnow().isoformat()
        }

        get_container("users").create_item(body=user_doc)

        return func.HttpResponse(
            json.dumps({"message": "Registration Successful", "userId": user_id}),
            status_code=201,
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 2. LOGIN ───
@app.route(route="login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        input_password = str(body.get("password"))

        users = get_container("users")

        # ✅ FIX: use keyword arguments so Cosmos SDK receives them correctly
        results = list(users.query_items(
            query="SELECT * FROM c WHERE c.email = @e",
            parameters=[{"name": "@e", "value": email}],
            enable_cross_partition_query=True
        ))

        # Check if user exists
        if not results:
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)

        user = results[0]
        stored_password = str(user.get("passwordHash"))

        # Direct plain text comparison
        if input_password != stored_password:
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)

        # Generate JWT Token
        token = create_token(user['id'], user['email'], user['role'])

        return func.HttpResponse(
            json.dumps({
                "token": token,
                "user": {"name": user['name'], "role": user['role']}
            }),
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 3. MOVIES ───
@app.route(route="getMovies", methods=["GET"])
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    try:
        movies = list(get_container("movies").read_all_items())
        return func.HttpResponse(json.dumps({"movies": movies}), headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)

@app.route(route="addMovie", methods=["POST"])
def add_movie(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        get_container("movies").create_item(body)
        return func.HttpResponse(json.dumps({"message": "Movie Added"}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 4. BOOKINGS ───
@app.route(route="bookTicket", methods=["POST"])
def book_ticket(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        body["status"] = "confirmed"
        get_container("bookings").create_item(body)
        return func.HttpResponse(json.dumps({"message": "Booking Success"}), status_code=201, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)'''

import azure.functions as func
import json, uuid, os
from datetime import datetime
from azure.cosmos import exceptions

from shared.cosmos_helper import get_container
from shared.auth_helper import create_token, require_role

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
HEADERS = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}


# ─── 1. REGISTER ───
@app.route(route="register", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        name = body.get("name", "").strip()
        password = body.get("password")
        role = body.get("role", "user")
        user_id = f"usr_{uuid.uuid4().hex[:12]}"

        user_doc = {
            "id": user_id,
            "email": email,
            "name": name,
            "passwordHash": password,
            "role": role,
            "companyName": body.get("companyName", ""),
            "phone": body.get("phone", ""),
            "status": "active",
            "approvalStatus": "pending" if role == "admin" else "approved",
            "isEmailVerified": True,
            "createdAt": datetime.utcnow().isoformat()
        }

        get_container("users").create_item(body=user_doc)

        return func.HttpResponse(
            json.dumps({"message": "Registration Successful", "userId": user_id}),
            status_code=201,
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 2. LOGIN ───
@app.route(route="login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        email = body.get("email", "").strip().lower()
        input_password = str(body.get("password"))

        users = get_container("users")

        # FIX: use keyword arguments for query_items
        results = list(users.query_items(
            query="SELECT * FROM c WHERE c.email = @e",
            parameters=[{"name": "@e", "value": email}],
            enable_cross_partition_query=True
        ))

        if not results:
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)

        user = results[0]
        stored_password = str(user.get("passwordHash"))

        if input_password != stored_password:
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, headers=HEADERS)

        token = create_token(user["id"], user["email"], user["role"])

        return func.HttpResponse(
            json.dumps({
                "token": token,
                # FIX: include email so "Logged in as undefined" is fixed
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"],
                    "companyName": user.get("companyName", "")
                }
            }),
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 3. MOVIES ───
@app.route(route="getMovies", methods=["GET"])
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    try:
        theater_id = req.params.get("theaterId")
        if theater_id:
            movies = list(get_container("movies").query_items(
                query="SELECT * FROM c WHERE c.theaterId = @t",
                parameters=[{"name": "@t", "value": theater_id}],
                enable_cross_partition_query=True
            ))
        else:
            movies = list(get_container("movies").read_all_items())
        return func.HttpResponse(json.dumps({"movies": movies}), headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="addMovie", methods=["POST"])
def add_movie(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        body["createdAt"] = datetime.utcnow().isoformat()
        get_container("movies").create_item(body)
        return func.HttpResponse(json.dumps({"message": "Movie Added"}), status_code=201, headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 4. THEATERS ───
@app.route(route="addTheater", methods=["POST"])
def add_theater(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        body["status"] = "active"
        body["createdAt"] = datetime.utcnow().isoformat()
        get_container("theaters").create_item(body)
        return func.HttpResponse(
            json.dumps({"message": "Theater Added", "theaterId": body["id"]}),
            status_code=201,
            headers=HEADERS
        )
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="getTheaters", methods=["GET"])
def get_theaters(req: func.HttpRequest) -> func.HttpResponse:
    try:
        city = req.params.get("city")
        if city:
            theaters = list(get_container("theaters").query_items(
                query="SELECT * FROM c WHERE c.city = @c",
                parameters=[{"name": "@c", "value": city}],
                enable_cross_partition_query=True
            ))
        else:
            theaters = list(get_container("theaters").read_all_items())
        return func.HttpResponse(json.dumps({"theaters": theaters}), headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="flagTheater", methods=["POST"])
def flag_theater(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["superadmin"])
        body = req.get_json()
        theater_id = body.get("theaterId")
        action = body.get("action")
        reason = body.get("reason", "")

        theaters = get_container("theaters")
        results = list(theaters.query_items(
            query="SELECT * FROM c WHERE c.id = @id",
            parameters=[{"name": "@id", "value": theater_id}],
            enable_cross_partition_query=True
        ))
        if not results:
            return func.HttpResponse(json.dumps({"error": "Theater not found"}), status_code=404, headers=HEADERS)

        theater = results[0]
        theater["status"] = action
        theater["flagReason"] = reason
        theaters.replace_item(item=theater_id, body=theater)

        return func.HttpResponse(json.dumps({"message": f"Theater {action} successfully"}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 5. BOOKINGS ───
@app.route(route="bookTicket", methods=["POST"])
def book_ticket(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        body["id"] = str(uuid.uuid4())
        body["status"] = "confirmed"
        body["createdAt"] = datetime.utcnow().isoformat()
        get_container("bookings").create_item(body)
        return func.HttpResponse(
            json.dumps({"message": "Booking Success", "bookingId": body["id"]}),
            status_code=201,
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="bulkBooking", methods=["POST"])
def bulk_booking(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        movie_id = body.get("movieId")
        theater_id = body.get("theaterId")
        show_timing = body.get("showTiming")
        show_date = body.get("showDate")
        users_list = body.get("users", [])

        batch_id = str(uuid.uuid4())
        failed = []
        bookings_container = get_container("bookings")

        for u in users_list:
            try:
                booking = {
                    "id": str(uuid.uuid4()),
                    "batchId": batch_id,
                    "movieId": movie_id,
                    "theaterId": theater_id,
                    "showTiming": show_timing,
                    "showDate": show_date,
                    "userId": u.get("userId"),
                    "userEmail": u.get("userEmail"),
                    "userName": u.get("userName"),
                    "ticketCount": u.get("ticketCount", 1),
                    "status": "confirmed",
                    "createdAt": datetime.utcnow().isoformat()
                }
                bookings_container.create_item(booking)
            except Exception:
                failed.append(u.get("userEmail"))

        return func.HttpResponse(
            json.dumps({
                "message": f"{len(users_list) - len(failed)} bookings confirmed",
                "batchId": batch_id,
                "failed": failed
            }),
            status_code=201,
            headers=HEADERS
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="getMyBookings", methods=["GET"])
def get_my_bookings(req: func.HttpRequest) -> func.HttpResponse:
    try:
        claims = require_role(req, ["user", "admin", "superadmin"])
        user_id = claims.get("sub")

        bookings = list(get_container("bookings").query_items(
            query="SELECT * FROM c WHERE c.userId = @uid",
            parameters=[{"name": "@uid", "value": user_id}],
            enable_cross_partition_query=True
        ))
        return func.HttpResponse(json.dumps({"bookings": bookings}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="getAllBookings", methods=["GET"])
def get_all_bookings(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        bookings = list(get_container("bookings").read_all_items())
        return func.HttpResponse(json.dumps({"bookings": bookings}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 6. USERS ───
@app.route(route="getAllUsers", methods=["GET"])
def get_all_users(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        users = list(get_container("users").read_all_items())
        for u in users:
            u.pop("passwordHash", None)
        return func.HttpResponse(json.dumps({"users": users}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="getUserProfile", methods=["GET"])
def get_user_profile(req: func.HttpRequest) -> func.HttpResponse:
    try:
        claims = require_role(req, ["user", "admin", "superadmin"])
        user_id = claims.get("sub")

        results = list(get_container("users").query_items(
            query="SELECT * FROM c WHERE c.id = @id",
            parameters=[{"name": "@id", "value": user_id}],
            enable_cross_partition_query=True
        ))
        if not results:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, headers=HEADERS)

        user = results[0]
        user.pop("passwordHash", None)
        return func.HttpResponse(json.dumps({"user": user}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="updateProfile", methods=["PUT"])
def update_profile(req: func.HttpRequest) -> func.HttpResponse:
    try:
        claims = require_role(req, ["user", "admin", "superadmin"])
        user_id = claims.get("sub")
        body = req.get_json()

        users = get_container("users")
        results = list(users.query_items(
            query="SELECT * FROM c WHERE c.id = @id",
            parameters=[{"name": "@id", "value": user_id}],
            enable_cross_partition_query=True
        ))
        if not results:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, headers=HEADERS)

        user = results[0]
        if body.get("name"):
            user["name"] = body["name"]
        if body.get("phone"):
            user["phone"] = body["phone"]

        users.replace_item(item=user_id, body=user)
        return func.HttpResponse(json.dumps({"message": "Profile updated"}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="removeUser", methods=["POST"])
def remove_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["admin", "superadmin"])
        body = req.get_json()
        email = body.get("email", "").strip().lower()

        users = get_container("users")
        results = list(users.query_items(
            query="SELECT * FROM c WHERE c.email = @e",
            parameters=[{"name": "@e", "value": email}],
            enable_cross_partition_query=True
        ))
        if not results:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, headers=HEADERS)

        user = results[0]
        user["status"] = "deactivated"
        user["deactivatedAt"] = datetime.utcnow().isoformat()
        user["deactivationReason"] = body.get("reason", "")
        users.replace_item(item=user["id"], body=user)

        return func.HttpResponse(json.dumps({"message": "User deactivated"}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="deactivateAccount", methods=["POST"])
def deactivate_account(req: func.HttpRequest) -> func.HttpResponse:
    try:
        claims = require_role(req, ["user", "admin", "superadmin"])
        user_id = claims.get("sub")

        users = get_container("users")
        results = list(users.query_items(
            query="SELECT * FROM c WHERE c.id = @id",
            parameters=[{"name": "@id", "value": user_id}],
            enable_cross_partition_query=True
        ))
        if not results:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, headers=HEADERS)

        user = results[0]
        user["status"] = "deactivated"
        users.replace_item(item=user_id, body=user)
        return func.HttpResponse(json.dumps({"message": "Account deactivated"}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


# ─── 7. ADMIN APPROVALS ───
@app.route(route="getPendingAdmins", methods=["GET"])
def get_pending_admins(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["superadmin"])
        admins = list(get_container("users").query_items(
            query="SELECT * FROM c WHERE c.role = 'admin'",
            enable_cross_partition_query=True
        ))
        for a in admins:
            a.pop("passwordHash", None)
        return func.HttpResponse(json.dumps({"admins": admins}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)


@app.route(route="approveCompany", methods=["POST"])
def approve_company(req: func.HttpRequest) -> func.HttpResponse:
    try:
        require_role(req, ["superadmin"])
        body = req.get_json()
        admin_email = body.get("adminEmail", "").strip().lower()
        decision = body.get("decision")

        users = get_container("users")
        results = list(users.query_items(
            query="SELECT * FROM c WHERE c.email = @e",
            parameters=[{"name": "@e", "value": admin_email}],
            enable_cross_partition_query=True
        ))
        if not results:
            return func.HttpResponse(json.dumps({"error": "Admin not found"}), status_code=404, headers=HEADERS)

        user = results[0]
        user["approvalStatus"] = decision
        users.replace_item(item=user["id"], body=user)

        return func.HttpResponse(json.dumps({"message": f"Admin {decision} successfully"}), headers=HEADERS)
    except PermissionError as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=403, headers=HEADERS)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=HEADERS)