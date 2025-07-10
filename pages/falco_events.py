import streamlit as st
import plotly.express as px
from services.falco import fetch_falco_logs

st.header("🚨 Falco Runtime Alerts")

loki_url = st.text_input("Loki Endpoint", "http://localhost:3100")
query = st.text_input("Loki Query", '{job="falco"}')

if st.button("Fetch Logs"):
    df = fetch_falco_logs(loki_url, query)

    if df.empty:
        st.warning("No logs found.")
    else:
        # Pie chart of severities
        st.subheader("🔴 Alert Distribution by Severity")
        fig = px.pie(df, names='priority', title='Falco Alerts by Priority')
        st.plotly_chart(fig, use_container_width=True)

        # Top rules
        st.subheader("📋 Top Triggered Rules")
        st.dataframe(df['rule'].value_counts().reset_index().rename(columns={'index': 'Rule', 'rule': 'Count'}))

        # Raw logs
        st.subheader("📝 Recent Alerts")
        st.dataframe(df[['time', 'priority', 'rule', 'output']])
