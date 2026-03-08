# ═══════════════════════════════════════════════════════════════
# page_scheme_detail.py — Individual Scheme Detail Page
# ═══════════════════════════════════════════════════════════════

import streamlit as st
from data import SCHEME_DATA


def show():
    scheme_name = st.session_state.get("scheme", "")
    data        = st.session_state.get("student_data", {})

    st.title("📚 Scheme Details")

    if st.button("⬅️ Back to Schemes List"):
        st.session_state.page = "schemes"
        st.rerun()

    st.markdown("---")

    if not scheme_name or scheme_name not in SCHEME_DATA:
        st.error("Scheme not found. Please go back and select a scheme.")
        return

    info = SCHEME_DATA[scheme_name]

    # Header
    st.header(f"🏛️ {scheme_name}")

    # Eligibility check
    try:
        is_eligible = info["eligibility_rules"](data)
    except Exception:
        is_eligible = False

    if is_eligible:
        st.success("🎉 **This student IS ELIGIBLE** for this scheme based on the information provided!")
    else:
        st.warning("⚠️ This student may not meet all eligibility criteria for this scheme.")

    st.markdown("---")

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📖 About")
        st.write(info["description"])

        st.subheader("💰 Benefit")
        st.info(info["benefit"])

        st.subheader("🌐 Apply Online")
        st.markdown(f"[{info['website']}]({info['website']})")

    with col2:
        st.subheader("✅ Eligibility Criteria")
        for crit in info["eligibility_display"]:
            icon = "✅" if is_eligible else "⚪"
            st.markdown(f"{icon} {crit}")

        st.subheader("📋 Documents Required")
        for doc in info["documents"]:
            st.checkbox(f"📄 {doc}", key=f"doc_{scheme_name}_{doc}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Schemes", use_container_width=True):
            st.session_state.page = "schemes"
            st.rerun()
