---

## 🏢 Intelligent Floor Plan Management System

### 🔍 Overview

The **Intelligent Floor Plan Management System** is a FastAPI-based backend that enables organizations to **digitally manage floor plans, rooms, and seat allocations**, and supports **real-time concurrent editing with optimistic locking**.

---

## ⚙️ Tech Stack

| Layer                                 | Technology                                        |
| ------------------------------------- | ------------------------------------------------- |
| **Backend Framework**                 | FastAPI (Python 3.12)                             |
| **Database**                          | PostgreSQL                                        |
| **ORM**                               | SQLAlchemy                                        |
| **Authentication**                    | JWT-based (OAuth2PasswordBearer)                  |
| **Password Hashing**                  | bcrypt + passlib                                  |
| **File Handling**                     | Uploads stored locally in `/uploads`              |
| **Schema Validation**                 | Pydantic                                          |
| **Containerization (Optional)**       | Docker + Docker Compose                           |
| **Future Storage Upgrade (Optional)** | MinIO or AWS S3                                   |
| **Frontend (Next Step)**              | React + Fabric.js (for visual floor plan editing) |

---

## 📁 Project Structure

```
Floor_Plan_Management_System/
│
├── app/
│   ├── main.py                # FastAPI entry point & admin creation
│   ├── database.py            # PostgreSQL session & connection
│   ├── config.py              # Environment variables
│   ├── oAuth2.py              # JWT token management
│   ├── schemas.py             # Pydantic models
│   ├── tablesmodel.py         # SQLAlchemy models
│   ├── utils.py               # Password hashing utilities
│   ├── routers/
|   |   ├── admin.py           # admin promote users
│   │   ├── auth.py            # Login, register
│   │   ├── floorplans.py      # Upload & versioned floor plan routes
│   │   ├── overlays.py        # Room & seat CRUD operations
│   │   ├── bookings.py        # Booking endpoints with conflict handling
│   │   └── users.py           # (Optional) User listing & roles
│
├── uploads/                   # Stored floor plan images
├── .env                       # Environment variables (DB URL, secrets)
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🔑 Features Implemented

### ✅ **1. Authentication & Role-based Access**

* Admin & Normal user roles.
* JWT Bearer authentication with token generation.
* Admin bootstrap via environment variables:

  ```
  INITIAL_ADMIN_EMAIL=admin@example.com
  INITIAL_ADMIN_PASSWORD=admin@123
  ```

---

### ✅ **2. Floor Plan Management**

* Upload floor plans (`POST /floorplans`) — supports image/PDF + metadata.
* Auto-versioning system on every edit.
* Stores files locally under `/uploads`.
* Floor plan retrieval & listing endpoints.

Example Upload (Postman Form-Data):

```
file: floorplan_demo.png
name: HQ Level 1
building: HQ
floor_number: 1
pixels_per_meter: 100
```

---

### ✅ **3. Overlay Management (Rooms / Seats)**

* Create overlays (rooms, seats) on floor plans.
* Retrieve overlays via `GET /overlays/floorplan/{id}`.
* Each save updates floor plan version.
* Supports optimistic locking to prevent concurrent edits.

---

### ✅ **4. Optimistic Locking (Version Conflict Handling)**

* Prevents overwriting floor plans edited by other users.
* Each save sends `client_version`, server checks `server_version`.

**Demo Flow (Postman):**

1. Client A → save with `client_version: 1` ✅
   → Response: `{"status": "ok", "new_version": 2}`
2. Client B → save again with stale `client_version: 1` ⚠️
   → Response:

   ```json
   {
     "message": "version_mismatch",
     "server_version": 2,
     "server_overlays": [...]
   }
   ```
3. Client B reloads latest overlays → resubmits with `"client_version": 2` ✅
   → Response: `{"status": "ok", "new_version": 3}`

---

### ✅ **5. Booking System**

* Create bookings for room overlays.
* Detect overlapping time conflicts (`HTTP 409`).
* Retrieve bookings by overlay or booking ID.
* Check available rooms for a given time range.

**Conflict Example:**

```json
{
  "message": "booking_conflict",
  "conflicts": [
    {"id": 1, "start_ts": "...", "end_ts": "...", "organizer_id": 1}
  ]
}
```

---

## 👥 User Roles Summary

| Feature              | Admin | Normal User |
| -------------------- | ----- | ----------- |
| Upload floor plans   | ✅     | ❌           |
| Edit floor plans     | ✅     | ❌           |
| Create overlays      | ✅     | ❌           |
| View floor plans     | ✅     | ✅           |
| Create bookings      | ✅     | ✅           |
| Cancel own booking   | ✅     | ✅           |
| View available rooms | ✅     | ✅           |
| Manage users         | ✅     | ❌           |

---

## 🚀 How to Run Locally

1. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   Create `.env` file:

   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=your_database_password
   DATABASE_NAME=your_database_name
   DATABASE_USERNAME=your_database_username
   SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   EMAIL=your_email
   SMTP_PASSWORD=your_smtp_password
   INITIAL_ADMIN_EMAIL=admin@example.com
   INITIAL_ADMIN_PASSWORD=admin@123
   ```

4. **Run the server**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access Swagger UI**

   ```
   http://127.0.0.1:8000/docs
   ```

---

## 🧪 Testing (Demo Flow for Interview)

| Step | Description               | Endpoint                                    |
| ---- | ------------------------- | ------------------------------------------- |
| 1    | Admin Login               | `POST /login`                               |
| 2    | Upload Floor Plan         | `POST /floorplans`                          |
| 3    | Save Overlays             | `PUT /floorplans/{id}/save`                 |
| 4    | Simulate Version Conflict | 2 tabs → 409 Conflict                       |
| 5    | Create Booking            | `POST /bookings`                            |
| 6    | Overlapping Booking       | 409 Conflict                                |
| 7    | List Available Rooms      | `GET /bookings/available?start=...&end=...` |

---

## 🧩 Future Improvements (Phase 2)

| Category                 | Improvement                                                         |
| ------------------------ | ------------------------------------------------------------------- |
| **Storage**              | Integrate MinIO or AWS S3 for scalable image/PDF storage.           |
| **Containerization**     | Add Dockerfile & docker-compose.yml for full environment setup.     |
| **Frontend (Next Step)** | React + Fabric.js canvas editor for drawing overlays interactively. |
| **Collaboration**        | Real-time multi-user editing with WebSockets.                       |
| **Notifications**        | Email or Slack alerts for booking conflicts or approvals.           |
| **Analytics**            | Dashboard for occupancy rate, utilization trends, and heatmaps.     |
| **Admin Dashboard**      | Role management UI and audit history of edits.                      |

---

## 🧠 Key Learnings

* Implemented **optimistic concurrency control** using version tracking.
* Designed modular FastAPI architecture with clean router separation.
* Built **secure authentication** and **role-based access control**.
* Implemented email functionality for user communication, including welcome/signup and one-time password (OTP) for password reset, utilizing Python's smtplib and HTML content.
* Implemented **conflict detection** in both bookings and overlay editing.
* Demonstrated strong understanding of database transactions & RESTful design.

---