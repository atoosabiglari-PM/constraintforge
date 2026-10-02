import json
import streamlit as st
from google import genai
from google.genai import types

PROJECT_ID = "constraintforge-atoosa-2026"
LOCATION = "global"

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)

st.set_page_config(page_title="ConstraintForge", page_icon="⚡", layout="wide")

st.title("⚡ ConstraintForge")
st.subheader("Don't trust the first AI answer. Make solutions compete.")

st.write(
    "ConstraintForge uses Gemini to generate competing solutions, "
    "scores them against measurable constraints, and selects the strongest plan."
)

budget = st.number_input("Maximum staffing budget ($)", value=1200, step=50)
workers = st.number_input("Available workers", value=8, min_value=1, step=1)

demand = st.text_area(
    "Expected demand",
    value="""9–11 AM: Low
11 AM–1 PM: High
1–3 PM: Medium
3–5 PM: Very High
5–7 PM: Medium"""
)

constraints = st.text_area(
    "Additional constraints",
    value="Each worker costs $25/hour. No worker should work more than 8 hours."
)


def deterministic_score(candidate):
    score = 100
    reasons = []

    cost = float(candidate.get("total_cost", 999999))
    coverage = float(candidate.get("coverage_percent", 0))
    violations = int(candidate.get("constraint_violations", 99))

    if cost > budget:
        score -= min(40, (cost - budget) / max(budget, 1) * 100)
        reasons.append("Over budget")
    else:
        reasons.append("Within budget")

    score -= max(0, 100 - coverage) * 0.4

    if coverage >= 95:
        reasons.append("Strong demand coverage")

    score -= violations * 15

    if violations == 0:
        reasons.append("No constraint violations")

    return max(0, round(score, 1)), reasons


if st.button("Forge the Best Plan", type="primary"):

    prompt = f"""
You are competing to design the best staffing plan.

Available workers: {workers}
Maximum budget: ${budget}

Demand:
{demand}

Constraints:
{constraints}

Generate exactly 3 DIFFERENT candidate staffing plans.

For every candidate provide:
- name
- strategy
- total_cost (number)
- coverage_percent (number from 0 to 100)
- constraint_violations (integer)
- schedule (short description)

Return ONLY valid JSON in this exact structure:

{{
  "candidates": [
    {{
      "name": "Candidate 1",
      "strategy": "...",
      "total_cost": 1000,
      "coverage_percent": 95,
      "constraint_violations": 0,
      "schedule": "..."
    }}
  ]
}}
"""

    with st.spinner("Gemini is generating competing solutions..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

    try:
        data = json.loads(response.text)
        candidates = data["candidates"]

        scored = []

        for candidate in candidates:
            score, reasons = deterministic_score(candidate)
            candidate["score"] = score
            candidate["score_reasons"] = reasons
            scored.append(candidate)

        scored.sort(key=lambda x: x["score"], reverse=True)

        st.success("Evolution complete — strongest candidate selected.")

        cols = st.columns(len(scored))

        for col, candidate in zip(cols, scored):
            with col:
                st.metric(candidate["name"], f'{candidate["score"]}/100')
                st.write(candidate["strategy"])
                st.write(f"**Cost:** ${candidate['total_cost']}")
                st.write(f"**Coverage:** {candidate['coverage_percent']}%")
                st.write(
                    f"**Violations:** {candidate['constraint_violations']}"
                )

        winner = scored[0]

        st.divider()
        st.header("🏆 Winning Solution")
        st.subheader(winner["name"])
        st.write(winner["schedule"])

        st.write("### Why it won")
        for reason in winner["score_reasons"]:
            st.write(f"✓ {reason}")

        st.caption(
            "Gemini generates possibilities. "
            "ConstraintForge's deterministic evaluator decides which solution wins."
        )

    except Exception as e:
        st.error(f"Could not evaluate the candidates: {e}")