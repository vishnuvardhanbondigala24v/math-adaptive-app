from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Attempt:
    difficulty: str
    correct: bool
    time_sec: float

@dataclass
class SessionTracker:
    user: str
    attempts: List[Attempt] = field(default_factory=list)

    def log(self, difficulty: str, correct: bool, time_sec: float):
        self.attempts.append(Attempt(difficulty, correct, time_sec))

    def stats(self) -> Dict:
        if not self.attempts:
            return {
                "total": 0, "accuracy": 0.0, "avg_time": 0.0,
                "by_difficulty": {}
            }
        total = len(self.attempts)
        corrects = sum(1 for a in self.attempts if a.correct)
        avg_time = sum(a.time_sec for a in self.attempts) / total
        by_diff = {}
        for a in self.attempts:
            if a.difficulty not in by_diff:
                by_diff[a.difficulty] = {"count": 0, "correct": 0, "avg_time": 0.0}
            by_diff[a.difficulty]["count"] += 1
            by_diff[a.difficulty]["correct"] += int(a.correct)
        for d in by_diff:
            count = by_diff[d]["count"]
            times = [a.time_sec for a in self.attempts if a.difficulty == d]
            by_diff[d]["avg_time"] = sum(times) / count if count else 0.0

        return {
            "total": total,
            "accuracy": corrects / total,
            "avg_time": avg_time,
            "by_difficulty": by_diff
        }
