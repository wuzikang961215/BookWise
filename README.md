# 📘 BookWise: Merchant Booking Platform (FastAPI + PostgreSQL)

**BookWise is an online booking and payment system for real-world services.**

A production-grade backend system for managing merchant-based services (escape rooms, studios, barbershops, etc) — with robust booking, payment, review, and role management.

> ✅ Designed to scale: tested with 170K+ users and 1.6M+ simulated bookings  
> 🔧 Tech stack: FastAPI · PostgreSQL · Redis · Celery · Docker  
> 🚀 Deployed on Fly.io — [Live API](https://bookwise.fly.dev/docs#/)

---

## 🧭 Why I built BookWise

In Australia, I observed that many merchants — such as escape rooms, massage shops, and barbers — still rely on phone calls, Excel sheets, or WeChat to manage bookings. This manual workflow leads to issues like:

- ❌ Overbooked time slots  
- ❌ Miscommunication between staff  
- ❌ Missed or untracked payments

**BookWise** was created to solve that. It automates the full booking workflow:

- ✅ Merchants create services and available time slots  
- ✅ Users browse, book, pay, and review  
- ✅ Admins manage everything centrally

---

## 👥 Who uses BookWise?

### 🧑 Users
- Browse merchants and filter by categories (KTV, massage, escape rooms, etc.)
- View services (themes) and book open time slots
- Register and log in to book, pay, cancel, and review

### 🧑‍💼 Merchants
- Use their account to create/manage themes and time slots
- View all bookings and payments per slot
- Access stats like most booked themes or top customers

### 👑 Admins
- Manage all merchants, users, bookings, payments, reviews, and system data

---

## 🛠️ Core Services & API Overview

### 🔐 Auth Service  
Handles user registration, login, and refresh token flow using JWT.

| Endpoint          | Method | Purpose                                 | Role    |
|-------------------|--------|-----------------------------------------|---------|
| `/auth/register`  | POST   | Register a new user                     | Public  |
| `/auth/login`     | POST   | Login and receive access + refresh JWT  | Public  |
| `/auth/refresh`   | POST   | Refresh access token using refresh JWT  | Requires refresh token |

---

### 👤 User Service  
Fetch user info, personal bookings, and admin-only user lookups.

| Endpoint               | Method | Purpose                                        | Role        |
|------------------------|--------|------------------------------------------------|-------------|
| `/users/me`            | GET    | Get current logged-in user's profile          | User |
| `/users/me/bookings`   | GET    | Get current user's booking history            | User    |
| `/users/`              | GET    | Get list of all users                         | Admin only   |
| `/users/{user_id}`     | GET    | Get any user by ID                            | Admin only   |

---

### 🏪 Merchant Service  
Allows users to become merchants and view merchant directories.

| Endpoint              | Method | Purpose                                           | Role         |
|-----------------------|--------|---------------------------------------------------|--------------|
| `/merchants`          | GET    | List all merchants, with optional category filter | Public       |
| `/merchants`          | POST   | Create merchant profile (user becomes merchant)   | User         |

---

### 🎭 Theme Service  
Merchants can manage their services (themes), such as escape room types or massage offerings.

| Endpoint                          | Method | Purpose                                   | Role      |
|-----------------------------------|--------|-------------------------------------------|-----------|
| `/merchants/{merchant_id}/themes`          | GET    | Get all themes under a merchant           | Public    |
| `/merchants/{merchant_id}/themes`          | POST   | Create a new theme under a merchant  | Merchant / Admin |

---

### ⏱️ Slot Service  
Merchants create and manage time slots under each theme.

| Endpoint                               | Method | Purpose                                    | Role      |
|----------------------------------------|--------|--------------------------------------------|-----------|
| `/themes/{theme_id}/slots`                   | GET    | List all slots under a theme               | Public    |
| `/themes/{theme_id}/slots`                   | POST   | Create a new slot under a theme            | Merchant / Admin  |
| `/slots/{theme_id}/availability`             | GET    | Check slot availability (capacity status)  | Public    |

---

### 📅 Booking Service  
Users book available slots, merchants can view confirmed bookings.

| Endpoint                           | Method | Purpose                                              | Role       |
|------------------------------------|--------|------------------------------------------------------|------------|
| `/slots/{slot_id}/book`                 | POST   | User books a slot and triggers payment intent        | User     |
| `/slots/{slot_id}/bookings`            | GET    | Merchant views confirmed bookings under the slot     | Merchant / Admin  |
| `/slots/{slot_id}/booking-count`       | GET    | View number of confirmed bookings + slot capacity    | Public     |


---

### 💳 Payment Service  
Handles payment records linked to bookings. Typically queried after booking is created.

| Endpoint                             | Method | Purpose                                                              | Role    |
|--------------------------------------|--------|----------------------------------------------------------------------|---------|
| `/bookings/{booking_id}/payment`     | GET    | Get payment info for a booking (user must own booking)              | User    |

---

### ✍️ Review Service  
Users can review themes they’ve experienced. One review per user per theme.

| Endpoint                             | Method | Purpose                                                                 | Role    |
|--------------------------------------|--------|-------------------------------------------------------------------------|---------|
| `/themes/{theme_id}/review`          | POST   | Submit a review (must have completed + paid booking for that theme)    | User    |
| `/themes/{theme_id}/reviews`         | GET    | Get all reviews for a theme                                            | Public  |

---

### 🧪 Stripe Webhook (Mock)

This is a mock webhook endpoint used to simulate Stripe’s payment confirmation flow during development/testing.

| Endpoint               | Method | Purpose                                          | Role     |
|------------------------|--------|--------------------------------------------------|----------|
| `/webhooks/stripe`     | POST   | Receive mock Stripe webhook payloads to simulate payment success | Internal (Mock) |

> ⚠️ This endpoint is for **internal development use only**. It does not perform signature verification and is not intended for production Stripe usage.


---

## 🔄 System Flow Diagrams

### 🔐 Refresh Token Flow

```mermaid
sequenceDiagram
  participant User
  participant BookWise API
  participant Database

  User->>BookWise API: POST /auth/login (email + password)
  BookWise API->>Database: Validate credentials
  BookWise API-->>User: Return Access Token + Refresh Token
  BookWise API->>Database: Store refresh token

  Note over User, BookWise API: (15 minutes later...)

  User->>BookWise API: POST /auth/refresh (with refresh token)
  BookWise API->>Database: Compare refresh token
  alt Valid and not expired
    BookWise API-->>User: Return new Access + Refresh Token
    BookWise API->>Database: Update refresh token
  else Invalid or expired
    BookWise API-->>User: 401 Unauthorized
  end
```

> ⏳ Access tokens expire every 15 minutes  
> ♻️ Refresh tokens are valid for 30 days and rotated with every use  
> 🗃️ Expired refresh tokens remain in the database and are ignored on validation

---


## ⚙️ Tech Stack

| Category       | Tools                                      |
|----------------|---------------------------------------------|
| Web API        | FastAPI, Pydantic                          |
| DB Layer       | PostgreSQL, SQLAlchemy, Alembic            |
| Auth           | JWT (access/refresh), bcrypt               |
| Async / Jobs   | Celery, Redis                              |
| Payments       | Stripe (intent + webhook + idempotency)    |
| DevOps         | Docker, Fly.io                             |
| Dev Tools      | Postman                    |

---

## 🗂️ Database Design (ERD)

> ![ERD Image](link-to-your-image-or-dbdiagram)

**Key Entities:**
- `User` → may become `Merchant`
- `Merchant` → owns `Themes` (services like escape rooms)
- `Theme` → has multiple `Slots`
- `Slot` → can be booked → `Booking` / `Participant`
- `Review` → linked to `(User, Theme)` pair

---

## 🔄 Booking Flow Diagram

```mermaid
graph TD
User -->|Login/Register| App
App -->|Browse Themes| /themes
User -->|Join Slot| /slots/:id/join
Merchant -->|View Participants| /slots/:id/participants
Merchant -->|Confirm Attendance| /attendance
User -->|Review Theme| /reviews
```

---

## 🔌 API Examples

| Endpoint                  | Method | Description             |
|---------------------------|--------|-------------------------|
| `/auth/register`          | POST   | User signup             |
| `/themes`                 | GET    | List all themes         |
| `/slots/:id/join`         | POST   | Book a slot             |
| `/slots/:id/participants` | GET    | List participants       |
| `/reviews`                | POST   | Submit theme review     |
| `/payments/create`        | POST   | Stripe intent           |

📎 [Postman Collection](#)  
📎 [cURL Examples](#)

---

## 🧠 Design Highlights

- Optimized SQL with index testing, JOIN patterns, and EXPLAIN ANALYZE
- Role-aware permission logic (admin vs merchant vs user routes)
- Strict data model: enforced FK constraints, 1–1 review per theme
- Modular codebase: fully separated concerns (router/service/crud)
- Async retry-safe payment handling via Celery

---

## 🚀 Deployment & Usage

- Deployed with Docker + Fly.io
- Uses Upstash Redis for async job backend
- Environment variables: `.env.example` included
- Live backend link: [https://bookwise.fly.dev](https://bookwise.fly.dev)

---

## 📸 Screenshots / Demo (optional)

> _[Insert screenshot or GIF of flow / schema visualizer / logs / etc]_

---

## 👥 Credits & Status

Created and maintained by Peter Wu.  
Currently backend-only — frontend collaboration welcome.
