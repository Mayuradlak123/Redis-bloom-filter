# Redis Bloom Filter Username Checker

A high-performance, real-time username availability checker built with Flask and Redis. This project implements a custom Bloom Filter using Redis bitsets, making it compatible even with older Redis versions that do not support the `RedisBloom` module.

## 🚀 Features
- **Instant Lookup**: Debounced client-side input triggers real-time availability checks.
- **Custom Bloom Filter**: Scalable manual implementation using Redis `SETBIT` and `GETBIT`.
- **Clean Architecture**: Backend organized into `api/routes` for endpoints and `api/services` for business logic.
- **Premium UI**: Modern glassmorphism design using Tailwind CSS.
- **Efficient**: Optimized for large datasets (up to 1 crore records) with a low false-positive rate.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Cache/Storage**: Redis
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Debounced Fetch API)
- **Hashing**: SHA-256 (via `hashlib`)

## 📂 Project Structure
```text
System Design/
├── api/
│   ├── routes/
│   │   └── auth.py          # API route definitions & seeding logic
│   └── services/
│       └── bloom_filter.py  # Manual Bloom Filter implementation
├── data/
│   └── users.json           # Initial seeding data (optional)
├── templates/
│   └── index.html           # Frontend UI
├── app.py                   # Flask entry point
└── README.md                # Project documentation
```

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.x
- Redis server running locally on port `6379`

### 2. Prepare Seeding Data
Create a `data/users.json` file (ignored by git) with the following structure:
```json
[
  {
    "username": "Dorthy71",
    "email": "user@example.com"
  },
  {
    "username": "MayurDev",
    "email": "mayur@example.com"
  }
]
```

### 3. Setup & Installation
```bash
pip install -r requirements.txt
cp .env.example .env
```

### 3. Run the Application
```bash
python app.py
```
The application will start on `http://127.0.0.1:5000`.

## 📡 API Reference

### Check Username Availability
- **URL**: `/api/check-username`
- **Method**: `GET`
- **URL Params**: `username=[string]`
- **Success Response**: 
  - `{"available": true, "username": "JohnDoe"}` (Username not in Bloom filter)
  - `{"available": false, "username": "Dorthy71"}` (Username potentially taken)

## 💡 How it Works
1. **Seeding**: On startup, the `api/routes/auth.py` script reads `data/users.json` and adds all existing usernames to the Redis Bloom filter.
2. **Checking**: When a user types in the UI, a debounced request is sent to the Flask API.
3. **Lookup**: The `BloomFilter` service runs the username through 7 different hash functions and checks the corresponding bits in Redis.
4. **Result**: If any bit is `0`, the username is **definitely available**. If all are `1`, the username is **likely taken**.
