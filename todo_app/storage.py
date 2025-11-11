"""
Storage module for persisting TODO tasks.
"""

import json
import os
from typing import List, Optional
from pathlib import Path

from .task import Task


class Storage:
    """
    Handles data persistence for TODO tasks using JSON file storage.
    
    Attributes:
        filepath (Path): Path to the storage file
    """
    
    def __init__(self, filepath: Optional[str] = None):
        """
        Initialize storage with a file path.
        
        Args:
            filepath: Path to storage file. Defaults to ~/.legrand_todo.json
        """
        if filepath is None:
            filepath = os.path.expanduser("~/.legrand_todo.json")
        
        self.filepath = Path(filepath)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create the storage file if it doesn't exist."""
        if not self.filepath.exists():
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            self.save_tasks([])
    
    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save tasks to storage file.
        
        Args:
            tasks: List of Task objects to save
        
        Raises:
            IOError: If file cannot be written
        """
        try:
            data = [task.to_dict() for task in tasks]
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Failed to save tasks: {str(e)}")
    
    def load_tasks(self) -> List[Task]:
        """
        Load tasks from storage file.
        
        Returns:
            List of Task objects
        
        Raises:
            IOError: If file cannot be read
            ValueError: If file contains invalid data
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # Handle empty file
                if not content:
                    return []
                data = json.loads(content)
            
            if not isinstance(data, list):
                raise ValueError("Storage file contains invalid data format")
            
            tasks = []
            for item in data:
                try:
                    tasks.append(Task.from_dict(item))
                except Exception as e:
                    # Log error but continue loading other tasks
                    print(f"Warning: Failed to load task {item.get('id', 'unknown')}: {str(e)}")
            
            return tasks
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            raise ValueError(f"Storage file contains invalid JSON: {str(e)}")
        except Exception as e:
            raise IOError(f"Failed to load tasks: {str(e)}")
    
    def clear(self) -> None:
        """Clear all tasks from storage."""
        self.save_tasks([])
    
    def backup(self, backup_path: Optional[str] = None) -> str:
        """
        Create a backup of the current storage file.
        
        Args:
            backup_path: Optional path for backup file
        
        Returns:
            Path to the backup file
        
        Raises:
            IOError: If backup cannot be created
        """
        if backup_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = str(self.filepath.parent / f"{self.filepath.stem}_backup_{timestamp}.json")
        
        try:
            import shutil
            shutil.copy2(self.filepath, backup_path)
            return backup_path
        except Exception as e:
            raise IOError(f"Failed to create backup: {str(e)}")
