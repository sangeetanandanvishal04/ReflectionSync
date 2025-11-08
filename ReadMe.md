# 🏢 ReflectionSync — Floor Plan Management System 
---

## 🚀 Current Progress — Phase 1 (Authentication & Role Management)

### ✅ Completed Features

**User Management**
- User registration (`/signup`) with password hashing and welcome email.
- Secure login (`/login`) returning JWT-based access tokens.
- Password reset using OTP (`/forgot-password`, `/otp-verification`, `/reset-password`).
- Fetch currently logged-in user (`/me`).

**Role Management**
- Roles supported:  
  - `admin` — Can promote users and manage floor plan data.  
  - `user` — Can view and edit their own data, book seats, etc.
- Admin-only route to promote other users: `/admin/promote`.

**Security**
- Uses JWT tokens for authentication.
- Passwords hashed using **Argon2** (stronger and safer than bcrypt).
- Email notifications via Gmail SMTP (for signup and OTP verification).

**Database**
- PostgreSQL with SQLAlchemy ORM and Pydantic schemas.
- Auto-migration setup through SQLAlchemy metadata creation.

---

## ⚙️ Tech Stack

| Layer | Technology |
|--------|-------------|
| **Backend Framework** | FastAPI |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Auth** | JWT (via `python-jose`) |
| **Password Hashing** | Argon2 (`passlib[argon2]`) |
| **Email Service** | Gmail SMTP |

---

## 📦 Next Phase (Upcoming Features)

**Phase 2 — Floor Plan Management**

* Upload Floor Plan (Image/PDF + metadata).
* CRUD operations for Rooms and Seats.
* Assign seats to users.
* Visual Floor Plan Editor (React frontend).

**Phase 3 — Seat Booking & Analytics**

* Booking system with availability check.
* Usage analytics and heatmap visualization.

---

## 🧑‍💻 Developer

**Vishal Singh**
B.Tech (IT), IIIT Allahabad

---

## 🏁 Status

✅ **Completed:** Authentication & Role-based Access Control
🛠️ **Next:** Floor Plan Uploads and Room/Seat CRUD

```