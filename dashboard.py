import streamlit as st
import requests

# CONFIGURATION (Replace with your details!)
GITHUB_TOKEN = "PASTE_YOUR_TOKEN_HERE"  # <--- PASTE TOKEN FROM STEP 3.3
REPO_OWNER = "YOUR_GITHUB_USERNAME"  # <--- YOUR USERNAME
REPO_NAME = "api-testops-demo"  # <--- REPO NAME

st.title("🚀 API TestOps Control Plane")

endpoint = st.text_input("Endpoint to Test", "/api/users/2")

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