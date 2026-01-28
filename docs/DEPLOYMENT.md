# Deployment Guide 🚀

## Prerequisites

- **Docker Desktop** (for local containerization)
- **Node.js 18+** & **Python 3.10+** (for local dev without Docker)
- **Render Account** (for production)
- **GitHub Account** (for CI/CD)

---

## 🏠 Local Development (Docker)

The easiest way to run the full stack locally.

1. **Clone the Repo**
   ```bash
   git clone https://github.com/Gbolahan43/chainquery-ai.git
   cd chainquery-ai
   ```

2. **Setup Environment**
   Copy `.env.example` to `backend/.env` and add your keys:
   ```bash
   cp backend/.env.example backend/.env
   ```
   *Required variables: `OPENAI_API_KEY` or `GROQ_API_KEY`.*

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```
   - Frontend: `http://localhost:5173`
   - Backend: `http://localhost:8000`
   - Database: `localhost:5432`

---

## ☁️ Production Deployment (Render)

We use **Render** for hosting (Backend + Frontend + DB).

### 1. Setup Postgres
1. Create a "New PostgreSQL" on Render.
2. Copy the `Internal Connection URL`.
3. Save it as `DATABASE_URL` in your Backend service environment variables.

### 2. Deploy Backend (Web Service)
1. **Build Command**: 
   ```bash
   pip install -r requirements.txt && alembic upgrade head
   ```
2. **Start Command**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```
3. **Environment Variables**:
   - `DATABASE_URL`: (From Postgres step)
   - `SECRET_KEY`: (Generate a secure random string)
   - `OPENAI_API_KEY` / `GROQ_API_KEY`
   - `PROJECT_NAME`: "ChainQuery AI"

### 3. Deploy Frontend (Static Site)
1. **Build Command**: `npm install && npm run build`
2. **Publish Directory**: `dist`
3. **Rewrite Rules**:
   - Source: `/*`
   - Destination: `/index.html`
   - Action: Rewrite
   *(This is crucial for React Router to work)*

### 4. CI/CD Auto-Deploy
Our GitHub Actions pipeline (`.github/workflows/deploy.yml`) is configured to notify you of deployments.
- Ensure "Auto-Deploy" is enabled in your Render settings for the Main branch.

---

## 🗄️ Database Migrations

Access database migrations via Alembic.

**Create a new migration:**
```bash
cd backend
alembic revision --autogenerate -m "Add new table"
```

**Apply migrations manually:**
```bash
alembic upgrade head
```

> **Note**: In production, the Build Command (`alembic upgrade head`) automatically applies migrations on every deploy.

---

## 🔍 Troubleshooting

### "Relationship ... expects a class or a mapper"
This usually happens if you have circular imports in your models. Check `app/models/sql.py`.

### "CORS Error" on Frontend
Ensure the Backend (`app/main.py`) CORSMiddleware allows the Frontend URL.
```python
allow_origins=[
    "http://localhost:5173",
    "https://your-frontend-app.onrender.com"
]
```

### Docker "Port already in use"
Stop any local instances of Postgres or other apps using port 5432/8000.
```bash
docker stop $(docker ps -aq)
```
