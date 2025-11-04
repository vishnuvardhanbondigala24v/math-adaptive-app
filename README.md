#  Math Adventures — AI-Powered Adaptive Learning Prototype

A minimal adaptive math learning system designed for children (ages 5–10).  
It generates simple math puzzles, tracks performance, and dynamically adjusts difficulty using either **rule-based logic** or a **lightweight ML engine**.  

The goal: keep learners in their **optimal challenge zone** — not too easy, not too hard.

---

##  Features
- **3 difficulty levels**: Easy, Medium, Hard  
- **Operations**: Addition, Subtraction, Multiplication, Division (division ensures exact answers)  
- **Performance tracking**: correctness + response time  
- **Adaptive engine**:
  - Rule-based thresholds (accuracy + speed)
  - Lightweight ML engine (logistic-style online updates)  
- **Session summary**: accuracy %, average time, per-difficulty breakdown, and recommended next level  
- **Two interfaces**:
  - Console app (minimal, fast to test)
  - Streamlit app (kid-friendly web UI)

---

##  Repo Structure
math-adaptive-prototype/
├─ README.md 
├─ requirements.txt 
├─ technical_note.md 
├─ src/ 
│ ├─ main.py # Console app 
│ ├─ puzzle_generator.py # Puzzle creation │ 
│ ├─ tracker.py # Performance logging │ 
│ └─ adaptive_engine.py # Rule-based + ML adaptive logic 
└─ app.py # Streamlit web app

Code

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Run console version
bash
python src/main.py
Flow:

Enter your name

Choose adaptive engine (Rule-based or ML)

Choose starting difficulty

Answer questions → difficulty adapts automatically

End summary shows stats + next recommended level

3. Run Streamlit version
bash
streamlit run app.py
Opens in your browser at http://localhost:8501

Sidebar: enter name, engine choice, starting difficulty, number of questions

Main area: interactive Q&A with adaptive feedback

End summary displayed in the app