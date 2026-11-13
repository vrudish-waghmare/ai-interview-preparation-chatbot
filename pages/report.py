import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import io
from utils.session import require_login

st.set_page_config(layout="wide")

# auto login using cookie
require_login()


st.title("📊 Interview Report")

history = st.session_state.get("history", [])
total_score = st.session_state.get("total_score", 0)

# handle no interview data
if not history:
    st.warning("No interview data found.")
    if st.button("Start New Interview"):
        st.switch_page("streamlit_app.py")
    st.stop()

# average score
avg_score = total_score / len(history)
st.metric("Average Score", f"{avg_score:.2f}/10")

st.markdown("---")

# skill aggregate
skill_totals = {
    "communication": 0,
    "technical": 0,
    "clarity": 0,
    "problem_solving": 0
}

for item in history:
    skills = item.get("skills", {})
    for key in skill_totals:
        skill_totals[key] += skills.get(key, 0)

count = len(history)

if count > 0:
    for key in skill_totals:
        skill_totals[key] /= count

# skill data
st.subheader("🧠 Skill Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Communication", f"{skill_totals['communication']:.1f}")
col2.metric("Technical", f"{skill_totals['technical']:.1f}")
col3.metric("Clarity", f"{skill_totals['clarity']:.1f}")
col4.metric("Problem Solving", f"{skill_totals['problem_solving']:.1f}")

# bar chart
st.subheader("📊 Skill Visualization")

skills_names = list(skill_totals.keys())
skills_values = list(skill_totals.values())

fig, ax = plt.subplots()
ax.bar(skills_names, skills_values)

ax.set_ylabel("Score")
ax.set_title("Skill Performance")

st.pyplot(fig)

st.markdown("---")


# radar chart
st.subheader("🕸 Radar Chart (Skill Overview)")

labels = list(skill_totals.keys())
values = list(skill_totals.values())


values += values[:1]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(subplot_kw=dict(polar=True))

ax.plot(angles, values)
ax.fill(angles, values, alpha=0.1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(
    [label.replace("_", " ").title() for label in labels]
)

st.pyplot(fig)

# question breakdown
st.subheader("📌 Detailed Feedback")

for i, item in enumerate(history):
    with st.expander(f"Question {i+1}"):

        st.markdown("**Question:**")
        st.write(item["question"])

        st.markdown("**Your Answer:**")
        st.write(item["answer"])

        st.markdown("**Score:**")
        st.write(item["score"])

        # Skill breakdown per question
        st.markdown("**Skill Scores:**")
        skills = item.get("skills", {})
        for k, v in skills.items():
            st.write(f"- {k.capitalize()}: {v}/10")

        st.markdown("**Strengths:**")
        for s in item.get("strengths", []):
            st.write(f"- {s}")

        st.markdown("**Weaknesses:**")
        for w in item.get("weaknesses", []):
            st.write(f"- {w}")

        st.markdown("**Missing Concepts:**")
        for m in item.get("missing_concepts", []):
            st.write(f"- {m}")



st.markdown("---")
st.subheader("📤 Export & Share")


# export json
report_data = {
    "average_score": avg_score,
    "skills": skill_totals,
    "history": history
}

json_bytes = json.dumps(report_data, indent=2).encode("utf-8")

st.download_button(
    label="⬇️ Download JSON",
    data=json_bytes,
    file_name="interview_report.json",
    mime="application/json",
    use_container_width=True
)

# export pdf
def generate_pdf():
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Interview Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Average Score: {avg_score:.2f}/10", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Skill Summary:", styles["Heading2"]))
    for k, v in skill_totals.items():
        elements.append(Paragraph(f"{k.capitalize()}: {v:.1f}", styles["Normal"]))

    elements.append(Spacer(1, 12))

    for i, item in enumerate(history):
        elements.append(Paragraph(f"Q{i+1}: {item['question']}", styles["Heading3"]))
        elements.append(Paragraph(f"Answer: {item['answer']}", styles["Normal"]))
        elements.append(Paragraph(f"Score: {item['score']}", styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)
    buffer.seek(0)

    return buffer


pdf_file = generate_pdf()

st.download_button(
    label="⬇️ Download PDF",
    data=pdf_file,
    file_name="interview_report.pdf",
    mime="application/pdf",
    use_container_width=True
)

# share data

st.markdown("### 🔗 Share Report")

share_text = json.dumps(report_data)

st.code(share_text[:500] + "...", language="json")


# restart button
if st.button("🔁 Restart Interview"):
    st.session_state.clear()
    st.switch_page("streamlit_app.py")