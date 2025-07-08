# 📘 BookWise: Merchant Booking Platform (FastAPI + PostgreSQL)

**BookWise is an online booking and payment system for real-world services like escape rooms, massage, or barbers.**

A production-grade backend system for managing merchant-based services (escape rooms, studios, barbershops, etc) — with robust booking, payment, review, and role management.

> ✅ Designed to scale: tested with 170K+ users and 1.6M+ simulated bookings  
> 🔧 Tech stack: FastAPI · PostgreSQL · Redis · Celery · Stripe · Docker  
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
- Access (future) stats like most booked themes or top customers

### 👑 Admins
- Manage all merchants, users, bookings, payments, reviews, and system data

## 🌟 Key Features

- 🧾 Booking flow: Merchant → Service (Theme) → Slot → Booking
- 🔐 Role-based access: Admin · Merchant · User
- 📅 Slot availability enforcement + overbooking prevention
- 💬 Review system: one-review-per-theme per user
- 💳 Stripe integration (idempotency + webhook)
- 🚦 JWT auth + refresh token
- 📦 Async background jobs via Celery (e.g. payment retry)
- 🧱 Modular clean architecture (Router ➝ Service ➝ CRUD ➝ Model)

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
