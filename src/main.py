import time
from puzzle_generator import PuzzleGenerator
from tracker import SessionTracker
from adaptive_engine import RuleBasedAdaptiveEngine, LightweightMLAdaptiveEngine, LEVELS

def get_initial_difficulty():
    while True:
        choice = input("Choose starting difficulty (Easy / Medium / Hard): ").strip().title()
        if choice in LEVELS:
            return choice
        print("Invalid choice. Please type Easy, Medium, or Hard.")

def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")

def run_session(user_name: str, max_questions: int = 10, use_ml: bool = False):
    gen = PuzzleGenerator()
    tracker = SessionTracker(user=user_name)
    adaptive = LightweightMLAdaptiveEngine() if use_ml else RuleBasedAdaptiveEngine()

    current = get_initial_difficulty()
    print(f"\nStarting session for {user_name} at {current}\n")

    history = []  # rolling window

    for i in range(1, max_questions + 1):
        puzzle = gen.generate(current)
        print(f"Q{i} [{puzzle.difficulty}] ({puzzle.operation}): {puzzle.question}")
        start = time.time()
        user_ans = ask_int("Your answer: ")
        elapsed = round(time.time() - start, 2)
        correct = (user_ans == puzzle.answer)
        tracker.log(difficulty=current, correct=correct, time_sec=elapsed)
        print("Correct!" if correct else f"Oops! The right answer is {puzzle.answer}.")
        print(f"Time: {elapsed:.2f}s\n")

        # Update rolling window
        history.append(tracker.attempts[-1])
        if len(history) > 3:
            history = history[-3:]

        # Recommend next difficulty
        if use_ml:
            next_level, reason, score = adaptive.recommend(current, history)
            # Update model with reward = window accuracy
            reward = sum(a.correct for a in history) / len(history)
            adaptive.update(history, reward)
            print(f"Adaptive (ML): {reason} (score={score:.2f}). Next: {next_level}\n")
        else:
            next_level, reason = adaptive.recommend(current, history)
            print(f"Adaptive (Rule): {reason}. Next: {next_level}\n")

        current = next_level

    # Summary
    stats = tracker.stats()
    next_reco = current  # last recommended difficulty
    accuracy_pct = round(100 * stats["accuracy"])
    print("==== Session Summary ====")
    print(f"User: {tracker.user}")
    print(f"Total questions: {stats['total']}")
    print(f"Accuracy: {accuracy_pct}%")
    print(f"Average time: {stats['avg_time']:.2f}s")
    print("Breakdown by difficulty:")
    for d, s in stats["by_difficulty"].items():
        acc = (s["correct"] / s["count"]) if s["count"] else 0
        print(f" - {d}: {s['count']} questions, {round(100*acc)}% correct, avg {s['avg_time']:.2f}s")
    print(f"Recommended starting level for next session: {next_reco}")
    print("=========================\n")

if __name__ == "__main__":
    name = input("Enter your name: ").strip() or "Learner"
    mode = input("Use ML adaptive engine? (y/N): ").strip().lower() == 'y'
    run_session(user_name=name, max_questions=10, use_ml=mode)
