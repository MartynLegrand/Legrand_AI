# Legrand AI TODO - Examples and Use Cases

This document provides real-world examples and use cases for the TODO application.

## Table of Contents

1. [Personal Task Management](#personal-task-management)
2. [Project Management](#project-management)
3. [Shopping List](#shopping-list)
4. [Daily Routine](#daily-routine)
5. [Study Planner](#study-planner)
6. [Work Tasks](#work-tasks)

## Personal Task Management

### Scenario: Managing daily personal tasks

```bash
# Add morning routine tasks
python todo.py add "Morning exercise" -p high --due 2025-11-12
python todo.py add "Prepare breakfast" -p medium
python todo.py add "Check emails" -p low

# Add evening tasks
python todo.py add "Grocery shopping" -d "Milk, eggs, bread" -p high
python todo.py add "Call dentist" -d "Schedule annual checkup" -p medium --due 2025-11-13

# View all tasks for the day
python todo.py list

# Mark completed tasks
python todo.py complete <task-id>

# Check progress
python todo.py stats
```

## Project Management

### Scenario: Managing a software development project

```bash
# Add project tasks with priorities
python todo.py add "Design database schema" -p high --due 2025-11-15
python todo.py add "Create API endpoints" -p high --due 2025-11-20
python todo.py add "Write unit tests" -p medium --due 2025-11-22
python todo.py add "Update documentation" -p low --due 2025-11-25
python todo.py add "Code review" -p medium --due 2025-11-23

# View high-priority tasks
python todo.py list -p high

# Track project progress
python todo.py stats

# Update task as you progress
python todo.py update <task-id> -t "Design and implement database schema"

# Mark tasks complete as you finish them
python todo.py complete <task-id>

# Check what's overdue
python todo.py list --overdue
```

## Shopping List

### Scenario: Creating and managing a shopping list

```bash
# Add grocery items
python todo.py add "Buy vegetables" -d "Tomatoes, lettuce, carrots" -p high
python todo.py add "Get cleaning supplies" -d "Detergent, paper towels" -p medium
python todo.py add "Pick up prescriptions" -p high
python todo.py add "Buy office supplies" -d "Printer paper, pens" -p low

# Search for specific items
python todo.py search "buy"

# Complete items as you shop
python todo.py complete <task-id>

# Clear completed items when done
python todo.py clear -y
```

## Daily Routine

### Scenario: Creating a daily routine checklist

```bash
# Morning routine
python todo.py add "Wake up at 6 AM" -p high
python todo.py add "Morning meditation" -p medium -d "10 minutes mindfulness"
python todo.py add "Exercise" -p high -d "30 minutes cardio"
python todo.py add "Healthy breakfast" -p high

# Work routine
python todo.py add "Check priority emails" -p high
python todo.py add "Daily standup meeting" -p high --due 2025-11-12
python todo.py add "Complete project tasks" -p high
python todo.py add "Review pull requests" -p medium

# Evening routine
python todo.py add "Prepare dinner" -p medium
python todo.py add "Read for 30 minutes" -p low
python todo.py add "Plan tomorrow" -p medium

# View all today's tasks
python todo.py list

# At end of day, clear completed tasks
python todo.py clear -y
```

## Study Planner

### Scenario: Planning study sessions for exams

```bash
# Add study topics with deadlines
python todo.py add "Study Chapter 1: Introduction" -p high --due 2025-11-12
python todo.py add "Study Chapter 2: Data Structures" -p high --due 2025-11-13
python todo.py add "Study Chapter 3: Algorithms" -p high --due 2025-11-14
python todo.py add "Practice problems Set 1" -p medium --due 2025-11-15
python todo.py add "Practice problems Set 2" -p medium --due 2025-11-16
python todo.py add "Review all notes" -p high --due 2025-11-17
python todo.py add "Take practice exam" -p high --due 2025-11-18

# View study schedule
python todo.py list -a

# Update study notes
python todo.py update <task-id> -d "Completed 80% - need to review binary trees"

# Mark chapters as completed
python todo.py complete <task-id>

# Check exam preparation progress
python todo.py stats

# See what needs urgent attention
python todo.py list -p high
```

## Work Tasks

### Scenario: Managing work tasks and deadlines

```bash
# Add weekly work tasks
python todo.py add "Prepare quarterly report" -p high --due 2025-11-15 \
  -d "Include Q3 metrics and Q4 projections"

python todo.py add "Team performance reviews" -p high --due 2025-11-20 \
  -d "Complete reviews for 5 team members"

python todo.py add "Update project documentation" -p medium --due 2025-11-18 \
  -d "Add new features and API changes"

python todo.py add "Client meeting preparation" -p high --due 2025-11-13 \
  -d "Prepare slides and demo"

python todo.py add "Code refactoring" -p low --due 2025-11-25 \
  -d "Refactor authentication module"

# View all work tasks
python todo.py list -a

# Show specific task details
python todo.py show <task-id>

# Update task with additional notes
python todo.py update <task-id> -d "Added: Review budget allocation"

# Search for specific tasks
python todo.py search "report"

# Check for overdue tasks
python todo.py list --overdue

# View incomplete tasks only
python todo.py list -i

# Weekly cleanup
python todo.py clear -y
```

## Advanced Workflows

### Weekly Planning Routine

```bash
# Monday morning: Plan the week
python todo.py list -a
python todo.py stats

# Add weekly goals
python todo.py add "Complete project milestone" -p high --due 2025-11-15
python todo.py add "Attend all meetings" -p high

# Mid-week: Check progress
python todo.py list -p high
python todo.py list --overdue

# Friday: Review and cleanup
python todo.py stats
python todo.py clear -y
```

### Using Search Effectively

```bash
# Find all tasks related to meetings
python todo.py search "meeting"

# Find tasks with specific keywords
python todo.py search "report"
python todo.py search "review"
python todo.py search "documentation"

# Find tasks by description content
python todo.py search "API"
python todo.py search "client"
```

### Priority Management

```bash
# View tasks by priority
python todo.py list -p high    # Urgent tasks
python todo.py list -p medium  # Normal tasks
python todo.py list -p low     # Can wait

# Adjust priorities as needed
python todo.py update <task-id> -p high  # Increase priority
python todo.py update <task-id> -p low   # Decrease priority
```

### Deadline Management

```bash
# Add tasks with various deadlines
python todo.py add "Urgent task" -p high --due 2025-11-12
python todo.py add "This week task" -p medium --due 2025-11-15
python todo.py add "Next week task" -p low --due 2025-11-22

# Check what's due soon
python todo.py list -a

# Check overdue tasks
python todo.py list --overdue
```

## Tips for Effective Task Management

1. **Use Descriptive Titles**: Make titles clear and actionable
   ```bash
   # Good
   python todo.py add "Review and approve budget proposal"
   
   # Less clear
   python todo.py add "Budget"
   ```

2. **Add Detailed Descriptions**: Include context and details
   ```bash
   python todo.py add "Client meeting" \
     -d "Discuss Q4 deliverables, timeline concerns, budget review" \
     -p high --due 2025-11-15
   ```

3. **Set Realistic Priorities**: Don't make everything high priority
   ```bash
   # Balance your priorities
   python todo.py list -p high   # Should be few critical tasks
   python todo.py list -p medium # Most tasks
   python todo.py list -p low    # Nice to have tasks
   ```

4. **Regular Reviews**: Check your tasks daily
   ```bash
   # Morning routine
   python todo.py list -p high
   python todo.py list --overdue
   
   # Evening routine
   python todo.py stats
   python todo.py list -i
   ```

5. **Clean Up Regularly**: Remove completed tasks
   ```bash
   # Weekly cleanup
   python todo.py clear -y
   ```

6. **Use Due Dates Wisely**: Set realistic deadlines
   ```bash
   # Add buffer time
   python todo.py add "Project deadline" --due 2025-11-20
   python todo.py add "Project completion" --due 2025-11-18  # Finish early
   ```

## Integration with Other Tools

### Shell Aliases

Add to your `.bashrc` or `.zshrc`:
```bash
alias td='python /path/to/todo.py'
alias tdl='python /path/to/todo.py list'
alias tda='python /path/to/todo.py add'
alias tds='python /path/to/todo.py stats'
```

Then use:
```bash
td list
tda "New task" -p high
tds
```

### Cron Jobs for Reminders

Create a script to email yourself overdue tasks:
```bash
#!/bin/bash
overdue=$(python /path/to/todo.py list --overdue)
if [ ! -z "$overdue" ]; then
    echo "$overdue" | mail -s "Overdue Tasks Reminder" you@email.com
fi
```

Add to crontab:
```bash
0 9 * * * /path/to/reminder.sh  # Run daily at 9 AM
```
