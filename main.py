"""
Main script for PawPal+ - Demo of scheduling system with multiple pets
"""

from datetime import time
from pawpal_system import Owner, Pet, Task, Priority, Scheduler


def main():
    """Main function to demonstrate PawPal+ scheduling for multiple pets"""
    
    # Create owner
    print("=" * 60)
    print("🐾 PawPal+ - Daily Pet Care Scheduler")
    print("=" * 60)
    print()
    
    owner = Owner("Alex", available_start=time(7, 0), available_end=time(23, 0))
    print(f"Owner: {owner.name}")
    print(f"Available: {owner.available_start.strftime('%H:%M')} - {owner.available_end.strftime('%H:%M')}")
    print(f"Total available hours: {owner.available_hours_per_day()} hours")
    print()
    
    # Create first pet - Dog
    print("-" * 60)
    print("Pet 1: Dog")
    print("-" * 60)
    dog = Pet("Buddy", "dog", 5)
    dog_tasks = [
        Task(
            name="Morning Walk",
            type="exercise",
            priority=Priority.HIGH,
            duration_minutes=45,
            description="Energetic walk in the park",
            frequency="daily"
        ),
        Task(
            name="Breakfast",
            type="feeding",
            priority=Priority.HIGH,
            duration_minutes=10,
            description="Morning meal",
            frequency="daily"
        ),
        Task(
            name="Play Time",
            type="enrichment",
            priority=Priority.MEDIUM,
            duration_minutes=30,
            description="Fetch and interactive play",
            frequency="daily"
        ),
        Task(
            name="Dinner",
            type="feeding",
            priority=Priority.HIGH,
            duration_minutes=10,
            description="Evening meal",
            frequency="daily"
        ),
    ]
    
    dog.tasks = dog_tasks
    owner.add_pet(dog)
    print(f"Added {dog.get_summary()} with {len(dog.tasks)} tasks")
    for task in dog.tasks:
        print(f"  - {task.name} ({task.duration_minutes}m, {task.priority.name})")
    print()
    
    # Create second pet - Cat
    print("-" * 60)
    print("Pet 2: Cat")
    print("-" * 60)
    cat = Pet("Luna", "cat", 3)
    cat_tasks = [
        Task(
            name="Feeding",
            type="feeding",
            priority=Priority.HIGH,
            duration_minutes=5,
            description="Wet food meal",
            frequency="daily"
        ),
        Task(
            name="Litter Box",
            type="maintenance",
            priority=Priority.HIGH,
            duration_minutes=10,
            description="Clean and refill litter box",
            frequency="daily"
        ),
        Task(
            name="Play Session",
            type="enrichment",
            priority=Priority.MEDIUM,
            duration_minutes=25,
            description="Laser pointer and toy time",
            frequency="daily"
        ),
        Task(
            name="Grooming",
            type="grooming",
            priority=Priority.LOW,
            duration_minutes=20,
            description="Brushing session",
            frequency="daily"
        ),
    ]
    
    cat.tasks = cat_tasks
    owner.add_pet(cat)
    print(f"Added {cat.get_summary()} with {len(cat.tasks)} tasks")
    for task in cat.tasks:
        print(f"  - {task.name} ({task.duration_minutes}m, {task.priority.name})")
    print()
    
    # Generate schedules for each pet
    print("=" * 60)
    print("📅 TODAY'S SCHEDULE")
    print("=" * 60)
    print()
    
    # Schedule for dog
    print("🐕 BUDDY'S SCHEDULE")
    print("-" * 60)
    scheduler_dog = Scheduler(owner, dog)
    schedule_dog = scheduler_dog.generate_daily_schedule(dog.tasks)
    print(schedule_dog.get_schedule_summary())
    validation_dog = scheduler_dog.validate_schedule(schedule_dog)
    print(f"✓ Valid: {validation_dog['is_valid']}")
    if validation_dog['issues']:
        for issue in validation_dog['issues']:
            print(f"  ⚠️  {issue}")
    print()
    
    # Schedule for cat
    print("🐱 LUNA'S SCHEDULE")
    print("-" * 60)
    scheduler_cat = Scheduler(owner, cat)
    schedule_cat = scheduler_cat.generate_daily_schedule(cat.tasks)
    print(schedule_cat.get_schedule_summary())
    validation_cat = scheduler_cat.validate_schedule(schedule_cat)
    print(f"✓ Valid: {validation_cat['is_valid']}")
    if validation_cat['issues']:
        for issue in validation_cat['issues']:
            print(f"  ⚠️  {issue}")
    print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    all_tasks = owner.get_all_tasks()
    print(f"Total pets: {len(owner.pets)}")
    print(f"Total tasks across all pets: {len(all_tasks)}")
    
    total_time_dog = sum(task.duration_minutes for task in schedule_dog.tasks_scheduled)
    total_time_cat = sum(task.duration_minutes for task in schedule_cat.tasks_scheduled)
    total_time_combined = total_time_dog + total_time_cat
    
    print(f"Buddy's scheduled time: {total_time_dog} minutes ({total_time_dog // 60}h {total_time_dog % 60}m)")
    print(f"Luna's scheduled time: {total_time_cat} minutes ({total_time_cat // 60}h {total_time_cat % 60}m)")
    print(f"Combined daily commitment: {total_time_combined} minutes ({total_time_combined // 60}h {total_time_combined % 60}m)")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
