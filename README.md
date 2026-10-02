# ⚡ ConstraintForge

## Don't trust the first AI answer. Make solutions compete.

ConstraintForge is an AI decision engine that uses **Google Gemini on Vertex AI** to generate multiple competing solutions to a constrained real-world problem, then uses a **deterministic evaluator** to score, rank, and select the strongest solution.

### The Problem

Generative AI usually gives users one answer.

But for real operational decisions, the first plausible answer is not necessarily the best answer.

### The ConstraintForge Approach

**Constraints → Gemini candidate generation → Deterministic evaluation → Competition → Winning solution**

Instead of asking Gemini for one recommendation, ConstraintForge generates competing strategies.

Each candidate is evaluated against measurable criteria such as:

- Budget compliance
- Demand coverage
- Constraint violations

The strongest candidate wins based on the evaluator — not simply because the model says it is best.

### Demo

The current MVP solves a staffing optimization problem.

Given:

- Available workers
- Maximum budget
- Demand peaks
- Labor constraints

Gemini generates three different staffing strategies. ConstraintForge independently scores them and selects the strongest plan.

### Architecture

User Constraints  
↓  
Gemini 2.5 Flash on Vertex AI  
↓  
Multiple Candidate Solutions  
↓  
Deterministic Python Evaluator  
↓  
Score + Rank  
↓  
🏆 Winning Solution

### Built With

- Google Cloud
- Vertex AI
- Gemini 2.5 Flash
- Python
- Streamlit
- Google Gen AI SDK

### Why ConstraintForge?

The core idea is simple:

> **Generation proposes. Evaluation decides.**

ConstraintForge separates AI creativity from deterministic decision logic, creating a foundation for evolutionary optimization across staffing, scheduling, logistics, resource allocation, infrastructure planning, and other constrained decision problems.

### DevFest Bay Area 2026

Built at DevFest Bay Area 2026.
