import streamlit as st
from supabase import create_client

def upload_to_supabase(file_path):
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        bucket = st.secrets["SUPABASE_BUCKET"]

        supabase = create_client(url, key)

        file_name = file_path.split("/")[-1]
        with open(file_path, "rb") as f:
            supabase.storage.from_(bucket).upload(file_name, f)

        return True

    except Exception as e:
        print("Supabase upload error:", e)
        return False
