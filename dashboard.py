import streamlit as st
import requests
from dotenv import load_dotenv
import os

# CONFIGURATION (Replace with your details!)
# 1. Load environment variables
load_dotenv()

# 2. Get secrets safely
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")

st.title("🚀 API TestOps Control Plane")

endpoint = st.text_input("Endpoint to Test", "/todos/1")

if st.button("Trigger Cloud Test"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/main.yml/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": "main", "inputs": {"endpoint": endpoint}}

    resp = requests.post(url, json=data, headers=headers)

    if resp.status_code == 204:
        st.success("✅ Test Triggered on GitHub!")
        st.markdown(f"[View Report History](https://{REPO_OWNER}.github.io/{REPO_NAME})")
    else:
        st.error(f"Error: {resp.text}")