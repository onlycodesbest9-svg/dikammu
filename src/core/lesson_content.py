"""
Lesson Content and Structure
"""

from typing import List, Dict, Any


class LessonContent:
    """Manages lesson content and structure"""
    
    @staticmethod
    def get_all_lessons() -> List[Dict[str, Any]]:
        """Get all available lessons"""
        return [
            {
                "id": "lesson1",
                "title": "Lesson 1: Sequences and Recurrence Relations",
                "description": "Introduction to sequences and basic recurrence relations",
                "order": 1,
                "content": LessonContent._get_lesson1_content(),
                "exercises": LessonContent._get_lesson1_exercises()
            },
            {
                "id": "lesson2",
                "title": "Lesson 2: Solving Linear Homogeneous Recurrence Relations",
                "description": "Learn to solve linear homogeneous recurrence relations",
                "order": 2,
                "content": LessonContent._get_lesson2_content(),
                "exercises": LessonContent._get_lesson2_exercises()
            },
            {
                "id": "lesson3",
                "title": "Lesson 3: Applications of Recurrence Relations",
                "description": "Real-world applications and problem solving",
                "order": 3,
                "content": LessonContent._get_lesson3_content(),
                "exercises": LessonContent._get_lesson3_exercises()
            }
        ]
    
    @staticmethod
    def _get_lesson1_content() -> str:
        """Content for Lesson 1"""
        return """
<h2>Sequences and Recurrence Relations</h2>

<h3>What is a Sequence?</h3>
<p>A <b>sequence</b> is an ordered list of numbers. Each number in the sequence is called a <b>term</b>.</p>

<p><b>Example:</b> 1, 3, 5, 7, 9, ... (odd numbers)</p>

<p>We denote sequences using notation like <i>a₀, a₁, a₂, a₃, ...</i> or <i>a(n)</i> where n is the index.</p>

<h3>What is a Recurrence Relation?</h3>
<p>A <b>recurrence relation</b> is an equation that defines a sequence recursively. Each term is defined in terms of previous terms.</p>

<p><b>General form:</b> aₙ = f(aₙ₋₁, aₙ₋₂, ..., aₙ₋ₖ)</p>

<h3>Example 1: Simple Linear Recurrence</h3>
<div class="example">
<p><b>Problem:</b> aₙ = aₙ₋₁ + 5, with a₀ = 5</p>
<p><b>Solution:</b></p>
<ul>
<li>a₀ = 5</li>
<li>a₁ = a₀ + 5 = 5 + 5 = 10</li>
<li>a₂ = a₁ + 5 = 10 + 5 = 15</li>
<li>a₃ = a₂ + 5 = 15 + 5 = 20</li>
<li>a₄ = a₃ + 5 = 20 + 5 = 25</li>
</ul>
<p>This is an arithmetic sequence with common difference 5.</p>
<p><b>Closed form:</b> aₙ = 5 + 5n</p>
</div>

<h3>Example 2: Compound Interest</h3>
<div class="example">
<p>Suppose you invest $10,000 at 7% annual interest. How much will you have after n years?</p>
<p><b>Recurrence:</b> Aₙ = 1.07 × Aₙ₋₁, with A₀ = 10,000</p>
<p><b>Solution:</b></p>
<ul>
<li>A₀ = 10,000</li>
<li>A₁ = 1.07 × 10,000 = 10,700</li>
<li>A₂ = 1.07 × 10,700 = 11,449</li>
<li>A₃ = 1.07 × 11,449 = 12,250.43</li>
</ul>
<p><b>Closed form:</b> Aₙ = 10,000 × (1.07)ⁿ</p>
</div>

<h3>Example 3: Number of Subsets</h3>
<div class="example">
<p>How many subsets does a set with n elements have?</p>
<p><b>Recurrence:</b> Sₙ = 2 × Sₙ₋₁, with S₀ = 1</p>
<p><b>Reasoning:</b> When adding a new element, each existing subset can either include or exclude it, doubling the count.</p>
<p><b>Closed form:</b> Sₙ = 2ⁿ</p>
</div>

<h3>Example 4: Tower of Hanoi</h3>
<div class="example">
<p>The Tower of Hanoi puzzle: Move n disks from one peg to another, with the rule that no larger disk can be on top of a smaller one.</p>
<p><b>Recurrence:</b> Tₙ = 2 × Tₙ₋₁ + 1, with T₁ = 1</p>
<p><b>Reasoning:</b></p>
<ul>
<li>Move top n-1 disks to auxiliary peg (Tₙ₋₁ moves)</li>
<li>Move largest disk to target peg (1 move)</li>
<li>Move n-1 disks to target peg (Tₙ₋₁ moves)</li>
</ul>
<p><b>Closed form:</b> Tₙ = 2ⁿ - 1</p>
</div>

<h3>Key Concepts</h3>
<ul>
<li><b>Initial conditions:</b> Values needed to start computing the sequence</li>
<li><b>Order:</b> The number of previous terms used (e.g., aₙ = aₙ₋₁ + aₙ₋₂ is second-order)</li>
<li><b>Linear vs. Non-linear:</b> Linear relations have terms that aren't multiplied together</li>
<li><b>Homogeneous vs. Non-homogeneous:</b> Homogeneous relations have no constant term</li>
</ul>
"""
    
    @staticmethod
    def _get_lesson1_exercises() -> List[Dict]:
        """Exercises for Lesson 1"""
        return [
            {
                "question": "Find the first 5 terms of the sequence defined by aₙ = aₙ₋₁ + 3, a₀ = 2",
                "type": "terms",
                "answer": [2, 5, 8, 11, 14],
                "hint": "Start with a₀ = 2 and add 3 repeatedly"
            },
            {
                "question": "What is the closed form of aₙ = 2aₙ₋₁, a₀ = 3?",
                "type": "multiple_choice",
                "options": ["aₙ = 3 × 2ⁿ", "aₙ = 2 × 3ⁿ", "aₙ = 2n + 3", "aₙ = 3n + 2"],
                "answer": 0,
                "hint": "Each term is multiplied by 2"
            },
            {
                "question": "If you invest $5000 at 5% annual interest, how much will you have after 3 years?",
                "type": "numeric",
                "answer": 5788.13,
                "tolerance": 0.5,
                "hint": "Use Aₙ = A₀ × (1.05)ⁿ"
            }
        ]
    
    @staticmethod
    def _get_lesson2_content() -> str:
        """Content for Lesson 2"""
        return """
<h2>Solving Linear Homogeneous Recurrence Relations</h2>

<h3>What is a Linear Homogeneous Recurrence Relation?</h3>
<p>A <b>linear homogeneous recurrence relation</b> of degree k with constant coefficients has the form:</p>
<p><b>aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ + ... + cₖaₙ₋ₖ</b></p>
<p>where c₁, c₂, ..., cₖ are constants and cₖ ≠ 0.</p>

<h3>The Characteristic Equation Method</h3>
<p>To solve these relations, we use the <b>characteristic equation</b> approach:</p>

<h4>Step 1: Form the Characteristic Equation</h4>
<p>Assume aₙ = rⁿ is a solution. Substituting into the recurrence:</p>
<p>rⁿ = c₁rⁿ⁻¹ + c₂rⁿ⁻² + ... + cₖrⁿ⁻ᵏ</p>
<p>Dividing by rⁿ⁻ᵏ:</p>
<p><b>rᵏ - c₁rᵏ⁻¹ - c₂rᵏ⁻² - ... - cₖ = 0</b></p>

<h4>Step 2: Solve for the Roots</h4>
<p>Find the roots r₁, r₂, ..., rₖ of the characteristic equation.</p>

<h4>Step 3: Form the General Solution</h4>
<p><b>Case 1: Distinct Roots</b></p>
<p>If all roots are distinct: <b>aₙ = α₁r₁ⁿ + α₂r₂ⁿ + ... + αₖrₖⁿ</b></p>

<p><b>Case 2: Repeated Roots</b></p>
<p>If a root r is repeated m times: <b>aₙ = (α₁ + α₂n + α₃n² + ... + αₘnᵐ⁻¹)rⁿ</b></p>

<h4>Step 4: Use Initial Conditions</h4>
<p>Use the initial conditions to solve for α₁, α₂, ..., αₖ.</p>

<h3>Example 1: Second-Order Relation</h3>
<div class="example">
<p><b>Problem:</b> Solve aₙ = 3aₙ₋₁ - 2aₙ₋₂, with a₀ = 1, a₁ = 4</p>

<p><b>Step 1: Characteristic Equation</b></p>
<p>r² - 3r + 2 = 0</p>

<p><b>Step 2: Find Roots</b></p>
<p>(r - 1)(r - 2) = 0</p>
<p>r₁ = 1, r₂ = 2</p>

<p><b>Step 3: General Solution</b></p>
<p>aₙ = α₁(1)ⁿ + α₂(2)ⁿ = α₁ + α₂(2ⁿ)</p>

<p><b>Step 4: Use Initial Conditions</b></p>
<p>a₀ = 1: α₁ + α₂ = 1</p>
<p>a₁ = 4: α₁ + 2α₂ = 4</p>
<p>Solving: α₂ = 3, α₁ = -2</p>

<p><b>Final Solution:</b> aₙ = -2 + 3(2ⁿ) = 3(2ⁿ) - 2</p>
</div>

<h3>Example 2: Fibonacci Sequence</h3>
<div class="example">
<p><b>Problem:</b> Solve Fₙ = Fₙ₋₁ + Fₙ₋₂, with F₀ = 0, F₁ = 1</p>

<p><b>Characteristic Equation:</b> r² - r - 1 = 0</p>

<p><b>Roots:</b> r = (1 ± √5) / 2</p>
<p>r₁ = φ = (1 + √5) / 2 ≈ 1.618 (golden ratio)</p>
<p>r₂ = (1 - √5) / 2 ≈ -0.618</p>

<p><b>General Solution:</b> Fₙ = α₁φⁿ + α₂((1-√5)/2)ⁿ</p>

<p>Using initial conditions: <b>Fₙ = (φⁿ - (1-√5)/2)ⁿ) / √5</b></p>

<p>This is Binet's formula!</p>
</div>

<h3>Practice Tips</h3>
<ul>
<li>Always check the order of your recurrence relation</li>
<li>Make sure you have enough initial conditions</li>
<li>Verify your solution by computing a few terms</li>
<li>Watch for repeated roots - they change the solution form</li>
</ul>
"""
    
    @staticmethod
    def _get_lesson2_exercises() -> List[Dict]:
        """Exercises for Lesson 2"""
        return [
            {
                "question": "What is the characteristic equation for aₙ = 4aₙ₋₁ - 3aₙ₋₂?",
                "type": "multiple_choice",
                "options": [
                    "r² - 4r + 3 = 0",
                    "r² + 4r - 3 = 0",
                    "r² - 3r + 4 = 0",
                    "4r² - 3r = 0"
                ],
                "answer": 0,
                "hint": "Form: rⁿ = 4rⁿ⁻¹ - 3rⁿ⁻², divide by rⁿ⁻²"
            },
            {
                "question": "Find the roots of r² - 5r + 6 = 0",
                "type": "multiple_choice",
                "options": ["r = 2, 3", "r = 1, 6", "r = -2, -3", "r = 5, 1"],
                "answer": 0,
                "hint": "Factor: (r - 2)(r - 3) = 0"
            },
            {
                "question": "If the characteristic roots are r₁ = 2 and r₂ = 3, what is the general solution?",
                "type": "multiple_choice",
                "options": [
                    "aₙ = α₁(2ⁿ) + α₂(3ⁿ)",
                    "aₙ = α₁(2) + α₂(3)",
                    "aₙ = (α₁ + α₂n)(2ⁿ)",
                    "aₙ = 2ⁿ + 3ⁿ"
                ],
                "answer": 0,
                "hint": "For distinct roots, use aₙ = α₁r₁ⁿ + α₂r₂ⁿ"
            }
        ]
    
    @staticmethod
    def _get_lesson3_content() -> str:
        """Content for Lesson 3"""
        return """
<h2>Applications of Recurrence Relations</h2>

<h3>Introduction</h3>
<p>Recurrence relations appear throughout computer science, mathematics, and real-world problems. Let's explore some important applications.</p>

<h3>Application 1: Algorithm Analysis</h3>
<div class="example">
<h4>Binary Search Complexity</h4>
<p>Binary search divides the search space in half each time.</p>
<p><b>Recurrence:</b> T(n) = T(n/2) + 1, T(1) = 1</p>
<p><b>Solution:</b> T(n) = log₂(n)</p>
<p>This tells us binary search has O(log n) time complexity.</p>
</div>

<div class="example">
<h4>Merge Sort Complexity</h4>
<p>Merge sort divides array in half, sorts each half, then merges.</p>
<p><b>Recurrence:</b> T(n) = 2T(n/2) + n, T(1) = 1</p>
<p><b>Solution:</b> T(n) = n log₂(n)</p>
<p>This gives us O(n log n) time complexity.</p>
</div>

<h3>Application 2: Counting Problems</h3>
<div class="example">
<h4>Binary Strings Without Consecutive 1s</h4>
<p>Count n-bit binary strings with no two consecutive 1s.</p>
<p><b>Analysis:</b></p>
<ul>
<li>If string ends in 0: previous n-1 bits can be any valid string (aₙ₋₁ ways)</li>
<li>If string ends in 1: must end in 01, so previous n-2 bits can be any valid string (aₙ₋₂ ways)</li>
</ul>
<p><b>Recurrence:</b> aₙ = aₙ₋₁ + aₙ₋₂, with a₁ = 2, a₂ = 3</p>
<p>This is the Fibonacci sequence shifted!</p>
</div>

<h3>Application 3: Financial Mathematics</h3>
<div class="example">
<h4>Loan Payments</h4>
<p>A loan of $L at interest rate r with monthly payment P.</p>
<p><b>Recurrence:</b> Aₙ = (1 + r)Aₙ₋₁ - P, with A₀ = L</p>
<p>This is a non-homogeneous recurrence relation.</p>
<p><b>Solution gives:</b> Number of months to pay off the loan</p>
</div>

<h3>Application 4: Combinatorics</h3>
<div class="example">
<h4>Catalan Numbers</h4>
<p>Count of valid parenthesis sequences, binary trees, etc.</p>
<p><b>Recurrence:</b> Cₙ = Σ(Cᵢ × Cₙ₋ᵢ₋₁) for i = 0 to n-1, C₀ = 1</p>
<p><b>Closed form:</b> Cₙ = (2n)! / ((n+1)! × n!)</p>
<p><b>Values:</b> 1, 1, 2, 5, 14, 42, 132, ...</p>
</div>

<h3>Application 5: Game Theory</h3>
<div class="example">
<h4>Nim Game</h4>
<p>Two players, pile of n stones, take 1 or 2 stones per turn.</p>
<p><b>Recurrence for winning positions:</b> W(n) = ¬(W(n-1) ∧ W(n-2))</p>
<p>Analysis reveals: positions n where n ≡ 0 (mod 3) are losing positions.</p>
</div>

<h3>Application 6: Dynamic Programming</h3>
<div class="example">
<h4>Climbing Stairs</h4>
<p>Ways to climb n stairs taking 1 or 2 steps at a time.</p>
<p><b>Recurrence:</b> W(n) = W(n-1) + W(n-2), W(1) = 1, W(2) = 2</p>
<p>This is another Fibonacci sequence!</p>
</div>

<h3>Key Takeaways</h3>
<ul>
<li>Many real-world problems can be modeled with recurrence relations</li>
<li>Solving the recurrence gives insight into growth rates and complexity</li>
<li>The same recurrence pattern can appear in very different contexts</li>
<li>Recognizing common patterns (Fibonacci, geometric, etc.) helps solve new problems</li>
</ul>
"""
    
    @staticmethod
    def _get_lesson3_exercises() -> List[Dict]:
        """Exercises for Lesson 3"""
        return [
            {
                "question": "A bacteria population doubles every hour. If you start with 100 bacteria, how many after 5 hours?",
                "type": "numeric",
                "answer": 3200,
                "tolerance": 0,
                "hint": "Use Pₙ = P₀ × 2ⁿ"
            },
            {
                "question": "How many ways can you tile a 2×n board with 1×2 dominoes?",
                "type": "multiple_choice",
                "options": [
                    "Fibonacci sequence",
                    "Powers of 2",
                    "Factorial",
                    "Linear sequence"
                ],
                "answer": 0,
                "hint": "Consider last domino: vertical or two horizontal"
            },
            {
                "question": "What's the time complexity of a recursive function with T(n) = 2T(n-1) + 1?",
                "type": "multiple_choice",
                "options": ["O(2ⁿ)", "O(n²)", "O(n log n)", "O(log n)"],
                "answer": 0,
                "hint": "Exponential growth pattern"
            }
        ]
