import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf_content, propmt):
    model = genai.GenerativeModel("gemini-3-pro-preview")
    response= model.generate_content([input, pdf_content[0], propmt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        uploaded_file.seek(0)
        images = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=r"C:\poppler\Library\bin")
        first_page = images[0]


        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System 📝")
input_text = st.text_area("Job description : ", key="input")
uploaded_file = st.file_uploader("Upload Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("Resume uploaded successfully!")

sumbit1 = st.button("Tell Me About the Resume")

##submit2 = st.button("How Can I Improvise my skills")

submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR With Tech experience in the field full Stack, Data Science,Big Data Engineering, Data Analyst, web Development , Devops, Cloud Engineer, your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on wheather the candidate's profile aligns with Highlight
the strengths and weaknesses of the applicant in relation to the specified job description.
"""

input_prompt3 = """
You are an skilled ATS(Applicant Tracking System) specialist with expertise in evaluating resumes against job descriptions for roles such as Full Stack Developer, Data Scientist, Big Data Engineer, Data Analyst, Web Developer, DevOps Engineer, and Cloud Engineer. Your task is to analyze the provided resume and job description, and provide a percentage match indicating how well the candidate's qualifications align with the job requirements. Give me the precentage for the job description provided based on the resume uploaded. First the output should come as the percentage and then keywords missing and the keywords missing and last final thoughts on how to improve the resume to match the job description.
"""

if sumbit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload a resume to proceed.")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload a resume to proceed.")    