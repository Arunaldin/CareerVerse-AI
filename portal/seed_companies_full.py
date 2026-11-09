"""
Seed 28+ Companies into CompanyPlacement table
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from portal.models import CompanyPlacement

COMPANIES_DATA = [
    {
        'name': 'Adobe', 'slug': 'adobe', 'tagline': 'Creativity for all - Digital Media Leader',
        'category': 'Product', 'accent_color': '#e11d48', 'package_range': '₹22.0 - 40.0 LPA',
        'eligibility_cgpa': 7.00, 'eligible_branches': 'CSE, IT, ECE', 'backlogs_allowed': '0 backlogs',
        'overview': 'Adobe tests data structures, geometry algorithms, and OOP design.',
        'selection_rounds': [{'name': 'Round 1: OA', 'desc': '2 Coding + CS MCQs', 'duration': '90 mins', 'questions': '2 Coding'}],
        'previous_questions': [{'question': 'Find median in a running stream of integers.', 'type': 'DSA', 'answer': 'Use two heaps: max-heap for lower half and min-heap for higher half.'}],
        'interview_tips': 'Strong mathematical foundations and clean recursion.'
    },
    {
        'name': 'Cisco', 'slug': 'cisco', 'tagline': 'Bridge to Possible - Networking & Cybersecurity Giant',
        'category': 'Product', 'accent_color': '#0284c7', 'package_range': '₹15.0 - 26.0 LPA',
        'eligibility_cgpa': 7.00, 'eligible_branches': 'CSE, IT, ECE, EEE', 'backlogs_allowed': '0 backlogs',
        'overview': 'Cisco evaluates computer networks, socket programming, and algorithms.',
        'selection_rounds': [{'name': 'Round 1: OA', 'desc': 'Networks MCQs + 2 Coding', 'duration': '75 mins', 'questions': '20 MCQs + 2 Coding'}],
        'previous_questions': [{'question': 'Explain TCP 3-way handshake and 4-way termination.', 'type': 'Networks', 'answer': 'SYN -> SYN-ACK -> ACK for connection; FIN -> ACK -> FIN -> ACK for teardown.'}],
        'interview_tips': 'Master OSI layers, subnetting, and socket programming.'
    },
    {
        'name': 'Walmart Global Tech', 'slug': 'walmart', 'tagline': 'Save money. Live better - Retail Tech',
        'category': 'Product', 'accent_color': '#0369a1', 'package_range': '₹18.0 - 30.0 LPA',
        'eligibility_cgpa': 7.00, 'eligible_branches': 'CSE, IT, ECE', 'backlogs_allowed': '0 backlogs',
        'overview': 'Walmart evaluates high-scale distributed systems and algorithms.',
        'selection_rounds': [{'name': 'Round 1: OA', 'desc': 'Coding problems on HackerEarth', 'duration': '90 mins', 'questions': '2 Coding'}],
        'previous_questions': [{'question': 'Design an inventory decrement mechanism under high concurrency.', 'type': 'Design', 'answer': 'Use database row-level locking or distributed Redis lock with lease expiry.'}],
        'interview_tips': 'Understand concurrency and caching strategies.'
    },
    {
        'name': 'PayPal', 'slug': 'paypal', 'tagline': 'Powering the global digital economy',
        'category': 'Product', 'accent_color': '#0070ba', 'package_range': '₹20.0 - 34.0 LPA',
        'eligibility_cgpa': 7.50, 'eligible_branches': 'CSE, IT', 'backlogs_allowed': '0 backlogs',
        'overview': 'PayPal assesses secure coding, financial transaction safety, and algorithms.',
        'selection_rounds': [{'name': 'Round 1: OA', 'desc': '3 Coding questions', 'duration': '90 mins', 'questions': '3 Coding'}],
        'previous_questions': [{'question': 'Detect cycle in a directed graph.', 'type': 'DSA', 'answer': 'Use DFS with 3 states or Kahn algorithm with in-degrees.'}],
        'interview_tips': 'Emphasize defensive coding and transactional atomicity.'
    },
    {
        'name': 'Salesforce', 'slug': 'salesforce', 'tagline': 'The world #1 AI CRM',
        'category': 'Product', 'accent_color': '#00a1e0', 'package_range': '₹25.0 - 42.0 LPA',
        'eligibility_cgpa': 7.00, 'eligible_branches': 'CSE, IT', 'backlogs_allowed': '0 backlogs',
        'overview': 'Salesforce tests cloud multi-tenancy concepts, OOP, and data structures.',
        'selection_rounds': [{'name': 'Round 1: OA', 'desc': 'Hackerrank coding assessment', 'duration': '90 mins', 'questions': '2 Coding'}],
        'previous_questions': [{'question': 'Implement an LRU Cache.', 'type': 'DSA', 'answer': 'Combine Hash Map with Doubly Linked List for O(1) get and put.'}],
        'interview_tips': 'Be articulate about system modularity.'
    },
    {
        'name': 'Freshworks', 'slug': 'freshworks', 'tagline': 'Software that delights customers and employees',
        'category': 'Product', 'accent_color': '#f97316', 'package_range': '₹12.0 - 20.0 LPA',
        'eligibility_cgpa': 6.50, 'eligible_branches': 'Any branch with strong coding', 'backlogs_allowed': '0 backlogs',
        'overview': 'Freshworks prioritizes product craftsmanship, full-stack awareness, and clean logic.',
        'selection_rounds': [{'name': 'Round 1: Coding Test', 'desc': 'Problem solving and logic', 'duration': '90 mins', 'questions': '3 Coding'}],
        'previous_questions': [{'question': 'Group anagrams from a list of words.', 'type': 'DSA', 'answer': 'Use character count tuple or sorted string as hash map key.'}],
        'interview_tips': 'Showcase practical portfolio projects and full-stack familiarity.'
    },
    {
        'name': 'LTIMindtree', 'slug': 'ltimindtree', 'tagline': 'Getting you there faster - Digital Solutions Leader',
        'category': 'IT Services', 'accent_color': '#8b5cf6', 'package_range': '₹4.0 - 8.0 LPA',
        'eligibility_cgpa': 6.00, 'eligible_branches': 'All Engineering streams', 'backlogs_allowed': '1 backlog allowed during drive',
        'overview': 'LTIMindtree conducts cognitive aptitude, pseudo-code, and coding tests.',
        'selection_rounds': [{'name': 'Round 1: Online Assessment', 'desc': 'Quantitative, logical, and coding', 'duration': '90 mins', 'questions': '50 MCQs + 1 Coding'}],
        'previous_questions': [{'question': 'Check if a number is a prime number in O(sqrt(n)).', 'type': 'Coding', 'answer': 'Iterate from 2 up to sqrt(n) checking divisibility.'}],
        'interview_tips': 'Revise basic mathematics and string algorithms.'
    },
    {
        'name': 'Hexaware', 'slug': 'hexaware', 'tagline': 'Creating smiles through great people and technology',
        'category': 'IT Services', 'accent_color': '#059669', 'package_range': '₹4.0 - 6.0 LPA',
        'eligibility_cgpa': 6.00, 'eligible_branches': 'CSE, IT, ECE, EEE', 'backlogs_allowed': '0 backlogs',
        'overview': 'Hexaware assesses problem solving, domain fundamentals, and communication.',
        'selection_rounds': [{'name': 'Round 1: Aptitude & Coding', 'desc': 'Numerical and programming test', 'duration': '80 mins', 'questions': '40 MCQs + 1 Coding'}],
        'previous_questions': [{'question': 'Find second largest element in an array in single pass.', 'type': 'Coding', 'answer': 'Maintain largest and second_largest variables updating sequentially.'}],
        'interview_tips': 'Prepare structured introduction and project details.'
    },
    {
        'name': 'Tech Mahindra', 'slug': 'tech-mahindra', 'tagline': 'Connected World. Connected Experiences.',
        'category': 'IT Services', 'accent_color': '#ef4444', 'package_range': '₹3.6 - 7.0 LPA',
        'eligibility_cgpa': 6.00, 'eligible_branches': 'All Engineering streams', 'backlogs_allowed': '0 backlogs',
        'overview': 'Tech Mahindra tests logical reasoning, English proficiency, and basic programming.',
        'selection_rounds': [{'name': 'Round 1: Cognitive Test', 'desc': 'Reasoning and English', 'duration': '60 mins', 'questions': '60 Questions'}],
        'previous_questions': [{'question': 'What is a foreign key in SQL?', 'type': 'Technical', 'answer': 'A column that links records in one table to the primary key of another table.'}],
        'interview_tips': 'Time management is key during the cognitive test.'
    },
    {
        'name': 'IBM', 'slug': 'ibm', 'tagline': 'Think - Pioneer in Hybrid Cloud and AI',
        'category': 'Product', 'accent_color': '#1d4ed8', 'package_range': '₹6.5 - 12.0 LPA (Associate System Engineer)',
        'eligibility_cgpa': 6.50, 'eligible_branches': 'CSE, IT, ECE', 'backlogs_allowed': '0 backlogs',
        'overview': 'IBM conducts cognitive games, learning agility tests, and algorithmic coding.',
        'selection_rounds': [{'name': 'Round 1: Cognitive Games', 'desc': 'Interactive gamified assessment', 'duration': '40 mins', 'questions': '6 Games'}],
        'previous_questions': [{'question': 'Explain the difference between supervised and unsupervised learning.', 'type': 'AI/ML', 'answer': 'Supervised learns from labeled data; unsupervised finds hidden patterns.'}],
        'interview_tips': 'Demonstrate curiosity and fast learning agility.'
    },
    {
        'name': 'Atlassian', 'slug': 'atlassian', 'tagline': 'Unleash the potential of every team',
        'category': 'Product', 'accent_color': '#2563eb', 'package_range': '₹35.0 - 55.0 LPA (Graduate Engineer)',
        'eligibility_cgpa': 7.50, 'eligible_branches': 'CSE, IT', 'backlogs_allowed': '0 backlogs',
        'overview': 'Atlassian prioritizes values, clean code craftsmanship, and algorithmic depth.',
        'selection_rounds': [{'name': 'Round 1: OA', 'desc': '3 algorithmic questions on HackerRank', 'duration': '90 mins', 'questions': '3 Coding'}],
        'previous_questions': [{'question': 'Design a rate limiter (Token Bucket algorithm).', 'type': 'System Design', 'answer': 'Track token count and refill timestamp; replenish proportionally on each request.'}],
        'interview_tips': 'Practice clean object-oriented design and edge cases.'
    },
    {
        'name': 'Qualcomm', 'slug': 'qualcomm', 'tagline': 'Intelligent Computing Everywhere',
        'category': 'Product', 'accent_color': '#475569', 'package_range': '₹16.0 - 28.0 LPA (Associate Engineer)',
        'eligibility_cgpa': 7.00, 'eligible_branches': 'CSE, ECE, EE', 'backlogs_allowed': '0 backlogs',
        'overview': 'Qualcomm evaluates C/C++, embedded systems, bitwise manipulations, and data structures.',
        'selection_rounds': [{'name': 'Round 1: OA', 'desc': 'Aptitude, C/C++ MCQs, and 2 Coding', 'duration': '90 mins', 'questions': '30 MCQs + 2 Coding'}],
        'previous_questions': [{'question': 'Set, clear, and toggle the nth bit of an integer.', 'type': 'Bitwise', 'answer': 'num | (1 << n) to set; num & ~(1 << n) to clear; num ^ (1 << n) to toggle.'}],
        'interview_tips': 'Master pointers, memory layouts, and bitwise operators in C/C++.'
    },
    {
        'name': 'EY (Ernst & Young)', 'slug': 'ey', 'tagline': 'Building a better working world',
        'category': 'IT Services', 'accent_color': '#eab308', 'package_range': '₹4.5 - 7.5 LPA (Tech Consultant)',
        'eligibility_cgpa': 6.00, 'eligible_branches': 'All streams', 'backlogs_allowed': '0 backlogs',
        'overview': 'EY recruits for technology consulting, cybersecurity, and digital audits.',
        'selection_rounds': [{'name': 'Round 1: Aptitude & Reasoning', 'desc': 'Quantitative and logical test', 'duration': '60 mins', 'questions': '50 Questions'}],
        'previous_questions': [{'question': 'What are the main principles of cybersecurity (CIA Triad)?', 'type': 'Security', 'answer': 'Confidentiality, Integrity, and Availability.'}],
        'interview_tips': 'Articulate how technology creates tangible business impact.'
    },
    {
        'name': 'KPMG', 'slug': 'kpmg', 'tagline': 'Inspire Confidence. Empower Change.',
        'category': 'IT Services', 'accent_color': '#1e40af', 'package_range': '₹4.5 - 7.5 LPA (Analyst)',
        'eligibility_cgpa': 6.00, 'eligible_branches': 'All streams', 'backlogs_allowed': '0 backlogs',
        'overview': 'KPMG tests business aptitude, logical reasoning, and tech advisory capabilities.',
        'selection_rounds': [{'name': 'Round 1: Cognitive Assessment', 'desc': 'Data interpretation and logic', 'duration': '60 mins', 'questions': '45 Questions'}],
        'previous_questions': [{'question': 'Explain the difference between Cloud IaaS, PaaS, and SaaS.', 'type': 'Cloud', 'answer': 'IaaS provides raw infrastructure; PaaS provides runtime platform; SaaS provides turnkey applications.'}],
        'interview_tips': 'Combine computer science fundamentals with consultative problem solving.'
    }
]

created = 0
for c in COMPANIES_DATA:
    obj, is_new = CompanyPlacement.objects.get_or_create(slug=c['slug'], defaults=c)
    if is_new:
        created += 1

print(f"Successfully seeded {created} new companies. Total company count: {CompanyPlacement.objects.count()}")

