# ═══════════════════════════════════════════════════════════════
# app.py — Main Entry Point
# ═══════════════════════════════════════════════════════════════

import streamlit as st

st.set_page_config(
    page_title="EduSaviour",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #1e293b !important;
}
[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}
[data-testid="stSidebar"] .stButton > button {
    border: 1px solid #334155 !important;
    background: #0f172a !important;
    text-align: left !important;
    width: 100% !important;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    color: #e2e8f0 !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #334155 !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #2563eb !important;
    border-color: #3b82f6 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
}
</style>
""", unsafe_allow_html=True)

DEFAULTS = {
    "page":                "login",
    "result":              None,
    "student_data":        {},
    "scheme":              "",
    "show_cohort":         False,
    "cohort_data":         {},
    "role":                None,
    "user":                None,
    "assignments":         {},
    "counselling_records": [],
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

USERS = {
    "admin":       {"password": "admin123",   "role": "administrator"},
    "teacher":     {"password": "teacher123", "role": "teacher"},
    "counsellor":  {"password": "c123",       "role": "counsellor"},
    "counsellor2": {"password": "c234",       "role": "counsellor"},
    "counsellor3": {"password": "c345",       "role": "counsellor"},
    "counsellor4": {"password": "c456",       "role": "counsellor"},
}

import page_predict
import page_schemes
import page_scheme_detail
import page_message
import page_counselling
import page_cohort
import page_heatmap


# ── Login ──────────────────────────────────────────────────────
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🎓 EduSaviour")
        st.markdown("---")
        st.subheader("Login")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("Login", use_container_width=True, type="primary"):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.role = USERS[username]["role"]
                st.session_state.user = username
                st.session_state.page = "counselling" if USERS[username]["role"] == "counsellor" else "main"
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")


# ── Sidebar ────────────────────────────────────────────────────
def sidebar():
    role = st.session_state.role
    user = st.session_state.user
    role_label = {
        "administrator": "🛡️ Administrator",
        "teacher":       "👩‍🏫 Teacher",
        "counsellor":    "🧑‍⚕️ Counsellor",
    }.get(role, role)
    with st.sidebar:
        st.markdown("### 🎓 Dropout System")
        st.markdown("---")
        st.markdown(f"👤 **{user}**")
        st.caption(role_label)
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, key="nav_logout"):
            keep = {
                "assignments":         st.session_state.assignments,
                "counselling_records": st.session_state.counselling_records,
            }
            st.session_state.clear()
            st.session_state.update(keep)
            st.session_state.page = "login"
            st.session_state.role = None
            st.session_state.user = None
            st.rerun()


# ── Router ─────────────────────────────────────────────────────
page = st.session_state.page
role = st.session_state.role

if page == "login" or role is None:
    login_page()

elif role == "counsellor":
    sidebar()
    page_counselling.show()

else:
    # Teacher / Admin
    sidebar()
    if   page == "main":          page_predict.show()
    elif page == "schemes":       page_schemes.show()
    elif page == "scheme_detail": page_scheme_detail.show()
    elif page == "message":       page_message.show()
    elif page == "counselling":   page_counselling.show()
    elif page == "cohort":        page_cohort.show()
    elif page == "heatmap":       page_heatmap.show()
    else:
        st.session_state.page = "main"
        st.rerun()