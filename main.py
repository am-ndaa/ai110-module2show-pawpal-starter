from pawpal_system import Owner, Pet, Task, Scheduler

# Create an Owner
owner = Owner(name="John", time_available=120)  # 120 minutes available

# Create at least two Pets
pet1 = Pet(species="Dog", name="Buddy", age=3)
pet2 = Pet(species="Cat", name="Whiskers", age=2)

# Add pets to the owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create at least three Tasks with different times
task1 = Task(pet=pet1, description="Walk", time=30, frequency="daily", start_time=0)
task2 = Task(pet=pet2, description="Feed", time=10, frequency="daily", start_time=0)  # same start time
task3 = Task(pet=pet1, description="Play", time=20, frequency="daily", start_time=40)

# Create Scheduler and add tasks
scheduler = Scheduler(owner)
scheduler.add_task(task1)
scheduler.add_task(task2)
scheduler.add_task(task3)

# Calculate and print Today's Schedule
schedule = scheduler.calculate_daily_schedule()
print("Today's Schedule:")
total_time = 0
for task in schedule:
    print(f"- {task.description} for {task.pet.name} ({task.time} min at {task.start_time} min)")
    total_time += task.time
print(f"Total time: {total_time} min (out of {owner.time_available} min available)")

# Check for conflicts
conflicts = scheduler.check_conflicts()
if conflicts:
    print("Warnings:")
    for warning in conflicts:
        print(f"- {warning}")
else:
    print("No conflicts detected.")
