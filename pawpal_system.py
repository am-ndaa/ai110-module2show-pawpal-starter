"""
PawPal+ System: Pet care scheduling and planning logic
"""

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    """Task priority levels"""
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class Pet:
    """Represents a pet with care needs"""
    name: str
    species: str
    age: int
    tasks: List['Task'] = field(default_factory=list)
    
    def get_summary(self) -> str:
        """Return a human-readable summary of the pet"""
        return f"{self.name} ({self.species}, {self.age} years old)"
    
    def get_species_based_tasks(self) -> List[str]:
        """Return default task suggestions based on species"""
        default_tasks = {
            "dog": ["Walk", "Feeding", "Play/Enrichment", "Grooming", "Training"],
            "cat": ["Feeding", "Litter box cleaning", "Play/Enrichment", "Grooming"],
            "hamster": ["Feeding", "Cage cleaning", "Wheel maintenance"],
        }
        return default_tasks.get(self.species.lower(), ["Feeding", "Enrichment"])


@dataclass
class Task:
    """Represents a pet care task"""
    name: str
    type: str
    priority: Priority
    duration_minutes: int
    description: Optional[str] = None
    time: Optional[time] = None
    frequency: str = "daily"  # daily, weekly, one-time
    completed: bool = False
    
    def get_priority_value(self) -> int:
        """Return numeric priority for sorting"""
        return self.priority.value
    
    def mark_complete(self) -> None:
        """Mark the task as completed"""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete"""
        self.completed = False


class Owner:
    """Represents the pet owner and their availability"""
    
    def __init__(self, name: str, available_start: time = time(8, 0), available_end: time = time(22, 0), 
                 work_start: Optional[time] = None, work_end: Optional[time] = None):
        self.name = name
        self.available_start = available_start
        self.available_end = available_end
        self.work_start = work_start
        self.work_end = work_end
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection"""
        self.pets.append(pet)
    
    def remove_pet(self, pet: Pet) -> bool:
        """Remove a pet from the owner's collection"""
        if pet in self.pets:
            self.pets.remove(pet)
            return True
        return False
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from all pets"""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks
    
    def is_available_at(self, scheduled_time: time) -> bool:
        """Check if owner is available at a specific time"""
        return self.available_start <= scheduled_time <= self.available_end
    
    def available_hours_per_day(self) -> int:
        """Calculate available hours for pet care"""
        start_min = self.available_start.hour * 60 + self.available_start.minute
        end_min = self.available_end.hour * 60 + self.available_end.minute
        return (end_min - start_min) // 60


class Schedule:
    """Represents a day's schedule of tasks"""
    
    def __init__(self, pet: Pet, owner: Owner, date: datetime = None):
        self.pet = pet
        self.owner = owner
        self.tasks_scheduled: List[Task] = []
        self.date = date or datetime.now()
    
    def add_task(self, task: Task, scheduled_time: time) -> bool:
        """Add a task to the schedule at a specific time"""
        # Check if owner is available
        if not self.owner.is_available_at(scheduled_time):
            return False
        
        # Check for conflicts
        if self._has_conflict(scheduled_time, task.duration_minutes):
            return False
        
        task.time = scheduled_time
        self.tasks_scheduled.append(task)
        self._sort_tasks()
        return True
    
    def remove_task(self, task: Task) -> bool:
        """Remove a task from the schedule"""
        if task in self.tasks_scheduled:
            self.tasks_scheduled.remove(task)
            return True
        return False
    
    def _has_conflict(self, start_time: time, duration_minutes: int) -> bool:
        """Check if a task overlaps with existing tasks"""
        task_start_min = start_time.hour * 60 + start_time.minute
        task_end_min = task_start_min + duration_minutes
        
        for scheduled_task in self.tasks_scheduled:
            if scheduled_task.time is None:
                continue
            
            existing_start_min = (scheduled_task.time.hour * 60 + 
                                 scheduled_task.time.minute)
            existing_end_min = existing_start_min + scheduled_task.duration_minutes
            
            # Check for overlap
            if not (task_end_min <= existing_start_min or task_start_min >= existing_end_min):
                return True
        
        return False
    
    def _sort_tasks(self) -> None:
        """Sort tasks by scheduled time"""
        self.tasks_scheduled.sort(key=lambda t: (t.time.hour, t.time.minute) if t.time else (23, 59))
    
    def get_schedule_summary(self) -> str:
        """Return a human-readable summary of the day's schedule"""
        if not self.tasks_scheduled:
            return f"No tasks scheduled for {self.pet.get_summary()} today."
        
        summary = f"Daily plan for {self.pet.get_summary()}:\n"
        for task in self.tasks_scheduled:
            time_str = task.time.strftime("%H:%M") if task.time else "TBD"
            summary += f"  {time_str} — {task.name} ({task.duration_minutes} min) [priority: {task.priority.name.lower()}]\n"
        
        total_time = sum(task.duration_minutes for task in self.tasks_scheduled)
        summary += f"\nTotal time needed: {total_time // 60}h {total_time % 60}m"
        return summary
    
    def is_feasible(self) -> bool:
        """Check if schedule is feasible (fits within available time)"""
        available_minutes = self.owner.available_hours_per_day() * 60
        total_minutes = sum(task.duration_minutes for task in self.tasks_scheduled)
        return total_minutes <= available_minutes


class Scheduler:
    """Main scheduling engine for PawPal+"""
    
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
    
    def generate_daily_schedule(self, tasks: List[Task]) -> Schedule:
        """Generate an optimized daily schedule for the given tasks"""
        schedule = Schedule(self.pet, self.owner)
        
        # Sort tasks by priority (high first)
        sorted_tasks = sorted(tasks, key=lambda t: -t.get_priority_value())
        
        # Try to schedule each task
        for task in sorted_tasks:
            slot_time = self._find_available_slot(schedule, task)
            if slot_time:
                schedule.add_task(task, slot_time)
        
        return schedule
    
    def _find_available_slot(self, schedule: Schedule, task: Task) -> Optional[time]:
        """Find the next available time slot for a task"""
        current_min = schedule.owner.available_start.hour * 60 + schedule.owner.available_start.minute
        end_min = schedule.owner.available_end.hour * 60 + schedule.owner.available_end.minute
        
        while current_min + task.duration_minutes <= end_min:
            current_hour = current_min // 60
            current_minute = current_min % 60
            slot_time = time(current_hour, current_minute)
            
            if not schedule._has_conflict(slot_time, task.duration_minutes):
                return slot_time
            
            current_min += 15  # Move forward by 15-minute increments
        
        return None
    
    def validate_schedule(self, schedule: Schedule) -> dict:
        """Validate a schedule and return status and any issues"""
        issues = []
        
        # Check if schedule fits in available time
        if not schedule.is_feasible():
            total = sum(task.duration_minutes for task in schedule.tasks_scheduled)
            available = schedule.owner.available_hours_per_day() * 60
            issues.append(f"Schedule requires {total}m but only {available}m available")
        
        # Check if all high-priority tasks are scheduled
        high_priority_tasks = [t for t in schedule.tasks_scheduled if t.priority == Priority.HIGH]
        if len(high_priority_tasks) == 0 and any(t.priority == Priority.HIGH for t in schedule.pet.tasks):
            issues.append("Warning: Not all high-priority tasks scheduled")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues
        }


# Example usage:
if __name__ == "__main__":
    # Create owner
    owner = Owner("Jordan", available_start=time(8, 0), available_end=time(22, 0))
    
    # Create pet
    pet = Pet("Mochi", "dog", 3)
    
    # Create tasks
    tasks = [
        Task("Morning Walk", "exercise", Priority.HIGH, 30, "Daily morning walk", frequency="daily"),
        Task("Feeding", "feeding", Priority.HIGH, 10, "Breakfast", frequency="daily"),
        Task("Play Time", "enrichment", Priority.MEDIUM, 20, "Interactive play"),
        Task("Grooming", "grooming", Priority.LOW, 45, "Brushing and grooming"),
    ]
    
    # Add tasks to pet
    pet.tasks = tasks
    
    # Add pet to owner
    owner.add_pet(pet)
    
    # Generate schedule
    scheduler = Scheduler(owner, pet)
    schedule = scheduler.generate_daily_schedule(tasks)
    
    # Print results
    print(schedule.get_schedule_summary())
    print("\nValidation:", scheduler.validate_schedule(schedule))
