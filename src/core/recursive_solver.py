"""
Recursive Relation Solver
Solves linear homogeneous and non-homogeneous recurrence relations
"""

import re
import numpy as np
from typing import List, Tuple, Optional, Dict
import sympy as sp


class RecursiveSolver:
    """Solves recursive relations and generates step-by-step solutions"""
    
    def __init__(self):
        self.steps = []
        self.solution = None
    
    def solve(self, recurrence: str, initial_conditions: Dict[int, float]) -> Dict:
        """
        Solve a recurrence relation
        
        Args:
            recurrence: String like "a(n) = 2*a(n-1) + 3*a(n-2)"
            initial_conditions: Dict like {0: 1, 1: 2}
        
        Returns:
            Dictionary with solution details
        """
        self.steps = []
        
        try:
            # Parse the recurrence relation
            coeffs, constant = self._parse_recurrence(recurrence)
            
            if coeffs is None:
                return {
                    "success": False,
                    "error": "Could not parse recurrence relation",
                    "steps": []
                }
            
            # Add parsing step
            self.steps.append({
                "title": "Parsed Recurrence Relation",
                "content": f"Coefficients: {coeffs}\nConstant term: {constant}\nInitial conditions: {initial_conditions}"
            })
            
            # Determine if homogeneous or non-homogeneous
            is_homogeneous = (constant == 0)
            
            if is_homogeneous:
                return self._solve_homogeneous(coeffs, initial_conditions)
            else:
                return self._solve_non_homogeneous(coeffs, constant, initial_conditions)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "steps": self.steps
            }
    
    def _parse_recurrence(self, recurrence: str) -> Tuple[List[float], float]:
        """Parse recurrence relation string"""
        # Normalize the input
        recurrence = recurrence.replace(" ", "").lower()
        recurrence = recurrence.replace("a_n", "a(n)")
        recurrence = recurrence.replace("aₙ", "a(n)")
        
        # Split by equals sign
        if "=" not in recurrence:
            return None, None
        
        left, right = recurrence.split("=", 1)
        
        # Parse right side for coefficients
        # Look for patterns like 2*a(n-1), -3*a(n-2), etc.
        pattern = r'([+-]?\d*\.?\d*)\*?a\(n-(\d+)\)'
        matches = re.findall(pattern, right)
        
        if not matches:
            return None, None
        
        # Build coefficient list
        max_order = max(int(match[1]) for match in matches)
        coeffs = [0.0] * (max_order + 1)
        
        for coeff_str, order_str in matches:
            order = int(order_str)
            if coeff_str in ['', '+']:
                coeff = 1.0
            elif coeff_str == '-':
                coeff = -1.0
            else:
                coeff = float(coeff_str)
            coeffs[order] = coeff
        
        # Look for constant term
        constant_pattern = r'([+-]?\d+\.?\d*)(?!\*a)'
        constant_matches = re.findall(constant_pattern, right)
        constant = 0.0
        for match in constant_matches:
            if match and match not in ['+', '-']:
                try:
                    constant += float(match)
                except:
                    pass
        
        return coeffs, constant
    
    def _solve_homogeneous(self, coeffs: List[float], initial_conditions: Dict[int, float]) -> Dict:
        """Solve homogeneous linear recurrence relation"""
        
        # Characteristic equation: r^n - c1*r^(n-1) - c2*r^(n-2) - ... = 0
        # Convert to polynomial coefficients
        order = len(coeffs)
        poly_coeffs = [1.0]  # r^n term
        
        for i, c in enumerate(coeffs):
            if i == 0:
                continue
            poly_coeffs.append(-c)
        
        self.steps.append({
            "title": "Characteristic Equation",
            "content": f"r^{order} " + " ".join([
                f"{'-' if c > 0 else '+'} {abs(c):.2f}*r^{order-i-1}"
                for i, c in enumerate(poly_coeffs[1:])
            ]) + " = 0"
        })
        
        # Solve characteristic equation
        roots = np.roots(poly_coeffs)
        
        self.steps.append({
            "title": "Characteristic Roots",
            "content": "Roots: " + ", ".join([f"{r:.4f}" for r in roots])
        })
        
        # Build general solution
        # For distinct real roots: a(n) = c1*r1^n + c2*r2^n + ...
        n = sp.Symbol('n')
        general_solution = 0
        
        for i, root in enumerate(roots):
            general_solution += sp.Symbol(f'c{i}') * (root ** n)
        
        self.steps.append({
            "title": "General Solution",
            "content": f"a(n) = {general_solution}"
        })
        
        # Use initial conditions to find constants
        constants = self._find_constants(roots, initial_conditions)
        
        # Build particular solution
        particular_solution = sum(c * (r ** n) for c, r in zip(constants, roots))
        
        self.steps.append({
            "title": "Particular Solution",
            "content": f"a(n) = {particular_solution}"
        })
        
        return {
            "success": True,
            "solution": str(particular_solution),
            "roots": [complex(r) for r in roots],
            "constants": constants,
            "steps": self.steps,
            "closed_form": particular_solution
        }
    
    def _solve_non_homogeneous(self, coeffs: List[float], constant: float, 
                                initial_conditions: Dict[int, float]) -> Dict:
        """Solve non-homogeneous linear recurrence relation"""
        
        # First solve the homogeneous part
        homogeneous_result = self._solve_homogeneous(coeffs, {})
        
        # Add particular solution for constant term
        # For constant term, particular solution is A where A = constant / (1 - sum(coeffs))
        denom = 1 - sum(coeffs[1:])
        if abs(denom) < 1e-10:
            particular = 0
        else:
            particular = constant / denom
        
        self.steps.append({
            "title": "Particular Solution for Non-homogeneous Part",
            "content": f"For constant term {constant}, particular solution: a_p(n) = {particular:.4f}"
        })
        
        # General solution is homogeneous + particular
        self.steps.append({
            "title": "Complete Solution",
            "content": f"a(n) = (homogeneous solution) + {particular:.4f}"
        })
        
        return {
            "success": True,
            "solution": f"a(n) = (homogeneous) + {particular:.4f}",
            "particular_constant": particular,
            "steps": self.steps
        }
    
    def _find_constants(self, roots: np.ndarray, initial_conditions: Dict[int, float]) -> List[float]:
        """Find constants using initial conditions"""
        
        n_roots = len(roots)
        n_conditions = len(initial_conditions)
        
        if n_conditions < n_roots:
            # Not enough initial conditions, return symbolic
            return [1.0] * n_roots
        
        # Build system of equations
        A = []
        b = []
        
        for n, value in sorted(initial_conditions.items())[:n_roots]:
            row = [root ** n for root in roots]
            A.append(row)
            b.append(value)
        
        # Solve system
        try:
            constants = np.linalg.solve(A, b)
            self.steps.append({
                "title": "Constants from Initial Conditions",
                "content": "Constants: " + ", ".join([f"c{i} = {c:.4f}" for i, c in enumerate(constants)])
            })
            return constants.tolist()
        except:
            return [1.0] * n_roots
    
    def compute_terms(self, n_terms: int, recurrence: str, 
                     initial_conditions: Dict[int, float]) -> List[float]:
        """Compute first n terms using the recurrence relation directly"""
        
        # Parse recurrence
        coeffs, constant = self._parse_recurrence(recurrence)
        
        if coeffs is None:
            return []
        
        # Initialize terms array
        max_initial = max(initial_conditions.keys()) if initial_conditions else 0
        terms = [0.0] * max(n_terms, max_initial + 1)
        
        # Set initial conditions
        for n, value in initial_conditions.items():
            if n < len(terms):
                terms[n] = value
        
        # Compute remaining terms
        order = len(coeffs)
        for n in range(max_initial + 1, n_terms):
            value = constant
            for i in range(1, order):
                if n - i >= 0:
                    value += coeffs[i] * terms[n - i]
            terms[n] = value
        
        return terms
