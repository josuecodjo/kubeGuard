import streamlit as st
from services.falco import fetch_falco_logs

st.header("🚨 Falco Runtime Alerts")

loki_url = st.text_input("Loki Endpoint", "http://localhost:3100")
query = st.text_input("Loki Query", '{job="falco"}')

if st.button("Fetch Logs"):
    df = fetch_falco_logs(loki_url, query)
    st.dataframe(df)
