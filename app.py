import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json

# --- Bulk Upload Integration ---
def bulk_upload_interface(data_file):
    st.markdown("---")
    st.subheader("📥 Bulk Upload Intern Data from Spreadsheet")

    uploaded_file = st.file_uploader("Upload Excel/CSV file", type=["xlsx", "csv"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            bulk_df = pd.read_csv(uploaded_file)
        else:
            bulk_df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")
        st.dataframe(bulk_df.head())

        required_cols = [
            "Name", "Cohort", "Team(eg :2 or 3)", "GitLab User Name", "Year", "Received Offer letter", "College",
            "GitLab Acc (README.md)", "GitLab Acc Link",
            "Innings Courses (Python & AI)", "Huggingchat/Dify", "Huggingchat Link",
            "Streamlit app and Deployment", "Streamlit Link",
            "Huggingface+streamlit integration", "HF+Streamlit Link",
            "Pushed Apps onto GitLab", "Data Collection (started?)", "Size of Data",
            "Can go to any other places", "Blockers?", "Remarks"
        ]

        missing_cols = [col for col in required_cols if col not in bulk_df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
        else:
            if st.button("📤 Upload and Merge Intern Data"):
                existing_df = pd.read_csv(data_file) if os.path.exists(data_file) else pd.DataFrame(columns=required_cols)
                combined_df = pd.concat([existing_df, bulk_df], ignore_index=True)
                combined_df.drop_duplicates(subset=["Name"], keep="last", inplace=True)
                combined_df.to_csv(data_file, index=False)
                st.success(f"✅ {len(bulk_df)} intern(s) uploaded and merged successfully!")
                st.rerun()

# ✅ Main Application
st.set_page_config(page_title="Intern Tracker", layout="wide")
st.title("🧠 Intern Tracker")

page = st.sidebar.selectbox("Navigate", ["Dashboard", "Add/Update Intern"])
data_file = "data/demo.csv"
os.makedirs("data", exist_ok=True)

if page == "Add/Update Intern":
    bulk_upload_interface(data_file)
else:
    st.info("📊 Dashboard coming soon... Upload intern data to get started.")
