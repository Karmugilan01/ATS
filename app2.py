import streamlit as st
import os
from dotenv import load_dotenv
import pdfplumber
from groq import Groq

# Load environment variables
load_dotenv()

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- FUNCTIONS ----------

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def get_groq_response(prompt, resume_text, job_description):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # FREE & best for ATS
        messages=[
            {"role": "system", "content": "You are an ATS resume evaluation system."},
            {"role": "user", "content": f"""
{prompt}

Resume:
{resume_text}

Job Description:
{job_description}
"""}
        ],
        temperature=0.2,
        max_tokens=600
    )
    return completion.choices[0].message.content


# ---------- STREAMLIT UI ----------

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System 📝")

input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("Resume uploaded successfully!")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# ---------- PROMPTS ----------

input_prompt1 = """
You are an experienced HR With Tech experience in the field full Stack, Data Science,Big Data Engineering, Data Analyst, web Development , Devops, Cloud Engineer, your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on wheather the candidate's profile aligns with Highlight
the strengths and weaknesses of the applicant in relation to the specified job description.
"""

input_prompt3 = """
You are an skilled ATS(Applicant Tracking System) specialist with expertise in evaluating resumes against job descriptions for roles such as Full Stack Developer, Data Scientist, Big Data Engineer, Data Analyst, Web Developer, DevOps Engineer, and Cloud Engineer. Your task is to analyze the provided resume and job description, and provide a percentage match indicating how well the candidate's qualifications align with the job requirements. Give me the precentage for the job description provided based on the resume uploaded. First the output should come as the percentage and then keywords missing and the keywords missing and last final thoughts on how to improve the resume to match the job description.
"""

# ---------- BUTTON ACTIONS ----------

if submit1:
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        response = get_groq_response(input_prompt1, resume_text, input_text)
        st.subheader("ATS Evaluation")
        st.write(response)
    else:
        st.warning("Please upload a resume.")

elif submit3:
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        response = get_groq_response(input_prompt3, resume_text, input_text)
        st.subheader("ATS Match Result")
        st.write(response)
    else:
        st.warning("Please upload a resume.")
