import os
import streamlit as st
from groq import Groq

# Initialize Groq client 
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=API_KEY)

st.set_page_config(page_title="AI Interview Question Generator", layout="centered")
st.title("🎯 AI Interview Question Generator ")

# ===== USER INPUTS =====
job_role = st.selectbox(
    "Select Job Role",
    ["Software Engineer", "Data Scientist", "Frontend Developer", "Backend Developer", "AI/ML Engineer"]
)

experience_level = st.selectbox(
    "Select Experience Level",
    ["Junior", "Mid", "Senior"]
)

question_type = st.multiselect(
    "Select Question Type",
    ["Technical Questions", "HR / Behavioral Questions"],
    default=["Technical Questions", "HR / Behavioral Questions"]
)

generate_btn = st.button("Generate Interview Questions")

# ===== PROMPT CREATION =====
def build_prompt(role, level, q_types):
    return f"""
You are an experienced technical interviewer.

Generate interview questions for the following:
- Job Role: {role}
- Experience Level: {level}
- Question Types: {', '.join(q_types)}

Rules:
- Provide 5 questions per selected type
- Keep questions clear and concise
- Do not add explanations or answers
- Format as numbered bullet points
"""

# ===== LLM CALL =====
def generate_questions(prompt):
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return chat_completion.choices[0].message.content

# ===== OUTPUT =====
if generate_btn:
    if not GROQ_API_KEY:
        st.error("API key not found. Please set GROQ_API_KEY.")
    else:
        with st.spinner("Generating questions..."):
            prompt = build_prompt(job_role, experience_level, question_type)
            result = generate_questions(prompt)
            st.subheader("📋 Generated Interview Questions")
            st.write(result)
