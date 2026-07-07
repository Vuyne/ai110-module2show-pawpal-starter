from datetime import date, time, timedelta

from pawpal_system import Pet, Scheduler, Task


def test_mark_complete_updates_task_status():
    task = Task(title="Morning walk", duration_minutes=20)

    assert task.status == "pending"

    task.mark_complete()

    assert task.status == "complete"


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi")
    initial_count = pet.task_count

    pet.add_task(Task(title="Feeding", duration_minutes=10))

    assert pet.task_count == initial_count + 1


def test_sort_by_time_orders_tasks_by_time_value():
    scheduler = Scheduler(owner=None)  # type: ignore[arg-type]
    morning = Task(title="Morning walk", duration_minutes=20)
    morning.time_of_day = "09:30"
    evening = Task(title="Evening feed", duration_minutes=10)
    evening.time_of_day = "18:00"
    noon = Task(title="Lunch check", duration_minutes=15)
    noon.time_of_day = "12:00"

    ordered = scheduler.sort_by_time([evening, morning, noon])

    assert [task.title for task in ordered] == ["Morning walk", "Lunch check", "Evening feed"]


def test_filter_tasks_by_status_and_pet_name():
    scheduler = Scheduler(owner=None)  # type: ignore[arg-type]
    pending_mochi = Task(title="Feed", duration_minutes=10)
    pending_mochi.pet_name = "Mochi"
    complete_mochi = Task(title="Play", duration_minutes=15)
    complete_mochi.status = "complete"
    complete_mochi.pet_name = "Mochi"
    pending_biscuit = Task(title="Walk", duration_minutes=20)
    pending_biscuit.pet_name = "Biscuit"

    filtered = scheduler.filter_tasks(
        [pending_mochi, complete_mochi, pending_biscuit],
        status="pending",
        pet_name="Mochi",
    )

    assert filtered == [pending_mochi]


def test_daily_task_completion_creates_next_occurrence():
    task = Task(title="Water bowl", duration_minutes=5, recurrence="daily")
    task.due_date = date(2026, 7, 6)

    task.mark_complete()

    assert task.status == "complete"
    assert task.next_due_date == date(2026, 7, 7)


def test_weekly_task_completion_creates_next_occurrence():
    task = Task(title="Grooming", duration_minutes=30, recurrence="weekly", weekday=0)
    task.due_date = date(2026, 7, 6)

    task.mark_complete()

    assert task.status == "complete"
    assert task.next_due_date == date(2026, 7, 13)


def test_check_conflicts_returns_warning_for_overlapping_tasks():
    scheduler = Scheduler(owner=None)  # type: ignore[arg-type]
    first = Task(title="Feed", duration_minutes=15)
    first.start_time = time(8, 30)
    second = Task(title="Walk", duration_minutes=20)
    second.start_time = time(8, 30)

    warnings = scheduler.check_conflicts([first, second])

    assert len(warnings) == 1
    assert "Warning:" in warnings[0]
