import streamlit as st
import pandas as pd

def show():

    st.title("📊 Cohort Comparison")

    data = pd.DataFrame({
        "Class":["6","7","8","9","10"],
        "Low Risk":[40,35,30,28,25],
        "Medium Risk":[15,18,20,22,25],
        "High Risk":[5,7,9,12,15]
    })

    st.bar_chart(data.set_index("Class"))

    if st.button("⬅ Back"):
        st.session_state.page = "main"
        st.rerun()