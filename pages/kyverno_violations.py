import streamlit as st
from services.kyverno import get_policy_violations

st.header("📜 Kyverno Policy Violations")

url = st.text_input("Policy Reporter API", "http://localhost:8080")
if st.button("Get Violations"):
    df = get_policy_violations(url)
    st.dataframe(df)
