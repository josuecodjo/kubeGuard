import streamlit as st
import plotly.express as px
from services.kyverno import get_policy_violations

st.header("📜 Kyverno Policy Violations")

url = st.text_input("Policy Reporter API URL", "http://localhost:8080")

if st.button("Get Violations"):
    df = get_policy_violations(url)

    if df.empty:
        st.warning("No violations found.")
    else:
        st.subheader("🔴 Violations Summary")

        # Pie chart by severity
        fig = px.pie(df, names="severity", title="Violations by Severity")
        st.plotly_chart(fig, use_container_width=True)

        # Violations by Policy
        st.subheader("📋 Top Violated Policies")
        top_policies = df["policy"].value_counts().reset_index()
        top_policies.columns = ["Policy", "Count"]
        st.dataframe(top_policies)

        # Filter panel
        st.subheader("🔍 Filter Violations")
        namespace = st.selectbox("Namespace", options=["All"] + sorted(df["namespace"].unique().tolist()))
        status = st.selectbox("Status", options=["All"] + sorted(df["status"].unique().tolist()))
        
        filtered_df = df.copy()
        if namespace != "All":
            filtered_df = filtered_df[filtered_df["namespace"] == namespace]
        if status != "All":
            filtered_df = filtered_df[filtered_df["status"] == status]

        st.dataframe(filtered_df[['timestamp', 'policy', 'rule', 'resourceKind', 'resourceName', 'namespace', 'severity', 'status', 'message']])
