from collections import defaultdict
from datetime import date, timedelta

from app.models.exam import Exam

PRIORITY_MULTIPLIER = {1: 0.8, 2: 0.9, 3: 1.0, 4: 1.15, 5: 1.3}
MAX_HOURS_PER_DAY = 6.0


def round_quarter(value: float) -> float:
    return round(value * 4) / 4


def generate_exam_allocations(exams: list[Exam], today: date) -> dict[tuple[str, date], float]:
    daily_entries = defaultdict(list)

    for exam in exams:
        days_left = (exam.exam_date - today).days + 1
        if days_left < 1:
            continue

        base_daily = exam.target_hours / days_left
        adjusted = base_daily * PRIORITY_MULTIPLIER[exam.priority]

        for offset in range(days_left):
            current_date = today + timedelta(days=offset)
            daily_entries[current_date].append((str(exam.id), adjusted))

    output: dict[tuple[str, date], float] = {}
    for dt, values in daily_entries.items():
        total = sum(hour for _, hour in values)
        scale = 1.0 if total <= MAX_HOURS_PER_DAY else MAX_HOURS_PER_DAY / total

        for exam_id, hour in values:
            output[(exam_id, dt)] = round_quarter(hour * scale)

    return output
