"""
Tests for PawPal+ system - Task and Pet management
"""

import pytest
from datetime import time
from pawpal_system import Task, Pet, Priority


class TestTaskCompletion:
    """Test cases for task completion status"""
    
    def test_mark_complete(self):
        """Verify that mark_complete() changes task's completed status to True"""
        task = Task(
            name="Morning Walk",
            type="exercise",
            priority=Priority.HIGH,
            duration_minutes=30
        )
        
        # Initially, task should not be completed
        assert task.completed is False
        
        # Mark task as complete
        task.mark_complete()
        
        # Verify task is now completed
        assert task.completed is True
    
    def test_mark_incomplete(self):
        """Verify that mark_incomplete() changes task's completed status to False"""
        task = Task(
            name="Feeding",
            type="feeding",
            priority=Priority.HIGH,
            duration_minutes=10,
            completed=True  # Start with completed=True
        )
        
        # Verify task starts as completed
        assert task.completed is True
        
        # Mark task as incomplete
        task.mark_incomplete()
        
        # Verify task is now incomplete
        assert task.completed is False


class TestTaskAddition:
    """Test cases for adding tasks to pets"""
    
    def test_add_task_to_pet(self):
        """Verify that adding a task to a Pet increases that pet's task count"""
        pet = Pet(name="Buddy", species="dog", age=3)
        
        # Initially, pet should have no tasks
        assert len(pet.tasks) == 0
        
        # Create and add a task
        task = Task(
            name="Morning Walk",
            type="exercise",
            priority=Priority.HIGH,
            duration_minutes=30
        )
        pet.tasks.append(task)
        
        # Verify task count increased to 1
        assert len(pet.tasks) == 1
    
    def test_add_multiple_tasks_to_pet(self):
        """Verify that adding multiple tasks correctly increases the task count"""
        pet = Pet(name="Luna", species="cat", age=2)
        
        # Start with empty task list
        assert len(pet.tasks) == 0
        
        # Add multiple tasks
        tasks = [
            Task(name="Feeding", type="feeding", priority=Priority.HIGH, duration_minutes=5),
            Task(name="Play Time", type="enrichment", priority=Priority.MEDIUM, duration_minutes=20),
            Task(name="Grooming", type="grooming", priority=Priority.LOW, duration_minutes=15),
        ]
        
        for task in tasks:
            pet.tasks.append(task)
        
        # Verify all tasks were added
        assert len(pet.tasks) == 3
        
        # Verify each task is in the pet's task list
        assert tasks[0] in pet.tasks
        assert tasks[1] in pet.tasks
        assert tasks[2] in pet.tasks
