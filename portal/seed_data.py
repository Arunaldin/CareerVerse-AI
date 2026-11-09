"""
Seed data script to populate Aptitude Questions, Coding Problems, and Company Placements.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portal.models import AptitudeQuestion, CodingProblem, CompanyPlacement


def seed_aptitude():
    if AptitudeQuestion.objects.count() >= 15:
        print(f"Aptitude questions already exist ({AptitudeQuestion.objects.count()}). Skipping.")
        return

    questions = [
        # QUANTITATIVE
        {
            "category": "quantitative",
            "topic": "Percentages",
            "question_text": "A shopkeeper marks an item at 25% above cost price and allows a discount of 10% on the marked price. What is his net profit percentage?",
            "option_a": "12.5%", "option_b": "15%", "option_c": "10%", "option_d": "17.5%",
            "correct_option": "A",
            "explanation": "Let CP = 100. Marked Price (MP) = 100 + 25 = 125. Selling Price (SP) = 125 - 10% of 125 = 125 - 12.5 = 112.5. Profit = 112.5 - 100 = 12.5%.",
            "difficulty": "Easy"
        },
        {
            "category": "quantitative",
            "topic": "Time & Work",
            "question_text": "A can finish a piece of work in 12 days and B can finish the same work in 18 days. If they work together, in how many days will the work be completed?",
            "option_a": "6 days", "option_b": "7.2 days", "option_c": "8 days", "option_d": "7.5 days",
            "correct_option": "B",
            "explanation": "A's 1-day work = 1/12. B's 1-day work = 1/18. (A + B)'s 1-day work = (1/12) + (1/18) = (3 + 2)/36 = 5/36. Total days = 36/5 = 7.2 days.",
            "difficulty": "Easy"
        },
        {
            "category": "quantitative",
            "topic": "Speed, Time & Distance",
            "question_text": "A train 180 meters long is running at a speed of 72 km/h. How many seconds will it take to cross a pole?",
            "option_a": "7 seconds", "option_b": "9 seconds", "option_c": "10 seconds", "option_d": "12 seconds",
            "correct_option": "B",
            "explanation": "Speed in m/s = 72 * (5/18) = 20 m/s. Time to cross pole = Length of train / Speed = 180 / 20 = 9 seconds.",
            "difficulty": "Easy"
        },
        {
            "category": "quantitative",
            "topic": "Ratios & Proportions",
            "question_text": "If A : B = 2 : 3 and B : C = 4 : 5, find the ratio A : B : C.",
            "option_a": "8 : 12 : 15", "option_b": "6 : 9 : 10", "option_c": "8 : 10 : 15", "option_d": "2 : 4 : 5",
            "correct_option": "A",
            "explanation": "Multiply A : B by 4 -> 8 : 12. Multiply B : C by 3 -> 12 : 15. Hence A : B : C = 8 : 12 : 15.",
            "difficulty": "Easy"
        },
        {
            "category": "quantitative",
            "topic": "Probability",
            "question_text": "Two unbiased dice are rolled simultaneously. What is the probability that the sum of the numbers appearing on both dice is equal to 8?",
            "option_a": "5/36", "option_b": "7/36", "option_c": "1/6", "option_d": "1/9",
            "correct_option": "A",
            "explanation": "Total outcomes = 6 * 6 = 36. Favorable outcomes where sum = 8 are (2,6), (3,5), (4,4), (5,3), (6,2). Total = 5 pairs. Probability = 5/36.",
            "difficulty": "Medium"
        },
        {
            "category": "quantitative",
            "topic": "Permutations & Combinations",
            "question_text": "In how many distinct ways can the letters of the word 'LEADER' be arranged?",
            "option_a": "720", "option_b": "360", "option_c": "120", "option_d": "180",
            "correct_option": "B",
            "explanation": "The word LEADER contains 6 letters where 'E' appears twice. Total arrangements = 6! / 2! = 720 / 2 = 360.",
            "difficulty": "Medium"
        },
        {
            "category": "quantitative",
            "topic": "Averages",
            "question_text": "The average score of 5 students in a test is 82. If the score of a 6th student is included, the new average becomes 84. What is the score of the 6th student?",
            "option_a": "90", "option_b": "92", "option_c": "94", "option_d": "96",
            "correct_option": "C",
            "explanation": "Total of 5 students = 5 * 82 = 410. Total of 6 students = 6 * 84 = 504. Score of 6th student = 504 - 410 = 94.",
            "difficulty": "Easy"
        },
        {
            "category": "quantitative",
            "topic": "Compound Interest",
            "question_text": "What will be the compound interest on ₹10,000 for 2 years at 10% per annum compounded annually?",
            "option_a": "₹2,000", "option_b": "₹2,100", "option_c": "₹2,200", "option_d": "₹2,050",
            "correct_option": "B",
            "explanation": "Amount A = P(1 + r/100)^t = 10000 * (1.1)^2 = 10000 * 1.21 = 12100. CI = 12100 - 10000 = ₹2,100.",
            "difficulty": "Easy"
        },

        # LOGICAL REASONING
        {
            "category": "logical",
            "topic": "Number Series",
            "question_text": "Find the missing number in the sequence: 4, 9, 25, 49, 121, ?",
            "option_a": "144", "option_b": "169", "option_c": "196", "option_d": "225",
            "correct_option": "B",
            "explanation": "The terms are squares of consecutive prime numbers: 2^2=4, 3^2=9, 5^2=25, 7^2=49, 11^2=121. The next prime number is 13, so 13^2 = 169.",
            "difficulty": "Medium"
        },
        {
            "category": "logical",
            "topic": "Coding-Decoding",
            "question_text": "In a certain code, 'APPLE' is written as 'BQQMF'. How will 'DELHI' be written in that same code?",
            "option_a": "EDMIJ", "option_b": "EFMIJ", "option_c": "EFMIK", "option_d": "DEMIJ",
            "correct_option": "B",
            "explanation": "Each letter is shifted by +1: D->E, E->F, L->M, H->I, I->J. Therefore, DELHI becomes EFMIJ.",
            "difficulty": "Easy"
        },
        {
            "category": "logical",
            "topic": "Blood Relations",
            "question_text": "Pointing to a photograph, Rahul said, 'She is the daughter of my grandfather's only son.' How is the girl related to Rahul?",
            "option_a": "Mother", "option_b": "Sister", "option_c": "Aunt", "option_d": "Cousin",
            "correct_option": "B",
            "explanation": "Grandfather's only son = Rahul's father. Daughter of Rahul's father = Rahul's sister.",
            "difficulty": "Easy"
        },
        {
            "category": "logical",
            "topic": "Syllogisms",
            "question_text": "Statements: (1) All mangoes are golden. (2) No golden things are cheap. Conclusions: I. All mangoes are cheap. II. Golden things are mangoes.",
            "option_a": "Only Conclusion I follows", "option_b": "Only Conclusion II follows", "option_c": "Neither I nor II follows", "option_d": "Both follow",
            "correct_option": "C",
            "explanation": "Since all mangoes are golden and no golden things are cheap, no mangoes are cheap. Conclusion I is false. Also, while all mangoes are golden, not all golden things are mangoes. Neither follows.",
            "difficulty": "Medium"
        },
        {
            "category": "logical",
            "topic": "Direction Sense",
            "question_text": "A man walks 5 km South, turns left and walks 3 km, then turns left again and walks 5 km. In which direction is he from his starting point?",
            "option_a": "North", "option_b": "South", "option_c": "East", "option_d": "West",
            "correct_option": "C",
            "explanation": "5 km South puts him at (0, -5). Turning left faces East; 3 km puts him at (3, -5). Turning left faces North; 5 km puts him at (3, 0). (3, 0) is directly East of origin (0, 0).",
            "difficulty": "Easy"
        },

        # VERBAL ABILITY
        {
            "category": "verbal",
            "topic": "Synonyms",
            "question_text": "Select the synonym of the word: CANDID",
            "option_a": "Secretive", "option_b": "Frank / Honest", "option_c": "Deceptive", "option_d": "Arrogant",
            "correct_option": "B",
            "explanation": "Candid means truthful, straightforward, and outspoken. Frank or honest is the exact synonym.",
            "difficulty": "Easy"
        },
        {
            "category": "verbal",
            "topic": "Sentence Correction",
            "question_text": "Choose the grammatically correct sentence:",
            "option_a": "Neither of the two candidates have completed their paperwork.",
            "option_b": "Neither of the two candidates has completed his paperwork.",
            "option_c": "Neither of the two candidate has completed their paperwork.",
            "option_d": "Neither of the two candidates are completing paperwork.",
            "correct_option": "B",
            "explanation": "'Neither' is a singular distributive pronoun and takes a singular verb 'has' and singular possessive 'his'.",
            "difficulty": "Medium"
        },
        {
            "category": "verbal",
            "topic": "Idioms & Phrases",
            "question_text": "What does the idiom 'Bite the bullet' mean?",
            "option_a": "To commit an act of aggression",
            "option_b": "To face an inevitable grim situation with courage",
            "option_c": "To eat food quickly",
            "option_d": "To waste ammunition",
            "correct_option": "B",
            "explanation": "'Bite the bullet' means to face a difficult situation with courage and fortitude rather than running away from it.",
            "difficulty": "Easy"
        },
        {
            "category": "verbal",
            "topic": "Antonyms",
            "question_text": "Choose the antonym of the word: METICULOUS",
            "option_a": "Careless", "option_b": "Precise", "option_c": "Diligent", "option_d": "Scrupulous",
            "correct_option": "A",
            "explanation": "Meticulous means showing great attention to detail; very careful and precise. Its exact opposite is Careless.",
            "difficulty": "Easy"
        },
        {
            "category": "verbal",
            "topic": "Spotting Errors",
            "question_text": "Identify the part of the sentence containing an error: 'One of the player (A) / forgot to bring (B) / his kitbag to the stadium (C) / No error (D)'",
            "option_a": "Part (A)", "option_b": "Part (B)", "option_c": "Part (C)", "option_d": "Part (D)",
            "correct_option": "A",
            "explanation": "The phrase 'One of the' is always followed by a plural noun. It should be 'One of the players', not 'player'.",
            "difficulty": "Medium"
        },
    ]

    for q in questions:
        AptitudeQuestion.objects.create(**q)
    print(f"Successfully seeded {len(questions)} aptitude questions.")


def seed_coding():
    if CodingProblem.objects.count() >= 8:
        print(f"Coding problems already exist ({CodingProblem.objects.count()}). Skipping.")
        return

    problems = [
        # PYTHON
        {
            "title": "Two Sum",
            "slug": "two-sum",
            "category": "python",
            "difficulty": "Easy",
            "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
            "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\nOnly one valid answer exists.",
            "sample_input": "nums = [2, 7, 11, 15], target = 9",
            "sample_output": "[0, 1]",
            "starter_code": "def two_sum(nums, target):\n    # Return a list of two indices [i, j]\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n\n# Test call\nprint(two_sum([2, 7, 11, 15], 9))\n",
            "solution_hint": "Use a hash table / dictionary to store seen values and their index for O(n) lookup time.",
            "test_cases": [
                {"input": "[2, 7, 11, 15], 9", "expected_output": "[0, 1]"},
                {"input": "[3, 2, 4], 6", "expected_output": "[1, 2]"}
            ]
        },
        {
            "title": "Valid Palindrome",
            "slug": "valid-palindrome",
            "category": "python",
            "difficulty": "Easy",
            "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.",
            "constraints": "1 <= s.length <= 2 * 10^5",
            "sample_input": "s = 'A man, a plan, a canal: Panama'",
            "sample_output": "True",
            "starter_code": "def is_palindrome(s: str) -> bool:\n    cleaned = [c.lower() for c in s if c.isalnum()]\n    return cleaned == cleaned[::-1]\n\nprint(is_palindrome('A man, a plan, a canal: Panama'))\n",
            "solution_hint": "Filter using `.isalnum()`, convert to `.lower()`, and check if string equals its reverse.",
            "test_cases": [
                {"input": "'race a car'", "expected_output": "False"},
                {"input": "' '", "expected_output": "True"}
            ]
        },
        {
            "title": "Reverse Words in a String",
            "slug": "reverse-words-in-string",
            "category": "python",
            "difficulty": "Medium",
            "description": "Given an input string `s`, reverse the order of the words. Return a string of the words in reverse order concatenated by a single space.",
            "constraints": "1 <= s.length <= 10^4",
            "sample_input": "s = 'the sky is blue'",
            "sample_output": "'blue is sky the'",
            "starter_code": "def reverse_words(s: str) -> str:\n    words = s.strip().split()\n    return ' '.join(reversed(words))\n\nprint(reverse_words('  hello world  '))\n",
            "solution_hint": "Python's `s.split()` automatically splits on whitespace runs.",
            "test_cases": [
                {"input": "'  hello world  '", "expected_output": "'world hello'"}
            ]
        },

        # SQL
        {
            "title": "Second Highest Salary",
            "slug": "second-highest-salary",
            "category": "sql",
            "difficulty": "Easy",
            "description": "Write a SQL query to find the second highest distinct salary from the `Employee` table. If there is no second highest salary, return NULL.",
            "constraints": "Employee table: id INT, salary INT",
            "sample_input": "+----+--------+\n| id | salary |\n+----+--------+\n| 1  | 100    |\n| 2  | 200    |\n| 3  | 300    |\n+----+--------+",
            "sample_output": "+---------------------+\n| SecondHighestSalary |\n+---------------------+\n| 200                 |\n+---------------------+",
            "starter_code": "-- Write your SQL query here\nSELECT (\n    SELECT DISTINCT salary\n    FROM Employee\n    ORDER BY salary DESC\n    LIMIT 1 OFFSET 1\n) AS SecondHighestSalary;\n",
            "solution_hint": "Use `DISTINCT salary`, `ORDER BY salary DESC`, and `LIMIT 1 OFFSET 1` inside a scalar subquery.",
            "test_cases": []
        },
        {
            "title": "Department Highest Salary",
            "slug": "department-highest-salary",
            "category": "sql",
            "difficulty": "Medium",
            "description": "Write a SQL query to find employees who have the highest salary in each department.",
            "constraints": "Employee table (id, name, salary, departmentId)\nDepartment table (id, name)",
            "sample_input": "Employee and Department tables",
            "sample_output": "Department, Employee, Salary",
            "starter_code": "-- Write your SQL query here\nSELECT \n    d.name AS Department,\n    e.name AS Employee,\n    e.salary AS Salary\nFROM Employee e\nJOIN Department d ON e.departmentId = d.id\nWHERE (e.departmentId, e.salary) IN (\n    SELECT departmentId, MAX(salary)\n    FROM Employee\n    GROUP BY departmentId\n);\n",
            "solution_hint": "Use a subquery with `GROUP BY departmentId` finding `MAX(salary)`.",
            "test_cases": []
        },

        # DSA
        {
            "title": "Valid Parentheses",
            "slug": "valid-parentheses",
            "category": "dsa",
            "difficulty": "Easy",
            "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            "constraints": "1 <= s.length <= 10^4",
            "sample_input": "s = '()[]{}'",
            "sample_output": "True",
            "starter_code": "def is_valid_parentheses(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    \n    for char in s:\n        if char in mapping:\n            top_elem = stack.pop() if stack else '#'\n            if mapping[char] != top_elem:\n                return False\n        else:\n            stack.append(char)\n            \n    return not stack\n\nprint(is_valid_parentheses('()[]{}'))\n",
            "solution_hint": "Use a LIFO Stack. Match closing brackets against top of stack.",
            "test_cases": [
                {"input": "'([)]'", "expected_output": "False"},
                {"input": "'{[]}'", "expected_output": "True"}
            ]
        },
        {
            "title": "Maximum Subarray (Kadane's Algorithm)",
            "slug": "maximum-subarray-kadane",
            "category": "dsa",
            "difficulty": "Medium",
            "description": "Given an integer array `nums`, find the contiguous subarray with the largest sum and return its sum.",
            "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4",
            "sample_input": "nums = [-2,1,-3,4,-1,2,1,-5,4]",
            "sample_output": "6",
            "starter_code": "def max_sub_array(nums):\n    max_so_far = nums[0]\n    current_max = nums[0]\n    \n    for num in nums[1:]:\n        current_max = max(num, current_max + num)\n        max_so_far = max(max_so_far, current_max)\n        \n    return max_so_far\n\nprint(max_sub_array([-2,1,-3,4,-1,2,1,-5,4]))\n",
            "solution_hint": "Kadane's algorithm runs in O(n) time.",
            "test_cases": [
                {"input": "[1]", "expected_output": "1"},
                {"input": "[5,4,-1,7,8]", "expected_output": "23"}
            ]
        },
        {
            "title": "Search in Rotated Sorted Array",
            "slug": "search-rotated-sorted-array",
            "category": "dsa",
            "difficulty": "Medium",
            "description": "Given an array `nums` sorted in ascending order that is rotated at an unknown pivot, return the index of `target` or -1.",
            "constraints": "O(log n) time complexity required.",
            "sample_input": "nums = [4,5,6,7,0,1,2], target = 0",
            "sample_output": "4",
            "starter_code": "def search_rotated(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[left] <= nums[mid]:\n            if nums[left] <= target < nums[mid]:\n                right = mid - 1\n            else:\n                left = mid + 1\n        else:\n            if nums[mid] < target <= nums[right]:\n                left = mid + 1\n            else:\n                right = mid - 1\n    return -1\n\nprint(search_rotated([4,5,6,7,0,1,2], 0))\n",
            "solution_hint": "Modified Binary Search: at least one half of the array is always strictly sorted.",
            "test_cases": [
                {"input": "[4,5,6,7,0,1,2], 3", "expected_output": "-1"}
            ]
        }
    ]

    for p in problems:
        CodingProblem.objects.create(**p)
    print(f"Successfully seeded {len(problems)} coding problems.")


def seed_companies():
    if CompanyPlacement.objects.count() >= 6:
        print(f"Company placements already exist ({CompanyPlacement.objects.count()}). Skipping.")
        return

    companies = [
        {
            "name": "Tata Consultancy Services (TCS)",
            "slug": "tcs",
            "tagline": "Building on Belief - India's Largest IT Services Multinational",
            "category": "IT Services",
            "logo_icon": "server",
            "accent_color": "#0284c7",
            "package_range": "₹3.6 LPA (Ninja) | ₹7.0 LPA (Digital) | ₹9.0 LPA (Prime)",
            "eligibility_cgpa": 6.00,
            "eligible_branches": "B.E/B.Tech/M.E/M.Tech/MCA/M.Sc in CS, IT, ECE, EEE, Mechanical, Civil",
            "backlogs_allowed": "Up to 1 active backlog permitted during test; must clear before joining",
            "overview": "TCS conducts the National Qualifier Test (TCS NQT) to evaluate cognitive and programming aptitude. Top performers qualify for Digital and Prime technical interview rounds.",
            "selection_rounds": [
                {"name": "Round 1: TCS NQT Assessment", "desc": "Cognitive Skills (Numerical, Verbal, Reasoning) + Advanced Coding (2 programming problems).", "duration": "165 mins", "questions": "80 Questions"},
                {"name": "Round 2: Technical Interview", "desc": "Data Structures, OOP, SQL, Academic Projects, and live code debugging.", "duration": "30-45 mins", "questions": "5-8 Questions"},
                {"name": "Round 3: Managerial & HR Round", "desc": "Behavioral suitability, relocation willingness, night shift flexibility, and leadership qualities.", "duration": "20 mins", "questions": "4-6 Questions"}
            ],
            "previous_questions": [
                {"question": "Find the maximum subarray product in an array.", "type": "Coding", "answer": "Use modified Kadane's algorithm tracking both max and min product so far due to negative sign flips."},
                {"question": "What is normalization? Explain 1NF, 2NF, 3NF, and BCNF.", "type": "Technical", "answer": "Normalization organizes database tables to eliminate redundancy and prevent anomalies."},
                {"question": "Why TCS over other competitors?", "type": "HR", "answer": "Highlight TCS's global client footprint, stability, vast internal learning ecosystem, and consistent technological modernization."}
            ],
            "interview_tips": "Be thorough with basic Python/Java OOP concepts, SQL joins, and your final year project architecture."
        },
        {
            "name": "Infosys",
            "slug": "infosys",
            "tagline": "Navigate your next - Global Leader in Next-Generation Digital Services",
            "category": "IT Services",
            "logo_icon": "cpu",
            "accent_color": "#0ea5e9",
            "package_range": "₹3.6 LPA (SE) | ₹6.25 LPA (DSE) | ₹9.5 LPA (Specialist Programmer)",
            "eligibility_cgpa": 6.50,
            "eligible_branches": "All Engineering Streams, MCA, M.Sc",
            "backlogs_allowed": "0 active backlogs at the time of drive",
            "overview": "Infosys recruits through on-campus drives and competitions like HackWithInfy. Strong coding skills open the door to the elite Specialist Programmer (SP) role.",
            "selection_rounds": [
                {"name": "Round 1: Online Assessment", "desc": "Reasoning Ability, Technical Ability (Pseudo-code), Verbal Ability, and Numerical Puzzle Solving.", "duration": "100 mins", "questions": "54 Questions"},
                {"name": "Round 2: Technical Interview", "desc": "Programming fundamentals, Pseudo-code analysis, Cloud basics, and Project demonstration.", "duration": "30-40 mins", "questions": "6-10 Questions"},
                {"name": "Round 3: HR Interview", "desc": "Values, cultural alignment, communication skills, and DC flexibility.", "duration": "15 mins", "questions": "3-5 Questions"}
            ],
            "previous_questions": [
                {"question": "Predict output of complex bitwise operation & pointer expressions.", "type": "Pseudo-code", "answer": "Practice operator precedence, short-circuit evaluation in logic, and memory offsets."},
                {"question": "How does Garbage Collection operate in managed languages?", "type": "Technical", "answer": "Generational garbage collection cleans unreferenced memory objects automatically."},
                {"question": "Tell me about a time you worked on a project under high pressure.", "type": "HR", "answer": "Use the STAR method to describe task prioritization and team synchronization."}
            ],
            "interview_tips": "Master pseudo-code tracing (recursion loops and bitwise operations). For SP, practice DP and Graphs on LeetCode Medium."
        },
        {
            "name": "Zoho Corporation",
            "slug": "zoho",
            "tagline": "The Operating System for Business - Product Engineering Powerhouse",
            "category": "Product",
            "logo_icon": "layout-grid",
            "accent_color": "#dc2626",
            "package_range": "₹5.6 - 12.0 LPA (Software Developer)",
            "eligibility_cgpa": 5.00,
            "eligible_branches": "Any Degree / Branch (Skills and problem solving prioritize over marks)",
            "backlogs_allowed": "Standing backlogs allowed if coding prowess is exceptional",
            "overview": "Zoho evaluates pure problem-solving capability without filtering candidates solely on marks. Multi-round programming tests demand deep fundamental mastery without built-in library shortcuts.",
            "selection_rounds": [
                {"name": "Round 1: General Aptitude & C/C++ MCQs", "desc": "Basic math puzzles, flow of control, loop tracing, pointers, and memory operations.", "duration": "90 mins", "questions": "30 Questions"},
                {"name": "Round 2: Basic Programming Round", "desc": "5-7 programming problems (Pattern printing, String manipulation, Array rotations) without built-in methods.", "duration": "120 mins", "questions": "5-7 Coding"},
                {"name": "Round 3: Advanced Programming Round", "desc": "Complex mini-applications (e.g. Railway Reservation System, Dungeon Game, CLI Tools).", "duration": "180 mins", "questions": "1-2 Systems"},
                {"name": "Round 4 & 5: Tech & HR Interview", "desc": "Deep review of your written code, data structures, and Zoho philosophy alignment.", "duration": "60 mins", "questions": "In-depth Discussion"}
            ],
            "previous_questions": [
                {"question": "Implement an interactive Railway Reservation System with waiting lists and seat allocation.", "type": "Design & Code", "answer": "Use OOP with classes for Passenger, Ticket, Coach, and Queue for waiting list."},
                {"question": "Print a matrix in spiral order without extra auxiliary space.", "type": "Coding", "answer": "Maintain four boundary pointers (top, bottom, left, right) and shrink boundaries after each traversal."}
            ],
            "interview_tips": "Avoid depending on built-in helper functions like `split()` or `.reverse()`. Write algorithms from scratch."
        },
        {
            "name": "Amazon",
            "slug": "amazon",
            "tagline": "Work Hard. Have Fun. Make History - World Leader in Cloud & E-Commerce",
            "category": "Tech Giant",
            "logo_icon": "shopping-bag",
            "accent_color": "#f59e0b",
            "package_range": "₹28.0 - 45.0 LPA (SDE-1 Base + Stocks + Signing Bonus)",
            "eligibility_cgpa": 7.00,
            "eligible_branches": "CSE, IT, ECE, EE, Mathematics & Computing",
            "backlogs_allowed": "0 backlogs allowed",
            "overview": "Amazon focuses on Data Structures, Algorithms, System Scalability, and their world-famous 16 Leadership Principles (LPs). Every technical round includes leadership scenario questions.",
            "selection_rounds": [
                {"name": "Round 1: Online Assessment (OA)", "desc": "2 Algorithmic coding questions (LeetCode Medium-Hard) + Amazon Work Style Simulation.", "duration": "90 mins", "questions": "2 Coding + Scenarios"},
                {"name": "Round 2: Technical Interview 1", "desc": "Data Structures: Trees, Graphs, Hash Maps, Priority Queues + 1 Leadership Principle question.", "duration": "60 mins", "questions": "2 DSA + 1 LP"},
                {"name": "Round 3: Technical Interview 2", "desc": "Dynamic Programming, BFS/DFS, Recursion, Time/Space analysis + 2 Leadership Principles.", "duration": "60 mins", "questions": "2 DSA + 2 LP"},
                {"name": "Round 4: Bar Raiser Round", "desc": "Rigorous evaluation by an independent Amazonian testing behavioral depth and core customer obsession.", "duration": "60 mins", "questions": "Behavioral & Tech"}
            ],
            "previous_questions": [
                {"question": "Design an LRU (Least Recently Used) Cache with get and put in O(1) time.", "type": "DSA", "answer": "Combine a Hash Map (key to node pointer) with a Doubly Linked List."},
                {"question": "Serialize and Deserialize a Binary Tree.", "type": "DSA", "answer": "Use BFS level-order traversal with delimiter '#' for null nodes."}
            ],
            "interview_tips": "Prepare 2-3 detailed real-world stories for every Amazon Leadership Principle. Always speak aloud your thought process while coding."
        },
        {
            "name": "Accenture",
            "slug": "accenture",
            "tagline": "Let There Be Change - Global Professional Services Leader",
            "category": "IT Services",
            "logo_icon": "sparkles",
            "accent_color": "#a855f7",
            "package_range": "₹4.5 LPA (ASE) | ₹6.5 LPA (FSE)",
            "eligibility_cgpa": 6.50,
            "eligible_branches": "All Engineering branches, MCA, M.Sc",
            "backlogs_allowed": "0 active backlogs allowed",
            "overview": "Accenture conducts a phased hiring assessment: Cognitive & Technical knowledge, Coding round, AI-monitored Communication Assessment, and a panel interview.",
            "selection_rounds": [
                {"name": "Round 1: Cognitive & Technical Assessment", "desc": "Critical Thinking, Problem Solving, English Ability, Cloud, Security, MS Office, and Network fundamentals.", "duration": "90 mins", "questions": "90 MCQs"},
                {"name": "Round 2: Coding Assessment", "desc": "2 Coding questions evaluating algorithm implementation and boundary handling.", "duration": "45 mins", "questions": "2 Coding"},
                {"name": "Round 3: Communication Assessment", "desc": "Voice-recorded test assessing pronunciation, fluency, and reading comprehension.", "duration": "20 mins", "questions": "Speaking & Listening"},
                {"name": "Round 4: Technical & HR Interview", "desc": "Combined interview discussing projects, problem solving, adaptability, and corporate skills.", "duration": "25 mins", "questions": "4-6 Questions"}
            ],
            "previous_questions": [
                {"question": "Count frequency of characters in a string without case sensitivity.", "type": "Coding", "answer": "Use an array of size 26 or a hash map with `.lower()` normalization."},
                {"question": "Explain the difference between IaaS, PaaS, and SaaS in Cloud Computing.", "type": "Technical", "answer": "IaaS provides compute/storage; PaaS provides runtime platform; SaaS delivers ready web applications."}
            ],
            "interview_tips": "Do not skip the communication assessment practice. Speak in a quiet room with good headphones."
        },
        {
            "name": "Google",
            "slug": "google",
            "tagline": "Organizing the world's information and making it universally accessible",
            "category": "Tech Giant",
            "logo_icon": "globe",
            "accent_color": "#10b981",
            "package_range": "₹32.0 - 55.0 LPA (SWE Entry Level)",
            "eligibility_cgpa": 7.50,
            "eligible_branches": "CSE, IT, EE, Math, Data Science",
            "backlogs_allowed": "0 backlogs permitted",
            "overview": "Google software engineering interviews evaluate algorithmic optimization and 'Googleyness' (collaboration, intellectual humility, doing the right thing).",
            "selection_rounds": [
                {"name": "Round 1: Google Online Challenge (GOC)", "desc": "2-3 complex algorithmic challenges involving Graphs, Segment Trees, and Combinatorics.", "duration": "60 mins", "questions": "2-3 Questions"},
                {"name": "Round 2 & 3: Technical Phone Screens", "desc": "Collaborative Google Doc coding on advanced Data Structures and Graph traversals.", "duration": "45 mins each", "questions": "1-2 Problems each"},
                {"name": "Round 4, 5, 6: Onsite Coding & Googleyness", "desc": "3 Pure Coding rounds + 1 Googleyness & Leadership interview.", "duration": "45 mins each", "questions": "System & Algorithm"}
            ],
            "previous_questions": [
                {"question": "Find the shortest path in a weighted directed acyclic graph (DAG).", "type": "DSA", "answer": "Perform Topological Sort in O(V+E) time, then relax outgoing edges in topological order."},
                {"question": "What is Googleyness to you?", "type": "Behavioral", "answer": "Thriving in ambiguity, prioritizing user interest over short-term metrics, valuing diverse perspectives."}
            ],
            "interview_tips": "Never jump straight into writing code. Clarify requirements and constraints, discuss edge cases, outline brute force, optimize, analyze complexities, and dry run."
        }
    ]

    for c in companies:
        CompanyPlacement.objects.create(**c)
    print(f"Successfully seeded {len(companies)} company placement guides.")


if __name__ == '__main__':
    seed_aptitude()
    seed_coding()
    seed_companies()
    print("Database seeding completed successfully!")
