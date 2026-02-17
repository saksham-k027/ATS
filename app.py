from dotenv import load_dotenv
load_dotenv()



import os
import shutil
import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from google import genai

st.write("API KEY LOADED:", bool(os.getenv("GOOGLE_API_KEY")))
# ================= SYSTEM CONFIG =================

# ---- Tesseract Detection ----
tesseract_path = shutil.which("tesseract")
if not tesseract_path:
    st.error("❌ Tesseract OCR not found. Install with: brew install tesseract")
    st.stop()

pytesseract.pytesseract.tesseract_cmd = tesseract_path

# ---- Poppler Detection ----
pdfinfo_path = shutil.which("pdfinfo")
if not pdfinfo_path:
    st.error("❌ Poppler not found. Install with: brew install poppler")
    st.stop()

poppler_path = os.path.dirname(pdfinfo_path)

# ---- Gemini Client ----
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY missing in .env")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)

# ================= GEMINI FUNCTION =================
def get_gemini_response(prompt, resume_text, job_description):
    full_prompt = f"""
{prompt}

Resume Content:
{resume_text}

Job Description:
{job_description}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text


# ================= PDF → OCR =================
def extract_text_from_pdf(uploaded_file):
    images = convert_from_bytes(
        uploaded_file.read(),
        dpi=200,
        poppler_path=poppler_path
    )

    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)

    return text


# ================= STREAMLIT UI =================
st.set_page_config(page_title="ATS Resume Expert", layout="wide")
st.title("📄 ATS Resume Tracking System")

job_description = st.text_area("📌 Job Description", height=200)
uploaded_file = st.file_uploader("📤 Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("Resume uploaded successfully")

col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("🔍 Tell Me About the Resume")
with col2:
    submit2 = st.button("📊 Percentage Match")

# ================= PROMPTS =================
prompt_review = """
You are an experienced Technical HR.
Analyze the resume against the job description.
Highlight strengths, weaknesses, and improvement suggestions.
"""

prompt_match = """
You are a professional ATS scanner.
Evaluate the resume against the job description and return:
1. Percentage match
2. Missing keywords
3. Final hiring recommendation
"""

# ================= BUTTON ACTIONS =================
if submit1 or submit2:
    if not uploaded_file:
        st.warning("Please upload a resume PDF")
        st.stop()

    if not job_description.strip():
        st.warning("Please enter the job description")
        st.stop()

    with st.spinner("Analyzing resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

        if submit1:
            st.subheader("🧠 ATS Resume Review")
            st.write(get_gemini_response(prompt_review, resume_text, job_description))

        if submit2:
            st.subheader("📈 ATS Match Result")
            st.write(get_gemini_response(prompt_match, resume_text, job_description))
