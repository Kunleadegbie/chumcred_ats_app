import streamlit as st
import pandas as pd
import os
from helpers.cv_parser import extract_text
from helpers.jd_processor import process_job_description
from helpers.matcher import evaluate_candidate
from helpers.report_generator import export_results_to_excel
from config.supabase_config import upload_to_supabase

# ---------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ---------------------------------------------
st.set_page_config(
    page_title="Chumcred ATS Screening System",
    page_icon="📄",
    layout="wide"
)

# Create necessary folders
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/results", exist_ok=True)


# Display Logo
from PIL import Image

logo_path = "assets/logo.png"

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=180)
else:
    st.warning("Logo file not found. Make sure assets/logo.png exists.")

# ---------------------------------------------
# HEADER
# ---------------------------------------------
st.markdown(
    """
    <h1 style='text-align:center;color:#02457A;'>
        CHUMCRED LIMITED — AI-POWERED ATS CV SCREENING SYSTEM
    </h1>
    <p style='text-align:center;font-size:17px;margin-top:-10px;'>
        Upload Job Description & CVs → AI Analyzes → Get Match Scores, Insights & Ranking
    </p>
    """,
    unsafe_allow_html=True
)



# ---------------------------------------------
# SIDEBAR SETTINGS
# ---------------------------------------------
# st.sidebar.header("Configuration")
# use_supabase = st.sidebar.checkbox("Enable Supabase Cloud Storage", value=False)


# ---------------------------------------------
# STEP 1 — JOB DESCRIPTION
# ---------------------------------------------
st.subheader("📌 Step 1: Upload Job Description")

jd_text = st.text_area("Paste Job Description Here", height=200)

uploaded_jd = st.file_uploader("Or upload JD file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_jd:
    jd_text = extract_text(uploaded_jd)


# ---------------------------------------------
# STEP 2 — UPLOAD CVS
# ---------------------------------------------
st.subheader("📌 Step 2: Upload CVs (Unlimited)")

uploaded_cvs = st.file_uploader(
    "Upload all applicant CVs (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

st.write("---")


# ---------------------------------------------
# RUN ATS ENGINE
# ---------------------------------------------
if st.button("🚀 Run ATS Screening"):

    # Validate JD
    if not jd_text:
        st.error("❗Please provide a Job Description.")
        st.stop()

    # Validate CVs
    if not uploaded_cvs:
        st.error("❗Please upload at least one CV.")
        st.stop()

    with st.spinner("Processing CVs using Chumcred Hybrid ATS Engine… Please wait ⏳"):

        # Process Job Description
        jd_keywords, jd_vector = process_job_description(jd_text)

        results = []

        for cv in uploaded_cvs:

            filename = cv.name
            file_path = f"data/uploads/{filename}"

            # Save CV file
            with open(file_path, "wb") as f:
                f.write(cv.read())

            # Extract CV text
            cv_text = extract_text(file_path)

            # Evaluate
            result = evaluate_candidate(filename, cv_text, jd_keywords, jd_vector)
            results.append(result)

            # Optional Supabase Upload
            if use_supabase:
                upload_to_supabase(file_path)

        # Convert to DataFrame
        df = pd.DataFrame(results)

        # Sort by Match Score
        df = df.sort_values(by="Match Score (%)", ascending=False)

        # Export results
        output_path = "data/results/chumcred_ats_results.xlsx"
        export_results_to_excel(df, output_path)


    # ---------------------------------------------
    # DISPLAY RESULTS (INDENTED CORRECTLY)
    # ---------------------------------------------
    st.success("✔ Screening Completed Successfully!")
    st.subheader("📊 ATS Screening Results")

    st.dataframe(df, use_container_width=True)

    st.write("---")

    # Explanation of scores (NOW IT WILL DISPLAY)
    with st.expander("📘 Understanding the ATS Scores (Click to Expand)"):
        st.markdown("""
        | Score Type            | What It Means                                           |
        | --------------------- | ------------------------------------------------------- |
        | **Match Score (%)**   | Overall suitability for the role (final combined score) |
        | **Keyword Match (%)** | How many JD keywords appear directly in the CV          |
        | **TF-IDF Score (%)**  | How similar the content of the CV is to the JD          |
        | **Mini Semantic (%)** | How similar the meaning is, even with different wording |
        """)

    st.write("---")

    # Download Button (NOW VALID)
    with open(output_path, "rb") as f:
        st.download_button(
            label="📥 Download Full ATS Report (Excel)",
            data=f,
            file_name="chumcred_ats_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
