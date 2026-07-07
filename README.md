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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Sorts tasks by their preferred `time_of_day` value so the day starts in a natural order. |
| Filtering behavior | `Scheduler.filter_tasks()` | Filters tasks by completion status and pet name so pending tasks for a specific pet are easy to view. |
| Conflict detection logic | `Scheduler.check_conflicts()` | Detects overlapping scheduled tasks and returns a lightweight warning message instead of crashing. |
| Recurring task logic | `Task.mark_complete()` | When a daily or weekly task is completed, the task records the next due date using `timedelta`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
