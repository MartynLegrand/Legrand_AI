# Legrand AI TODO - API Documentation

## Overview

This document provides detailed API documentation for the Legrand AI TODO application modules.

## Modules

### Task Module (`todo_app.task`)

The Task module provides the core data model for TODO items.

#### Task Class

Represents a single TODO task.

**Constructor:**
```python
Task(
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: Optional[datetime] = None,
    task_id: Optional[str] = None,
    completed: bool = False,
    created_at: Optional[datetime] = None,
    updated_at: Optional[datetime] = None
)
```

**Parameters:**
- `title` (str, required): Task title
- `description` (str, optional): Task description
- `priority` (str, optional): Priority level - "low", "medium", or "high". Default: "medium"
- `due_date` (datetime, optional): Due date for the task
- `task_id` (str, optional): Unique identifier (auto-generated if not provided)
- `completed` (bool, optional): Completion status. Default: False
- `created_at` (datetime, optional): Creation timestamp (auto-generated if not provided)
- `updated_at` (datetime, optional): Last update timestamp (auto-generated if not provided)

**Methods:**

##### `mark_completed()`
Mark the task as completed.
```python
task.mark_completed()
```

##### `mark_incomplete()`
Mark the task as incomplete.
```python
task.mark_incomplete()
```

##### `update(title=None, description=None, priority=None, due_date=None)`
Update task properties.
```python
task.update(title="New Title", priority="high")
```

##### `to_dict()`
Convert task to dictionary format.
```python
data = task.to_dict()
```

##### `from_dict(data)`
Create Task from dictionary (class method).
```python
task = Task.from_dict(data)
```

**Attributes:**
- `id` (str): Unique identifier
- `title` (str): Task title
- `description` (str): Task description
- `completed` (bool): Completion status
- `priority` (str): Priority level
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `due_date` (datetime): Due date

---

### Storage Module (`todo_app.storage`)

The Storage module handles data persistence using JSON file storage.

#### Storage Class

Manages task data persistence.

**Constructor:**
```python
Storage(filepath: Optional[str] = None)
```

**Parameters:**
- `filepath` (str, optional): Path to storage file. Default: `~/.legrand_todo.json`

**Methods:**

##### `save_tasks(tasks: List[Task])`
Save tasks to storage file.
```python
storage.save_tasks(tasks)
```

##### `load_tasks() -> List[Task]`
Load tasks from storage file.
```python
tasks = storage.load_tasks()
```

##### `clear()`
Clear all tasks from storage.
```python
storage.clear()
```

##### `backup(backup_path: Optional[str] = None) -> str`
Create a backup of the storage file.
```python
backup_path = storage.backup()
```

---

### TaskManager Module (`todo_app.task_manager`)

The TaskManager module provides high-level task management operations.

#### TaskManager Class

Manages TODO tasks with CRUD operations and filtering.

**Constructor:**
```python
TaskManager(storage: Optional[Storage] = None)
```

**Parameters:**
- `storage` (Storage, optional): Storage instance (creates default if not provided)

**Methods:**

##### `add_task(title, description="", priority="medium", due_date=None) -> Task`
Add a new task.
```python
task = manager.add_task("Buy groceries", priority="high")
```

##### `get_task(task_id: str) -> Optional[Task]`
Get a task by ID.
```python
task = manager.get_task(task_id)
```

##### `update_task(task_id, title=None, description=None, priority=None, due_date=None) -> Optional[Task]`
Update an existing task.
```python
task = manager.update_task(task_id, title="New Title")
```

##### `delete_task(task_id: str) -> bool`
Delete a task by ID.
```python
success = manager.delete_task(task_id)
```

##### `mark_completed(task_id: str) -> Optional[Task]`
Mark a task as completed.
```python
task = manager.mark_completed(task_id)
```

##### `mark_incomplete(task_id: str) -> Optional[Task]`
Mark a task as incomplete.
```python
task = manager.mark_incomplete(task_id)
```

##### `get_all_tasks() -> List[Task]`
Get all tasks.
```python
tasks = manager.get_all_tasks()
```

##### `get_completed_tasks() -> List[Task]`
Get all completed tasks.
```python
tasks = manager.get_completed_tasks()
```

##### `get_incomplete_tasks() -> List[Task]`
Get all incomplete tasks.
```python
tasks = manager.get_incomplete_tasks()
```

##### `get_tasks_by_priority(priority: str) -> List[Task]`
Get tasks by priority level.
```python
tasks = manager.get_tasks_by_priority("high")
```

##### `get_overdue_tasks() -> List[Task]`
Get tasks that are overdue.
```python
tasks = manager.get_overdue_tasks()
```

##### `search_tasks(query: str) -> List[Task]`
Search tasks by title or description.
```python
tasks = manager.search_tasks("grocery")
```

##### `clear_completed_tasks() -> int`
Remove all completed tasks.
```python
count = manager.clear_completed_tasks()
```

##### `get_statistics() -> dict`
Get task statistics.
```python
stats = manager.get_statistics()
# Returns: {
#     'total': int,
#     'completed': int,
#     'incomplete': int,
#     'completion_rate': float,
#     'priority_counts': {'low': int, 'medium': int, 'high': int},
#     'overdue': int
# }
```

---

## Usage Examples

### Basic Usage

```python
from todo_app import TaskManager

# Create manager
manager = TaskManager()

# Add tasks
task1 = manager.add_task("Buy groceries", priority="high")
task2 = manager.add_task("Call dentist", description="Schedule checkup")

# List tasks
for task in manager.get_incomplete_tasks():
    print(task)

# Complete a task
manager.mark_completed(task1.id)

# Search tasks
results = manager.search_tasks("dentist")

# Get statistics
stats = manager.get_statistics()
print(f"Total tasks: {stats['total']}")
print(f"Completed: {stats['completed']}")
```

### Custom Storage Location

```python
from todo_app import TaskManager, Storage

# Use custom storage location
storage = Storage("/path/to/custom/tasks.json")
manager = TaskManager(storage)
```

### Working with Task Objects

```python
from todo_app import Task
from datetime import datetime, timedelta

# Create a task
task = Task(
    title="Project deadline",
    description="Complete final report",
    priority="high",
    due_date=datetime.now() + timedelta(days=7)
)

# Update task
task.update(priority="medium")

# Mark as completed
task.mark_completed()

# Convert to/from dictionary
data = task.to_dict()
restored_task = Task.from_dict(data)
```

---

## Error Handling

All modules raise appropriate exceptions:

- `ValueError`: Invalid input data (empty title, invalid priority, etc.)
- `IOError`: Storage read/write errors
- `TypeError`: Invalid parameter types

Example:
```python
try:
    task = manager.add_task("")  # Empty title
except ValueError as e:
    print(f"Error: {e}")
```
