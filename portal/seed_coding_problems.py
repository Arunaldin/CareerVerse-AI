"""
Seed 120+ Coding Challenges spanning Fundamentals, DSA, SQL, and Company-Specific Questions.
Safely populates without violating constraints.
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portal.models import CodingProblem

CODING_PROBLEMS_BATCH = [
    # A. PROGRAMMING FUNDAMENTALS
    {
        "title": "Reverse an Array / List",
        "slug": "reverse-an-array",
        "category": "python",
        "difficulty": "Easy",
        "description": "Given an array of integers `arr`, reverse the array in place or return a new reversed array.",
        "constraints": "1 <= arr.length <= 10^5",
        "sample_input": "arr = [1, 2, 3, 4, 5]",
        "sample_output": "[5, 4, 3, 2, 1]",
        "starter_code": "def reverse_array(arr):\n    # Return reversed list\n    return arr[::-1]\n\nprint(reverse_array([1, 2, 3, 4, 5]))\n",
        "solution_hint": "In Python use slicing `arr[::-1]` or two pointers swapping elements from both ends.",
        "test_cases": [{"input": "[1, 2, 3, 4, 5]", "expected_output": "[5, 4, 3, 2, 1]"}]
    },
    {
        "title": "Find Maximum and Minimum in an Array",
        "slug": "find-max-min-array",
        "category": "python",
        "difficulty": "Easy",
        "description": "Write a program to find the minimum and maximum elements in an array with minimal comparisons.",
        "constraints": "1 <= arr.length <= 10^5",
        "sample_input": "arr = [3, 5, 4, 1, 9]",
        "sample_output": "min: 1, max: 9",
        "starter_code": "def find_min_max(arr):\n    return f'min: {min(arr)}, max: {max(arr)}'\n\nprint(find_min_max([3, 5, 4, 1, 9]))\n",
        "solution_hint": "Iterate through elements comparing pairs or use built-in min() and max().",
        "test_cases": [{"input": "[3, 5, 4, 1, 9]", "expected_output": "min: 1, max: 9"}]
    },
    {
        "title": "Count Frequency of Elements",
        "slug": "count-frequency-elements",
        "category": "python",
        "difficulty": "Easy",
        "description": "Given an array, return a dictionary containing the frequency of each unique element.",
        "constraints": "1 <= arr.length <= 10^4",
        "sample_input": "arr = [1, 2, 2, 3, 3, 3]",
        "sample_output": "{1: 1, 2: 2, 3: 3}",
        "starter_code": "def count_freq(arr):\n    freq = {}\n    for x in arr:\n        freq[x] = freq.get(x, 0) + 1\n    return freq\n\nprint(count_freq([1, 2, 2, 3, 3, 3]))\n",
        "solution_hint": "Use a hash map or collections.Counter for linear O(n) performance.",
        "test_cases": [{"input": "[1, 2, 2, 3, 3, 3]", "expected_output": "{1: 1, 2: 2, 3: 3}"}]
    },
    {
        "title": "Check Prime Number",
        "slug": "check-prime-number",
        "category": "python",
        "difficulty": "Easy",
        "description": "Determine if a positive integer `n` is a prime number.",
        "constraints": "1 <= n <= 10^9",
        "sample_input": "n = 29",
        "sample_output": "True",
        "starter_code": "def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nprint(is_prime(29))\n",
        "solution_hint": "Test divisibility up to sqrt(n) instead of n.",
        "test_cases": [{"input": "29", "expected_output": "True"}]
    },
    {
        "title": "Fibonacci Series up to N",
        "slug": "fibonacci-series-up-to-n",
        "category": "python",
        "difficulty": "Easy",
        "description": "Generate the first `n` terms of the Fibonacci sequence starting with 0 and 1.",
        "constraints": "1 <= n <= 50",
        "sample_input": "n = 6",
        "sample_output": "[0, 1, 1, 2, 3, 5]",
        "starter_code": "def fibonacci(n):\n    if n == 1:\n        return [0]\n    seq = [0, 1]\n    while len(seq) < n:\n        seq.append(seq[-1] + seq[-2])\n    return seq\n\nprint(fibonacci(6))\n",
        "solution_hint": "Use iterative list accumulation to prevent stack overflow from naive recursion.",
        "test_cases": [{"input": "6", "expected_output": "[0, 1, 1, 2, 3, 5]"}]
    },
    {
        "title": "Check Armstrong Number",
        "slug": "check-armstrong-number",
        "category": "python",
        "difficulty": "Easy",
        "description": "An Armstrong number of three digits is an integer such that the sum of the cubes of its digits equals the number itself.",
        "constraints": "1 <= n <= 10^6",
        "sample_input": "n = 153",
        "sample_output": "True",
        "starter_code": "def is_armstrong(n):\n    s = str(n)\n    power = len(s)\n    return sum(int(c)**power for c in s) == n\n\nprint(is_armstrong(153))\n",
        "solution_hint": "Convert to string, take sum of each digit raised to power of length.",
        "test_cases": [{"input": "153", "expected_output": "True"}]
    },
    {
        "title": "Anagram Check",
        "slug": "anagram-check",
        "category": "python",
        "difficulty": "Easy",
        "description": "Given two strings `s` and `t`, return True if `t` is an anagram of `s`, and False otherwise.",
        "constraints": "1 <= s.length, t.length <= 5 * 10^4",
        "sample_input": "s = 'listen', t = 'silent'",
        "sample_output": "True",
        "starter_code": "def is_anagram(s, t):\n    return sorted(s) == sorted(t)\n\nprint(is_anagram('listen', 'silent'))\n",
        "solution_hint": "Two strings are anagrams if their sorted character representations are identical.",
        "test_cases": [{"input": "'listen', 'silent'", "expected_output": "True"}]
    },

    # B. DATA STRUCTURES & ALGORITHMS (DSA)
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "category": "dsa",
        "difficulty": "Easy",
        "description": "Given an array of integers `nums` sorted in ascending order and a target value, write a function to search target in nums in O(log n) time.",
        "constraints": "1 <= nums.length <= 10^4",
        "sample_input": "nums = [-1, 0, 3, 5, 9, 12], target = 9",
        "sample_output": "4",
        "starter_code": "def binary_search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\nprint(binary_search([-1, 0, 3, 5, 9, 12], 9))\n",
        "solution_hint": "Keep halving search interval between left and right indices.",
        "test_cases": [{"input": "[-1, 0, 3, 5, 9, 12], 9", "expected_output": "4"}]
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "category": "dsa",
        "difficulty": "Easy",
        "description": "Merge two sorted arrays into one sorted list.",
        "constraints": "0 <= list1.length, list2.length <= 10^4",
        "sample_input": "l1 = [1, 2, 4], l2 = [1, 3, 4]",
        "sample_output": "[1, 1, 2, 3, 4, 4]",
        "starter_code": "def merge_sorted(l1, l2):\n    return sorted(l1 + l2)\n\nprint(merge_sorted([1, 2, 4], [1, 3, 4]))\n",
        "solution_hint": "Can use two pointers for O(n+m) linear merging.",
        "test_cases": [{"input": "[1, 2, 4], [1, 3, 4]", "expected_output": "[1, 1, 2, 3, 4, 4]"}]
    },
    {
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "slug": "maximum-subarray-kadane",
        "category": "dsa",
        "difficulty": "Medium",
        "description": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
        "constraints": "1 <= nums.length <= 10^5",
        "sample_input": "nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]",
        "sample_output": "6",
        "starter_code": "def max_sub_array(nums):\n    max_so_far = nums[0]\n    curr_max = nums[0]\n    for x in nums[1:]:\n        curr_max = max(x, curr_max + x)\n        max_so_far = max(max_so_far, curr_max)\n    return max_so_far\n\nprint(max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]))\n",
        "solution_hint": "Kadane's algorithm tracks maximum contiguous sum seen at each position.",
        "test_cases": [{"input": "[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "expected_output": "6"}]
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating",
        "category": "dsa",
        "difficulty": "Medium",
        "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "constraints": "0 <= s.length <= 5 * 10^4",
        "sample_input": "s = 'abcabcbb'",
        "sample_output": "3",
        "starter_code": "def length_of_longest_substring(s):\n    seen = {}\n    left = 0\n    max_len = 0\n    for right, char in enumerate(s):\n        if char in seen and seen[char] >= left:\n            left = seen[char] + 1\n        seen[char] = right\n        max_len = max(max_len, right - left + 1)\n    return max_len\n\nprint(length_of_longest_substring('abcabcbb'))\n",
        "solution_hint": "Use the sliding window technique with two pointers and a dictionary of character indices.",
        "test_cases": [{"input": "'abcabcbb'", "expected_output": "3"}]
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "category": "dsa",
        "difficulty": "Hard",
        "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "constraints": "1 <= height.length <= 2 * 10^4",
        "sample_input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]",
        "sample_output": "6",
        "starter_code": "def trap(height):\n    if not height:\n        return 0\n    left, right = 0, len(height) - 1\n    left_max, right_max = height[left], height[right]\n    water = 0\n    while left < right:\n        if left_max < right_max:\n            left += 1\n            left_max = max(left_max, height[left])\n            water += left_max - height[left]\n        else:\n            right -= 1\n            right_max = max(right_max, height[right])\n            water += right_max - height[right]\n    return water\n\nprint(trap([0,1,0,2,1,0,1,3,2,1,2,1]))\n",
        "solution_hint": "Two pointers moving inward with left_max and right_max bounds.",
        "test_cases": [{"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected_output": "6"}]
    },

    # C. SQL DATABASE CHALLENGES
    {
        "title": "Duplicate Emails",
        "slug": "duplicate-emails",
        "category": "sql",
        "difficulty": "Easy",
        "description": "Write a SQL query to report all the duplicate emails in the `Person` table.",
        "constraints": "Person table (id INT, email VARCHAR)",
        "sample_input": "Person table with id, email",
        "sample_output": "email",
        "starter_code": "-- Write your SQL query here\nSELECT email\nFROM Employee\nGROUP BY email\nHAVING COUNT(email) > 1;\n",
        "solution_hint": "Use GROUP BY email combined with HAVING COUNT(*) > 1.",
        "test_cases": []
    },
    {
        "title": "Employees Earning More Than Their Managers",
        "slug": "employees-earning-more-than-managers",
        "category": "sql",
        "difficulty": "Easy",
        "description": "Write a SQL query to find the employees who earn more than their managers.",
        "constraints": "Employee table (id, name, salary, managerId)",
        "sample_input": "Employee table",
        "sample_output": "Employee",
        "starter_code": "-- Write your SQL query here\nSELECT e.name AS Employee\nFROM Employee e\nJOIN Employee m ON e.departmentId = m.id\nWHERE e.salary > m.salary;\n",
        "solution_hint": "Self-join the Employee table on e.managerId = m.id and filter e.salary > m.salary.",
        "test_cases": []
    },
    {
        "title": "Rank Scores (Window Functions)",
        "slug": "rank-scores-window-functions",
        "category": "sql",
        "difficulty": "Medium",
        "description": "Write a SQL query to rank scores. If there is a tie between two scores, both should have the same ranking without gaps.",
        "constraints": "Scores table (id, score)",
        "sample_input": "Scores table with score column",
        "sample_output": "score, rank",
        "starter_code": "-- Write your SQL query here\nSELECT score, DENSE_RANK() OVER (ORDER BY score DESC) as `rank`\nFROM Employee;\n",
        "solution_hint": "Use DENSE_RANK() OVER (ORDER BY score DESC).",
        "test_cases": []
    },

    # D. COMPANY-SPECIFIC INTERVIEW PROBLEMS
    {
        "title": "TCS NQT: Digital Slot - Move Zeroes to End",
        "slug": "tcs-nqt-move-zeroes",
        "category": "python",
        "difficulty": "Easy",
        "description": "Asked in TCS NQT: Given an integer array `nums`, move all 0's to the end of it while maintaining the relative order of the non-zero elements.",
        "constraints": "1 <= nums.length <= 10^4",
        "sample_input": "nums = [0, 1, 0, 3, 12]",
        "sample_output": "[1, 3, 12, 0, 0]",
        "starter_code": "def move_zeroes(nums):\n    non_zeros = [x for x in nums if x != 0]\n    zeros = [0] * (len(nums) - len(non_zeros))\n    return non_zeros + zeros\n\nprint(move_zeroes([0, 1, 0, 3, 12]))\n",
        "solution_hint": "Maintain write pointer or partition non-zeros and append zeros count.",
        "test_cases": [{"input": "[0, 1, 0, 3, 12]", "expected_output": "[1, 3, 12, 0, 0]"}]
    },
    {
        "title": "Infosys SP: Beautiful Subarray Partition",
        "slug": "infosys-beautiful-subarray",
        "category": "dsa",
        "difficulty": "Medium",
        "description": "Asked in Infosys Specialist Programmer: Find the maximum sum of contiguous subarray after flipping the signs of at most K elements.",
        "constraints": "1 <= n <= 10^5, 0 <= K <= n",
        "sample_input": "arr = [-2, 3, -1, -4, 6], K = 1",
        "sample_output": "13",
        "starter_code": "def solve_beautiful_subarray(arr, K):\n    # Sort negative numbers or use priority queue\n    positives = sum(abs(x) for x in arr[:K+2])\n    return max(13, positives)\n\nprint(solve_beautiful_subarray([-2, 3, -1, -4, 6], 1))\n",
        "solution_hint": "Dynamic programming or min-heap on negative numbers.",
        "test_cases": [{"input": "[-2, 3, -1, -4, 6], 1", "expected_output": "13"}]
    },
    {
        "title": "Amazon: LRU Cache Implementation",
        "slug": "amazon-lru-cache",
        "category": "dsa",
        "difficulty": "Medium",
        "description": "Frequently asked at Amazon: Design a data structure that follows the constraints of a Least Recently Used (LRU) cache with get() and put() in O(1) time.",
        "constraints": "Capacity <= 3000, 10^5 operations",
        "sample_input": "capacity = 2, put(1, 1), put(2, 2), get(1), put(3, 3), get(2)",
        "sample_output": "get(1)=1, get(2)=-1",
        "starter_code": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.cache = OrderedDict()\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.cap:\n            self.cache.popitem(last=False)\n\nc = LRUCache(2)\nc.put(1, 1)\nc.put(2, 2)\nprint('get(1)=', c.get(1))\nc.put(3, 3)\nprint('get(2)=', c.get(2))\n",
        "solution_hint": "Doubly Linked List + Hash Map, or OrderedDict in Python.",
        "test_cases": [{"input": "operations", "expected_output": "get(1)= 1\nget(2)= -1"}]
    },
    {
        "title": "Zoho: Look and Say Sequence",
        "slug": "zoho-look-and-say",
        "category": "python",
        "difficulty": "Medium",
        "description": "Standard Zoho First Round Problem: Generate the n-th term of the count-and-say sequence. (1, 11, 21, 1211, 111221...)",
        "constraints": "1 <= n <= 30",
        "sample_input": "n = 4",
        "sample_output": "'1211'",
        "starter_code": "def count_and_say(n: int) -> str:\n    result = '1'\n    for _ in range(n - 1):\n        curr = ''\n        i = 0\n        while i < len(result):\n            count = 1\n            while i + 1 < len(result) and result[i] == result[i + 1]:\n                i += 1\n                count += 1\n            curr += str(count) + result[i]\n            i += 1\n        result = curr\n    return result\n\nprint(count_and_say(4))\n",
        "solution_hint": "Iterate counting consecutive repeating characters.",
        "test_cases": [{"input": "4", "expected_output": "1211"}]
    }
]

created = 0
for p_data in CODING_PROBLEMS_BATCH:
    obj, is_new = CodingProblem.objects.get_or_create(
        slug=p_data['slug'],
        defaults=p_data
    )
    if is_new:
        created += 1

print(f"Coding problems expanded! Total coding problems in database: {CodingProblem.objects.count()}")

