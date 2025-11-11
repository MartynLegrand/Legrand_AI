"""
Unit tests for Task model.
"""

import unittest
from datetime import datetime, timedelta
from todo_app.task import Task


class TestTask(unittest.TestCase):
    """Test cases for Task class."""
    
    def test_create_task_basic(self):
        """Test creating a basic task."""
        task = Task(title="Test Task")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.id)
        self.assertIsInstance(task.created_at, datetime)
        self.assertIsInstance(task.updated_at, datetime)
    
    def test_create_task_full(self):
        """Test creating a task with all parameters."""
        due_date = datetime.now() + timedelta(days=7)
        task = Task(
            title="Complete Task",
            description="Test description",
            priority="high",
            due_date=due_date
        )
        self.assertEqual(task.title, "Complete Task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.due_date, due_date)
    
    def test_create_task_empty_title(self):
        """Test that empty title raises ValueError."""
        with self.assertRaises(ValueError):
            Task(title="")
        with self.assertRaises(ValueError):
            Task(title="   ")
    
    def test_create_task_invalid_priority(self):
        """Test that invalid priority raises ValueError."""
        with self.assertRaises(ValueError):
            Task(title="Test", priority="urgent")
    
    def test_mark_completed(self):
        """Test marking task as completed."""
        task = Task(title="Test")
        self.assertFalse(task.completed)
        
        task.mark_completed()
        self.assertTrue(task.completed)
    
    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = Task(title="Test", completed=True)
        self.assertTrue(task.completed)
        
        task.mark_incomplete()
        self.assertFalse(task.completed)
    
    def test_update_task(self):
        """Test updating task properties."""
        task = Task(title="Original Title", description="Original description")
        
        task.update(title="New Title", priority="high")
        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.description, "Original description")
    
    def test_update_task_empty_title(self):
        """Test that updating with empty title raises ValueError."""
        task = Task(title="Test")
        with self.assertRaises(ValueError):
            task.update(title="")
    
    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(title="Test Task", description="Test", priority="high")
        data = task.to_dict()
        
        self.assertEqual(data['title'], "Test Task")
        self.assertEqual(data['description'], "Test")
        self.assertEqual(data['priority'], "high")
        self.assertFalse(data['completed'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            'id': 'test-id-123',
            'title': 'Test Task',
            'description': 'Test description',
            'priority': 'low',
            'completed': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'due_date': None
        }
        
        task = Task.from_dict(data)
        self.assertEqual(task.id, 'test-id-123')
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test description')
        self.assertEqual(task.priority, 'low')
        self.assertTrue(task.completed)
    
    def test_task_str(self):
        """Test string representation of task."""
        task = Task(title="Test Task", priority="high")
        string_repr = str(task)
        self.assertIn("Test Task", string_repr)
        self.assertIn("↑", string_repr)  # High priority symbol
        self.assertIn("○", string_repr)  # Incomplete symbol
        
        task.mark_completed()
        string_repr = str(task)
        self.assertIn("✓", string_repr)  # Completed symbol
    
    def test_task_repr(self):
        """Test developer representation of task."""
        task = Task(title="Test Task")
        repr_str = repr(task)
        self.assertIn("Task", repr_str)
        self.assertIn("Test Task", repr_str)


if __name__ == '__main__':
    unittest.main()
