# ═══════════════════════════════════════════════════════════════
# page_schemes.py — Eligible Government Schemes Page
# ═══════════════════════════════════════════════════════════════

import streamlit as st
from data import SCHEME_DATA
from utils import get_eligible_schemes


def show():
    st.title("🏛️ Eligible Government Schemes")

    data = st.session_state.get("student_data", {})
    result = st.session_state.get("result", {})
    risk = result.get("Risk_Level", "Moderate") if result else "Moderate"

    # Back button at top
    if st.button("⬅️ Back to Prediction Results"):
        st.session_state.page = "main"
        st.rerun()

    st.markdown("---")

    if not data:
        st.warning("⚠️ No student data found. Please go back and predict first.")
        return

    eligible_schemes = get_eligible_schemes(data)

    if not eligible_schemes:
        st.info("No specific schemes matched for this student profile.")
        eligible_schemes = ["General Counselling & RTE Support"]

    # Risk banner
    if risk == "High":
        st.error(f"🚨 **High Risk Student** — {len(eligible_schemes)} scheme(s) available for immediate support.")
    else:
        st.warning(f"⚠️ **Moderate Risk Student** — {len(eligible_schemes)} scheme(s) available.")

    st.markdown(f"### 📋 {len(eligible_schemes)} Eligible Scheme(s) Found")
    st.markdown("Click on any scheme to see full details.")
    st.markdown("---")

    # Show each scheme as a card
    for scheme_name in eligible_schemes:
        info = SCHEME_DATA.get(scheme_name)
        if not info:
            continue

        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 📋 {scheme_name}")
                st.markdown(f"_{info['description']}_")
                st.markdown(f"💰 **Benefit:** {info['benefit']}")

                # Eligibility criteria tags
                criteria_str = " &nbsp;|&nbsp; ".join(
                    [f"✅ {c}" for c in info["eligibility_display"]]
                )
                st.markdown(criteria_str, unsafe_allow_html=True)

            with col2:
                st.markdown("")
                st.markdown("")
                if st.button("📄 Full Details", key=f"scheme_btn_{scheme_name}", use_container_width=True):
                    st.session_state.scheme      = scheme_name
                    st.session_state.page        = "scheme_detail"
                    st.rerun()
                st.markdown(f"[🌐 Apply]({info['website']})")

            st.markdown("---")

    # Bottom back button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Results", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()
    with col2:
        if st.button("✉️ Send Message to Parents", use_container_width=True, type="primary"):
            st.session_state.page = "message"
            st.rerun()