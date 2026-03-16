from dataclasses import dataclass
from typing import List


@dataclass
class Pet:
    species: str
    name: str
    age: int


@dataclass
class Task:
    pet: Pet
    title: str
    duration: int
    priority: int


class Owner:
    def __init__(self, name: str, time_available: int):
        self.name = name
        self.time_available = time_available


class DailySchedule:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def calculate_daily_schedule(self):
        pass
