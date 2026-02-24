# StudyFlow MVP

StudyFlow is a minimal study planning app where users register, add subjects and exams, generate a bounded daily study plan, mark progress, and view dashboard stats.

## Tech Stack
- Backend: FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, JWT auth, passlib/bcrypt
- Frontend: React + Vite, React Router, Axios
- Local infra: docker-compose for PostgreSQL

## Monorepo Structure
- `backend/` FastAPI API server
- `frontend/` React app

## 1) Start PostgreSQL
```bash
docker compose up -d db
```

## 2) Configure environment

Backend:
```bash
cd backend
cp .env.example .env
```

Frontend:
```bash
cd ../frontend
cp .env.example .env
```

## 3) Run backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000`.

Optional seed:
```bash
python seed.py
```
Demo user: `demo@studyflow.dev / password123`

## 4) Run frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## MVP Flow
1. Register or login.
2. Add subjects.
3. Add exams with exam date, target hours, and priority.
4. Open Plan page and click **Generate Plan**.
5. Mark plan items done/undone.
6. View Dashboard for weekly totals and nearest exam.

## API Endpoints
- Auth: `POST /auth/register`, `POST /auth/login`
- Subjects: `GET/POST /subjects`, `PUT/DELETE /subjects/{id}`
- Exams: `GET/POST /exams`, `PUT/DELETE /exams/{id}`
- Plan: `POST /plan/generate`, `GET /plan?date=YYYY-MM-DD`, `GET /plan/week?start=YYYY-MM-DD`, `PATCH /plan/{id}`
- Dashboard: `GET /dashboard/stats?week_start=YYYY-MM-DD`

## Notes / assumptions
- Plan generation removes future (`date >= today`) items before regenerating.
- Hours are rounded to 0.25h after daily scaling with max 6h/day cap.
- All resources are user-scoped by JWT identity.
- Timestamps in user model are stored in UTC.
