# 📘 BookWise: Merchant Booking Platform (FastAPI + PostgreSQL)

A production-ready, backend-first booking system designed for merchant-based services (escape rooms, classes, etc).

---

## 🧱 Core Features

- Merchant → Service (Theme) → Slot → Booking flow
- Role-based access: Admins, Merchants, Users
- Slot availability & overbooking control
- Relational DB design with SQLAlchemy
- Clean architecture: Router ➜ Service ➜ CRUD ➜ Model
- JWT-based authentication (optional)
- Review system with FK enforcement

---

## 🧠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- Docker (optional)
- Redis / Celery (if implemented)

---

## 📐 Database Schema (ERD)

> ![ERD Image](link-to-your-image)  
> *(or embed dbdiagram code)*

- One User → may become a Merchant
- One Merchant → owns multiple Themes
- One Theme → has multiple Slots
- One Slot → has multiple Participants
- One Participant → optionally linked to User + one Review

---

## 🔌 API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/themes` | GET | List all themes |
| `/themes` | POST | Create a new theme |
| `/slots/:id/join` | POST | Book a slot |
| `/slots/:id/participants` | GET | List participants |
| ... | ... | ... |

📎 Full Postman Collection: [link]  
📎 Example curl commands: [link]

---

## 🔄 Typical Booking Workflow

```mermaid
graph TD
User -->|Login/Register| App
App -->|Browse Themes| /themes
User -->|Book Slot| /slots/:id/join
Merchant -->|See Participants| /slots/:id/participants
