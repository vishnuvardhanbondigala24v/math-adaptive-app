import time
import streamlit as st
from src.puzzle_generator import PuzzleGenerator
from src.tracker import SessionTracker
from src.adaptive_engine import RuleBasedAdaptiveEngine, LightweightMLAdaptiveEngine

st.title("🎲 Math Adventures — Adaptive Learning")

# ---------- Initialize session state ----------
defaults = {
    "active": False,
    "tracker": None,
    "gen": None,
    "adaptive": None,
    "current": "Easy",
    "q_index": 0,
    "max_q": 10,
    "history": [],
    "puzzle": None,
    "start_time": None,
    "answered": False,
    "feedback": [],
    "next_level": "Easy",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------- Sidebar ----------
user_name = st.sidebar.text_input("Enter your name", "Learner")
engine_choice = st.sidebar.radio("Adaptive Engine", ["Rule-based", "ML"])
start_level = st.sidebar.selectbox("Starting Difficulty", ["Easy", "Medium", "Hard"])
max_questions = st.sidebar.slider("Number of Questions", 5, 30, 10)

def start_session():
    st.session_state.tracker = SessionTracker(user=user_name)
    st.session_state.gen = PuzzleGenerator()
    st.session_state.adaptive = (
        LightweightMLAdaptiveEngine() if engine_choice == "ML" else RuleBasedAdaptiveEngine()
    )
    st.session_state.current = start_level
    st.session_state.q_index = 0
    st.session_state.max_q = max_questions
    st.session_state.history = []
    st.session_state.puzzle = None
    st.session_state.start_time = None
    st.session_state.answered = False
    st.session_state.feedback = []
    st.session_state.active = True

if st.sidebar.button("Start Session"):
    start_session()

# ---------- Helper ----------
def ensure_puzzle():
    if st.session_state.puzzle is None:
        st.session_state.puzzle = st.session_state.gen.generate(st.session_state.current)
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.session_state.feedback = []

# ---------- Main flow ----------
if not st.session_state.active:
    st.info("Use the sidebar to start a session.")
else:
    tracker = st.session_state.tracker
    adaptive = st.session_state.adaptive
    q_index = st.session_state.q_index
    total_q = st.session_state.max_q

    st.progress(q_index / total_q)
    st.write(f"Question {q_index+1} of {total_q}")

    if q_index < total_q:
        ensure_puzzle()
        puzzle = st.session_state.puzzle

        st.subheader(f"Q{q_index+1} [{puzzle.difficulty}] ({puzzle.operation})")
        st.write(puzzle.question)

        if not st.session_state.answered:
            ans = st.number_input("Your answer:", step=1, format="%d", key=f"ans_{q_index}")
            if st.button("Submit", key=f"submit_{q_index}"):
                elapsed = round(time.time() - (st.session_state.start_time or time.time()), 2)
                correct = (ans == puzzle.answer)
                tracker.log(difficulty=st.session_state.current, correct=correct, time_sec=elapsed)

                # Feedback
                if correct:
                    st.session_state.feedback.append(("success", "Correct!"))
                else:
                    st.session_state.feedback.append(("error", f"Oops! The right answer is {puzzle.answer}"))
                st.session_state.feedback.append(("info", f"Time: {elapsed:.2f}s"))

                # Running score
                num_correct = sum(a.correct for a in tracker.attempts)
                st.session_state.feedback.append(("write", f"✅ Correct so far: {num_correct} / {len(tracker.attempts)}"))

                # Update rolling history
                st.session_state.history.append(tracker.attempts[-1])
                if len(st.session_state.history) > 3:
                    st.session_state.history = st.session_state.history[-3:]

                # Recommend next difficulty
                next_level, reason, score = adaptive.recommend(
                    st.session_state.current, st.session_state.history
                )
                if isinstance(adaptive, LightweightMLAdaptiveEngine):
                    reward = sum(a.correct for a in st.session_state.history) / len(st.session_state.history)
                    adaptive.update(st.session_state.history, reward)
                    st.session_state.feedback.append(("write", f"**Adaptive (ML):** {reason} (score={score:.2f}) → Next: {next_level}"))
                else:
                    st.session_state.feedback.append(("write", f"**Adaptive (Rule):** {reason} → Next: {next_level}"))

                st.session_state.next_level = next_level
                st.session_state.answered = True
                st.experimental_rerun()

        else:
            # Show stored feedback
            for kind, msg in st.session_state.feedback:
                if kind == "success":
                    st.success(msg)
                elif kind == "error":
                    st.error(msg)
                elif kind == "info":
                    st.info(msg)
                else:
                    st.write(msg)

            # Next Question button
            if st.button("Next Question"):
                st.session_state.current = st.session_state.next_level
                st.session_state.q_index += 1
                st.session_state.puzzle = None
                st.session_state.start_time = None
                st.session_state.answered = False
                st.session_state.feedback = []
                st.experimental_rerun()

    else:
        st.success("Session complete!")
        stats = tracker.stats()
        st.write("### Session Summary")
        st.write(f"✅ You got {sum(a.correct for a in tracker.attempts)} out of {stats['total']} correct")
        st.write(f"Accuracy: {round(100*stats['accuracy'])}%")
        st.write(f"Average time: {stats['avg_time']:.2f}s")
        st.write("Breakdown by difficulty:")
        for d, s in stats["by_difficulty"].items():
            acc = (s['correct']/s['count']) if s['count'] else 0
            st.write(f"- {d}: {s['count']} questions, {round(100*acc)}% correct, avg {s['avg_time']:.2f}s")
        st.write(f"Recommended starting level for next session: {st.session_state['current']}")

        if st.button("Start New Session"):
            start_session()
            st.experimental_rerun()
