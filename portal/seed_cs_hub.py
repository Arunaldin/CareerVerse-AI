"""
Seed CS Learning Hub: Subjects, Topics, and Learning Paths
"""
import os
import sys
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portal.models import Subject, Topic, LearningPath, LearningPathStep

# ==============================================================================
# 1. SEED SUBJECTS
# ==============================================================================

SUBJECTS_DATA = [
    {
        "code": "python", "name": "Python Programming", "icon": "🐍",
        "accent_color": "#3b82f6", "order": 1, "difficulty_level": "All Levels",
        "description": "Master Python from fundamentals to advanced topics including OOP, file handling, exception handling and more."
    },
    {
        "code": "java", "name": "Java Programming", "icon": "☕",
        "accent_color": "#f59e0b", "order": 2, "difficulty_level": "All Levels",
        "description": "Learn Java programming from basics to advanced topics including Collections, Multithreading, and Enterprise concepts."
    },
    {
        "code": "c", "name": "C Programming", "icon": "🔵",
        "accent_color": "#6366f1", "order": 3, "difficulty_level": "All Levels",
        "description": "Foundation of programming – learn C with pointers, memory management, structures and algorithms."
    },
    {
        "code": "cpp", "name": "C++ Programming", "icon": "⚡",
        "accent_color": "#8b5cf6", "order": 4, "difficulty_level": "All Levels",
        "description": "Modern C++ including STL, templates, OOP, RAII and competitive programming techniques."
    },
    {
        "code": "javascript", "name": "JavaScript", "icon": "✨",
        "accent_color": "#f59e0b", "order": 5, "difficulty_level": "All Levels",
        "description": "Full JavaScript coverage including ES6+, async/await, DOM manipulation, and Node.js fundamentals."
    },
    {
        "code": "sql", "name": "SQL & Databases", "icon": "🗄️",
        "accent_color": "#10b981", "order": 6, "difficulty_level": "All Levels",
        "description": "Master SQL from basic SELECT to advanced window functions, stored procedures, and query optimization."
    },
    {
        "code": "dsa", "name": "Data Structures & Algorithms", "icon": "🌳",
        "accent_color": "#ef4444", "order": 7, "difficulty_level": "All Levels",
        "description": "Complete DSA curriculum with Big-O, arrays, trees, graphs, dynamic programming and competitive programming."
    },
    {
        "code": "dbms", "name": "Database Management Systems", "icon": "🏛️",
        "accent_color": "#0ea5e9", "order": 8, "difficulty_level": "Intermediate",
        "description": "DBMS theory: ER diagrams, normalization, ACID properties, transactions, indexing and query optimization."
    },
    {
        "code": "os", "name": "Operating Systems", "icon": "💻",
        "accent_color": "#6366f1", "order": 9, "difficulty_level": "Intermediate",
        "description": "OS fundamentals: processes, threads, scheduling, memory management, synchronization and file systems."
    },
    {
        "code": "cn", "name": "Computer Networks", "icon": "🌐",
        "accent_color": "#14b8a6", "order": 10, "difficulty_level": "Intermediate",
        "description": "OSI model, TCP/IP, DNS, HTTP, routing, subnetting, security and networking protocols."
    },
    {
        "code": "oop", "name": "Object-Oriented Programming", "icon": "🎯",
        "accent_color": "#a855f7", "order": 11, "difficulty_level": "Intermediate",
        "description": "OOP principles: encapsulation, abstraction, inheritance, polymorphism, SOLID and design patterns."
    },
    {
        "code": "se", "name": "Software Engineering", "icon": "🏗️",
        "accent_color": "#64748b", "order": 12, "difficulty_level": "Intermediate",
        "description": "SDLC, Agile, Scrum, testing, Git, CI/CD, documentation and software project management."
    },
    {
        "code": "sysdesign", "name": "System Design", "icon": "🏗️",
        "accent_color": "#f97316", "order": 13, "difficulty_level": "Advanced",
        "description": "Design scalable systems: load balancing, caching, databases, microservices, CAP theorem and more."
    },
    {
        "code": "ai", "name": "Artificial Intelligence", "icon": "🤖",
        "accent_color": "#ec4899", "order": 14, "difficulty_level": "Advanced",
        "description": "AI fundamentals, search algorithms, machine learning, neural networks and practical AI applications."
    },
    {
        "code": "cloud", "name": "Cloud Computing", "icon": "☁️",
        "accent_color": "#0284c7", "order": 15, "difficulty_level": "Intermediate",
        "description": "Cloud concepts, AWS/GCP/Azure fundamentals, serverless, containers, Kubernetes and DevOps."
    },
    {
        "code": "linux", "name": "Linux & Command Line", "icon": "🐧",
        "accent_color": "#854d0e", "order": 16, "difficulty_level": "Beginner",
        "description": "Linux basics, bash scripting, file system, process management, SSH, networking commands and automation."
    },
    {
        "code": "webdev", "name": "Web Development", "icon": "🌍",
        "accent_color": "#16a34a", "order": 17, "difficulty_level": "All Levels",
        "description": "HTML, CSS, JavaScript, responsive design, REST APIs, frontend frameworks and backend integration."
    },
    {
        "code": "ml", "name": "Machine Learning", "icon": "🧠",
        "accent_color": "#7c3aed", "order": 18, "difficulty_level": "Advanced",
        "description": "Supervised and unsupervised learning, regression, classification, model evaluation and deep learning intro."
    },
]

created_subjects = 0
for s in SUBJECTS_DATA:
    obj, created = Subject.objects.get_or_create(code=s['code'], defaults=s)
    if created:
        created_subjects += 1
    else:
        for k, v in s.items():
            setattr(obj, k, v)
        obj.save()

print(f"Subjects seeded: {Subject.objects.count()} total ({created_subjects} new)")

# ==============================================================================
# 2. SEED PYTHON TOPICS (Complete Curriculum)
# ==============================================================================

python_subj = Subject.objects.get(code='python')

PYTHON_TOPICS = [
    {
        "title": "Introduction to Python", "slug": "python-introduction",
        "summary": "What is Python, why use it, installation, and running your first program.",
        "content": """## What is Python?

Python is a high-level, interpreted, general-purpose programming language. Created by **Guido van Rossum** and first released in **1991**, Python emphasizes code readability and simplicity.

### Why Learn Python?

✅ **Simple & Readable** – Clean syntax that reads almost like English  
✅ **Versatile** – Web development, AI/ML, automation, data analysis, scripting  
✅ **Huge Community** – Millions of developers, thousands of libraries  
✅ **In Demand** – Top language for software engineering, data science, and AI  
✅ **Beginner Friendly** – Best first programming language for most learners  

### Where is Python Used?

- **Web Development**: Django, FastAPI, Flask
- **Data Science**: Pandas, NumPy, Matplotlib
- **Machine Learning**: TensorFlow, Scikit-learn, PyTorch
- **Automation**: Selenium, scripting, task automation
- **Backend APIs**: REST APIs, microservices

### Your First Python Program

```python
# This is a comment
print("Hello, World!")   # Output: Hello, World!

name = "CareerVerse"
print(f"Welcome to {name}!")  # f-strings interpolate variables
```

### Python Interactive Interpreter

Type `python` in your terminal to open the Python shell:
```
>>> 2 + 2
4
>>> print("Hello")
Hello
```""",
        "code_example": 'print("Hello, World!")\n\nname = input("Enter your name: ")\nprint(f"Welcome, {name}!")',
        "language": "python", "difficulty": "Beginner", "order": 1,
        "estimated_minutes": 20, "has_quiz": True,
        "key_points": ["Python is interpreted and dynamically typed", "Uses indentation for code blocks", "print() outputs to console", "Comments use the # symbol"],
        "interview_questions": [
            {"q": "What is Python? What are its key features?", "a": "Python is a high-level, interpreted, dynamically-typed language known for readability, versatility, and a large standard library. Key features: simple syntax, dynamic typing, garbage collection, and extensive libraries."},
            {"q": "Is Python interpreted or compiled?", "a": "Python is interpreted – code is executed line by line by the Python interpreter without a separate compilation step (though .pyc bytecode files are created internally)."},
        ]
    },
    {
        "title": "Variables and Data Types", "slug": "python-variables-datatypes",
        "summary": "Learn Python variables, naming rules, and the core data types: int, float, str, bool, None.",
        "content": """## Variables in Python

A **variable** is a named container that stores a value. Python does not require explicit type declaration.

```python
# Variable assignment
x = 10          # integer
price = 19.99   # float  
name = "Alice"  # string
is_valid = True # boolean
nothing = None  # NoneType
```

### Python Data Types

| Type | Example | Description |
|------|---------|-------------|
| `int` | `42`, `-7` | Whole numbers |
| `float` | `3.14`, `-0.5` | Decimal numbers |
| `str` | `"Hello"` | Text sequences |
| `bool` | `True`, `False` | Logical values |
| `None` | `None` | Absence of value |

### Type Checking and Conversion

```python
x = 42
print(type(x))       # <class 'int'>
print(isinstance(x, int))  # True

# Type conversion
s = str(100)         # "100"
n = int("42")        # 42
f = float("3.14")    # 3.14
b = bool(0)          # False
```

### Variable Naming Rules

✅ Start with a letter or underscore: `name`, `_value`  
✅ Can contain letters, digits, underscores: `user_name_2`  
✅ Case-sensitive: `Name` ≠ `name`  
❌ Cannot start with a digit: `2name` → Error  
❌ No spaces: `first name` → Error  
❌ No reserved keywords: `class`, `for`, `if` → Error  

### Python Naming Conventions

```python
# Variables and functions → snake_case
first_name = "Alice"
def calculate_tax():
    pass

# Constants → UPPER_SNAKE_CASE
MAX_SIZE = 100
PI = 3.14159

# Classes → PascalCase
class StudentProfile:
    pass
```""",
        "code_example": "age = 20\nname = 'Sugin'\nprice = 49.99\nis_free = True\n\nprint(type(age))    # int\nprint(type(price))  # float\nprint(type(name))   # str\n\n# Type conversion\nyear = int('2026')\nrating = float('9.5')\nprint(year, rating)",
        "language": "python", "difficulty": "Beginner", "order": 2,
        "estimated_minutes": 25, "has_quiz": True,
        "key_points": ["No type declarations needed", "Use type() to check type", "isinstance() for type checking", "snake_case for variable names"],
        "interview_questions": [
            {"q": "What are Python's basic data types?", "a": "int, float, str, bool, None, list, tuple, dict, set."},
            {"q": "What is the difference between int and float?", "a": "int stores whole numbers without decimal point; float stores numbers with decimal point. Division (/) always returns float; floor division (//) returns int."},
        ]
    },
    {
        "title": "Operators in Python", "slug": "python-operators",
        "summary": "Arithmetic, comparison, logical, assignment, bitwise and membership operators.",
        "content": """## Python Operators

### 1. Arithmetic Operators
```python
a, b = 10, 3
print(a + b)   # 13  Addition
print(a - b)   # 7   Subtraction
print(a * b)   # 30  Multiplication
print(a / b)   # 3.333  Division (float)
print(a // b)  # 3   Floor Division (int)
print(a % b)   # 1   Modulo (remainder)
print(a ** b)  # 1000 Exponentiation
```

### 2. Comparison Operators
```python
x, y = 5, 10
print(x == y)  # False  Equal
print(x != y)  # True   Not equal
print(x > y)   # False  Greater than
print(x < y)   # True   Less than
print(x >= y)  # False  Greater than or equal
print(x <= y)  # True   Less than or equal
```

### 3. Logical Operators
```python
print(True and False)  # False
print(True or False)   # True
print(not True)        # False

# Short-circuit evaluation
x = 5
print(x > 0 and x < 10)  # True
print(x < 0 or x > 3)    # True
```

### 4. Assignment Operators
```python
n = 10
n += 5   # n = 15
n -= 3   # n = 12
n *= 2   # n = 24
n //= 5  # n = 4
n **= 2  # n = 16
```

### 5. Membership and Identity Operators
```python
lst = [1, 2, 3]
print(2 in lst)       # True
print(5 not in lst)   # True

a = [1, 2]
b = a
print(a is b)         # True (same object)
print(a is not [])    # True
```""",
        "code_example": "# Try all operators\na, b = 15, 4\nprint(f'{a} + {b} = {a + b}')\nprint(f'{a} % {b} = {a % b}')\nprint(f'{a} ** 2 = {a ** 2}')\n\n# Comparison\nprint(f'Is {a} divisible by {b}? {a % b == 0}')\n\n# Logical\nage = 20\nprint(f'Adult: {age >= 18 and age <= 60}')",
        "language": "python", "difficulty": "Beginner", "order": 3,
        "estimated_minutes": 20, "has_quiz": True,
        "key_points": ["/ returns float, // returns int", "** is exponentiation", "and/or/not are logical operators", "in checks membership"],
        "interview_questions": [
            {"q": "What is the difference between / and // in Python?", "a": "/ is true division and always returns a float. // is floor division and returns the largest integer less than or equal to the result."},
        ]
    },
    {
        "title": "Conditional Statements", "slug": "python-conditionals",
        "summary": "if, elif, else – control program flow based on conditions.",
        "content": """## Conditional Statements

Control program flow using `if`, `elif`, and `else`.

```python
# Basic if-else
age = 20
if age >= 18:
    print("Adult")
else:
    print("Minor")

# elif chain
marks = 75
if marks >= 90:
    grade = 'A+'
elif marks >= 80:
    grade = 'A'
elif marks >= 70:
    grade = 'B'
elif marks >= 60:
    grade = 'C'
else:
    grade = 'F'
print(f"Grade: {grade}")  # Grade: B
```

### Nested Conditions
```python
x = 15
if x > 0:
    if x % 2 == 0:
        print("Positive even")
    else:
        print("Positive odd")  # This prints
else:
    print("Non-positive")
```

### Ternary Expression (Inline if)
```python
# one-liner conditional
n = 10
result = "even" if n % 2 == 0 else "odd"
print(result)  # even
```

### Truthy and Falsy Values
```python
# Falsy values: 0, 0.0, "", [], {}, None, False
# Everything else is truthy

if []:         # Falsy
    print("Not printed")

if [1, 2, 3]:  # Truthy
    print("Printed")
```""",
        "code_example": "# Grade calculator\nscore = int(input('Enter your score (0-100): '))\n\nif score >= 90:\n    grade, msg = 'A+', '🌟 Outstanding!'\nelif score >= 80:\n    grade, msg = 'A', '🎉 Excellent!'\nelif score >= 70:\n    grade, msg = 'B', '👍 Good job!'\nelif score >= 60:\n    grade, msg = 'C', '📚 Keep going!'\nelse:\n    grade, msg = 'F', '💪 Try harder!'\n\nprint(f'Grade: {grade} - {msg}')",
        "language": "python", "difficulty": "Beginner", "order": 4,
        "estimated_minutes": 25, "has_quiz": True,
        "key_points": ["Indentation defines blocks", "elif for multiple conditions", "Ternary: x if condition else y", "0, None, [], {} are falsy"],
        "interview_questions": [
            {"q": "What is the difference between if-elif-else and multiple if statements?", "a": "if-elif-else is a mutually exclusive chain – only one block executes. Multiple separate if statements are evaluated independently – multiple blocks can execute."},
        ]
    },
    {
        "title": "Loops in Python", "slug": "python-loops",
        "summary": "for loops, while loops, range(), break, continue, pass and loop-else.",
        "content": """## Python Loops

### for Loop
```python
# Iterate over a range
for i in range(5):
    print(i)        # 0 1 2 3 4

# range(start, stop, step)
for i in range(1, 11, 2):
    print(i)        # 1 3 5 7 9

# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Enumerate gives index and value
for idx, fruit in enumerate(fruits, start=1):
    print(f"{idx}. {fruit}")
```

### while Loop
```python
count = 0
while count < 5:
    print(count)
    count += 1      # 0 1 2 3 4

# Infinite loop with break
while True:
    answer = input("Type 'quit' to exit: ")
    if answer == "quit":
        break
    print(f"You said: {answer}")
```

### break, continue, pass
```python
# break: exit loop immediately
for i in range(10):
    if i == 5:
        break
    print(i)        # 0 1 2 3 4

# continue: skip current iteration
for i in range(10):
    if i % 2 == 0:
        continue    # skip even
    print(i)        # 1 3 5 7 9

# pass: placeholder (does nothing)
for i in range(5):
    pass            # valid empty block
```

### Nested Loops
```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}x{j}={i*j}", end="  ")
    print()
```

### Loop-else
```python
# else runs if loop completes without break
for n in [2, 4, 6]:
    if n % 2 != 0:
        break
else:
    print("All numbers are even!")  # Prints
```""",
        "code_example": "# Print triangle pattern\nfor i in range(1, 6):\n    print('*' * i)\n\nprint('---')\n\n# Sum of digits\nnum = int(input('Enter number: '))\ntotal = 0\nwhile num > 0:\n    total += num % 10\n    num //= 10\nprint(f'Sum of digits: {total}')",
        "language": "python", "difficulty": "Beginner", "order": 5,
        "estimated_minutes": 30, "has_quiz": True,
        "key_points": ["range(start, stop, step)", "break exits, continue skips", "enumerate() gives index + value", "Loop else runs if no break occurred"],
        "interview_questions": [
            {"q": "What is the difference between break and continue?", "a": "break immediately exits the entire loop. continue skips the rest of the current iteration and moves to the next one."},
            {"q": "How does loop-else work in Python?", "a": "The else block of a loop executes when the loop finishes normally (without hitting a break statement)."},
        ]
    },
    {
        "title": "Functions in Python", "slug": "python-functions",
        "summary": "Defining functions, parameters, return values, *args, **kwargs, and lambda.",
        "content": """## Python Functions

### Defining and Calling Functions
```python
def greet(name):
    \"\"\"This is a docstring – explains the function.\"\"\"
    return f"Hello, {name}!"

message = greet("Alice")
print(message)  # Hello, Alice!
```

### Default Parameters
```python
def power(base, exponent=2):
    return base ** exponent

print(power(3))     # 9  (uses default exponent=2)
print(power(3, 3))  # 27
```

### *args and **kwargs
```python
# *args: variable positional arguments → tuple
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3, 4))  # 10

# **kwargs: variable keyword arguments → dict
def describe(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

describe(name="Alice", age=20, city="Chennai")
```

### Lambda Functions
```python
# Anonymous single-expression function
square = lambda x: x ** 2
print(square(5))    # 25

# Common with sorted(), map(), filter()
nums = [3, 1, 4, 1, 5]
nums.sort(key=lambda x: -x)  # Sort descending
print(nums)  # [5, 4, 3, 1, 1]

# map and filter
evens = list(filter(lambda x: x % 2 == 0, range(10)))
squares = list(map(lambda x: x**2, range(5)))
```

### Scope: LEGB Rule
```python
x = 10  # Global scope

def outer():
    y = 20  # Enclosing scope
    def inner():
        z = 30  # Local scope
        print(x, y, z)  # 10 20 30
    inner()

outer()
```""",
        "code_example": "# Calculator with functions\ndef add(a, b): return a + b\ndef subtract(a, b): return a - b\ndef multiply(a, b): return a * b\ndef divide(a, b): return a / b if b != 0 else 'Error: Division by zero'\n\noperations = {'+': add, '-': subtract, '*': multiply, '/': divide}\n\na = float(input('First number: '))\nop = input('Operator (+,-,*,/): ')\nb = float(input('Second number: '))\n\nresult = operations[op](a, b)\nprint(f'{a} {op} {b} = {result}')",
        "language": "python", "difficulty": "Easy", "order": 6,
        "estimated_minutes": 35, "has_quiz": True,
        "key_points": ["def keyword defines functions", "return sends value back", "*args for variable positional", "**kwargs for variable keyword", "lambda for simple one-liners"],
        "interview_questions": [
            {"q": "What is the difference between *args and **kwargs?", "a": "*args captures extra positional arguments as a tuple. **kwargs captures extra keyword arguments as a dictionary."},
            {"q": "What is a lambda function?", "a": "A lambda is an anonymous single-expression function. lambda args: expression. Used for short throwaway functions with map, filter, sort."},
        ]
    },
    {
        "title": "Lists and List Methods", "slug": "python-lists",
        "summary": "Creating, indexing, slicing, and manipulating Python lists with built-in methods.",
        "content": """## Python Lists

Lists are ordered, mutable, indexed collections that can hold any type.

### Creating Lists
```python
# Empty list
empty = []

# List with values
nums = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2], [3, 4], [5, 6]]
```

### Indexing and Slicing
```python
lst = [10, 20, 30, 40, 50]
print(lst[0])    # 10  (first element)
print(lst[-1])   # 50  (last element)
print(lst[1:3])  # [20, 30]  (slice)
print(lst[::-1]) # [50, 40, 30, 20, 10]  (reversed)
print(lst[::2])  # [10, 30, 50]  (every 2nd)
```

### Common List Methods
```python
lst = [3, 1, 4, 1, 5, 9, 2, 6]

lst.append(7)         # Add to end
lst.insert(2, 99)     # Insert at index 2
lst.extend([10, 11])  # Extend with another list
lst.remove(1)         # Remove first occurrence of 1
popped = lst.pop()    # Remove and return last element
lst.sort()            # Sort in-place
lst.reverse()         # Reverse in-place
lst.clear()           # Remove all elements

lst2 = [3, 1, 4, 1, 5]
print(lst2.count(1))  # 2  (count occurrences)
print(lst2.index(4))  # 2  (index of first 4)
copy = lst2.copy()    # Shallow copy
```

### List Comprehensions
```python
# [expression for item in iterable if condition]
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [item for sublist in nested for item in sublist]
```

### Useful Built-in Functions
```python
nums = [4, 2, 7, 1, 9, 3]
print(len(nums))       # 6
print(min(nums))       # 1
print(max(nums))       # 9
print(sum(nums))       # 26
print(sorted(nums))    # [1, 2, 3, 4, 7, 9] (new list)
print(list(reversed(nums)))  # [3, 9, 1, 7, 2, 4]
```""",
        "code_example": "# Remove duplicates while preserving order\ndef remove_duplicates(lst):\n    seen = set()\n    return [x for x in lst if not (x in seen or seen.add(x))]\n\n# Flatten nested list\ndef flatten(nested):\n    return [item for sublist in nested for item in sublist]\n\nnums = [1, 2, 2, 3, 4, 3, 5]\nprint('Deduped:', remove_duplicates(nums))\n\nnested = [[1, 2], [3, 4], [5]]\nprint('Flattened:', flatten(nested))",
        "language": "python", "difficulty": "Easy", "order": 7,
        "estimated_minutes": 30, "has_quiz": True,
        "key_points": ["Lists are mutable and ordered", "Slicing: lst[start:stop:step]", "append vs extend vs insert", "List comprehension: [expr for x in lst]"],
        "interview_questions": [
            {"q": "What is the difference between append() and extend()?", "a": "append() adds a single element to the end. extend() adds all elements of an iterable to the end. append([1,2]) adds the list as one element; extend([1,2]) adds 1 and 2 separately."},
        ]
    },
    {
        "title": "Strings and String Methods", "slug": "python-strings",
        "summary": "String operations, f-strings, slicing, and essential built-in string methods.",
        "content": """## Python Strings

Strings are immutable sequences of Unicode characters.

### Creating Strings
```python
s1 = 'Single quotes'
s2 = "Double quotes"
s3 = '''Multi-line
string'''
s4 = r"Raw string \\n (backslash not escaped)"
```

### String Formatting
```python
name = "Alice"
score = 95.5
# f-strings (preferred – Python 3.6+)
print(f"Name: {name}, Score: {score:.1f}")

# format() method
print("Name: {}, Score: {:.1f}".format(name, score))
```

### String Indexing and Slicing
```python
s = "Python"
print(s[0])     # P
print(s[-1])    # n
print(s[1:4])   # yth
print(s[::-1])  # nohtyP (reversed)
```

### Essential String Methods
```python
s = "  Hello, World!  "

s.strip()           # "Hello, World!"  Remove whitespace
s.lower()           # "  hello, world!  "
s.upper()           # "  HELLO, WORLD!  "
s.replace("World", "Python")
s.split(", ")       # ['Hello', 'World!']
s.startswith("Hello")  # True (after strip)
s.endswith("!")        # True (after strip)
s.find("World")     # 7 (index) or -1
s.count("l")        # 3
s.isdigit()         # False
s.isalpha()         # False (has spaces/punctuation)
"  ".join(["a", "b", "c"])  # "a  b  c"
```

### String Immutability
```python
s = "hello"
# s[0] = "H"  # ERROR! Strings are immutable
s = "H" + s[1:]  # Create a new string
print(s)  # Hello
```""",
        "code_example": "# Count words, sentences and unique characters\ntext = input('Enter a paragraph: ')\n\nwords = text.split()\nword_count = len(words)\nchar_count = len(text.replace(' ', ''))\nunique_chars = len(set(text.lower().replace(' ', '')))\nsentences = text.count('.') + text.count('!') + text.count('?')\n\nprint(f'Words: {word_count}')\nprint(f'Characters (no spaces): {char_count}')\nprint(f'Unique characters: {unique_chars}')\nprint(f'Sentences: {sentences}')",
        "language": "python", "difficulty": "Easy", "order": 8,
        "estimated_minutes": 30, "has_quiz": True,
        "key_points": ["Strings are immutable", "f-strings are the modern way to format", "split() returns a list", "join() is the inverse of split()"],
        "interview_questions": [
            {"q": "Are Python strings mutable or immutable?", "a": "Immutable. You cannot modify a string in place; every operation creates a new string object."},
        ]
    },
    {
        "title": "Dictionaries", "slug": "python-dictionaries",
        "summary": "Key-value mappings, dict methods, comprehensions, and common patterns.",
        "content": """## Python Dictionaries

Dictionaries store data as **key: value** pairs. Keys must be unique and immutable.

### Creating Dictionaries
```python
# Empty dict
d = {}
d = dict()

# With values
person = {
    "name": "Alice",
    "age": 20,
    "skills": ["Python", "SQL"]
}

# dict() constructor
config = dict(host="localhost", port=5432, debug=True)
```

### Accessing and Modifying
```python
person = {"name": "Alice", "age": 20}

# Access
print(person["name"])         # Alice
print(person.get("age"))      # 20
print(person.get("city", "Unknown"))  # Unknown (default)

# Modify
person["age"] = 21
person["city"] = "Chennai"   # Add new key
del person["age"]             # Remove key

# Check key
print("name" in person)       # True
```

### Dictionary Methods
```python
d = {"a": 1, "b": 2, "c": 3}

d.keys()         # dict_keys(['a', 'b', 'c'])
d.values()       # dict_values([1, 2, 3])
d.items()        # dict_items([('a', 1), ('b', 2), ('c', 3)])

d.update({"d": 4})  # Merge another dict
d.pop("b")           # Remove and return value for 'b'
d.setdefault("e", 0) # Set if key not present

# Iterating
for key, value in d.items():
    print(f"{key}: {value}")
```

### Dictionary Comprehensions
```python
# Square of each number
squares = {n: n**2 for n in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter dict
large = {k: v for k, v in squares.items() if v > 10}
```""",
        "code_example": "# Word frequency counter\ntext = 'the cat sat on the mat the cat is fat'\nwords = text.split()\n\nfreq = {}\nfor word in words:\n    freq[word] = freq.get(word, 0) + 1\n\n# Sort by frequency descending\nsorted_freq = dict(sorted(freq.items(), key=lambda x: -x[1]))\n\nfor word, count in sorted_freq.items():\n    print(f'{word}: {count}')",
        "language": "python", "difficulty": "Easy", "order": 9,
        "estimated_minutes": 30, "has_quiz": True,
        "key_points": ["Keys must be hashable (immutable)", "get() avoids KeyError", "items() gives (key, value) tuples", "Dict comprehension: {k: v for k, v in items}"],
        "interview_questions": [
            {"q": "What is the time complexity of dict lookup?", "a": "O(1) average case. Python dictionaries are implemented as hash tables."},
        ]
    },
    {
        "title": "Tuples and Sets", "slug": "python-tuples-sets",
        "summary": "Tuples (immutable sequences) and Sets (unique unordered collections).",
        "content": """## Tuples

Tuples are **immutable** ordered sequences. Use when data should not change.

```python
# Creating tuples
t1 = (1, 2, 3)
t2 = 1, 2, 3     # No parentheses needed
single = (1,)    # Single element MUST have trailing comma
empty = ()

# Indexing (same as list)
print(t1[0])     # 1
print(t1[-1])    # 3

# Unpacking
a, b, c = (10, 20, 30)
x, *rest = (1, 2, 3, 4, 5)  # x=1, rest=[2,3,4,5]

# Named tuples
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(p.x, p.y)   # 3 4
```

## Sets

Sets are **unordered collections of unique elements**.

```python
# Creating sets
s1 = {1, 2, 3, 4}
s2 = set([1, 2, 2, 3])  # Duplicates removed → {1, 2, 3}
empty_set = set()   # NOT {} (that's a dict)

# Set operations
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

print(A | B)   # {1,2,3,4,5,6,7,8} Union
print(A & B)   # {4, 5}            Intersection
print(A - B)   # {1, 2, 3}         Difference
print(A ^ B)   # {1,2,3,6,7,8}    Symmetric difference

# Membership check: O(1) average
print(3 in A)  # True

# Adding and removing
A.add(6)
A.discard(1)   # Remove if present (no error if missing)
A.remove(2)    # Remove (raises KeyError if missing)
```""",
        "code_example": "# Remove duplicates from list\nlst = [1, 2, 2, 3, 4, 3, 5, 5]\nunique = list(set(lst))\nprint('Unique:', sorted(unique))\n\n# Common elements in two lists\nlist1 = [1, 2, 3, 4, 5]\nlist2 = [3, 4, 5, 6, 7]\ncommon = list(set(list1) & set(list2))\nprint('Common:', sorted(common))\n\n# Tuple unpacking\ncoordinates = [(0, 0), (1, 2), (3, 4)]\nfor x, y in coordinates:\n    dist = (x**2 + y**2) ** 0.5\n    print(f'Point ({x},{y}) distance from origin: {dist:.2f}')",
        "language": "python", "difficulty": "Easy", "order": 10,
        "estimated_minutes": 25, "has_quiz": True,
        "key_points": ["Tuples are immutable", "Single element tuple needs trailing comma: (1,)", "Sets have no duplicates and are unordered", "Set lookup is O(1)"],
        "interview_questions": [
            {"q": "When would you use a tuple instead of a list?", "a": "When data should not change (immutability), as dictionary keys (lists cannot be keys), when memory efficiency matters, or for unpacking multiple return values from functions."},
        ]
    },
    {
        "title": "Object-Oriented Programming in Python", "slug": "python-oop",
        "summary": "Classes, objects, __init__, inheritance, encapsulation, polymorphism and special methods.",
        "content": """## OOP in Python

### Classes and Objects
```python
class Student:
    # Class variable (shared by all instances)
    college = "CareerVerse University"

    def __init__(self, name, age, cgpa):
        # Instance variables (unique to each object)
        self.name = name
        self.age = age
        self.cgpa = cgpa

    def study(self, subject):
        return f"{self.name} is studying {subject}"

    def __str__(self):
        return f"Student({self.name}, CGPA: {self.cgpa})"

    def __repr__(self):
        return f"Student(name='{self.name}', age={self.age}, cgpa={self.cgpa})"

# Creating objects
s1 = Student("Alice", 20, 8.5)
s2 = Student("Bob", 21, 7.8)

print(s1.study("Python"))  # Alice is studying Python
print(s1)                  # Student(Alice, CGPA: 8.5)
print(Student.college)     # CareerVerse University
```

### Inheritance
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hi, I'm {self.name}"

class Employee(Person):  # Inherits from Person
    def __init__(self, name, age, salary):
        super().__init__(name, age)  # Call parent __init__
        self.salary = salary

    def greet(self):  # Override parent method
        return f"Hi, I'm {self.name} and I earn ₹{self.salary}/month"

e = Employee("Alice", 25, 50000)
print(e.greet())       # Polymorphism
print(e.age)           # Inherited from Person
```

### Properties and Encapsulation
```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance   # Private attribute (name mangling)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = amount

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance
```""",
        "code_example": "class Shape:\n    def area(self): return 0\n    def perimeter(self): return 0\n\nclass Circle(Shape):\n    PI = 3.14159\n    def __init__(self, r): self.r = r\n    def area(self): return self.PI * self.r ** 2\n    def perimeter(self): return 2 * self.PI * self.r\n\nclass Rectangle(Shape):\n    def __init__(self, l, w): self.l, self.w = l, w\n    def area(self): return self.l * self.w\n    def perimeter(self): return 2 * (self.l + self.w)\n\nshapes = [Circle(5), Rectangle(4, 6), Circle(3)]\nfor shape in shapes:\n    print(f'{type(shape).__name__}: area={shape.area():.2f}')",
        "language": "python", "difficulty": "Medium", "order": 11,
        "estimated_minutes": 45, "has_quiz": True,
        "key_points": ["__init__ is the constructor", "self refers to the current instance", "super() calls parent class methods", "@property creates managed attributes"],
        "interview_questions": [
            {"q": "What is the difference between class variables and instance variables?", "a": "Class variables are shared across all instances and defined directly in the class body. Instance variables are unique to each object and defined with self in __init__."},
            {"q": "What are the four pillars of OOP?", "a": "Encapsulation (data hiding), Abstraction (hiding complexity), Inheritance (code reuse from parent class), Polymorphism (same interface, different behavior)."},
        ]
    },
]

created_topics = 0
for t_data in PYTHON_TOPICS:
    topic, created = Topic.objects.get_or_create(
        slug=t_data['slug'],
        defaults={**t_data, 'subject': python_subj}
    )
    if not created:
        for k, v in t_data.items():
            setattr(topic, k, v)
        topic.subject = python_subj
        topic.save()
    if created:
        created_topics += 1

print(f"Python topics seeded: {Topic.objects.filter(subject=python_subj).count()} total")

# ==============================================================================
# 3. SEED DSA TOPICS
# ==============================================================================

dsa_subj = Subject.objects.get(code='dsa')

DSA_TOPICS = [
    {
        "title": "Introduction to DSA and Big-O Notation", "slug": "dsa-intro-big-o",
        "summary": "What is DSA, why it matters, time complexity, space complexity, and Big-O notation.",
        "content": """## Data Structures & Algorithms

### Why DSA?

Every top tech company (Amazon, Google, Microsoft, Zoho, TCS) tests DSA in their coding rounds. DSA helps you:

- Write **faster programs** that scale
- **Solve problems** systematically
- **Pass technical interviews**
- **Think algorithmically**

### Big-O Notation

Big-O describes how an algorithm's time or space requirement **grows with input size n**.

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array index access |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Loop through array |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Recursive subset generation |
| O(n!) | Factorial | Brute force permutations |

### Time Complexity Analysis
```python
# O(1) - Constant time
def get_first(arr):
    return arr[0]           # Always 1 operation

# O(n) - Linear time
def find_max(arr):
    max_val = arr[0]
    for x in arr:           # n iterations
        if x > max_val:
            max_val = x
    return max_val

# O(n²) - Quadratic time
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):        # n iterations
        for j in range(n-1):  # n-1 iterations each
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
```

### Space Complexity
```python
# O(1) space - no extra space with input size
def reverse_in_place(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

# O(n) space - creates new array same size as input
def reverse_copy(arr):
    return arr[::-1]
```""",
        "code_example": "import time\n\ndef linear_search(arr, target):\n    for i, x in enumerate(arr):\n        if x == target:\n            return i\n    return -1\n\ndef binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    steps = 0\n    while left <= right:\n        steps += 1\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            print(f'Binary search found in {steps} steps')\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\narr = list(range(1, 1001))\nprint('Linear:', linear_search(arr, 999))\nbinary_search(arr, 999)",
        "language": "python", "difficulty": "Beginner", "order": 1,
        "estimated_minutes": 30, "has_quiz": True,
        "key_points": ["Big-O describes worst-case growth", "O(1) < O(log n) < O(n) < O(n log n) < O(n²)", "Drop constants and lower-order terms", "Space complexity also matters"],
        "interview_questions": [
            {"q": "What is the difference between time complexity and space complexity?", "a": "Time complexity measures how running time grows with input size. Space complexity measures how memory usage grows with input size."},
            {"q": "What is the best, worst, and average case complexity of linear search?", "a": "Best: O(1) – element is at index 0. Worst: O(n) – element is last or not present. Average: O(n/2) = O(n)."},
        ]
    },
    {
        "title": "Arrays and Array Algorithms", "slug": "dsa-arrays",
        "summary": "Array operations, two-pointer technique, prefix sums and sliding window.",
        "content": """## Arrays

An array is a **fixed-size sequential collection** of elements of the same type stored in contiguous memory.

In Python, `list` is a dynamic array. In C/Java, arrays have fixed sizes.

### Core Array Operations
| Operation | Time Complexity |
|-----------|----------------|
| Access arr[i] | O(1) |
| Search (unsorted) | O(n) |
| Search (sorted) | O(log n) |
| Insert at end | O(1) amortized |
| Insert at index | O(n) |
| Delete from end | O(1) |
| Delete from index | O(n) |

### Two-Pointer Technique
Used for sorted arrays or when dealing with pairs:

```python
def two_sum_sorted(arr, target):
    \"\"\"Find pair summing to target in SORTED array\"\"\"
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

def remove_duplicates_sorted(arr):
    \"\"\"Remove duplicates in-place, return new length\"\"\"
    if not arr:
        return 0
    write = 1
    for read in range(1, len(arr)):
        if arr[read] != arr[write - 1]:
            arr[write] = arr[read]
            write += 1
    return write
```

### Sliding Window Technique
For subarrays or substrings:

```python
def max_sum_subarray_k(arr, k):
    \"\"\"Maximum sum of subarray of length k\"\"\"
    if len(arr) < k:
        return None
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

def smallest_subarray_with_sum_k(arr, target):
    \"\"\"Minimum length subarray with sum >= target\"\"\"
    min_len = float('inf')
    left = window_sum = 0
    for right in range(len(arr)):
        window_sum += arr[right]
        while window_sum >= target:
            min_len = min(min_len, right - left + 1)
            window_sum -= arr[left]
            left += 1
    return min_len if min_len != float('inf') else 0
```

### Prefix Sum
```python
def build_prefix(arr):
    prefix = [0] * (len(arr) + 1)
    for i, x in enumerate(arr):
        prefix[i+1] = prefix[i] + x
    return prefix

def range_sum(prefix, l, r):
    return prefix[r+1] - prefix[l]  # O(1) range query
```""",
        "code_example": "# Dutch National Flag (3-way partition)\ndef sort_colors(arr):\n    low, mid, high = 0, 0, len(arr) - 1\n    while mid <= high:\n        if arr[mid] == 0:\n            arr[low], arr[mid] = arr[mid], arr[low]\n            low += 1; mid += 1\n        elif arr[mid] == 1:\n            mid += 1\n        else:\n            arr[mid], arr[high] = arr[high], arr[mid]\n            high -= 1\n    return arr\n\ncolors = [2, 0, 1, 1, 2, 0]\nprint('Sorted 0s, 1s, 2s:', sort_colors(colors))",
        "language": "python", "difficulty": "Easy", "order": 2,
        "estimated_minutes": 40, "has_quiz": True,
        "key_points": ["Random access O(1), insertion/deletion O(n)", "Two pointers for sorted arrays", "Sliding window for subarray problems", "Prefix sum for range sum queries"],
        "interview_questions": [
            {"q": "What is the time complexity of inserting an element at the beginning of an array?", "a": "O(n) because all existing elements must be shifted one position to the right."},
        ]
    },
    {
        "title": "Linked Lists", "slug": "dsa-linked-lists",
        "summary": "Singly and doubly linked lists, node operations, cycle detection and reversal.",
        "content": """## Linked Lists

A linked list is a **linear data structure** where each node points to the next.

```
[Data|Next] → [Data|Next] → [Data|Next] → None
```

### Singly Linked List Implementation
```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        new_node = Node(val)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def prepend(self, val):
        new_node = Node(val)
        new_node.next = self.head
        self.head = new_node

    def delete(self, val):
        if not self.head:
            return
        if self.head.val == val:
            self.head = self.head.next
            return
        curr = self.head
        while curr.next and curr.next.val != val:
            curr = curr.next
        if curr.next:
            curr.next = curr.next.next

    def print_list(self):
        values = []
        curr = self.head
        while curr:
            values.append(str(curr.val))
            curr = curr.next
        print(" → ".join(values) + " → None")
```

### Key Algorithms
```python
# Reverse a linked list
def reverse_list(head):
    prev, curr = None, head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# Floyd's Cycle Detection
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find middle node
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow   # slow points to middle
```

### Linked List vs Array
| | Array | Linked List |
|--|-------|-------------|
| Access | O(1) | O(n) |
| Insert front | O(n) | O(1) |
| Insert back | O(1) | O(n) or O(1) with tail |
| Delete front | O(n) | O(1) |
| Memory | Contiguous | Scattered |""",
        "code_example": "class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n\ndef reverse_list(head):\n    prev, curr = None, head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev\n\n# Create: 1 -> 2 -> 3 -> 4 -> 5\nhead = Node(1)\nfor v in [2, 3, 4, 5]:\n    curr = head\n    while curr.next: curr = curr.next\n    curr.next = Node(v)\n\n# Reverse it\nrev = reverse_list(head)\ncurr = rev\nwhile curr:\n    print(curr.val, end=' -> ' if curr.next else ' -> None\\n')\n    curr = curr.next",
        "language": "python", "difficulty": "Medium", "order": 3,
        "estimated_minutes": 40, "has_quiz": True,
        "key_points": ["Each node has data and a next pointer", "Reversal uses three pointers (prev, curr, next)", "Floyd's algorithm detects cycles with O(1) space", "Doubly linked list allows O(1) backward traversal"],
        "interview_questions": [
            {"q": "How do you detect a cycle in a linked list?", "a": "Floyd's Tortoise and Hare algorithm. Use two pointers – slow (moves 1 step) and fast (moves 2 steps). If they ever meet, there is a cycle. Time O(n), Space O(1)."},
        ]
    },
    {
        "title": "Stacks and Queues", "slug": "dsa-stacks-queues",
        "summary": "Stack (LIFO) and Queue (FIFO) operations, monotonic stacks and deque.",
        "content": """## Stacks

A **stack** follows LIFO – Last In, First Out.

```python
# Using Python list as stack
stack = []
stack.append(10)   # push
stack.append(20)
stack.append(30)
print(stack.pop()) # 30 (LIFO)
print(stack[-1])   # 20 (peek without removing)
```

### Stack Applications
```python
# Check balanced parentheses
def is_balanced(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in '({[':
            stack.append(ch)
        elif ch in ')}]':
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0

# Daily temperatures (monotonic stack)
def daily_temperatures(temps):
    result = [0] * len(temps)
    stack = []  # stores indices
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    return result
```

## Queues

A **queue** follows FIFO – First In, First Out.

```python
from collections import deque

queue = deque()
queue.append(10)    # enqueue (right end)
queue.append(20)
queue.append(30)
print(queue.popleft())  # 10 (FIFO)
print(queue[0])         # 20 (peek front)
```

### Priority Queue (Heap)
```python
import heapq

pq = []
heapq.heappush(pq, 3)
heapq.heappush(pq, 1)
heapq.heappush(pq, 2)
print(heapq.heappop(pq))  # 1 (minimum first)
```""",
        "code_example": "from collections import deque\n\n# BFS using queue\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    order = []\n    while queue:\n        node = queue.popleft()\n        order.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n    return order\n\ngraph = {1: [2, 3], 2: [4], 3: [4, 5], 4: [], 5: []}\nprint('BFS order:', bfs(graph, 1))",
        "language": "python", "difficulty": "Medium", "order": 4,
        "estimated_minutes": 35, "has_quiz": True,
        "key_points": ["Stack: LIFO – last in, first out", "Queue: FIFO – first in, first out", "deque is O(1) for both ends", "Monotonic stacks solve next-greater-element problems"],
        "interview_questions": [
            {"q": "What is the difference between a Stack and a Queue?", "a": "Stack is LIFO (Last In First Out) – elements are added and removed from the same end (top). Queue is FIFO (First In First Out) – elements are added at the rear and removed from the front."},
        ]
    },
    {
        "title": "Dynamic Programming", "slug": "dsa-dynamic-programming",
        "summary": "Memoization, tabulation, overlapping subproblems and optimal substructure.",
        "content": """## Dynamic Programming (DP)

DP solves complex problems by breaking them into simpler **overlapping subproblems** and storing results to avoid recomputation.

**Two conditions for DP:**
1. **Overlapping Subproblems** – same subproblems solved repeatedly
2. **Optimal Substructure** – optimal solution built from optimal subsolutions

### Two Approaches

**1. Memoization (Top-Down)**
```python
# Fibonacci with memoization
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

# Or using functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n-1) + fib_cached(n-2)
```

**2. Tabulation (Bottom-Up)**
```python
# Fibonacci with tabulation
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Space optimized
def fib_opt(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### Classic DP: Coin Change
```python
def coin_change(coins, amount):
    \"\"\"Minimum coins to make 'amount'\"\"\"
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change([1, 5, 6, 9], 11))  # 2 (5+6)
```

### Classic DP: 0/1 Knapsack
```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i-1][w]
            # Take item i if it fits
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i-1][w - weights[i-1]] + values[i-1])
    return dp[n][capacity]
```""",
        "code_example": "# Longest Common Subsequence (LCS)\ndef lcs(s1, s2):\n    m, n = len(s1), len(s2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if s1[i-1] == s2[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]\n\nprint(lcs('ABCBDAB', 'BDCAB'))  # 4 (BCAB)",
        "language": "python", "difficulty": "Hard", "order": 5,
        "estimated_minutes": 60, "has_quiz": True,
        "key_points": ["Identify overlapping subproblems", "Memoization = top-down with cache", "Tabulation = bottom-up with table", "Always define base cases clearly"],
        "interview_questions": [
            {"q": "What is dynamic programming and when do you use it?", "a": "DP is an optimization technique that stores solutions to subproblems to avoid recomputation. Use it when a problem has overlapping subproblems and optimal substructure."},
            {"q": "What is the difference between memoization and tabulation?", "a": "Memoization is top-down: recursively solve and cache results. Tabulation is bottom-up: iteratively build a table from base cases. Both have same time complexity but tabulation avoids recursion overhead."},
        ]
    },
]

created_dsa = 0
for t_data in DSA_TOPICS:
    topic, created = Topic.objects.get_or_create(
        slug=t_data['slug'],
        defaults={**t_data, 'subject': dsa_subj}
    )
    if not created:
        for k, v in t_data.items():
            setattr(topic, k, v)
        topic.subject = dsa_subj
        topic.save()
    if created:
        created_dsa += 1

print(f"DSA topics seeded: {Topic.objects.filter(subject=dsa_subj).count()} total")

# ==============================================================================
# 4. SEED LEARNING PATHS
# ==============================================================================

PATHS_DATA = [
    {
        "code": "placement",
        "name": "🎯 Placement Preparation (Campus)",
        "description": "Complete campus placement roadmap from aptitude to HR interview. Covers every round of TCS, Infosys, Zoho, Accenture, Amazon and more.",
        "icon": "🎯",
        "accent_color": "#ef4444",
        "target_role": "Software Engineer / Analyst",
        "duration_weeks": 16,
        "difficulty_level": "All Levels",
        "order": 1,
        "steps": [
            (1, "Quantitative Aptitude", "Master percentages, ratios, time-work, speed-distance, profit-loss.", 7),
            (2, "Logical Reasoning", "Number series, blood relations, coding-decoding, seating arrangements.", 7),
            (3, "Verbal Ability", "Reading comprehension, grammar, synonyms, antonyms.", 5),
            (4, "Programming Fundamentals", "Pick Python or Java. Learn syntax, loops, functions, arrays.", 14),
            (5, "Data Structures & Algorithms", "Arrays, strings, stacks, queues, trees, graphs – beginner to medium.", 21),
            (6, "DBMS & SQL", "Relational concepts, SQL queries, normalization, ACID.", 10),
            (7, "Operating Systems", "Processes, threads, scheduling, memory management, file systems.", 10),
            (8, "Computer Networks", "OSI, TCP/IP, DNS, HTTP, three-way handshake.", 10),
            (9, "OOP Concepts", "Encapsulation, inheritance, polymorphism, SOLID.", 7),
            (10, "Company-Specific Preparation", "Study each company's selection process, coding patterns, and interview style.", 14),
            (11, "Coding Assessments", "Solve 100+ problems on the platform – TCS, Infosys, Zoho patterns.", 21),
            (12, "Technical Interview Preparation", "Mock technical interviews with deep DBMS, OS, CN, DSA questions.", 14),
            (13, "HR Interview Preparation", "Tell me about yourself, strengths/weaknesses, situational questions.", 7),
            (14, "Resume Building & Profile", "Build an ATS-ready resume and optimize LinkedIn profile.", 5),
        ]
    },
    {
        "code": "python_dev",
        "name": "🐍 Python Developer Path",
        "description": "From Python basics to backend development, automation, and data handling.",
        "icon": "🐍",
        "accent_color": "#3b82f6",
        "target_role": "Python Developer / Backend Engineer",
        "duration_weeks": 12,
        "difficulty_level": "Beginner",
        "order": 2,
        "steps": [
            (1, "Python Fundamentals", "Variables, data types, operators, input/output.", 7),
            (2, "Control Flow", "Conditions (if/elif/else), loops (for/while), break/continue.", 5),
            (3, "Functions & Modules", "Function definitions, parameters, return values, importing modules.", 7),
            (4, "Data Structures", "Lists, tuples, sets, dictionaries – creation, operations, comprehensions.", 10),
            (5, "OOP with Python", "Classes, inheritance, polymorphism, properties, special methods.", 10),
            (6, "File Handling & Exceptions", "Read/write files, try/except/finally, custom exceptions.", 7),
            (7, "DSA Using Python", "Solve arrays, strings, stacks, queues problems in Python.", 14),
            (8, "SQL & Database Access", "SQL queries, Python sqlite3 / SQLAlchemy basics.", 7),
            (9, "Backend Fundamentals", "HTTP, REST APIs, Django or FastAPI basics.", 14),
            (10, "Projects", "Build 2 real projects: CLI app + web API.", 14),
        ]
    },
    {
        "code": "beginner_to_dev",
        "name": "🚀 Complete Beginner to Software Developer",
        "description": "Start from zero and build a solid foundation in computer science and programming.",
        "icon": "🚀",
        "accent_color": "#a855f7",
        "target_role": "Junior Software Engineer",
        "duration_weeks": 24,
        "difficulty_level": "Beginner",
        "order": 3,
        "steps": [
            (1, "Computer Fundamentals", "How computers work, binary, memory, OS basics.", 7),
            (2, "Introduction to Programming", "Concepts: algorithms, variables, loops, conditions – language-agnostic.", 7),
            (3, "Python Basics", "Learn your first language: Python from scratch.", 14),
            (4, "Problem Solving Basics", "Pattern problems, number programs, string manipulation.", 14),
            (5, "Data Structures", "Arrays, linked lists, stacks, queues, hash maps.", 21),
            (6, "Algorithms", "Sorting, searching, recursion, two-pointer.", 14),
            (7, "OOP Concepts", "Classes, objects, inheritance, polymorphism.", 10),
            (8, "DBMS & SQL", "Database design, SQL queries, normalization.", 14),
            (9, "Operating Systems", "Processes, memory, scheduling fundamentals.", 10),
            (10, "Computer Networks", "OSI model, TCP/IP, HTTP fundamentals.", 10),
            (11, "Git & Version Control", "Git commands, branching, GitHub workflow.", 7),
            (12, "Software Engineering", "Agile, testing, documentation, project lifecycle.", 7),
            (13, "Projects", "Build a real project applying your skills.", 21),
            (14, "Interview Preparation", "DSA interview questions, system design basics, coding assessment prep.", 14),
        ]
    },
    {
        "code": "fullstack_dev",
        "name": "🌍 Full Stack Developer Path",
        "description": "Frontend to backend: HTML, CSS, JavaScript, React, Node.js or Django, and databases.",
        "icon": "🌍",
        "accent_color": "#10b981",
        "target_role": "Full Stack Developer",
        "duration_weeks": 20,
        "difficulty_level": "Intermediate",
        "order": 4,
        "steps": [
            (1, "HTML Fundamentals", "HTML5 structure, semantic elements, forms, accessibility.", 7),
            (2, "CSS Fundamentals", "Selectors, Flexbox, Grid, responsive design, animations.", 10),
            (3, "JavaScript", "DOM manipulation, events, async/await, ES6+ features.", 14),
            (4, "Frontend Framework", "React.js or Vue.js basics, components, state management.", 21),
            (5, "Backend Fundamentals", "HTTP, REST APIs, authentication concepts.", 7),
            (6, "Python/Node.js Backend", "Build REST APIs with Django REST Framework or Express.", 21),
            (7, "Databases", "SQL with PostgreSQL, NoSQL with MongoDB basics.", 14),
            (8, "Authentication & Security", "JWT, session management, HTTPS, common vulnerabilities.", 10),
            (9, "Git & Deployment", "GitHub, CI/CD basics, deploying to cloud (Render/Vercel).", 10),
            (10, "Full Stack Projects", "Build 2 complete full-stack applications from scratch.", 28),
        ]
    },
    {
        "code": "ai_ml",
        "name": "🤖 AI/ML Beginner Path",
        "description": "Start your AI/ML journey with Python, mathematics, and hands-on model building.",
        "icon": "🤖",
        "accent_color": "#ec4899",
        "target_role": "AI/ML Engineer / Data Scientist",
        "duration_weeks": 20,
        "difficulty_level": "Intermediate",
        "order": 5,
        "steps": [
            (1, "Python for AI", "NumPy, Pandas, Matplotlib essentials.", 10),
            (2, "Mathematics Fundamentals", "Linear algebra basics, statistics, probability.", 14),
            (3, "Data Analysis", "Exploratory data analysis, data cleaning, visualization.", 14),
            (4, "Machine Learning Basics", "Supervised vs unsupervised, train/test split, model evaluation.", 14),
            (5, "Classification Algorithms", "Logistic regression, decision trees, SVM, KNN.", 14),
            (6, "Regression Algorithms", "Linear regression, polynomial regression.", 10),
            (7, "Clustering", "K-Means, hierarchical clustering.", 10),
            (8, "Feature Engineering", "Feature selection, encoding, scaling, PCA.", 14),
            (9, "Deep Learning Intro", "Neural networks, Keras/TensorFlow basics.", 21),
            (10, "AI Projects", "Build 2 ML projects with real datasets.", 28),
        ]
    },
]

created_paths = 0
for p_data in PATHS_DATA:
    steps = p_data.pop('steps')
    path, created = LearningPath.objects.get_or_create(code=p_data['code'], defaults=p_data)
    if not created:
        for k, v in p_data.items():
            setattr(path, k, v)
        path.save()
    if created:
        created_paths += 1

    # Seed steps
    for step_num, title, desc, days in steps:
        step, _ = LearningPathStep.objects.get_or_create(
            path=path,
            step_number=step_num,
            defaults={
                "title": title,
                "description": desc,
                "estimated_days": days
            }
        )

print(f"Learning Paths seeded: {LearningPath.objects.count()} total")
print(f"Path Steps seeded: {LearningPathStep.objects.count()} total")

print("\nCS Learning Hub seed completed!")
print(f"  Subjects: {Subject.objects.count()}")
print(f"  Topics: {Topic.objects.count()}")
print(f"  Learning Paths: {LearningPath.objects.count()}")
