# 🎟 User Profile Management System with Bulk Booking
**Cloud-Based | Azure Functions + Cosmos DB + Netlify**

---

## 🏗 Architecture
```
Browser (Netlify)
    ↓  fetch()
Azure Functions (Python APIs)
    ↓  Cosmos SDK
Cosmos DB Serverless (ticketing-db)
    ↓  SendGrid
Email Service
```

---

## 📁 Folder Structure
```
ticket-booking-project/
├── frontend/
│   ├── index.html        ← Landing page
│   ├── login.html        ← Login + OTP verify
│   ├── register.html     ← Registration (user/admin)
│   ├── dashboard.html    ← Role-based dashboard
│   ├── booking.html      ← Browse movies + bulk booking
│   ├── admin.html        ← Admin/superadmin panel
│   ├── style.css         ← Shared styles
│   └── api.js            ← API client + auth helpers
│
├── backend/
│   ├── shared/
│   │   ├── cosmos_helper.py   ← DB connection singleton
│   │   ├── auth_helper.py     ← JWT + bcrypt
│   │   └── email_helper.py    ← SendGrid
│   │
│   ├── register/__init__.py   → POST /api/register
│   │                          → POST /api/verifyOtp
│   ├── login/__init__.py      → POST /api/login
│   ├── getMovies/__init__.py  → GET  /api/getMovies
│   │                          → GET  /api/getTheaters
│   ├── bookTicket/__init__.py → POST /api/bookTicket
│   │                          → GET  /api/getMyBookings
│   ├── bulkBooking/__init__.py→ POST /api/bulkBooking
│   ├── addMovie/__init__.py   → POST /api/addMovie
│   │                          → POST /api/addTheater
│   │                          → POST /api/removeUser
│   │                          → POST /api/approveCompany
│   │                          → POST /api/flagTheater
│   │                          → GET  /api/getUserProfile
│   │                          → PUT  /api/updateProfile
│   │                          → POST /api/deactivateAccount
│   │                          → GET  /api/getPendingAdmins
│   │                          → GET  /api/getAllUsers
│   │                          → GET  /api/getAllBookings
│   │
│   ├── host.json
│   ├── requirements.txt
│   └── local.settings.json    ← LOCAL DEV ONLY (never deploy this)
│
└── netlify.toml
```

---

## ⚡ STEP 1 — Backend Deployment (Azure Functions)

### Prerequisites
- Azure account with an active subscription
- Azure Functions Core Tools installed: `npm install -g azure-functions-core-tools@4`
- Python 3.10+

### Create Function App in Azure Portal
1. Go to Azure Portal → Create Resource → Function App
2. Settings:
   - Runtime: Python 3.10
   - Plan: Consumption (Serverless)
   - Region: Same as your Cosmos DB (e.g. East US)
3. After creation, go to **Configuration → Application Settings** and add:

```
COSMOS_ENDPOINT   = https://tickerbooking-cosmos.documents.azure.com:443/
COSMOS_KEY        = RY2LDy0ClWeYVkpjEXrk9hybtMZ6p3pbOfeUbheWnnwQTtEYFw7gMipa1ZT0L7CMnVsJEiGgTq1FACDbdeH5ZQ==
COSMOS_DB_NAME    = ticketing-db
JWT_SECRET        = [generate a random 32+ char string]
SENDGRID_API_KEY  = [your SendGrid API key]
FROM_EMAIL        = noreply@yourdomain.com
```

4. Enable CORS: Function App → CORS → Add `*` (or your Netlify URL)

### Deploy from CLI
```bash
cd backend
pip install -r requirements.txt
func azure functionapp publish YOUR_FUNCTION_APP_NAME --python
```

### Your API base URL will be:
```
https://YOUR_FUNCTION_APP.azurewebsites.net/api
```

---

## 🌐 STEP 2 — Frontend Deployment (Netlify)

### Update API_BASE in api.js
Open `frontend/api.js` and set:
```js
const API_BASE = "https://YOUR_FUNCTION_APP.azurewebsites.net/api";
```

### Deploy to Netlify
**Option A — Drag & Drop:**
1. Go to netlify.com → Add new site → Deploy manually
2. Drag the `frontend/` folder into the deploy box
3. Done ✅

**Option B — Git:**
```bash
git init
git add .
git commit -m "initial"
# Push to GitHub, then connect repo in Netlify dashboard
```

---

## 🧪 STEP 3 — Create Super Admin Account

After deployment, manually create a superadmin user in Cosmos DB:

In Azure Portal → Cosmos DB → Data Explorer → users container → New Item:

```json
{
  "id": "usr_superadmin001",
  "email": "superadmin@yourdomain.com",
  "name": "Super Admin",
  "passwordHash": "$2b$12$[generate with bcrypt]",
  "role": "superadmin",
  "status": "active",
  "isEmailVerified": true,
  "approvalStatus": "approved",
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-01-01T00:00:00Z"
}
```

To generate the passwordHash, run this Python snippet locally:
```python
import bcrypt
print(bcrypt.hashpw(b"YourPassword123!", bcrypt.gensalt()).decode())
```

---

## 🔧 STEP 4 — Local Development

```bash
cd backend
pip install -r requirements.txt
# Edit local.settings.json with your real Cosmos keys
func start
```

Frontend: just open `frontend/index.html` in a browser (or use Live Server).
Update `api.js`: `const API_BASE = "http://localhost:7071/api";`

---

## 📋 API Reference

| Method | Endpoint           | Auth | Description                    |
|--------|--------------------|------|--------------------------------|
| POST   | /register          | ❌   | Register user/admin            |
| POST   | /verifyOtp         | ❌   | Verify OTP code                |
| POST   | /login             | ❌   | Login, returns JWT             |
| GET    | /getMovies         | ❌   | List active movies             |
| GET    | /getTheaters       | ❌   | List active theaters           |
| POST   | /bookTicket        | ✅   | Single ticket booking          |
| GET    | /getMyBookings     | ✅   | User's booking history         |
| POST   | /bulkBooking       | ✅   | Bulk booking (N users, 1 call) |
| POST   | /addMovie          | ✅   | Admin: add movie               |
| POST   | /addTheater        | ✅   | Admin: add theater             |
| POST   | /removeUser        | ✅   | Admin: deactivate user         |
| POST   | /approveCompany    | ✅   | Superadmin: approve admin      |
| POST   | /flagTheater       | ✅   | Superadmin: flag theater       |
| GET    | /getUserProfile    | ✅   | Get own profile                |
| PUT    | /updateProfile     | ✅   | Update own profile             |
| POST   | /deactivateAccount | ✅   | Deactivate own account         |
| GET    | /getPendingAdmins  | ✅   | Superadmin: list admins        |
| GET    | /getAllUsers        | ✅   | Admin: list all users          |
| GET    | /getAllBookings     | ✅   | Admin: list all bookings       |

---

## 💰 Cost Notes (Cosmos DB Serverless)

- Every query is designed to hit its **partition key** first
- Bulk booking = 1 movie read + N concurrent inserts (asyncio.gather)
- Cost calculation is done entirely in the frontend (zero RU)
- OTP TTL = 300s → Cosmos auto-deletes, no cleanup cost
- `SELECT c.id, c.title ...` projections reduce document charge vs `SELECT *`

Estimated monthly cost for a student project (low traffic): **< $1 USD**

---

## 🔐 Security Notes

- Passwords stored as bcrypt hashes (never plain text)
- OTP stored as bcrypt hash (never plain text)
- JWT tokens expire in 24 hours
- Role checks enforced in every backend function
- Frontend never accesses Cosmos DB directly
- `local.settings.json` is git-ignored — never commit it
