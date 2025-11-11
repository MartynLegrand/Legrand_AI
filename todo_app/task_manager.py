"""
Task Manager module for managing TODO tasks.
"""

from typing import List, Optional, Callable
from datetime import datetime

from .task import Task
from .storage import Storage


class TaskManager:
    """
    Manages TODO tasks with CRUD operations and filtering capabilities.
    
    Attributes:
        storage (Storage): Storage backend for persisting tasks
        tasks (List[Task]): In-memory list of tasks
    """
    
    def __init__(self, storage: Optional[Storage] = None):
        """
        Initialize TaskManager with storage backend.
        
        Args:
            storage: Storage instance (creates default if not provided)
        """
        self.storage = storage or Storage()
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Load tasks from storage into memory."""
        self.tasks = self.storage.load_tasks()
    
    def save_tasks(self) -> None:
        """Save tasks from memory to storage."""
        self.storage.save_tasks(self.tasks)
    
    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: Optional[datetime] = None
    ) -> Task:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Task description
            priority: Task priority (low, medium, high)
            due_date: Optional due date
        
        Returns:
            The created Task object
        
        Raises:
            ValueError: If task data is invalid
        """
        task = Task(title=title, description=description, priority=priority, due_date=due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID to search for (can be partial ID)
        
        Returns:
            Task object if found, None otherwise
        """
        # First try exact match
        for task in self.tasks:
            if task.id == task_id:
                return task
        
        # Then try partial match (prefix)
        matches = [task for task in self.tasks if task.id.startswith(task_id)]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            # Multiple matches - need more specific ID
            return None
        
        return None
    
    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[datetime] = None
    ) -> Optional[Task]:
        """
        Update an existing task.
        
        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            due_date: New due date (optional)
        
        Returns:
            Updated Task object if found, None otherwise
        
        Raises:
            ValueError: If update data is invalid
        """
        task = self.get_task(task_id)
        if task:
            task.update(title=title, description=description, priority=priority, due_date=due_date)
            self.save_tasks()
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID.
        
        Args:
            task_id: ID of task to delete
        
        Returns:
            True if task was deleted, False if not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return True
        return False
    
    def mark_completed(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of task to mark as completed
        
        Returns:
            Updated Task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.mark_completed()
            self.save_tasks()
        return task
    
    def mark_incomplete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as incomplete.
        
        Args:
            task_id: ID of task to mark as incomplete
        
        Returns:
            Updated Task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
            self.save_tasks()
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self.tasks.copy()
    
    def get_filtered_tasks(self, filter_func: Callable[[Task], bool]) -> List[Task]:
        """
        Get tasks filtered by a custom function.
        
        Args:
            filter_func: Function that takes a Task and returns bool
        
        Returns:
            List of filtered tasks
        """
        return [task for task in self.tasks if filter_func(task)]
    
    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.
        
        Returns:
            List of completed tasks
        """
        return self.get_filtered_tasks(lambda t: t.completed)
    
    def get_incomplete_tasks(self) -> List[Task]:
        """
        Get all incomplete tasks.
        
        Returns:
            List of incomplete tasks
        """
        return self.get_filtered_tasks(lambda t: not t.completed)
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """
        Get tasks by priority level.
        
        Args:
            priority: Priority level (low, medium, high)
        
        Returns:
            List of tasks with specified priority
        """
        return self.get_filtered_tasks(lambda t: t.priority == priority)
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        Get tasks that are overdue.
        
        Returns:
            List of overdue tasks
        """
        now = datetime.now()
        return self.get_filtered_tasks(
            lambda t: t.due_date is not None and t.due_date < now and not t.completed
        )
    
    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title or description.
        
        Args:
            query: Search query string
        
        Returns:
            List of matching tasks
        """
        query_lower = query.lower()
        return self.get_filtered_tasks(
            lambda t: query_lower in t.title.lower() or query_lower in t.description.lower()
        )
    
    def clear_completed_tasks(self) -> int:
        """
        Remove all completed tasks.
        
        Returns:
            Number of tasks removed
        """
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.completed]
        self.save_tasks()
        return initial_count - len(self.tasks)
    
    def get_statistics(self) -> dict:
        """
        Get statistics about tasks.
        
        Returns:
            Dictionary with task statistics
        """
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        incomplete = total - completed
        
        priority_counts = {
            'low': len(self.get_tasks_by_priority('low')),
            'medium': len(self.get_tasks_by_priority('medium')),
            'high': len(self.get_tasks_by_priority('high'))
        }
        
        overdue = len(self.get_overdue_tasks())
        
        return {
            'total': total,
            'completed': completed,
            'incomplete': incomplete,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'priority_counts': priority_counts,
            'overdue': overdue
        }
