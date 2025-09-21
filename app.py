# app.py
import streamlit as st
import requests
from PIL import Image

# ========================
# CONFIG
# ========================
FASTAPI_URL = "https://web-production-c05ed.up.railway.app"

st.set_page_config(
    page_title="Team ByteSquad - Resume Relevance Checker",
    page_icon="📄",
    layout="wide"
)

# ========================
# HEADER WITH LOGO
# ========================
try:
    logo = Image.open("logo.png")  # Add your logo in root
    st.image(logo, width=120)
except:
    pass

st.markdown(
    "<h1 style='text-align:center; color:#4B8BBE;'>Team ByteSquad - Automated Resume Relevance Checker</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Upload a <b>Resume</b> (PDF/DOCX) and optionally a <b>Job Description</b> to get a relevance score and key highlights.</p>",
    unsafe_allow_html=True
)
st.write("---")

# ========================
# FILE UPLOADER
# ========================
uploaded_resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])
uploaded_jd = st.file_uploader("Upload Job Description (optional)", type=["pdf", "docx"])

if uploaded_resume is not None:
    st.success(f"✅ Resume uploaded: {uploaded_resume.name}")
    files = {"resume": (uploaded_resume.name, uploaded_resume.getvalue())}

    if uploaded_jd is not None:
        st.success(f"✅ Job Description uploaded: {uploaded_jd.name}")
        files["jd"] = (uploaded_jd.name, uploaded_jd.getvalue())

    with st.spinner("Analyzing resume..."):
        try:
            response = requests.post(f"{FASTAPI_URL}/upload", files=files)

            if response.status_code == 200:
                result = response.json()
                
                # ========================
                # DISPLAY RESULTS
                # ========================
                st.success("✅ Analysis Completed!")
                
                # Score box
                score = result.get('relevance_score', 'N/A')
                st.markdown(
                    f"""
                    <div style='background-color:#4B8BBE; padding:20px; border-radius:10px; color:white; text-align:center;'>
                        <h2>Relevance Score</h2>
                        <h1 style='font-size:50px'>{score} / 100</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.write("")  # spacing

                # Display resume & JD
                st.markdown(f"**Resume:** {result.get('resume_name', 'N/A')}")
                if result.get('jd_name'):
                    st.markdown(f"**Job Description:** {result.get('jd_name')}")
                
                # Highlights as badges
                highlights = result.get("highlights", [])
                if highlights:
                    st.markdown("**Key Highlights:**")
                    cols = st.columns(len(highlights))
                    for i, item in enumerate(highlights):
                        cols[i].markdown(
                            f"<span style='background-color:#FFD43B; padding:8px; border-radius:8px;'>{item}</span>",
                            unsafe_allow_html=True
                        )
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Cannot reach backend server: {e}")
