"""
Unit tests for Storage module.
"""

import unittest
import tempfile
import os
from pathlib import Path
from todo_app.storage import Storage
from todo_app.task import Task


class TestStorage(unittest.TestCase):
    """Test cases for Storage class."""
    
    def setUp(self):
        """Create temporary storage file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = Storage(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_storage(self):
        """Test creating storage instance."""
        self.assertIsInstance(self.storage, Storage)
        self.assertTrue(os.path.exists(self.temp_file.name))
    
    def test_save_and_load_tasks(self):
        """Test saving and loading tasks."""
        tasks = [
            Task(title="Task 1", description="Description 1"),
            Task(title="Task 2", priority="high"),
            Task(title="Task 3", completed=True)
        ]
        
        self.storage.save_tasks(tasks)
        loaded_tasks = self.storage.load_tasks()
        
        self.assertEqual(len(loaded_tasks), 3)
        self.assertEqual(loaded_tasks[0].title, "Task 1")
        self.assertEqual(loaded_tasks[1].priority, "high")
        self.assertTrue(loaded_tasks[2].completed)
    
    def test_load_empty_storage(self):
        """Test loading from empty storage."""
        tasks = self.storage.load_tasks()
        self.assertEqual(tasks, [])
    
    def test_clear_storage(self):
        """Test clearing storage."""
        tasks = [Task(title="Task 1")]
        self.storage.save_tasks(tasks)
        
        self.storage.clear()
        loaded_tasks = self.storage.load_tasks()
        self.assertEqual(loaded_tasks, [])
    
    def test_backup(self):
        """Test creating backup of storage."""
        tasks = [Task(title="Task 1")]
        self.storage.save_tasks(tasks)
        
        backup_path = self.storage.backup()
        self.assertTrue(os.path.exists(backup_path))
        
        # Verify backup content
        backup_storage = Storage(backup_path)
        backup_tasks = backup_storage.load_tasks()
        self.assertEqual(len(backup_tasks), 1)
        self.assertEqual(backup_tasks[0].title, "Task 1")
        
        # Clean up backup
        os.unlink(backup_path)
    
    def test_load_invalid_json(self):
        """Test loading invalid JSON raises ValueError."""
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        with self.assertRaises(ValueError):
            self.storage.load_tasks()


if __name__ == '__main__':
    unittest.main()
