import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Get secrets safely
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")

st.set_page_config(page_title="TestOps Control Plane", page_icon="🚀")
st.title("🚀 API TestOps Control Plane")

# 3. Validation: Ensure secrets exist
if not GITHUB_TOKEN or not REPO_OWNER:
    st.error("❌ Missing configuration! Please check your .env file.")
    st.stop()

# Input for the test
endpoint = st.text_input("Endpoint to Test", "/todos/1")

if st.button("Trigger Cloud Test"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/main.yml/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Matches the inputs defined in the workflow file below
    data = {
        "ref": "main",
        "inputs": {
            "endpoint": endpoint
        }
    }

    with st.spinner("Dispatching to GitHub Actions..."):
        resp = requests.post(url, json=data, headers=headers)

        if resp.status_code == 204:
            st.success("✅ Workflow Triggered!")
            st.markdown(f"[View Live Results](https://github.com/{REPO_OWNER}/{REPO_NAME}/actions)")
            st.markdown(f"[View History Report](https://{REPO_OWNER}.github.io/{REPO_NAME})")
        else:
            st.error(f"Failed: {resp.status_code}")
            st.code(resp.text)