from datetime import date, time

from pawpal_system import Scheduler, Task


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler(owner=None)  # type: ignore[arg-type]
    morning = Task(title="Morning walk", duration_minutes=20)
    morning.time_of_day = "09:30"
    evening = Task(title="Evening feed", duration_minutes=10)
    evening.time_of_day = "18:00"
    noon = Task(title="Lunch check", duration_minutes=15)
    noon.time_of_day = "12:00"

    ordered = scheduler.sort_by_time([evening, morning, noon])

    assert [task.title for task in ordered] == ["Morning walk", "Lunch check", "Evening feed"]


def test_daily_task_completion_creates_next_occurrence_for_following_day():
    task = Task(title="Water bowl", duration_minutes=5, recurrence="daily")
    task.due_date = date(2026, 7, 6)

    next_task = task.mark_complete()

    assert task.status == "complete"
    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 7)
    assert next_task.status == "pending"


def test_check_conflicts_flags_duplicate_times():
    scheduler = Scheduler(owner=None)  # type: ignore[arg-type]
    first = Task(title="Feed", duration_minutes=15)
    first.start_time = time(8, 30)
    second = Task(title="Walk", duration_minutes=20)
    second.start_time = time(8, 30)

    warnings = scheduler.check_conflicts([first, second])

    assert len(warnings) == 1
    assert "overlaps" in warnings[0].lower()
