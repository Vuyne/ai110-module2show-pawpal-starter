"""PawPal+ — class skeletons.

Generated from diagrams/uml.mmd. Stubs only: attributes and method
signatures are defined, but the scheduling logic is intentionally left
for you to implement. Each method raises NotImplementedError so tests
fail loudly until you fill them in.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single unit of pet care (a walk, a feeding, a med dose, ...)."""

    title: str
    duration_minutes: int
    priority: str = "medium"          # "low" | "medium" | "high"
    recurrence: str = "daily"         # "daily" | "weekly" | "once"
    start_time: str | None = None     # assigned by the Scheduler, e.g. "08:00"

    def priority_rank(self) -> int:
        """Return a sortable number so higher priority sorts first."""
        raise NotImplementedError


@dataclass
class Pet:
    """An animal that has care tasks."""

    name: str
    species: str = "dog"              # "dog" | "cat" | "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    """The person planning care for one or more pets."""

    name: str
    available_minutes: int = 120
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def set_preference(self, key: str, value) -> None:
        raise NotImplementedError


@dataclass
class Plan:
    """The result of scheduling: what got in, what got cut, and why."""

    scheduled: list[Task] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    total_minutes: int = 0
    reasoning: str = ""


class Scheduler:
    """Builds a daily plan from a pet's tasks within a time budget."""

    def __init__(self, available_minutes: int = 120, start_time: str = "08:00") -> None:
        self.available_minutes = available_minutes
        self.start_time = start_time

    def build_plan(self, pet: Pet) -> Plan:
        """Sort, fit, and time tasks into a Plan for the given pet."""
        raise NotImplementedError

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by scheduling preference (priority, then duration)."""
        raise NotImplementedError

    def fits(self, task: Task, remaining: int) -> bool:
        """Return True if the task fits in the remaining minutes."""
        raise NotImplementedError

    def explain(self, plan: Plan) -> str:
        """Return a human-readable explanation of why the plan looks as it does."""
        raise NotImplementedError
