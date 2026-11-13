import random

QUESTIONS = {
    "Software Engineer": [
        "Explain how a REST API works.",
        "What is caching and why is it important?",
        "Explain database indexing.",
        "Difference between SQL and NoSQL?"
    ],
    "Data Scientist": [
        "Explain bias-variance tradeoff.",
        "What is overfitting?",
        "Difference between supervised and unsupervised learning?",
        "Explain logistic regression."
    ],
    "Product Manager": [
        "How do you prioritize features?",
        "What is a product roadmap?",
        "How do you measure product success?",
        "Describe a product you would improve and why."
    ]
}

def get_question(role):
    return random.choice(QUESTIONS.get(role, QUESTIONS["Software Engineer"]))