import streamlit as st
import pandas as pd
import json
import plotly.express as px
import threading

from services.kubescape import run_kubescape, parse_kubescape_summary_controls

st.header("Kubescape Historical Scans")
if st.button("▶️ Run Kubescape Scan"):
    st.info("Running Kubescape...")
    data = run_kubescape()
    if data:
        df = parse_kubescape_summary_controls(data)
        if not df.empty:
            st.success("✅ Scan Complete!")

            pie_fig = px.pie(df, names="Status", title="Control Status Distribution")
            st.plotly_chart(pie_fig, use_container_width=True)

            bar_fig = px.bar(
                df.sort_values("Compliance Score"),
                x="Control Name",
                y="Compliance Score",
                color="Status",
                hover_data=["Control ID", "Score", "Passed", "Failed", "Skipped"],
                title="Compliance Scores by Control",
            )
            st.plotly_chart(bar_fig, use_container_width=True)

            with st.expander("📋 Detailed Table"):
                st.dataframe(df)

            failed_df = df[df["Status"] == "failed"]
            if not failed_df.empty:
                st.subheader("🚨 Failed Controls Summary")
                st.dataframe(failed_df.sort_values("Failed", ascending=False))
