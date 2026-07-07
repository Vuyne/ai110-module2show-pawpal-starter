# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My initial UML design consisted of four main classes: Owner, Pet, Task, and Scheduler.

Owner was responsible for storing the owner's information, preferences, available time, and list of pets.
Pet represented an individual pet and managed its associated care tasks.
Task stored information about each care activity, including its title, duration, priority, recurrence, and preferred start time.
Scheduler handled the scheduling logic by sorting tasks based on priority and fitting them into the owner's available time.

The goal of the initial design was to separate the data model (Owner, Pet, and Task) from the scheduling logic (Scheduler), making the system easier to maintain and extend.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes. During implementation, I found that having the Scheduler return only a list of scheduled tasks made it difficult to store additional information, such as skipped tasks and the reasoning behind scheduling decisions.

To improve the design, I introduced a separate Plan class. Instead of returning a simple list, the Scheduler now returns a Plan object containing the scheduled tasks, skipped tasks, total scheduled time, and an explanation of the scheduling decisions.

This change made the code more organized by separating the scheduling algorithm from its output. It also made it easier to present clear results and explanations to the user.

After looking over my design again, I noticed a few problems and fixed them:

- **Storing the time budget in one place.** At first both the Owner and the Scheduler kept their own copy of the available time, so the two could easily disagree. I changed it so the Scheduler gets the Owner and reads the time, start of day, and preferences from there. Now there is only one place that holds this information.
- **Using an enum for priority.** Priority used to be a plain text value like "low" or "high", which was easy to misspell and hard to sort. I switched to a `Priority` enum where HIGH is greater than MEDIUM is greater than LOW, so tasks sort correctly and you cannot enter an invalid value.
- **Handling real times and overlaps.** Start times were just text, so I could not do math with them. I switched to real time values, added a way to get each task's end time, and added a check that spots when two tasks overlap. This means the scheduler can catch tasks that clash, not just tasks that run out of time.
- **Making recurring tasks work.** Tasks had a recurrence value that was never actually used. I added a day-of-week field and a check for whether a task runs on a given day, so weekly tasks only show up on the right day.

Together these changes made the classes work together more cleanly and made the scheduler easier to test.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the scheduler currently checks for simple overlaps using start and end times, but it does not yet reason about more complex scheduling patterns such as flexible task placement or partial overlap handling. In practice, this means a task is treated as conflicting if it overlaps even slightly, which can cause a task to be skipped even when a small adjustment would have worked. That tradeoff is reasonable for this starter version because it keeps the conflict logic lightweight, predictable, and easy to explain to a pet owner without adding more complicated scheduling rules.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
