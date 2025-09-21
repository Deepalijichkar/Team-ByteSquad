# app.py
import streamlit as st
import requests

# ========================
# CONFIG
# ========================
# Replace this with your live FastAPI backend URL once deployed
FASTAPI_URL = "https://web-production-c05ed.up.railway.app"  # local testing
# Example for deployed backend: "https://team-bytesquad.onrender.com"

st.set_page_config(page_title="Team ByteSquad", layout="centered")

# ========================
# HEADER
# ========================
st.title("Team ByteSquad Corruption Detection")
st.write("Upload a PDF or DOCX file to get analysis from the backend.")

# ========================
# FILE UPLOADER
# ========================
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

if uploaded_file is not None:
    st.write(f"File uploaded: {uploaded_file.name}")

    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

    with st.spinner("Processing file..."):
        try:
            # POST request to FastAPI endpoint
            response = requests.post(f"{FASTAPI_URL}/upload", files=files)

            if response.status_code == 200:
                st.success("File processed successfully!")
                result = response.json()
                st.json(result)  # display JSON result from backend
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Cannot reach FastAPI server: {e}")
