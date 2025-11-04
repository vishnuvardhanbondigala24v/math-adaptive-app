# Technical Note: Adaptive Math Prototype

## Architecture
Flow: Input → Puzzle → Attempt → Track → Adapt → Next Puzzle → Summary

```
+-------------+      +------------------+      +----------------+      +-----------------+
|   Console   | ---> | PuzzleGenerator  | ---> |  User Attempt  | ---> | SessionTracker  |
+-------------+      +------------------+      +----------------+      +-----------------+
         ^                                                         |
         |                                                         v
         +---------------------------------- AdaptiveEngine <------+
```

## Adaptive logic
### Rule-based engine
- Rolling window size: 3 attempts
- Increase difficulty if:
  - Accuracy ≥ 0.8 **and** Avg time ≤ 6s
- Decrease difficulty if:
  - Accuracy ≤ 0.5 **or** Avg time ≥ 12s
- Otherwise, keep the same level.

**Rationale:** Keeps learners in an optimal challenge zone by blending correctness and pace.

### Lightweight ML engine
- Features: `[bias, window accuracy, window avg time, current level index]`
- Score: `sigmoid(w·x)`; map to difficulty change:
  - `< 0.33`: decrease
  - `0.33–0.66`: stay
  - `> 0.66`: increase
- Online update: gradient step with `reward = window accuracy`

**Rationale:** Demonstrates a minimal model that adapts weights from performance signals without a dataset.

## Key metrics tracked
- **Correctness** (boolean per question)
- **Response time** (seconds per question)
- **Derived:**
  - Window accuracy and average time
  - Overall accuracy and average time
  - Per-difficulty breakdown

## Why this approach
- Clear, explainable rule-based baseline that’s robust and simple.
- Lightweight ML path shows how we can learn an adaptation policy online with minimal overhead, making it easy to extend to richer features later.

## Handling noisy performance
- Use rolling windows to smooth single outliers.
- Combine accuracy and time to reduce false positives from guessing.
- Cap difficulty changes to ±1 level per step to avoid oscillations.
- Optional: add cooldowns (e.g., require 2 stable recommendations before changing).

## Collecting real training data
- Log anonymized sessions: sequence of puzzles, difficulty, correctness, time.
- Derive features: recent accuracy, moving averages, time distributions, error types.
- Train supervised models to predict the difficulty that yields target engagement (e.g., 70–85% accuracy, 5–10s time).
- Evaluate via A/B tests against rule-based baseline.

## Trade-offs: rule-based vs ML
- **Rule-based:**  
  + Interpretable  
  + Low compute  
  + Easy to tune  
  − Limited personalization  

- **ML:**  
  + Captures richer patterns  
  + Can personalize  
  − Needs data  
  − Risk of overfitting  
  − Less transparent  

## Scaling beyond math
- Abstract the puzzle generator interface; plug in reading comprehension, spelling, logic puzzles.
- Keep tracker and adaptive engine unchanged; only swap content-specific generators and success criteria.