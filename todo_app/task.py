"""
Task model for TODO application.
"""

from datetime import datetime
from typing import Optional
import uuid


class Task:
    """
    Represents a single TODO task.
    
    Attributes:
        id (str): Unique identifier for the task
        title (str): Task title
        description (str): Detailed description of the task
        completed (bool): Task completion status
        priority (str): Task priority (low, medium, high)
        created_at (datetime): Timestamp when task was created
        updated_at (datetime): Timestamp when task was last updated
        due_date (datetime): Optional due date for the task
    """
    
    PRIORITY_LEVELS = ['low', 'medium', 'high']
    
    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: Optional[datetime] = None,
        task_id: Optional[str] = None,
        completed: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initialize a new Task.
        
        Args:
            title: Task title (required)
            description: Task description (optional)
            priority: Task priority - low, medium, or high (default: medium)
            due_date: Optional due date for the task
            task_id: Optional task ID (auto-generated if not provided)
            completed: Task completion status (default: False)
            created_at: Creation timestamp (auto-generated if not provided)
            updated_at: Update timestamp (auto-generated if not provided)
        
        Raises:
            ValueError: If priority is not valid or title is empty
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        if priority not in self.PRIORITY_LEVELS:
            raise ValueError(f"Priority must be one of: {', '.join(self.PRIORITY_LEVELS)}")
        
        self.id = task_id or str(uuid.uuid4())
        self.title = title.strip()
        self.description = description.strip()
        self.completed = completed
        self.priority = priority
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.due_date = due_date
    
    def mark_completed(self) -> None:
        """Mark the task as completed and update timestamp."""
        self.completed = True
        self.updated_at = datetime.now()
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete and update timestamp."""
        self.completed = False
        self.updated_at = datetime.now()
    
    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[datetime] = None
    ) -> None:
        """
        Update task properties.
        
        Args:
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            due_date: New due date (optional)
        
        Raises:
            ValueError: If title is empty or priority is invalid
        """
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            self.title = title.strip()
        
        if description is not None:
            self.description = description.strip()
        
        if priority is not None:
            if priority not in self.PRIORITY_LEVELS:
                raise ValueError(f"Priority must be one of: {', '.join(self.PRIORITY_LEVELS)}")
            self.priority = priority
        
        if due_date is not None:
            self.due_date = due_date
        
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """
        Convert task to dictionary format.
        
        Returns:
            Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create a Task instance from dictionary data.
        
        Args:
            data: Dictionary containing task data
        
        Returns:
            Task instance
        """
        return cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            task_id=data.get('id'),
            completed=data.get('completed', False),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        priority_symbol = {"low": "↓", "medium": "→", "high": "↑"}[self.priority]
        return f"[{status}] {priority_symbol} {self.title}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation of the task."""
        return f"Task(id={self.id[:8]}, title='{self.title}', completed={self.completed})"
