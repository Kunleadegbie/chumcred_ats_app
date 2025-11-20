import streamlit as st
import pandas as pd
import os
from PIL import Image

# ATS Imports
from helpers.cv_parser import extract_text
from helpers.jd_processor import process_job_description
from helpers.matcher import evaluate_candidate
from helpers.report_generator import export_results_to_excel

# Authentication Imports
from helpers.user_auth import (
    init_db, authenticate, add_user, get_all_users,
    block_user, unblock_user, reset_password
)

# Initialize database
init_db()

# ---------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ---------------------------------------------
st.set_page_config(
    page_title="Chumcred ATS System",
    page_icon="📄",
    layout="wide"
)

# Create necessary folders
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/results", exist_ok=True)

# Logo
if os.path.exists("assets/logo.png"):
    st.image("assets/logo.png", width=200)


# ---------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None


# ---------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------
def login_page():
    st.title("🔐 Chumcred ATS Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = authenticate(username, password)

        if not user:
            st.error("❌ Invalid username or password")
            return

        if user["status"] == "blocked":
            st.error("🚫 Your access has been blocked. Contact the administrator.")
            return

        # LOGIN SUCCESS
        st.session_state.logged_in = True
        st.session_state.username = user["username"]
        st.session_state.role = user["role"]

        st.success("Login successful! Redirecting...")
        st.rerun()


# ---------------------------------------------------
# ADMIN DASHBOARD
# ---------------------------------------------------
def admin_dashboard():

    st.sidebar.subheader("🛠 Admin Menu")
    menu = st.sidebar.radio("Select Action", ["ATS Screening", "Add User", "Manage Users", "Logout"])

    # ATS SCREENING PAGE
    if menu == "ATS Screening":
        ats_screening_page()

    # ADD USER
    elif menu == "Add User":
        st.header("➕ Create New User")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])

        if st.button("Create User"):
            if add_user(new_user, new_pass, role):
                st.success("User created successfully!")
            else:
                st.error("User already exists!")

    # MANAGE USERS
    elif menu == "Manage Users":
        st.header("👥 Manage System Users")

        users = get_all_users()
        df = pd.DataFrame(users, columns=["Username", "Role", "Status"])
        st.dataframe(df)

        selected_user = st.selectbox("Select User", [u[0] for u in users])

        if st.button("Block User"):
            block_user(selected_user)
            st.success("User blocked!")
            st.rerun()

        if st.button("Unblock User"):
            unblock_user(selected_user)
            st.success("User unblocked!")
            st.rerun()

        newp = st.text_input("New Password")
        if st.button("Reset Password"):
            reset_password(selected_user, newp)
            st.success("Password Updated")

    # LOGOUT
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()


# ---------------------------------------------------
# USER DASHBOARD
# ---------------------------------------------------
def user_dashboard():
    st.sidebar.subheader("User Menu")
    menu = st.sidebar.radio("Select Action", ["ATS Screening", "Logout"])

    if menu == "ATS Screening":
        ats_screening_page()

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()


# ---------------------------------------------------
# THE MAIN ATS SCREENING PAGE
# ---------------------------------------------------
def ats_screening_page():

    st.markdown(
        """
        <h2 style='color:#02457A;'>📄 ATS Screening System</h2>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📌 Step 1: Upload Job Description")
    jd_text = st.text_area("Paste Job Description Here", height=200)
    uploaded_jd = st.file_uploader("Or upload JD file", type=["pdf", "docx", "txt"])

    if uploaded_jd:
        jd_text = extract_text(uploaded_jd)

    st.subheader("📌 Step 2: Upload CVs (Unlimited)")
    uploaded_cvs = st.file_uploader("Upload CV files", type=["pdf", "docx"], accept_multiple_files=True)

    st.write("---")

    if st.button("🚀 Run ATS Screening"):

        if not jd_text:
            st.error("❗ Please provide a Job Description.")
            return

        if not uploaded_cvs:
            st.error("❗ Please upload at least one CV.")
            return

        with st.spinner("Processing CVs..."):

            # Process JD
            jd_keywords, jd_vector = process_job_description(jd_text)

            results = []

            for cv in uploaded_cvs:
                filename = cv.name
                file_path = f"data/uploads/{filename}"

                with open(file_path, "wb") as f:
                    f.write(cv.read())

                cv_text = extract_text(file_path)

                result = evaluate_candidate(filename, cv_text, jd_keywords, jd_vector)
                results.append(result)

            df = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False)

            output_path = "data/results/chumcred_ats_results.xlsx"
            export_results_to_excel(df, output_path)

        # Display results
        st.success("✔ Screening Completed Successfully!")
        st.dataframe(df, use_container_width=True)

        with st.expander("📘 Understanding ATS Scores"):
            st.markdown("""
            | Score Type            | What It Means                                           |
            | --------------------- | ------------------------------------------------------- |
            | **Match Score (%)**   | Overall suitability for the role (final combined score) |
            | **Keyword Match (%)** | How many JD keywords appear directly in the CV          |
            | **TF-IDF Score (%)**  | How similar the content of the CV is to the JD          |
            | **Mini Semantic (%)** | How similar the meaning is, even with different wording |
            """)

        with open(output_path, "rb") as f:
            st.download_button(
                "📥 Download Full ATS Report (Excel)",
                f,
                file_name="chumcred_ats_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# ---------------------------------------------------
# START APP
# ---------------------------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        user_dashboard()
