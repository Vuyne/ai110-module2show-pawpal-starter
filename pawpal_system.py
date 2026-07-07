"""PawPal+ — core implementation.

Data model (Owner, Pet, Task) plus the scheduling logic (Scheduler).
See diagrams/uml.mmd for the class diagram this mirrors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import IntEnum


class Priority(IntEnum):
    """Task priority. IntEnum so HIGH > MEDIUM > LOW sorts for free."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


def _parse_time(value: str | time) -> time:
    """Accept a 'HH:MM' string or a time and return a time."""
    if isinstance(value, time):
        return value
    hours, minutes = value.split(":")
    return time(int(hours), int(minutes))


@dataclass
class Task:
    """A single unit of pet care (a walk, a feeding, a med dose, ...)."""

    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    recurrence: str = "daily"          # "daily" | "weekly" | "once"
    weekday: int | None = None         # 0=Mon..6=Sun; used when recurrence == "weekly"
    start_time: time | None = None     # assigned by the Scheduler once placed
    status: str = "pending"
    time_of_day: str | None = None     # preferred time for display/sorting, e.g. "08:30"
    pet_name: str | None = None        # optional pet label for filtering
    due_date: date | None = None       # current occurrence date for recurring tasks
    next_due_date: date | None = None  # next occurrence date after completion

    def end_time(self) -> time:
        """Return start_time + duration_minutes (requires start_time set)."""
        if self.start_time is None:
            raise ValueError("Task has no start_time yet; schedule it first.")
        anchor = datetime.combine(date.min, self.start_time)
        return (anchor + timedelta(minutes=self.duration_minutes)).time()

    def priority_rank(self) -> int:
        """Return a sortable number so higher priority sorts first."""
        return int(self.priority)

    def runs_on(self, weekday: int) -> bool:
        """Return True if this task should appear in the plan for `weekday`."""
        if self.recurrence == "weekly":
            return self.weekday == weekday
        # "daily" and "once" are both eligible for any given day's plan.
        return True

    def mark_complete(self) -> Task | None:
        """Mark the task as complete and return a new pending task for the next occurrence if recurring."""
        self.status = "complete"
        if self.recurrence == "daily" and self.due_date is not None:
            next_due_date = self.due_date + timedelta(days=1)
            self.next_due_date = next_due_date
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                recurrence=self.recurrence,
                weekday=self.weekday,
                status="pending",
                time_of_day=self.time_of_day,
                pet_name=self.pet_name,
                due_date=next_due_date,
            )
        if self.recurrence == "weekly" and self.due_date is not None:
            next_due_date = self.due_date + timedelta(days=7)
            self.next_due_date = next_due_date
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                recurrence=self.recurrence,
                weekday=self.weekday,
                status="pending",
                time_of_day=self.time_of_day,
                pet_name=self.pet_name,
                due_date=next_due_date,
            )
        return None


@dataclass
class Pet:
    """An animal that has care tasks."""

    name: str
    species: str = "dog"               # "dog" | "cat" | "other"
    tasks: list[Task] = field(default_factory=list)

    @property
    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's care list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's care list."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """The person planning care. Single source of truth for constraints."""

    name: str
    available_minutes: int = 120
    day_start: str = "08:00"           # when the day's plan begins
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's profile."""
        self.pets.append(pet)

    def set_preference(self, key: str, value) -> None:
        """Store a preference for this owner."""
        self.preferences[key] = value


@dataclass
class Plan:
    """The result of scheduling: what got in, what got cut, and why."""

    scheduled: list[Task] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    total_minutes: int = 0
    reasoning: str = ""


class Scheduler:
    """Builds a daily plan from a pet's tasks within the owner's constraints."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner context."""
        # Constraints come from the owner, so there is one source of truth.
        self.owner = owner

    def build_plan(self, pet: Pet, weekday: int) -> Plan:
        """Filter to today's tasks, sort, fit, assign times, and return a Plan."""
        todays_tasks = [t for t in pet.tasks if t.runs_on(weekday)]
        ordered = self.sort_tasks(todays_tasks)

        plan = Plan()
        remaining = self.owner.available_minutes
        cursor = datetime.combine(date.min, _parse_time(self.owner.day_start))

        for task in ordered:
            task.start_time = cursor.time()
            if self.fits(task, remaining) and not self.has_conflict(task, plan.scheduled):
                plan.scheduled.append(task)
                plan.total_minutes += task.duration_minutes
                remaining -= task.duration_minutes
                cursor += timedelta(minutes=task.duration_minutes)
            else:
                task.start_time = None  # not placed; clear the tentative time
                plan.skipped.append(task)

        plan.reasoning = self.explain(plan)
        return plan

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order by priority (desc), then shorter duration as a tie-breaker."""
        return sorted(
            tasks,
            key=lambda t: (-t.priority_rank(), t.duration_minutes),
        )

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by preferred time using a time-based lambda key."""
        return sorted(tasks, key=lambda task: _parse_time(task.time_of_day or "23:59"))

    def filter_tasks(
        self,
        tasks: list[Task],
        status: str | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks that match the provided status and pet-name filters."""
        filtered = list(tasks)
        if status is not None:
            filtered = [task for task in filtered if task.status.lower() == status.lower()]
        if pet_name is not None:
            filtered = [
                task
                for task in filtered
                if (task.pet_name or "").lower() == pet_name.lower()
            ]
        return filtered

    def fits(self, task: Task, remaining: int) -> bool:
        """Return True if the task fits in the remaining minute budget."""
        return task.duration_minutes <= remaining

    def has_conflict(self, task: Task, scheduled: list[Task]) -> bool:
        """Return True if task's time range overlaps any already-scheduled task."""
        for other in scheduled:
            if task.start_time < other.end_time() and other.start_time < task.end_time():
                return True
        return False

    def check_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return lightweight warning messages for overlapping tasks."""
        warnings: list[str] = []
        for index, task in enumerate(tasks):
            for other in tasks[index + 1 :]:
                if task.start_time is None or other.start_time is None:
                    continue
                if task.start_time < other.end_time() and other.start_time < task.end_time():
                    warnings.append(
                        f"Warning: '{task.title}' overlaps with '{other.title}' at {task.start_time.strftime('%H:%M')}."
                    )
        return warnings

    def explain(self, plan: Plan) -> str:
        """Return a human-readable explanation of why the plan looks as it does."""
        lines = [
            f"Scheduled {len(plan.scheduled)} task(s) using "
            f"{plan.total_minutes} of {self.owner.available_minutes} available minutes."
        ]
        for task in plan.scheduled:
            lines.append(
                f"  {task.start_time.strftime('%H:%M')} — {task.title} "
                f"({task.duration_minutes} min) [priority: {task.priority.name.lower()}]"
            )
        if plan.skipped:
            lines.append(
                f"Skipped {len(plan.skipped)} task(s) that did not fit or conflicted: "
                + ", ".join(t.title for t in plan.skipped)
                + "."
            )
        return "\n".join(lines)
