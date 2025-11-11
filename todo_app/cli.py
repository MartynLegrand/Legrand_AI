"""
Command-line interface for TODO application.
"""

import sys
import argparse
from datetime import datetime
from typing import Optional

from .task_manager import TaskManager
from .storage import Storage


class TodoCLI:
    """
    Command-line interface for managing TODO tasks.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize CLI with task manager.
        
        Args:
            storage_path: Optional path to storage file
        """
        storage = Storage(storage_path) if storage_path else Storage()
        self.manager = TaskManager(storage)
    
    def run(self, args: list = None):
        """
        Run the CLI with given arguments.
        
        Args:
            args: Command-line arguments (uses sys.argv if None)
        """
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        
        if hasattr(parsed_args, 'func'):
            try:
                parsed_args.func(parsed_args)
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                sys.exit(1)
        else:
            parser.print_help()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            prog='todo',
            description='Legrand AI TODO - A simple task management tool',
            epilog='For more information, visit: https://github.com/MartynLegrand/Legrand_AI'
        )
        
        subparsers = parser.add_subparsers(title='commands', dest='command')
        
        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', help='Task title')
        add_parser.add_argument('-d', '--description', default='', help='Task description')
        add_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'],
                               default='medium', help='Task priority (default: medium)')
        add_parser.add_argument('--due', help='Due date (YYYY-MM-DD format)')
        add_parser.set_defaults(func=self._add_task)
        
        # List command
        list_parser = subparsers.add_parser('list', help='List tasks')
        list_parser.add_argument('-a', '--all', action='store_true', help='Show all tasks')
        list_parser.add_argument('-c', '--completed', action='store_true', help='Show completed tasks only')
        list_parser.add_argument('-i', '--incomplete', action='store_true', help='Show incomplete tasks only')
        list_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'],
                                help='Filter by priority')
        list_parser.add_argument('--overdue', action='store_true', help='Show overdue tasks only')
        list_parser.set_defaults(func=self._list_tasks)
        
        # Show command
        show_parser = subparsers.add_parser('show', help='Show task details')
        show_parser.add_argument('task_id', help='Task ID')
        show_parser.set_defaults(func=self._show_task)
        
        # Update command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('task_id', help='Task ID')
        update_parser.add_argument('-t', '--title', help='New task title')
        update_parser.add_argument('-d', '--description', help='New task description')
        update_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'],
                                  help='New task priority')
        update_parser.add_argument('--due', help='New due date (YYYY-MM-DD format)')
        update_parser.set_defaults(func=self._update_task)
        
        # Complete command
        complete_parser = subparsers.add_parser('complete', help='Mark task as completed')
        complete_parser.add_argument('task_id', help='Task ID')
        complete_parser.set_defaults(func=self._complete_task)
        
        # Uncomplete command
        uncomplete_parser = subparsers.add_parser('uncomplete', help='Mark task as incomplete')
        uncomplete_parser.add_argument('task_id', help='Task ID')
        uncomplete_parser.set_defaults(func=self._uncomplete_task)
        
        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('task_id', help='Task ID')
        delete_parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')
        delete_parser.set_defaults(func=self._delete_task)
        
        # Search command
        search_parser = subparsers.add_parser('search', help='Search tasks')
        search_parser.add_argument('query', help='Search query')
        search_parser.set_defaults(func=self._search_tasks)
        
        # Clear command
        clear_parser = subparsers.add_parser('clear', help='Clear completed tasks')
        clear_parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')
        clear_parser.set_defaults(func=self._clear_completed)
        
        # Stats command
        stats_parser = subparsers.add_parser('stats', help='Show task statistics')
        stats_parser.set_defaults(func=self._show_stats)
        
        return parser
    
    def _add_task(self, args):
        """Add a new task."""
        due_date = None
        if args.due:
            try:
                due_date = datetime.strptime(args.due, '%Y-%m-%d')
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD", file=sys.stderr)
                return
        
        task = self.manager.add_task(
            title=args.title,
            description=args.description,
            priority=args.priority,
            due_date=due_date
        )
        print(f"✓ Task added: {task.title} (ID: {task.id[:8]})")
    
    def _list_tasks(self, args):
        """List tasks based on filters."""
        if args.completed:
            tasks = self.manager.get_completed_tasks()
            title = "Completed Tasks"
        elif args.incomplete:
            tasks = self.manager.get_incomplete_tasks()
            title = "Incomplete Tasks"
        elif args.overdue:
            tasks = self.manager.get_overdue_tasks()
            title = "Overdue Tasks"
        elif args.priority:
            tasks = self.manager.get_tasks_by_priority(args.priority)
            title = f"{args.priority.capitalize()} Priority Tasks"
        elif args.all:
            tasks = self.manager.get_all_tasks()
            title = "All Tasks"
        else:
            tasks = self.manager.get_incomplete_tasks()
            title = "Incomplete Tasks"
        
        self._print_tasks(tasks, title)
    
    def _show_task(self, args):
        """Show detailed information about a task."""
        task = self.manager.get_task(args.task_id)
        if not task:
            print(f"Error: Task not found with ID: {args.task_id}", file=sys.stderr)
            return
        
        print(f"\n{'='*50}")
        print(f"Task: {task.title}")
        print(f"{'='*50}")
        print(f"ID:          {task.id}")
        print(f"Status:      {'Completed' if task.completed else 'Incomplete'}")
        print(f"Priority:    {task.priority.capitalize()}")
        print(f"Created:     {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Updated:     {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if task.due_date:
            print(f"Due Date:    {task.due_date.strftime('%Y-%m-%d')}")
        if task.description:
            print(f"\nDescription:\n{task.description}")
        print(f"{'='*50}\n")
    
    def _update_task(self, args):
        """Update an existing task."""
        due_date = None
        if args.due:
            try:
                due_date = datetime.strptime(args.due, '%Y-%m-%d')
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD", file=sys.stderr)
                return
        
        task = self.manager.update_task(
            task_id=args.task_id,
            title=args.title,
            description=args.description,
            priority=args.priority,
            due_date=due_date
        )
        
        if task:
            print(f"✓ Task updated: {task.title}")
        else:
            print(f"Error: Task not found with ID: {args.task_id}", file=sys.stderr)
    
    def _complete_task(self, args):
        """Mark a task as completed."""
        task = self.manager.mark_completed(args.task_id)
        if task:
            print(f"✓ Task marked as completed: {task.title}")
        else:
            print(f"Error: Task not found with ID: {args.task_id}", file=sys.stderr)
    
    def _uncomplete_task(self, args):
        """Mark a task as incomplete."""
        task = self.manager.mark_incomplete(args.task_id)
        if task:
            print(f"✓ Task marked as incomplete: {task.title}")
        else:
            print(f"Error: Task not found with ID: {args.task_id}", file=sys.stderr)
    
    def _delete_task(self, args):
        """Delete a task."""
        task = self.manager.get_task(args.task_id)
        if not task:
            print(f"Error: Task not found with ID: {args.task_id}", file=sys.stderr)
            return
        
        if not args.yes:
            confirm = input(f"Delete task '{task.title}'? (y/N): ")
            if confirm.lower() not in ['y', 'yes']:
                print("Cancelled")
                return
        
        if self.manager.delete_task(args.task_id):
            print(f"✓ Task deleted: {task.title}")
    
    def _search_tasks(self, args):
        """Search for tasks."""
        tasks = self.manager.search_tasks(args.query)
        self._print_tasks(tasks, f"Search results for '{args.query}'")
    
    def _clear_completed(self, args):
        """Clear all completed tasks."""
        completed = self.manager.get_completed_tasks()
        if not completed:
            print("No completed tasks to clear")
            return
        
        if not args.yes:
            confirm = input(f"Clear {len(completed)} completed task(s)? (y/N): ")
            if confirm.lower() not in ['y', 'yes']:
                print("Cancelled")
                return
        
        count = self.manager.clear_completed_tasks()
        print(f"✓ Cleared {count} completed task(s)")
    
    def _show_stats(self, args):
        """Show task statistics."""
        stats = self.manager.get_statistics()
        
        print(f"\n{'='*50}")
        print("Task Statistics")
        print(f"{'='*50}")
        print(f"Total Tasks:     {stats['total']}")
        print(f"Completed:       {stats['completed']}")
        print(f"Incomplete:      {stats['incomplete']}")
        print(f"Completion Rate: {stats['completion_rate']:.1f}%")
        print(f"\nBy Priority:")
        print(f"  High:          {stats['priority_counts']['high']}")
        print(f"  Medium:        {stats['priority_counts']['medium']}")
        print(f"  Low:           {stats['priority_counts']['low']}")
        if stats['overdue'] > 0:
            print(f"\nOverdue Tasks:   {stats['overdue']}")
        print(f"{'='*50}\n")
    
    def _print_tasks(self, tasks, title):
        """Print a list of tasks."""
        print(f"\n{title}")
        print(f"{'='*50}")
        
        if not tasks:
            print("No tasks found")
        else:
            for i, task in enumerate(tasks, 1):
                status = "✓" if task.completed else "○"
                priority_symbol = {"low": "↓", "medium": "→", "high": "↑"}[task.priority]
                
                # Truncate title if too long
                title_display = task.title[:40] + "..." if len(task.title) > 40 else task.title
                
                # Show ID prefix
                id_prefix = task.id[:8]
                
                line = f"{i}. [{status}] {priority_symbol} {title_display} ({id_prefix})"
                
                # Add due date if exists
                if task.due_date:
                    due_str = task.due_date.strftime('%Y-%m-%d')
                    is_overdue = task.due_date < datetime.now() and not task.completed
                    if is_overdue:
                        line += f" [DUE: {due_str} ⚠️]"
                    else:
                        line += f" [DUE: {due_str}]"
                
                print(line)
        
        print(f"{'='*50}\n")


def main():
    """Main entry point for CLI."""
    cli = TodoCLI()
    cli.run()


if __name__ == '__main__':
    main()
