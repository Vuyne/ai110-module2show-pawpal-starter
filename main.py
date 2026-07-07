"""Temporary testing ground for PawPal+.

Builds an owner with two pets and some tasks, then prints today's
schedule for each pet to the terminal. Run with: python main.py
"""

from datetime import time

from pawpal_system import Owner, Pet, Task, Priority, Scheduler

# 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
TODAY = 2  # Wednesday
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                 "Saturday", "Sunday"]


def build_data() -> Owner:
    """Create an owner with two pets and a handful of care tasks."""
    owner = Owner(name="Jordan", available_minutes=90, day_start="08:00")

    biscuit = Pet(name="Biscuit", species="dog")
    biscuit.add_task(Task("Evening walk", 20, Priority.MEDIUM, time_of_day="18:30", pet_name="Biscuit"))
    biscuit.add_task(Task("Morning feed", 10, Priority.HIGH, time_of_day="08:00", pet_name="Biscuit"))
    bath = Task("Bath", 45, Priority.LOW, recurrence="weekly", weekday=2, time_of_day="14:00", pet_name="Biscuit")
    biscuit.add_task(bath)
    play = Task("Fetch / play", 20, Priority.MEDIUM, time_of_day="16:00", pet_name="Biscuit")
    play.mark_complete()
    biscuit.add_task(play)

    mochi = Pet(name="Mochi", species="cat")
    mochi.add_task(Task("Feeding", 10, Priority.HIGH, time_of_day="07:30", pet_name="Mochi"))
    mochi.add_task(Task("Litter cleaning", 15, Priority.MEDIUM, time_of_day="12:00", pet_name="Mochi"))
    mochi.add_task(Task("Laser play", 15, Priority.LOW, time_of_day="17:00", pet_name="Mochi"))

    overlap_a = Task("Overlap A", 10, Priority.HIGH, time_of_day="08:30", pet_name="Mochi")
    overlap_a.start_time = time(8, 30)
    overlap_b = Task("Overlap B", 15, Priority.MEDIUM, time_of_day="08:30", pet_name="Biscuit")
    overlap_b.start_time = time(8, 30)
    owner.add_pet(Pet(name="Conflicted", species="dog"))

    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    return owner


def print_schedule(owner: Owner, weekday: int) -> None:
    """Print a readable 'Today's Schedule' for every pet the owner has."""
    scheduler = Scheduler(owner)
    day_name = WEEKDAY_NAMES[weekday]

    print("=" * 44)
    print(f"  Today's Schedule — {day_name}")
    print(f"  Owner: {owner.name}  |  Budget: {owner.available_minutes} min")
    print("=" * 44)

    overlap_tasks = [
        Task("Overlap A", 10, Priority.HIGH, time_of_day="08:30", pet_name="Mochi"),
        Task("Overlap B", 15, Priority.MEDIUM, time_of_day="08:30", pet_name="Biscuit"),
    ]
    overlap_tasks[0].start_time = time(8, 30)
    overlap_tasks[1].start_time = time(8, 30)

    for warning in scheduler.check_conflicts(overlap_tasks):
        print(warning)

    for pet in owner.pets:
        pet_tasks = [task for task in pet.tasks if task.runs_on(weekday)]
        sorted_tasks = scheduler.sort_by_time(pet_tasks)
        pending_tasks = scheduler.filter_tasks(sorted_tasks, status="pending", pet_name=pet.name)

        print(f"\n{pet.name} ({pet.species})")
        print("-" * 44)
        print("Sorted by time:")
        for task in pending_tasks:
            print(f"  {task.time_of_day or 'TBD'}  {task.title} [{task.priority.name.lower()}]")

        if not pending_tasks:
            print("  (nothing pending)")

        print(f"  Total visible tasks: {len(pending_tasks)}")

    print("\n" + "=" * 44)


if __name__ == "__main__":
    print_schedule(build_data(), TODAY)
