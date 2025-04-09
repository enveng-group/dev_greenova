# Python Learning Resource

## Introduction to Python

Python is a high-level, interpreted programming language known for its
readability, versatility, and extensive standard library. It supports multiple
programming paradigms including procedural, object-oriented, and functional
programming.

### Key Features

- **Readable syntax** with significant whitespace
- **Dynamic typing** and automatic memory management
- **Extensive standard library** ("batteries included" philosophy)
- Strong support for **integration** with other languages and tools
- **Cross-platform** compatibility

## Installation and Setup

### Installing Python

Official installation guides for various platforms are available at:

- [Python Installation Guide](https://docs.python.org/release/3.9.21/installing/index.html)

#### Quick Installation Commands

**Linux (Ubuntu/Debian)**:

```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-dev
```

**macOS (using Homebrew)**:

```bash
brew install python@3.9
```

**Windows**: Download the installer from
[python.org](https://www.python.org/downloads/)

### Virtual Environments

Always use virtual environments to isolate project dependencies:

```bash
# Create a virtual environment
python3.9 -m venv myenv

# Activate the virtual environment
# On Unix/macOS
source myenv/bin/activate
# On Windows
myenv\Scripts\activate

# Install packages
pip install package_name

# Generate requirements file
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## Python Basics

### Hello World

```python
print("Hello, World!")
```

### Variables and Data Types

```python
# Numbers
x = 10          # integer
y = 3.14        # float
z = complex(1, 2)  # complex

# Strings
name = "Python"
multiline = """Multiple
line string"""

# Boolean
is_active = True

# Lists
fruits = ["apple", "banana", "cherry"]

# Tuples (immutable)
coordinates = (10, 20)

# Dictionaries
person = {"name": "John", "age": 30}

# Sets
unique_numbers = {1, 2, 3, 3, 4}  # {1, 2, 3, 4}
```

### Control Flow

```python
# Conditionals
x = 10
if x > 5:
    print("x is greater than 5")
elif x == 5:
    print("x equals 5")
else:
    print("x is less than 5")

# Loops
for fruit in fruits:
    print(fruit)

i = 0
while i < 5:
    print(i)
    i += 1

# Break and continue
for n in range(10):
    if n == 3:
        continue  # Skip this iteration
    if n == 8:
        break     # Exit loop
    print(n)
```

### Functions

```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

# Default parameters
def greet_with_default(name="World"):
    return f"Hello, {name}!"

# *args and **kwargs
def flexible_function(*args, **kwargs):
    print(f"Positional arguments: {args}")
    print(f"Keyword arguments: {kwargs}")

# Type hints (Python 3.5+)
def add(a: int, b: int) -> int:
    return a + b
```

## Object-Oriented Programming

```python
class Person:
    # Class attribute
    species = "Homo sapiens"

    # Constructor
    def __init__(self, name, age):
        # Instance attributes
        self.name = name
        self.age = age

    # Method
    def greet(self):
        return f"Hello, my name is {self.name}"

    # Static method
    @staticmethod
    def is_adult(age):
        return age >= 18

    # Class method
    @classmethod
    def create_anonymous(cls):
        return cls("Anonymous", 0)

# Inheritance
class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id
```

## Advanced Python Features

### List Comprehensions

```python
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

### Generators

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

# Generator expression
sum_of_squares = sum(x**2 for x in range(10))
```

### Decorators

```python
def timing_decorator(func):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result

    return wrapper

@timing_decorator
def slow_function():
    import time
    time.sleep(1)
```

### Context Managers

```python
# Using a context manager
with open("file.txt", "w") as file:
    file.write("Hello, World!")

# Creating a context manager
from contextlib import contextmanager

@contextmanager
def managed_resource():
    # Setup
    resource = {"name": "Resource"}
    try:
        yield resource  # Provide the resource
    finally:
        # Cleanup
        resource.clear()
```

### Type Hints (Python 3.5+)

```python
from typing import List, Dict, Optional, Union, Callable

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def may_return_none(value: bool) -> Optional[str]:
    return "value" if value else None

def accepts_multiple_types(value: Union[str, int]) -> str:
    return str(value)

# Function type hints
def apply_function(func: Callable[[int], int], value: int) -> int:
    return func(value)
```

## Python in Practice

### Best Practices

1. **Follow PEP 8** - Python's style guide
2. **Write docstrings** - Document functions, classes, and modules
3. **Use virtual environments** - Isolate project dependencies
4. **Write test cases** - Use pytest for testing
5. **Handle exceptions properly** - Use try/except blocks appropriately

### Common Design Patterns

```python
# Singleton pattern
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Factory pattern
class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")
```

### Working with Files

```python
# Reading a file
with open("file.txt", "r") as file:
    content = file.read()

# Reading line by line
with open("file.txt", "r") as file:
    for line in file:
        print(line.strip())

# Writing to a file
with open("file.txt", "w") as file:
    file.write("Hello, World!")
```

### Working with JSON

```python
import json

# Parse JSON from string
data = '{"name": "John", "age": 30}'
person = json.loads(data)
print(person["name"])  # John

# Convert Python object to JSON
person = {"name": "John", "age": 30}
json_string = json.dumps(person)
print(json_string)  # {"name": "John", "age": 30}

# Read/write JSON files
with open("data.json", "w") as file:
    json.dump(person, file)

with open("data.json", "r") as file:
    loaded_person = json.load(file)
```

## Testing with pytest

Python offers various testing frameworks, with pytest being the most powerful
and flexible option for modern Python applications.

### Basic pytest Example

```python
# test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_string_methods():
    assert "hello".capitalize() == "Hello"
```

### pytest Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Test User", "email": "test@example.com"}

def test_user_name(sample_data):
    assert sample_data["name"] == "Test User"
```

### Django Testing with pytest

For Django projects, use pytest with pytest-django:

```python
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_page(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Welcome' in response.content.decode()
```

### Web UI Testing with Selenium

For browser-based testing:

```python
import pytest
from selenium.webdriver.common.by import By

@pytest.mark.selenium
def test_login_form(selenium, live_server):
    # Visit the login page
    selenium.get(f"{live_server.url}/accounts/login/")

    # Fill in the form
    username = selenium.find_element(By.NAME, "username")
    username.send_keys("test")

    # Submit the form
    submit = selenium.find_element(By.XPATH, "//button[@type='submit']")
    submit.click()

    # Check results
    assert "Dashboard" in selenium.page_source
```

### Testing Packages

- **pytest**: Core testing framework
- **pytest-django**: Django integration for pytest
- **pytest-selenium**: Selenium testing integration
- **pytest-cov**: Code coverage reporting
- **pytest-dotenv**: Environment variable management for tests

## Python Standard Library Highlights

Python comes with a rich standard library that provides modules for various
tasks:

- **os, sys** - Operating system interfaces
- **pathlib** - Object-oriented filesystem paths
- **datetime** - Date and time handling
- **re** - Regular expressions
- **math, random** - Mathematical functions and random numbers
- **collections** - Specialized container datatypes
- **itertools** - Functions for efficient looping
- **functools** - Higher-order functions and operations on callable objects
- **threading, multiprocessing** - Concurrent execution
- **sqlite3** - SQLite database access
- **http.server** - Simple HTTP servers
- **urllib, requests** - URL handling and HTTP requests
- **json, csv, xml** - Data format handling

## Additional Resources

### Official Documentation

- [Python Official Website](https://www.python.org/)
- [Python 3.9 Documentation](https://docs.python.org/release/3.9.21/)
- [What's New in Python 3.9](https://docs.python.org/release/3.9.21/whatsnew/3.9.html)
- [Python Tutorial](https://docs.python.org/release/3.9.21/tutorial/index.html)
- [Python Standard Library](https://docs.python.org/release/3.9.21/library/index.html)
- [Python Language Reference](https://docs.python.org/release/3.9.21/reference/index.html)
- [Python Setup and Usage](https://docs.python.org/release/3.9.21/using/index.html)
- [Installing Python Modules](https://docs.python.org/release/3.9.21/installing/index.html)
- [Distributing Python Modules](https://docs.python.org/release/3.9.21/distributing/index.html)
- [Extending Python](https://docs.python.org/release/3.9.21/extending/index.html)
- [Python/C API Reference](https://docs.python.org/release/3.9.21/c-api/index.html)

### Testing Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Selenium with Python](https://selenium-python.readthedocs.io/)

### Interactive Learning

- [Python Tutor](http://pythontutor.com/) - Visualize code execution
- [Exercism Python Track](https://exercism.io/tracks/python)
- [HackerRank Python](https://www.hackerrank.com/domains/python)
- [LeetCode](https://leetcode.com/)

### Books

- "Python Crash Course" by Eric Matthes
- "Fluent Python" by Luciano Ramalho
- "Effective Python" by Brett Slatkin
- "Python Cookbook" by David Beazley and Brian K. Jones
- "Python Testing with pytest" by Brian Okken
