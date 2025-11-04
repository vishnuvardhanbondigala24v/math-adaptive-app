import random
from dataclasses import dataclass

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

@dataclass
class Puzzle:
    question: str
    answer: int
    difficulty: str
    operation: str
    operands: tuple

class PuzzleGenerator:
    def __init__(self, operations=("addition", "subtraction", "multiplication", "division")):
        self.operations = operations

    def _range_for_difficulty(self, difficulty: str):
        if difficulty == "Easy":
            return (1, 10)
        elif difficulty == "Medium":
            return (5, 20)
        elif difficulty == "Hard":
            return (10, 50)
        else:
            return (1, 10)

    def _choose_operation(self, difficulty: str):
        # Keep operations age-friendly; control division complexity
        if difficulty == "Easy":
            return random.choice(["addition", "subtraction"])
        elif difficulty == "Medium":
            return random.choice(["addition", "subtraction", "multiplication"])
        else:
            return random.choice(["addition", "subtraction", "multiplication", "division"])

    def generate(self, difficulty: str):
        low, high = self._range_for_difficulty(difficulty)
        op = self._choose_operation(difficulty)
        a = random.randint(low, high)
        b = random.randint(low, high)

        if op == "addition":
            ans = a + b
            q = f"{a} + {b} = ?"
        elif op == "subtraction":
            # Ensure non-negative results for kids
            a, b = max(a, b), min(a, b)
            ans = a - b
            q = f"{a} - {b} = ?"
        elif op == "multiplication":
            # Keep products within manageable bounds
            ans = a * b
            q = f"{a} × {b} = ?"
        else:  # division
            # Force exact division to avoid fractions
            b = random.randint(low, max(2, high))
            ans = random.randint(low, high // max(2, b) if high > b else low)
            a = ans * b
            q = f"{a} ÷ {b} = ?"

        return Puzzle(question=q, answer=ans, difficulty=difficulty, operation=op, operands=(a, b))
