# System Design: Redis Bloom Filter & SSE Demo

A high-performance, real-time system demonstrating **Bloom Filters** for efficient membership testing and **Server-Sent Events (SSE)** for live data streaming. This project is built with Flask, Redis, and PostgreSQL, all orchestrated with Docker.

## 🚀 Features
- **Instant Username Check**: Fast-path validation using a Redis-backed Bloom Filter.
- **Multi-Layer Validation**: Fallback to PostgreSQL (Slow Path) to resolve Bloom Filter false positives.
- **Real-time Event Stream**: Live monitoring dashboard powered by Server-Sent Events (SSE).
- **Modern UI**: Fully responsive, glassmorphism design built with Tailwind CSS.
- **Cloud-Ready**: Fully dockerized with persistence for both Redis and PostgreSQL.

---

## 🛠️ Tech Stack
- **Backend**: Python (Flask)
- **Fast Path**: Redis (Bitsets for Bloom Filter)
- **Slow Path**: PostgreSQL (Source of Truth)
- **Streaming**: Server-Sent Events (SSE)
- **Infrastructure**: Docker & Docker Compose
- **Frontend**: Tailwind CSS & Vanilla JavaScript

---

## 📂 Project Structure
```text
System Design/
├── api/
│   ├── routes/
│   │   ├── auth.py          # Username check & seeding logic
│   │   └── events.py        # SSE stream generator
│   └── services/
│       ├── bloom_filter.py  # Manual Redis Bloom Filter implementation
│       └── database.py       # PostgreSQL service layer
├── data/
│   └── users.json           # Initial seeding data (Ignored by Git)
├── templates/
│   ├── index.html           # Bloom Filter UI
│   └── sse.html             # Real-time Events UI
├── app.py                   # Flask Application Entry
├── Dockerfile               # App Container Defintion
└── docker-compose.yml       # Infrastructure Orchestration
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Docker & Docker Compose

### 2. Prepare Seeding Data
Create a `data/users.json` file (ignored by git) to seed the system:
```json
[
  { "username": "Dorthy71", "email": "user@gmail.com" },
  { "username": "MayurDev", "email": "dev@example.com" }
]
```

### 3. Run with Docker (Recommended)
```bash
docker-compose up --build
```
- **App**: `http://localhost:5000`
- **Database UI (Adminer)**: `http://localhost:8080`

### 4. Local Setup (Alternative)
```bash
pip install -r requirements.txt
cp .env.example .env
# Ensure Redis and Postgres are running locally
python app.py
```

---

## 💡 How it Works: Bloom Filter

A Bloom Filter is a space-efficient probabilistic data structure.

### The Workflow
1.  **Seeding**: On startup, usernames are hashed and their bits are set in a Redis bitset.
2.  **Fast Path (Check)**: When checking a name, the system hashes it 7 times. If any corresponding bit in Redis is `0`, the name is **available**.
3.  **Slow Path (Lookup)**: If all 7 bits are `1`, it might be a false positive. The system then queries PostgreSQL to be 100% sure.

### Hashing Mechanism
We use SHA-256 with 7 different salts to generate unique positions in a 10-million-bit array.

---

## 📡 Server-Sent Events (SSE)
The SSE demo showcases how the server can push updates to the client without the client having to poll.
- **Endpoint**: `/stream` returns a `text/event-stream`.
- **UI**: A reactive dashboard that displays live "system metrics" as they arrive.

---

## 📡 API Reference

### Check Username Availability
- **URL**: `/api/check-username`
- **Method**: `GET`
- **Query Params**: `username=[string]`
- **Response**: 
  - `{"available": true, "username": "..."}`
  - `{"available": false, "username": "...", "source": "PostgreSQL"}`
