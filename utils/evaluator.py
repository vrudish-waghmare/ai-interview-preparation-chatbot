import json
from utils.llm import query_llm

def safe_parse_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except:
        return None

def evaluate_answer(question, answer):
    prompt = f"""
You are an expert interviewer.

Question: {question}
Answer: {answer}

Evaluate and return ONLY JSON:

{{
  "score": 0-10,
  "skills": {{
    "communication": 0-10,
    "technical": 0-10,
    "clarity": 0-10,
    "problem_solving": 0-10
  }},
  "strengths": ["..."],
  "weaknesses": ["..."],
  "missing_concepts": ["..."]
}}

Rules:
- Strict JSON only
- All scores must be integers
"""

    result = query_llm(prompt)

    if not result:
        return default_response("LLM failed")

    data = safe_parse_json(result)

    if not data:
        return default_response("Parsing failed")

    return data


def default_response(reason):
    return {
        "score": 5,
        "skills": {
            "communication": 5,
            "technical": 5,
            "clarity": 5,
            "problem_solving": 5
        },
        "strengths": [],
        "weaknesses": [reason],
        "missing_concepts": []
    }
