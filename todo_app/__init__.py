"""
Legrand AI TODO Application
A simple, efficient TODO list manager with CLI interface.
"""

__version__ = "1.0.0"
__author__ = "Martyn Legrand"

from .task import Task
from .task_manager import TaskManager
from .storage import Storage

__all__ = ['Task', 'TaskManager', 'Storage']
