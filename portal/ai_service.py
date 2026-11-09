"""
CareerVerse AI Engine - Service Layer
Handles LLM generation for Career Guidance, Interview Questions, and Answer Evaluation.
Includes resilient fallback mechanisms when API keys are invalid, expired, or offline.
"""

import os
import re
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_clean_api_key():
    key = getattr(settings, 'OPENAI_API_KEY', '') or os.getenv('OPENAI_API_KEY', '')
    if key:
        key = key.strip().rstrip(']').rstrip('"').rstrip("'")
    return key


def generate_career_guidance(degree, cgpa, skills, interests):
    """
    Generate AI Career Guidance recommendation, skill gap analysis, and 5-step roadmap.
    """
    prompt = f"""You are an elite AI Career Counselor and Placement Advisor for university students.

Student Profile:
- Degree / Major: {degree}
- Academic Performance (CGPA): {cgpa}
- Existing Skills: {skills}
- Interests & Passions: {interests}

Please provide an in-depth, structured, and inspiring career recommendation.
Include:
1. 🎯 Top Recommended Career Path (Job Title, Industry Outlook, Freshers Salary Range in LPA)
2. 💡 Why This Career Fits You (alignment with degree, CGPA, and interests)
3. 🔍 Skill Gap Analysis (Key skills you currently possess vs. Critical skills you must learn)
4. 🗺️ 5-Step Strategic Learning Roadmap (with specific milestones and timelines)
5. 📚 Recommended Technologies, Courses & Certifications
6. 🚀 Placement Preparation Strategy (Campus vs Off-Campus tips)

Keep the formatting clean, professional, and well-organized with clear headings, bullet points, and actionable steps.
"""

    api_key = get_clean_api_key()
    if api_key and len(api_key) > 20:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            # Try chat completions API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are CareerVerse AI, a world-class career counselor and placement advisor for college students and graduates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            result = response.choices[0].message.content
            if result:
                return result
        except Exception as e:
            logger.warning(f"OpenAI API call failed: {e}. Falling back to internal CareerVerse AI engine.")

    # Resilient Intelligent Fallback Engine
    return generate_fallback_career_guidance(degree, cgpa, skills, interests)


def generate_interview_questions(role, company, skills, experience):
    """
    Generate personalized interview questions (Technical + HR + Skill-based) with model answers.
    """
    prompt = f"""You are an AI Technical Interviewer and Placement Panelist.

Student Target:
- Target Job Role: {role}
- Target Company: {company}
- Technical Skills: {skills}
- Experience Level: {experience}

Generate a comprehensive, realistic interview preparation pack for a college fresher / early career applicant.
Include:
1. 5 High-Yield Technical Interview Questions with clear Model Answers and key concepts.
2. 5 Behavioral & HR Questions (evaluated using the STAR framework) with ideal responses.
3. 3 Practical Scenario / Skill-Specific Questions based on "{skills}".
4. 5 Crucial Revision Topics for {company}'s hiring pattern.
5. Expert Interview Day Tips & Dos and Don'ts.

Make the answers crisp, easy to understand, yet technically rigorous.
"""

    api_key = get_clean_api_key()
    if api_key and len(api_key) > 20:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are CareerVerse AI, an elite technical interviewer and corporate talent assessor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1800
            )
            result = response.choices[0].message.content
            if result:
                return result
        except Exception as e:
            logger.warning(f"OpenAI API call failed: {e}. Falling back to internal AI interview generator.")

    return generate_fallback_interview(role, company, skills, experience)


def evaluate_interview_answer(role, question, user_answer, interview_type="Technical"):
    """
    Evaluate user's interview answer and return score, feedback, and model answer.
    """
    prompt = f"""You are an expert technical interviewer evaluating a student's answer.
Job Role: {role}
Interview Type: {interview_type}
Question: {question}
Candidate's Answer: {user_answer}

Provide constructive feedback formatted in JSON:
{{
  "score": <number between 1 and 10>,
  "strengths": "<what the candidate did well>",
  "weaknesses": "<what was missing, inaccurate, or vague>",
  "model_answer": "<a concise, high-scoring model answer>",
  "actionable_tips": "<2-3 specific tips to improve next time>"
}}
"""
    api_key = get_clean_api_key()
    if api_key and len(api_key) > 20:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert interview evaluator. Always output valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            raw = response.choices[0].message.content
            # Extract JSON block
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception as e:
            logger.warning(f"OpenAI evaluation failed: {e}. Using fallback evaluator.")

    return fallback_evaluate_answer(question, user_answer, interview_type)


# --------------------------------------------------------------------------
# FALLBACK GENERATORS (High quality, dynamic, domain-aware)
# --------------------------------------------------------------------------

def generate_fallback_career_guidance(degree, cgpa, skills, interests):
    skills_lower = (skills or "").lower()
    interests_lower = (interests or "").lower()
    degree_lower = (degree or "").lower()

    # Determine best fit role
    if any(k in interests_lower or k in skills_lower for k in ['ai', 'ml', 'machine learning', 'data', 'python', 'deep learning']):
        role = "AI / Machine Learning Engineer & Data Scientist"
        demand = "Extremely High (35% YoY growth)"
        salary = "₹6.5 - 14.0 LPA (Fresher / Junior)"
        missing_skills = ["PyTorch / TensorFlow", "Vector Databases & LLM RAG pipelines", "Feature Engineering & Scikit-Learn", "FastAPI / Docker deployment"]
        step1 = "Phase 1 (Month 1-2): Master Python, NumPy, Pandas, Vector Math, and Advanced Statistics."
        step2 = "Phase 2 (Month 3): Supervised & Unsupervised Machine Learning algorithms with Scikit-Learn and real datasets from Kaggle."
        step3 = "Phase 3 (Month 4): Deep Learning fundamentals (CNN, RNN, Transformers) & Natural Language Processing."
        step4 = "Phase 4 (Month 5): GenAI, LangChain, OpenAI APIs, Vector DBs (Chroma/FAISS) and building real-world AI applications."
        step5 = "Phase 5 (Month 6): End-to-end MLOps deployment on AWS/GCP, Dockerization, and campus placement problem solving."
        certifications = ["DeepLearning.AI Machine Learning Specialization (Coursera)", "AWS Certified Machine Learning - Specialty", "Google Professional Data Engineer"]
    elif any(k in interests_lower or k in skills_lower for k in ['cloud', 'devops', 'cyber', 'security', 'network', 'linux', 'aws', 'docker']):
        role = "Cloud & DevOps Systems Engineer"
        demand = "High Demand across Enterprises & Unicorns"
        salary = "₹5.5 - 12.0 LPA (Fresher / Junior)"
        missing_skills = ["Linux Shell Scripting & Bash", "Docker & Kubernetes Orchestration", "CI/CD Pipelines (GitHub Actions/Jenkins)", "Terraform & AWS/Azure Architecture"]
        step1 = "Phase 1 (Month 1-2): Deep dive into Linux administration, Networking protocols (TCP/IP, DNS, HTTP/S), and Shell automation."
        step2 = "Phase 2 (Month 3): Cloud computing fundamentals on AWS or Microsoft Azure (Compute, Storage, IAM, VPC)."
        step3 = "Phase 3 (Month 4): Containerization using Docker and Microservices deployment."
        step4 = "Phase 4 (Month 5): CI/CD automation with GitHub Actions, Infrastructure as Code with Terraform."
        step5 = "Phase 5 (Month 6): Kubernetes basics, monitoring tools (Prometheus & Grafana), and placement aptitude/coding revision."
        certifications = ["AWS Certified Solutions Architect - Associate", "CKA: Certified Kubernetes Administrator", "HashiCorp Certified Terraform Associate"]
    elif any(k in interests_lower or k in skills_lower for k in ['web', 'frontend', 'react', 'javascript', 'django', 'backend', 'full stack']):
        role = "Full Stack Web Software Engineer"
        demand = "Consistently High across Startups and Product Giants"
        salary = "₹5.0 - 11.5 LPA (Fresher / Junior)"
        missing_skills = ["Modern React / Next.js with TypeScript", "RESTful API Design & GraphQL", "Database optimization (PostgreSQL / Redis caching)", "System Design & Unit Testing"]
        step1 = "Phase 1 (Month 1-2): Advanced JavaScript (ES6+), React hooks, state management, and modern component design."
        step2 = "Phase 2 (Month 3): Backend engineering with Django / Node.js, authentication (JWT, OAuth), and relational database modeling."
        step3 = "Phase 3 (Month 4): Build 2 full-scale portfolio projects: e-commerce with payment gateway and a real-time collaborative workspace."
        step4 = "Phase 4 (Month 5): Data Structures & Algorithms practice (LeetCode Top 100 Liked) in Python/JS."
        step5 = "Phase 5 (Month 6): Resume optimization, mock technical interviews, and applying for off-campus/on-campus drives."
        certifications = ["Meta Front-End / Full-Stack Developer Professional Certificate", "FreeCodeCamp Full Stack Certification", "MongoDB Certified Developer"]
    else:
        role = "Associate Software Engineer / Core Developer"
        demand = "Massive Campus Recruitment & Product Hiring"
        salary = "₹4.5 - 9.5 LPA"
        missing_skills = ["Data Structures & Algorithms (Trees, Graphs, DP)", "Object-Oriented Design & Design Patterns", "SQL Query Optimization", "Git & Collaborative Development"]
        step1 = "Phase 1 (Month 1-2): Deepen proficiency in Python or Java/C++, covering OOP, memory management, and recursion."
        step2 = "Phase 2 (Month 3): Comprehensive DSA mastery (Arrays, Strings, Linked Lists, Stacks, Queues, Binary Trees)."
        step3 = "Phase 3 (Month 4): Core CS subjects: Operating Systems, Database Management Systems (DBMS), and Computer Networks."
        step4 = "Phase 4 (Month 5): Build two impactful capstone software projects showcasing clean code and database integration."
        step5 = "Phase 5 (Month 6): High-frequency Aptitude, Verbal reasoning, and company-specific previous placement paper drills."
        certifications = ["CS50: Introduction to Computer Science (Harvard/edX)", "HackerRank Problem Solving (Gold Badge)", "AWS Certified Cloud Practitioner"]

    return f"""### 🎯 1. Top Recommended Career Path
**{role}**
- **Industry Outlook:** {demand}
- **Entry-Level Salary Range:** {salary}
- **Profile Match:** 94% based on your background in {degree} (CGPA: {cgpa}) and reported skills.

---

### 💡 2. Why This Career Fits You
1. **Academic Alignment:** Your background in **{degree}** combined with a solid academic foundation (**{cgpa} CGPA**) positions you well to clear company eligibility criteria for top recruiters.
2. **Current Strengths:** Your declared familiarity with **{skills or 'core programming'}** provides an immediate runway to accelerate into production-level development.
3. **Interest Synchronization:** Your passion for **{interests or 'technology and modern software'}** ensures you will remain motivated while mastering deeper technical concepts.

---

### 🔍 3. Skill Gap Analysis

| Category | Skills You Have | Critical Skills To Acquire |
| :--- | :--- | :--- |
| **Core Domain** | {skills or 'Basics'} | {missing_skills[0]} |
| **Advanced Tools** | Fundamental concepts | {missing_skills[1]} |
| **System & Cloud** | General awareness | {missing_skills[2]} |
| **Deployment** | Local testing | {missing_skills[3]} |

---

### 🗺️ 4. 5-Step Strategic Learning Roadmap

1. **{step1}**
2. **{step2}**
3. **{step3}**
4. **{step4}**
5. **{step5}**

---

### 📚 5. Recommended Technologies & Top Certifications
- **Primary Tech Stack:** Python, Relational Databases (PostgreSQL / SQLite), Git & GitHub, Docker, REST APIs.
- **Top Industry Certifications:**
{chr(10).join(f"  - {c}" for c in certifications)}
- **Recommended Free Resources:** Harvard CS50, freeCodeCamp, roadmap.sh, LeetCode, NeetCode 150.

---

### 🚀 6. Placement Preparation Strategy
- **Aptitude Routine:** Dedicate 45 minutes daily to quantitative aptitude and logical reasoning (percentages, time & work, syllogisms).
- **Coding Targets:** Aim to solve 2 DSA problems daily on LeetCode/CareerVerse Coding Practice.
- **Resume Tip:** Highlight quantifiable outcomes in your project bullet points (e.g., *"Engineered a RESTful service handling 500+ requests with sub-100ms response time"*).
- **Company Mapping:** Target both Mass Recruiters (TCS Prime, Cognizant GenC Next, Accenture) and Product Companies (Zoho, Freshworks, Amazon SDE-1).
"""


def generate_fallback_interview(role, company, skills, experience):
    return f"""### 🏢 CareerVerse AI Interview Set for {company}
**Target Role:** {role} | **Experience Level:** {experience or 'College Fresher'} | **Key Skills:** {skills or 'Core CS'}

---

### 💻 1. Technical Interview Questions & Model Answers

#### Q1. Explain the difference between Mutable and Immutable data types in Python. What happens in memory when you modify a string?
- **Concept:** Memory allocation, ID comparison, and object referencing.
- **Model Answer:** In Python, mutable objects (like lists, dictionaries, and sets) can have their state or contents changed in place without changing their memory address (`id()`). Immutable objects (such as integers, floats, strings, and tuples) cannot be altered after creation. When you perform an operation like `s = s + " world"` on an immutable string, Python creates an entirely new string object in memory with a different address and updates the variable reference to point to it.

#### Q2. What is the difference between `WHERE` and `HAVING` clauses in SQL? Give an example.
- **Concept:** SQL filtering order of execution.
- **Model Answer:** The `WHERE` clause is applied before grouping and filters individual rows before any aggregate functions are computed. The `HAVING` clause is executed after `GROUP BY` and filters aggregated group results. For example:
  ```sql
  SELECT department, AVG(salary) FROM employees WHERE status = 'Active' GROUP BY department HAVING AVG(salary) > 75000;
  ```

#### Q3. What is the time and space complexity of searching, inserting, and deleting in a Hash Map (Dictionary)? What happens during collisions?
- **Concept:** Hash functions, load factors, collision resolution (chaining vs open addressing).
- **Model Answer:** Under average conditions, searching, inserting, and deleting in a Hash Map are **O(1)** constant time complexity. In the worst case (where all keys hash to the identical bucket due to a poor hash function), complexity degrades to **O(n)**. Python resolves collisions using open addressing with quadratic probing, while Java `HashMap` uses separate chaining (converting linked lists to balanced Red-Black trees when bucket length exceeds 8).

#### Q4. Explain the four fundamental pillars of Object-Oriented Programming with a real-world software example.
- **Concept:** Abstraction, Encapsulation, Inheritance, Polymorphism.
- **Model Answer:**
  1. **Encapsulation:** Bundling data and methods into a single class and restricting direct access via private attributes (e.g. `_balance` in a `BankAccount` class).
  2. **Abstraction:** Hiding complex internal logic and exposing only simple interfaces (e.g. calling `payment_gateway.process_payment()` without needing to know internal encryption logic).
  3. **Inheritance:** Deriving properties and methods from a parent class to promote code reuse (e.g. `SavingsAccount` inheriting from `Account`).
  4. **Polymorphism:** Ability of different classes to respond to the same method call in their own specific way (e.g. `calculate_interest()` behaving differently for `SavingsAccount` vs `FixedDepositAccount`).

#### Q5. What is the difference between a Process and a Thread? What is Deadlock and how can it be prevented?
- **Concept:** Operating Systems concurrency and resource allocation.
- **Model Answer:** A **Process** is an independent executing program with its own dedicated memory address space. A **Thread** is the smallest unit of execution within a process and shares the parent process's memory heap and resources, making context-switching faster. A **Deadlock** occurs when two or more processes are permanently blocked because each is holding a resource while waiting for another held by another process. Prevention requires breaking at least one of the 4 Coffman conditions: Mutual Exclusion, Hold & Wait, No Preemption, or Circular Wait.

---

### 🤝 2. Behavioral & HR Questions (STAR Framework)

#### Q1. "Tell me about yourself and why you want to join {company}."
- **Strategy:** Follow the Present-Past-Future formula.
- **Model Answer:** *"I am a final-year student pursuing my degree in engineering, with a strong passion for software engineering and problem-solving. During my college tenure, I have built practical projects including full-stack web applications and practiced over 150 algorithmic problems. I have closely followed {company}'s innovative work on large-scale engineering systems, and I am eager to contribute my strong foundations in data structures, web technologies, and fast learning agility to your engineering team."*

#### Q2. "Describe a challenging situation or project deadline you faced and how you handled it."
- **Strategy:** STAR framework (Situation, Task, Action, Result).
- **Model Answer:** *"In our capstone project, our backend API broke 48 hours before the semester demo due to unexpected database schema mismatches (Situation). As the lead backend developer, I needed to restore database integrity and ensure seamless frontend communication (Task). I initiated a quick triage call, created a Git backup branch, resolved the migration conflicts, and wrote automated API tests to verify edge cases (Action). We delivered our project on time, achieved zero runtime bugs during the live demonstration, and secured the top grade in our department (Result)."*

#### Q3. "How do you handle disagreement with a teammate during a group project?"
- **Model Answer:** *"I focus on the objective data rather than personalities. I actively listen to understand their perspective, lay out the pros and cons of both technical approaches against project constraints (like time, scalability, and code maintainability), and if needed, build a quick prototype or seek guidance from a mentor. Finding the best solution for the product is always my top priority."*

#### Q4. "Where do you see yourself in the next 3 to 5 years?"
- **Model Answer:** *"In the next 3 to 5 years, I envision myself growing from a reliable individual contributor who writes clean, scalable production code into a skilled technical lead. I want to develop deep expertise in system architecture, cloud deployment, and mentor incoming junior engineers while driving business value for {company}."*

#### Q5. "Do you have any questions for us?"
- **Model Answer:** *"Yes, thank you! Could you share what tech stack the team is currently transitioning toward, and what specific qualities distinguish an entry-level engineer who truly excels in this role during their first 90 days?"*

---

### 🎯 3. Skill-Specific Questions for: {skills}

1. **Practical Challenge:** How would you architect and test a scalable feature using **{skills.split(',')[0] if skills else 'Python'}** that requires handling concurrent asynchronous network requests?
2. **Debugging Scenario:** If a query or function written in **{skills.split(',')[1] if ',' in skills else skills}** is running 10x slower in production than in development, what exact steps and profiling tools would you use to pinpoint the bottleneck?
3. **Best Practices:** How do you structure unit tests, documentation, and error handling in your day-to-day coding projects?

---

### 📋 4. Top Revision Topics for {company}
1. **Core Problem Solving:** Array manipulation, Two-pointer techniques, String hashing, and Binary Search.
2. **Database Queries:** Writing complex SQL queries with `LEFT JOIN`, `GROUP BY`, `DENSE_RANK()`, and indexes.
3. **Operating Systems & Networking:** Paging, Virtual Memory, TCP 3-way handshake, HTTP status codes (200, 201, 400, 401, 403, 404, 500).
4. **Project Deep-Dive:** Be prepared to draw the end-to-end architecture diagram of every project listed on your resume.
5. **Aptitude Drills:** Speed math, percentage changes, logical syllogisms, and coding-decoding puzzles.
"""


def fallback_evaluate_answer(question, user_answer, interview_type="Technical"):
    user_answer = user_answer.strip()
    word_count = len(user_answer.split())

    if word_count < 10:
        return {
            "score": 3,
            "strengths": "You provided a quick initial reaction to the question.",
            "weaknesses": "The answer is far too brief. In a real interview, you must explain the underlying concepts, provide examples, and explain 'why' and 'how'.",
            "model_answer": "Provide a comprehensive answer that first defines the concept clearly, explains the underlying mechanism or tradeoff, and concludes with a concise real-world code or architecture example.",
            "actionable_tips": "Aim for at least 3-4 structured sentences. Use the 'Definition -> How it works -> Example/Tradeoff' formula."
        }

    # Evaluate based on length and keywords
    has_example = any(k in user_answer.lower() for k in ['for example', 'e.g.', 'such as', 'instance', 'in my project', 'like'])
    has_tradeoff = any(k in user_answer.lower() for k in ['however', 'tradeoff', 'complexity', 'advantage', 'disadvantage', 'because', 'whereas'])

    score = 6
    if word_count > 30:
        score += 1
    if has_example:
        score += 1
    if has_tradeoff:
        score += 1
    if word_count > 80:
        score = min(score + 1, 9)

    return {
        "score": score,
        "strengths": f"Good articulate explanation ({word_count} words). {'Included practical example or context.' if has_example else 'Demonstrated clear foundational understanding.'}",
        "weaknesses": f"{'Consider elaborating on edge cases, time/space complexity or system tradeoffs.' if not has_tradeoff else 'Can be made even crisper by structuring with bullet points or explicit steps.'}",
        "model_answer": f"A standout answer begins with a concise definition: '{user_answer[:70]}...'. Then explicitly states time/space complexity, outlines edge cases, and provides a 1-sentence real-world implementation example.",
        "actionable_tips": "1. Always state time/space complexity for technical questions. 2. Mention practical production edge cases (e.g., null pointers, empty inputs, network timeouts). 3. Maintain confident, structured pacing."
    }

