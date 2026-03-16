from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


class Owner:
    def __init__(self, name: str, time_available: int, pets: List[Pet] = None):
        self.name = name
        self.time_available = time_available
        self.pets = pets or []
        self.daily_schedule = None

    def add_pet(self, pet: Pet):
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: Pet):
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None
            # Optionally remove pet's tasks from scheduler if it exists
            if self.daily_schedule:
                for task in pet.tasks[:]:  # copy to avoid modification during iteration
                    self.daily_schedule.remove_task(task)

    def get_all_tasks(self) -> List[Task]:
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
    species: str
    name: str
    age: int
    owner: Owner = None
    tasks: List[Task] = field(default_factory=list)

@dataclass
class Task:
    pet: Pet
    description: str
    time: int
    frequency: str
    start_time: int = None  # start time in minutes from start of day
    completion_status: bool = False

    def mark_complete(self):
        self.completion_status = True


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks = owner.get_all_tasks()

    def add_task(self, task: Task):
        if task not in self.tasks:
            self.tasks.append(task)
            if task not in task.pet.tasks:
                task.pet.tasks.append(task)

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)
            if task in task.pet.tasks:
                task.pet.tasks.remove(task)

    def calculate_daily_schedule(self) -> List[Task]:
        # Organize tasks: sort by frequency (e.g., 'daily' first), then by time (shorter first)
        # Only include tasks that fit within owner's available time
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.frequency != 'daily', t.time))
        scheduled = []
        total_time = 0
        current_time = 0  # start from 0
        for task in sorted_tasks:
            if total_time + task.time <= self.owner.time_available:
                scheduled.append(task)
                if task.start_time is None:
                    task.start_time = current_time
                current_time += task.time
                total_time += task.time
        return scheduled

    def check_conflicts(self) -> List[str]:
        warnings = []
        scheduled_tasks = [t for t in self.tasks if t.start_time is not None]
        for i, task1 in enumerate(scheduled_tasks):
            for task2 in scheduled_tasks[i+1:]:
                if task1.start_time < task2.start_time + task2.time and task2.start_time < task1.start_time + task1.time:
                    if task1.pet == task2.pet:
                        warnings.append(f"Conflict: {task1.description} for {task1.pet.name} overlaps with {task2.description} for {task2.pet.name}.")
                    else:
                        warnings.append(f"Conflict: {task1.description} for {task1.pet.name} overlaps with {task2.description} for {task2.pet.name}.")
        return warnings
