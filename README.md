# 🔗 FastAPI URL Shortener

A simple URL shortener built using **FastAPI**, **SQLite**, and **SQLAlchemy**.

## 🚀 Features
- Shortens long URLs
- Redirects users from short URL to original link
- Validates URL inputs
- Async database support using SQLAlchemy & SQLite

## 📦 Tech Stack
- FastAPI
- SQLAlchemy (Async)
- SQLite
- Uvicorn

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/your-username/fastapi-url-shortener.git
cd fastapi-url-shortener

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # for Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload



