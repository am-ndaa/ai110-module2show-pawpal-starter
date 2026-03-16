import unittest
from pawpal_system import Task, Pet


class TestPawPal(unittest.TestCase):

    def test_task_completion(self):
        """Verify that calling mark_complete() changes the task's status."""
        pet = Pet(species="Dog", name="Buddy", age=3)
        task = Task(pet=pet, description="Walk", time=30, frequency="daily")
        self.assertFalse(task.completion_status)
        task.mark_complete()
        self.assertTrue(task.completion_status)

    def test_task_addition(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(species="Cat", name="Whiskers", age=2)
        initial_count = len(pet.tasks)
        task = Task(pet=pet, description="Feed", time=10, frequency="daily")
        pet.tasks.append(task)
        self.assertEqual(len(pet.tasks), initial_count + 1)


if __name__ == '__main__':
    unittest.main()
