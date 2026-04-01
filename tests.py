import unittest
import os
from models import Database, Task
import sqlite3

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database for testing
        self.db = Database(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get_task(self):
        task = Task(None, "Test Assignment", "Write a report", "2026-10-15", "High", "Pending")
        self.db.add_task(task)
        
        all_tasks = self.db.get_all_tasks()
        self.assertEqual(len(all_tasks), 1)
        self.assertEqual(all_tasks[0].title, "Test Assignment")
        self.assertEqual(all_tasks[0].status, "Pending")

    def test_update_task(self):
        task = Task(None, "Old Title", "Old Desc", "2026-10-15", "Low", "Pending")
        self.db.add_task(task)
        
        saved_task = self.db.get_all_tasks()[0]
        self.assertEqual(saved_task.title, "Old Title")
        
        # Update it
        saved_task.title = "New Title"
        saved_task.status = "Completed"
        self.db.update_task(saved_task)
        
        updated_task = self.db.get_all_tasks()[0]
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.status, "Completed")

    def test_delete_task(self):
        task = Task(None, "Delete Me", "Desc", "2026-10-15", "High", "Pending")
        self.db.add_task(task)
        
        saved_task = self.db.get_all_tasks()[0]
        self.assertEqual(len(self.db.get_all_tasks()), 1)
        
        self.db.delete_task(saved_task.id)
        self.assertEqual(len(self.db.get_all_tasks()), 0)

    def test_filters(self):
        self.db.add_task(Task(None, "Task 1", "", "2026-10-10", "High", "Pending"))
        self.db.add_task(Task(None, "Task 2", "", "2026-10-11", "Low", "Completed"))
        self.db.add_task(Task(None, "Task 3", "", "2026-10-12", "High", "Completed"))
        
        # Filter by Status
        completed_tasks = self.db.get_all_tasks(filter_status="Completed")
        self.assertEqual(len(completed_tasks), 2)
        
        # Filter by Priority
        high_tasks = self.db.get_all_tasks(filter_priority="High")
        self.assertEqual(len(high_tasks), 2)
        
        # Filter by Both
        high_completed = self.db.get_all_tasks(filter_status="Completed", filter_priority="High")
        self.assertEqual(len(high_completed), 1)
        self.assertEqual(high_completed[0].title, "Task 3")

if __name__ == "__main__":
    unittest.main()
