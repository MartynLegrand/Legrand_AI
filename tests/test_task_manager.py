"""
Unit tests for TaskManager module.
"""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
from todo_app.task_manager import TaskManager
from todo_app.storage import Storage


class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager class."""
    
    def setUp(self):
        """Create temporary storage and task manager for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        storage = Storage(self.temp_file.name)
        self.manager = TaskManager(storage)
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task(self):
        """Test adding a task."""
        task = self.manager.add_task("Test Task", "Description", "high")
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.priority, "high")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
    
    def test_get_task(self):
        """Test getting a task by ID."""
        task = self.manager.add_task("Test Task")
        retrieved_task = self.manager.get_task(task.id)
        
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, "Test Task")
    
    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist."""
        task = self.manager.get_task("nonexistent-id")
        self.assertIsNone(task)
    
    def test_update_task(self):
        """Test updating a task."""
        task = self.manager.add_task("Original Title")
        updated_task = self.manager.update_task(task.id, title="New Title", priority="high")
        
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.priority, "high")
    
    def test_delete_task(self):
        """Test deleting a task."""
        task = self.manager.add_task("Test Task")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
        
        result = self.manager.delete_task(task.id)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_all_tasks()), 0)
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        result = self.manager.delete_task("nonexistent-id")
        self.assertFalse(result)
    
    def test_mark_completed(self):
        """Test marking task as completed."""
        task = self.manager.add_task("Test Task")
        self.assertFalse(task.completed)
        
        completed_task = self.manager.mark_completed(task.id)
        self.assertIsNotNone(completed_task)
        self.assertTrue(completed_task.completed)
    
    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = self.manager.add_task("Test Task")
        self.manager.mark_completed(task.id)
        
        incomplete_task = self.manager.mark_incomplete(task.id)
        self.assertIsNotNone(incomplete_task)
        self.assertFalse(incomplete_task.completed)
    
    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")
        
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 3)
    
    def test_get_completed_tasks(self):
        """Test getting completed tasks."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")
        
        self.manager.mark_completed(task1.id)
        self.manager.mark_completed(task2.id)
        
        completed = self.manager.get_completed_tasks()
        self.assertEqual(len(completed), 2)
    
    def test_get_incomplete_tasks(self):
        """Test getting incomplete tasks."""
        task1 = self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")
        
        self.manager.mark_completed(task1.id)
        
        incomplete = self.manager.get_incomplete_tasks()
        self.assertEqual(len(incomplete), 2)
    
    def test_get_tasks_by_priority(self):
        """Test getting tasks by priority."""
        self.manager.add_task("Task 1", priority="low")
        self.manager.add_task("Task 2", priority="high")
        self.manager.add_task("Task 3", priority="high")
        
        high_priority = self.manager.get_tasks_by_priority("high")
        self.assertEqual(len(high_priority), 2)
    
    def test_get_overdue_tasks(self):
        """Test getting overdue tasks."""
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)
        
        self.manager.add_task("Overdue Task", due_date=past_date)
        self.manager.add_task("Future Task", due_date=future_date)
        self.manager.add_task("No Due Date")
        
        overdue = self.manager.get_overdue_tasks()
        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0].title, "Overdue Task")
    
    def test_search_tasks(self):
        """Test searching tasks."""
        self.manager.add_task("Buy groceries", "Need milk and bread")
        self.manager.add_task("Pay bills", "Electricity and water")
        self.manager.add_task("Call dentist", "Schedule appointment")
        
        results = self.manager.search_tasks("bill")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Pay bills")
        
        results = self.manager.search_tasks("appointment")
        self.assertEqual(len(results), 1)
    
    def test_clear_completed_tasks(self):
        """Test clearing completed tasks."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")
        
        self.manager.mark_completed(task1.id)
        self.manager.mark_completed(task2.id)
        
        count = self.manager.clear_completed_tasks()
        self.assertEqual(count, 2)
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
    
    def test_get_statistics(self):
        """Test getting task statistics."""
        task1 = self.manager.add_task("Task 1", priority="high")
        self.manager.add_task("Task 2", priority="low")
        self.manager.add_task("Task 3", priority="high")
        
        self.manager.mark_completed(task1.id)
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['incomplete'], 2)
        self.assertEqual(stats['priority_counts']['high'], 2)
        self.assertEqual(stats['priority_counts']['low'], 1)
    
    def test_persistence(self):
        """Test that tasks persist across manager instances."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        
        # Create new manager with same storage
        new_manager = TaskManager(Storage(self.temp_file.name))
        tasks = new_manager.get_all_tasks()
        
        self.assertEqual(len(tasks), 2)


if __name__ == '__main__':
    unittest.main()
