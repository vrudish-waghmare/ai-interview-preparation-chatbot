from utils.llm import query_llm
def generate_followup(question, answer, feedback, role, difficulty, skills, profile):
    prompt = f"""
You are a senior interviewer.

Candidate Profile:
Name: {profile.get("first_name", "")}
Background: {profile.get("bio", "")}

Role: {role}
Difficulty: {difficulty}
Skills: {skills}

Question:
{question}

Answer:
{answer}

Feedback:
{feedback}

Ask ONE smart follow-up:
- personalized
- targets weaknesses
- matches candidate level

Only return question.
"""
    return query_llm(prompt)
