# Legrand AI TODO - Usage Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Commands](#basic-commands)
3. [Advanced Usage](#advanced-usage)
4. [Examples](#examples)
5. [Tips and Tricks](#tips-and-tricks)

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MartynLegrand/Legrand_AI.git
cd Legrand_AI
```

2. The application uses only Python standard library, so no additional dependencies are required.

3. Make the script executable (optional):
```bash
chmod +x todo.py
```

### First Steps

Add your first task:
```bash
python todo.py add "Buy groceries"
```

List your tasks:
```bash
python todo.py list
```

## Basic Commands

### Adding Tasks

Add a simple task:
```bash
python todo.py add "Task title"
```

Add a task with description:
```bash
python todo.py add "Buy groceries" -d "Milk, bread, eggs"
```

Add a task with priority:
```bash
python todo.py add "Urgent meeting" -p high
```

Add a task with due date:
```bash
python todo.py add "Submit report" --due 2025-12-31
```

Combine options:
```bash
python todo.py add "Project deadline" -d "Complete final report" -p high --due 2025-12-15
```

### Listing Tasks

List incomplete tasks (default):
```bash
python todo.py list
```

List all tasks:
```bash
python todo.py list -a
```

List completed tasks:
```bash
python todo.py list -c
```

List incomplete tasks:
```bash
python todo.py list -i
```

List by priority:
```bash
python todo.py list -p high
```

List overdue tasks:
```bash
python todo.py list --overdue
```

### Viewing Task Details

Show detailed information about a task:
```bash
python todo.py show <task-id>
```

Example:
```bash
python todo.py show a1b2c3d4
```

### Updating Tasks

Update task title:
```bash
python todo.py update <task-id> -t "New title"
```

Update priority:
```bash
python todo.py update <task-id> -p high
```

Update description:
```bash
python todo.py update <task-id> -d "New description"
```

Update due date:
```bash
python todo.py update <task-id> --due 2025-12-31
```

Combine updates:
```bash
python todo.py update <task-id> -t "New title" -p high --due 2025-12-31
```

### Completing Tasks

Mark a task as completed:
```bash
python todo.py complete <task-id>
```

Mark a task as incomplete:
```bash
python todo.py uncomplete <task-id>
```

### Deleting Tasks

Delete a task (with confirmation):
```bash
python todo.py delete <task-id>
```

Delete without confirmation:
```bash
python todo.py delete <task-id> -y
```

### Searching Tasks

Search tasks by keyword:
```bash
python todo.py search "grocery"
```

The search looks in both task titles and descriptions.

### Clearing Completed Tasks

Remove all completed tasks:
```bash
python todo.py clear
```

Remove without confirmation:
```bash
python todo.py clear -y
```

### Viewing Statistics

Show task statistics:
```bash
python todo.py stats
```

This displays:
- Total tasks
- Completed/incomplete counts
- Completion rate
- Priority distribution
- Overdue tasks count

## Advanced Usage

### Custom Storage Location

Use a custom storage file:
```bash
python todo.py --storage /path/to/tasks.json add "Task"
```

### Task IDs

Tasks are identified by unique IDs. When listing tasks, you'll see shortened IDs like `a1b2c3d4`.

You can use either:
- The short ID shown in lists: `a1b2c3d4`
- The full UUID: `a1b2c3d4-5e6f-7g8h-9i0j-k1l2m3n4o5p6`

### Priority Levels

Three priority levels are available:
- `low` (↓): Less urgent tasks
- `medium` (→): Normal priority (default)
- `high` (↑): Urgent tasks

### Due Dates

Due dates must be in YYYY-MM-DD format:
```bash
python todo.py add "Task" --due 2025-12-31
```

Overdue tasks (past due date and not completed) are marked with ⚠️ in listings.

## Examples

### Daily Workflow

Start your day by viewing incomplete tasks:
```bash
python todo.py list
```

Check for urgent tasks:
```bash
python todo.py list -p high
```

Check overdue tasks:
```bash
python todo.py list --overdue
```

### Project Management

Add project tasks:
```bash
python todo.py add "Design mockups" -p high --due 2025-11-20
python todo.py add "Implement frontend" -p medium --due 2025-11-25
python todo.py add "Write tests" -p medium --due 2025-11-28
python todo.py add "Deploy to production" -p high --due 2025-11-30
```

Track progress:
```bash
python todo.py stats
```

### Weekly Review

List all tasks:
```bash
python todo.py list -a
```

Clean up completed tasks:
```bash
python todo.py clear -y
```

Review statistics:
```bash
python todo.py stats
```

## Tips and Tricks

### Quick Task Entry

For quick task entry, use short commands:
```bash
python todo.py add "Quick task" -p h  # Note: Use full 'high', 'medium', 'low'
```

### Finding Tasks

When you can't remember the exact task title:
```bash
python todo.py search "keyword"
```

### Task Organization

Use descriptive titles and detailed descriptions:
```bash
python todo.py add "Weekly team meeting" \
  -d "Discuss project progress, blockers, and next steps" \
  -p medium \
  --due 2025-11-15
```

### Batch Operations

Complete multiple tasks in sequence:
```bash
python todo.py complete <task-id-1>
python todo.py complete <task-id-2>
python todo.py complete <task-id-3>
```

### Regular Maintenance

Periodically clean up completed tasks:
```bash
python todo.py clear -y
```

### Backup Your Data

The tasks are stored in `~/.legrand_todo.json`. Back it up regularly:
```bash
cp ~/.legrand_todo.json ~/.legrand_todo_backup.json
```

### Using with Shell Aliases

Add to your `.bashrc` or `.zshrc`:
```bash
alias todo='python /path/to/Legrand_AI/todo.py'
```

Then use simply:
```bash
todo add "New task"
todo list
todo complete <task-id>
```

### Task ID Shortcuts

Most commands accept task IDs. You only need to provide enough characters to uniquely identify a task (usually the first 8 characters shown in listings).

### Formatting Output

The list command uses symbols:
- ○ : Incomplete task
- ✓ : Completed task
- ↑ : High priority
- → : Medium priority
- ↓ : Low priority
- ⚠️ : Overdue task

## Data Storage

Tasks are stored in JSON format at `~/.legrand_todo.json` by default.

The file format is human-readable and can be edited directly if needed (though using the CLI is recommended).

To change the storage location, use a custom storage path or set an environment variable in your script wrapper.
