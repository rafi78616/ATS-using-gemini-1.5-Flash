from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_content(uploaded_file):
    """Convert PDF file to base64 encoded data"""
    if uploaded_file is not None:
        # Read PDF content
        pdf_bytes = uploaded_file.read()
        
        # Create the parts object expected by Gemini
        pdf_parts = [
            {
                "mime_type": "application/pdf",
                "data": base64.b64encode(pdf_bytes).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_gemini_response(input_prompt, pdf_content, job_description):
    """Get response from Gemini model"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, pdf_content[0], job_description])
    return response.text

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input areas
job_description = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

# Action buttons
col1, col2 = st.columns(2)
with col1:
    submit_review = st.button("Analyze Resume")
with col2:
    submit_match = st.button("Calculate Match %")

# Prompts
RESUME_REVIEW_PROMPT = """
You are an experienced Technical Human Resource Manager. Please review the provided resume 
against the job description and provide:
1. Overall evaluation of candidate's profile alignment with the role
2. Key strengths identified
3. Areas for improvement
4. Specific recommendations for the candidate

Be thorough but concise in your evaluation.
"""

MATCH_ANALYSIS_PROMPT = """
As an ATS (Applicant Tracking System) expert, analyze the resume against the job description 
and provide:
1. Overall match percentage
2. Missing keywords and required skills
3. Recommendations for improving the match percentage
4. Final assessment

Format the response clearly with sections and bullet points.
"""

# Process requests
if submit_review:
    if uploaded_file is not None:
        with st.spinner("Analyzing resume..."):
            try:
                pdf_content = get_pdf_content(uploaded_file)
                response = get_gemini_response(RESUME_REVIEW_PROMPT, pdf_content, job_description)
                st.subheader("Resume Analysis")
                st.write(response)
            except Exception as e:
                st.error(f"Error analyzing resume: {str(e)}")
                st.error("Details: Please make sure your PDF is not password protected and is readable.")
    else:
        st.warning("Please upload a resume first")

elif submit_match:
    if uploaded_file is not None:
        with st.spinner("Calculating match percentage..."):
            try:
                pdf_content = get_pdf_content(uploaded_file)
                response = get_gemini_response(MATCH_ANALYSIS_PROMPT, pdf_content, job_description)
                st.subheader("Match Analysis")
                st.write(response)
            except Exception as e:
                st.error(f"Error calculating match: {str(e)}")
                st.error("Details: Please make sure your PDF is not password protected and is readable.")
    else:
        st.warning("Please upload a resume first")