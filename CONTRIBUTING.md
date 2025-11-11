# Contributing to Legrand AI TODO

Thank you for your interest in contributing to Legrand AI TODO! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors:

- Be respectful and inclusive
- Be patient and welcoming
- Be collaborative
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Legrand_AI.git
   cd Legrand_AI
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

## Development Setup

### Requirements

- Python 3.7 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/MartynLegrand/Legrand_AI.git
cd Legrand_AI

# No additional dependencies needed for core functionality
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_task -v

# Run with coverage (if pytest-cov is installed)
pytest --cov=todo_app tests/
```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- Clear title and description
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Python version and OS
- Any relevant error messages or logs

**Example:**
```
Title: Task ID matching fails with certain UUIDs

Description: When trying to match a task ID that starts with '0', 
the partial ID matching returns no results even though the full 
UUID is valid.

Steps to reproduce:
1. Create a task
2. Use the show command with partial ID starting with '0'
3. Observe the error

Expected: Task should be found and displayed
Actual: "Task not found" error

Python version: 3.9.5
OS: Ubuntu 20.04
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

- Clear title describing the enhancement
- Detailed description of the proposed feature
- Use cases and benefits
- Any implementation ideas (optional)

### Contributing Code

1. **Find or Create an Issue**
   - Check existing issues for something to work on
   - Create a new issue if needed
   - Comment on the issue to indicate you're working on it

2. **Write Code**
   - Follow the coding standards below
   - Write tests for new features
   - Update documentation

3. **Submit a Pull Request**
   - Follow the PR process below

## Coding Standards

### Python Style

Follow PEP 8 style guide:

```python
# Good
def add_task(title: str, description: str = "") -> Task:
    """Add a new task with the given title."""
    pass

# Bad
def add_task(title,description=""):
    pass
```

### Documentation

- Add docstrings to all functions, classes, and modules
- Use Google-style or NumPy-style docstrings
- Include type hints
- Keep comments clear and concise

```python
def get_task(self, task_id: str) -> Optional[Task]:
    """
    Get a task by ID.
    
    Args:
        task_id: Task ID to search for (can be partial ID)
    
    Returns:
        Task object if found, None otherwise
    """
    pass
```

### Code Organization

- Keep functions focused and single-purpose
- Use meaningful variable and function names
- Avoid deep nesting (max 3-4 levels)
- Keep files under 500 lines when possible

## Testing

### Test Requirements

- Write tests for all new features
- Maintain test coverage above 80%
- Tests should be fast and isolated
- Use descriptive test names

### Test Structure

```python
class TestFeature(unittest.TestCase):
    """Test cases for Feature class."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_feature_behavior(self):
        """Test that feature behaves correctly."""
        # Arrange
        feature = Feature()
        
        # Act
        result = feature.do_something()
        
        # Assert
        self.assertEqual(result, expected_value)
```

## Pull Request Process

### Before Submitting

1. **Run Tests**
   ```bash
   python -m unittest discover tests -v
   ```

2. **Check Code Style**
   ```bash
   # If you have pylint installed
   pylint todo_app/
   ```

3. **Update Documentation**
   - Update README if needed
   - Update API docs if changed
   - Add examples if appropriate

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. Maintainer reviews the PR
2. Feedback is provided if changes needed
3. Make requested changes
4. PR is approved and merged

### After Merging

- Your contribution will be credited
- Delete your feature branch
- Celebrate! 🎉

## Feature Requests

We welcome feature requests! Some ideas we're considering:

- Task categories/tags
- Recurring tasks
- Task dependencies
- Export functionality
- Web interface
- Mobile app
- Integration with calendar apps
- Team collaboration features

## Questions?

If you have questions:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with the "question" label

## Recognition

All contributors will be recognized in:

- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to Legrand AI TODO! 🙏
