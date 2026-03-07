import streamlit as st
import pandas as pd

def show():

    st.title("🗺 District-Level Dropout Risk Heatmap")

    data = pd.DataFrame({
        "District":["Chennai","Madurai","Coimbatore","Salem","Trichy"],
        "Risk Score":[0.2,0.45,0.35,0.6,0.4]
    })

    st.map(
        pd.DataFrame({
            "lat":[13.08,9.93,11.01,11.66,10.79],
            "lon":[80.27,78.12,76.96,78.15,78.70]
        })
    )

    st.dataframe(data)

    if st.button("⬅ Back"):
        st.session_state.page = "main"
        st.rerun()