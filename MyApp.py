import streamlit as st
import pandas as pd
import re
from github import Github, Auth

def email_to_domain_name(email):
    if email is None:
        return "unknown"
    match = re.search(r'.+@(.+)', email)
    if match:
        return match.group(1)
    return "unknown"

@st.cache_data
def contributors_df(token, repository):
    g = Github(auth=Auth.Token(token)) if token != "" else Github()

    repo = g.get_repo(repository)

    contributors = [user for user in repo.get_contributors()]

    return pd.DataFrame({
        "name": [user.name for user in contributors],
        "domain": [email_to_domain_name(user.email) for user in contributors]
    })

st.write("""
# GitHub Contributor Analysis
""")

st.text_input("Please input your github auth token for accessing GitHub", key="token", value="") 
st.text_input("Please input the repository in owner/repo format", key="repo", value="google/leveldb") 

df = contributors_df(st.session_state.token, st.session_state.repo)

grouped = df.groupby("domain").size().reset_index(name="count")

grouped = grouped.sort_values(by="count", ascending=False).reset_index(drop=True)

st.bar_chart(grouped, y="count", color="domain")
