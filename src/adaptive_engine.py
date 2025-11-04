import numpy as np

class RuleBasedAdaptiveEngine:
    def recommend(self, current_level, history):
        """
        Returns (next_level, reason, score).
        For rule-based engine, score is always None.
        """
        if not history:
            return current_level, "No history yet", None

        acc = sum(a.correct for a in history) / len(history)
        avg_time = sum(a.time_sec for a in history) / len(history)
        levels = ["Easy", "Medium", "Hard"]
        idx = levels.index(current_level)

        if acc >= 0.8 and avg_time <= 6 and idx < 2:
            return levels[idx+1], "High accuracy and fast responses → harder", None
        elif (acc <= 0.5 or avg_time >= 12) and idx > 0:
            return levels[idx-1], "Low accuracy or slow responses → easier", None
        else:
            return current_level, "Stay at same level", None


class LightweightMLAdaptiveEngine:
    def __init__(self):
        # weights for logistic regression–style update
        self.weights = np.array([0.0, 1.0, -0.5, 0.2])
        self.levels = ["Easy", "Medium", "Hard"]

    def recommend(self, current_level, history):
        """
        Returns (next_level, reason, score).
        Score is a logistic probability between 0 and 1.
        """
        if not history:
            return current_level, "No history yet", 0.5

        acc = sum(a.correct for a in history) / len(history)
        avg_time = sum(a.time_sec for a in history) / len(history)
        idx = self.levels.index(current_level)

        x = np.array([1.0, acc, avg_time / 10.0, idx])
        score = 1 / (1 + np.exp(-np.dot(self.weights, x)))

        if score < 0.33 and idx > 0:
            return self.levels[idx-1], "Model suggests easier", score
        elif score > 0.66 and idx < 2:
            return self.levels[idx+1], "Model suggests harder", score
        else:
            return current_level, "Model suggests same level", score

    def update(self, history, reward, lr=0.1):
        """
        Online update of weights using reward signal.
        """
        acc = sum(a.correct for a in history) / len(history)
        avg_time = sum(a.time_sec for a in history) / len(history)
        idx = self.levels.index(history[-1].difficulty)

        x = np.array([1.0, acc, avg_time / 10.0, idx])
        pred = 1 / (1 + np.exp(-np.dot(self.weights, x)))
        grad = (reward - pred) * x
        self.weights += lr * grad
