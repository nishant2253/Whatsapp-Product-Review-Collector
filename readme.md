# WhatsApp Product Review Collector

A full-stack application where users submit product reviews via WhatsApp, and an admin/frontend dashboard displays all collected reviews.

## 🚀 Purpose of the Project

Retail and e-commerce companies often collect user product reviews through web forms, but users hesitate to fill long forms. WhatsApp is a familiar platform for everyone, which makes the review submission frictionless.

This project demonstrates how to build a:

- WhatsApp-based conversational review collector
- FastAPI backend that receives and processes messages
- PostgreSQL database to store reviews
- React frontend that displays all reviews in a clean dashboard

This project showcases skills in Twilio integrations, Webhooks, FastAPI, asynchronous programming, SQLAlchemy ORM, PostgreSQL, and React development.

## 🎥 Demo Video

[![Watch Demo](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge&logo=youtube)](https://youtu.be/Z1Lu0AqSrzE)

## 🧠 What This Project Does

✔️ Users send a WhatsApp message  
✔️ Bot collects:

- Product name
- User name
- Review text

✔️ Backend stores the review into Postgres  
✔️ React frontend fetches `/api/reviews` and displays them

## 🏗️ Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Async SQLAlchemy
- asyncpg (PostgreSQL driver)
- Twilio WhatsApp Sandbox
- ngrok (local tunneling)
- Pydantic
- python-multipart

### Database

- PostgreSQL
- SQLAlchemy ORM models

### Frontend

- React (Create React App)
- Fetch API

## 🔄 How the System Works (Architecture)

```
WhatsApp User
      ↓
Twilio WhatsApp Sandbox
      ↓ (HTTP POST)
ngrok Tunnel
      ↓
FastAPI Webhook (/webhook/twilio)
      ↓
Conversation Logic
      ↓
PostgreSQL (store review)
      ↓
Return TwiML Response
      ↓
Twilio sends reply to WhatsApp user

React Frontend → GET /api/reviews → Display List
```

## 💬 Conversation Flow Example

**User → Bot**  
`Hi`

**Bot →**  
`Which product is this review for?`

**User →**  
`iPhone 15`

**Bot →**  
`What's your name?`

**User →**  
`Aditi`

**Bot →**  
`Please send your review for iPhone 15.`

**User →**  
`Amazing battery life, very satisfied!`

**Bot (final) →**  
`Thanks Aditi — your review for iPhone 15 has been recorded.`

## 📦 Project Structure

```
backend/
│── app/
│   ├── main.py
│   ├── webhook.py
│   ├── conversation.py
│   ├── crud.py
│   ├── db.py
│   ├── models.py
│   └── config.py
│── requirements.txt
│── .env
│── README.md

frontend/
│── src/
│   ├── api/reviews.js
│   ├── components/ReviewsTable.js
│   └── App.js
```

## 🛠️ Backend Code Explanation (Important Files)

### 1️⃣ webhook.py — Main WhatsApp Webhook

- Twilio sends WhatsApp message → We handle POST request
- Extract `From` + `Body` fields
- Pass text to `conversation.handle_inbound_message`
- Return TwiML reply

**Purpose:** Entry point of WhatsApp communication.

### 2️⃣ conversation.py — Conversation State Machine

Handles all states:

- `ask_product`
- `ask_name`
- `ask_review`
- Finish → store review → delete conversation state

Stores partial progress until review is complete.

**Purpose:** Control dialogue flow.

### 3️⃣ models.py — Database Schema

Two tables:

**Review**

| Column         | Type      | Description            |
| -------------- | --------- | ---------------------- |
| id             | int       | Auto primary key       |
| contact_number | text      | User's WhatsApp number |
| user_name      | text      | Name                   |
| product_name   | text      | Product                |
| product_review | text      | Review                 |
| created_at     | timestamp | Auto timestamp         |

**ConversationState**  
Tracks where the user is in the dialog.

**Purpose:** DB structure for message state + review storage.

### 4️⃣ crud.py — Database Operations

Contains:

- `create_review`
- `get_all_reviews`
- `get_conversation`
- `upsert_conversation`
- `delete_conversation`

**Purpose:** Clean DB access separation from routes.

### 5️⃣ reviews.py — Public API

Defines:

- `GET /api/reviews`

Returns list of reviews for React frontend.

**Purpose:** Expose review data.

### 6️⃣ main.py — App Initialization

- Creates FastAPI app
- Includes routers
- Adds CORS for frontend
- Creates tables on startup

**Purpose:** Backend entry point.

## ⚙️ How to Run the Backend Locally

### 1. Clone the repo

```bash
git clone <your_repo_url>
cd backend
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL

Run Postgres locally:

```bash
sudo service postgresql start
```

Create DB:

```bash
psql -U postgres -c "CREATE DATABASE reviews_db;"
```

### 5. Create .env file

## 🔧 Environment Variables (`.env` Setup)

Before running the backend, you must create a `.env` file inside the `backend/` folder.

Use the following example template:

```bash
# ================================
# PostgreSQL Database Configuration
# ================================
# Format: postgresql+asyncpg://<username>:<password>@<host>:<port>/<database>
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/reviews_db

# ================================
# Twilio WhatsApp Sandbox Credentials
# ================================
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+1415XXXXXXX

# ================================
# Application Settings
# ================================
APP_ENV=development
```

**✔️ Steps to Configure:**

1. Copy `.env.example` → `.env`
2. Replace:
   - `yourpassword` with your PostgreSQL password
   - Twilio values with your actual credentials
   - Sandbox WhatsApp number (starts with `whatsapp:+1415...`)
3. Save the file and restart the backend server

### 6. Run Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Start ngrok

```bash
ngrok http 8000
```

Copy HTTPS URL → put in Twilio Console:

```
https://your-ngrok-url/webhook/twilio
```

## 🌐 API Routes

### GET /api/reviews

Returns JSON list of reviews:

```json
[
  {
    "id": 1,
    "contact_number": "+1415...",
    "user_name": "Aditi",
    "product_name": "iPhone 15",
    "product_review": "Amazing battery life",
    "created_at": "2025-11-20T12:34:56Z"
  }
]
```

## 🎨 Frontend Setup

### 1. Create React Project

```bash
npx create-react-app frontend
cd frontend
npm start
```

### 2. Install Dependencies

No additional libraries needed.

### 3. Fetch Reviews

**src/api/reviews.js**

```javascript
export async function fetchReviews() {
  const res = await fetch("http://localhost:8000/api/reviews");
  return res.json();
}
```

### 4. Display Table

**src/components/ReviewsTable.js**  
(Shows User Name, Product, Review, Timestamp)

## 🧪 End-to-End Testing

1. Send `Hi` to WhatsApp sandbox number
2. Complete review conversation
3. Visit React UI
4. Verify new review appears

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👤 Author

Nishant Gupta

---

**Made with using FastAPI, React, and Twilio**
