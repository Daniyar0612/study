from datetime import date, timedelta

from sqlalchemy import delete

from app.core.security import hash_password
from app.database import SessionLocal
from app.models import Exam, Subject, User


def run_seed():
    db = SessionLocal()
    try:
        db.execute(delete(Exam))
        db.execute(delete(Subject))
        db.execute(delete(User))

        user = User(email="demo@studyflow.dev", password_hash=hash_password("password123"))
        db.add(user)
        db.flush()

        math = Subject(user_id=user.id, name="Mathematics")
        history = Subject(user_id=user.id, name="History")
        db.add_all([math, history])
        db.flush()

        db.add_all([
            Exam(user_id=user.id, subject_id=math.id, title="Calculus Midterm", exam_date=date.today() + timedelta(days=10), target_hours=20, priority=5),
            Exam(user_id=user.id, subject_id=history.id, title="Essay Defense", exam_date=date.today() + timedelta(days=7), target_hours=12, priority=3),
        ])
        db.commit()
        print("Seed complete: demo@studyflow.dev / password123")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
