# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
============================================
  Today's Schedule — Wednesday
  Owner: Jordan  |  Budget: 90 min
============================================

Biscuit (dog)
--------------------------------------------
  08:00  Feeding             10 min  [high]
  08:10  Morning walk        30 min  [high]
  08:40  Fetch / play        20 min  [medium]
  Total: 60 min
  Skipped (no time / conflict): Bath

Mochi (cat)
--------------------------------------------
  08:00  Feeding             10 min  [high]
  08:10  Litter cleaning     15 min  [medium]
  08:25  Laser play          15 min  [low]
  Total: 40 min

============================================
```

## 🧪 Testing PawPal+

Run the full automated test suite with:

```bash
python -m pytest
```

These tests cover the core scheduling behaviors in the system, including task completion, recurrence, sorting by time, filtering by pet/status, and conflict detection for overlapping tasks.

Successful test run output:

```text
============================= test session starts ==============================
platform win32 -- Python 3.13.3, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\vykha\Desktop\Python\CodePath\ai110-module2show-pawpal-starter
plugins: anyio-4.10.0, typeguard-4.4.2
collected 10 items

tests\test_pawpal.py ...                                                 [ 30%]
tests\test_pawpal_system.py .......                                      [100%]

============================== 10 passed in 0.03s ==============================
```

Confidence Level: ★★★★★

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Sorts tasks by their preferred `time_of_day` value so the day starts in a natural order. |
| Filtering behavior | `Scheduler.filter_tasks()` | Filters tasks by completion status and pet name so pending tasks for a specific pet are easy to view. |
| Conflict detection logic | `Scheduler.check_conflicts()` | Detects overlapping scheduled tasks and returns a lightweight warning message instead of crashing. |
| Recurring task logic | `Task.mark_complete()` | When a daily or weekly task is completed, the task records the next due date using `timedelta`. |

## 🎬 Demo Walkthrough

PawPal+ combines a simple Streamlit interface with a scheduler backend that helps a pet owner organize care tasks for the day.

### Main UI features

- Add and manage pets for the owner.
- Add tasks with a title, duration, priority, and optional preferred time.
- View pending tasks in a cleaned-up, table-style layout.
- Generate a schedule view that shows sorted tasks and any conflict warnings.

### Example workflow

1. Open the app and enter an owner name.
2. Add a pet such as Mochi or Biscuit.
3. Add one or more tasks for that pet, for example a morning feed or evening walk.
4. Click Generate schedule to view the pending tasks in time order.
5. If two tasks overlap, the scheduler reports a warning so the owner can resolve the conflict.

### Scheduler behaviors shown in the demo

- Sorting by time using `Scheduler.sort_by_time()`.
- Filtering to pending tasks for the selected pet using `Scheduler.filter_tasks()`.
- Conflict warnings for overlapping tasks using `Scheduler.check_conflicts()`.
- Recurring task progression through `Task.mark_complete()` for daily and weekly tasks.

### Sample CLI output

```text
============================================
  Today's Schedule — Wednesday
  Owner: Jordan  |  Budget: 90 min
============================================

Biscuit (dog)
--------------------------------------------
Sorted by time:
  08:00  Morning feed [high]
  14:00  Bath [low]
  18:30  Evening walk [medium]
  Total visible tasks: 3

Mochi (cat)
--------------------------------------------
Sorted by time:
  07:30  Feeding [high]
  12:00  Litter cleaning [medium]
  17:00  Laser play [low]
  Total visible tasks: 3
============================================
```
