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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

============================================================
🐾 PawPal+ - Daily Pet Care Scheduler
============================================================

Owner: Alex
Available: 07:00 - 23:00
Total available hours: 16 hours      

------------------------------------------------------------
Pet 1: Dog
------------------------------------------------------------
Added Buddy (dog, 5 years old) with 4 tasks
  - Morning Walk (45m, HIGH)
  - Breakfast (10m, HIGH)
  - Play Time (30m, MEDIUM)
  - Dinner (10m, HIGH)

------------------------------------------------------------
Pet 2: Cat
------------------------------------------------------------
Added Luna (cat, 3 years old) with 4 tasks
  - Feeding (5m, HIGH)
  - Litter Box (10m, HIGH)
  - Play Session (25m, MEDIUM)       
  - Grooming (20m, LOW)

============================================================
📅 TODAY'S SCHEDULE
============================================================

🐕 BUDDY'S SCHEDULE
------------------------------------------------------------
Daily plan for Buddy (dog, 5 years old):
  07:00 — Morning Walk (45 min) [priority: high]
  07:45 — Breakfast (10 min) [priority: high]
  08:00 — Dinner (10 min) [priority: high]
  08:15 — Play Time (30 min) [priority: medium]

Total time needed: 1h 35m
✓ Valid: True

🐱 LUNA'S SCHEDULE
------------------------------------------------------------
Daily plan for Luna (cat, 3 years old):
  07:00 — Feeding (5 min) [priority: high]
  07:15 — Litter Box (10 min) [priority: high]
  07:30 — Play Session (25 min) [priority: medium]
  08:00 — Grooming (20 min) [priority: low]

Total time needed: 1h 0m
Total pets: 2
Total tasks across all pets: 8
Buddy's scheduled time: 95 minutes (1h 35m)
Luna's scheduled time: 60 minutes (1h 0m)
Combined daily commitment: 155 minutes (2h 35m)`

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

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
