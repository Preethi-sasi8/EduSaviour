# ═══════════════════════════════════════════════════════════════
# app.py — Main Entry Point
# ═══════════════════════════════════════════════════════════════

import streamlit as st

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Student Dropout Early Warning System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state defaults ─────────────────────────────────────
DEFAULTS = {
    "page": "login",
    "result": None,
    "student_data": {},
    "scheme": "",
    "role": None,
    "user": None,
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Login users ────────────────────────────────────────────────
USERS = {
    "admin": {"password": "admin123", "role": "administrator"},
    "teacher": {"password": "teacher123", "role": "teacher"},
    "counsellor": {"password": "c123", "role": "counsellor"},
}

# ── Page imports ───────────────────────────────────────────────
import page_predict
import page_schemes
import page_scheme_detail
import page_message
import page_counselling
import page_cohort
import page_heatmap


# ── Login Page ─────────────────────────────────────────────────
def login_page():

    st.title("🎓 AI Student Dropout Early Warning System")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in USERS and USERS[username]["password"] == password:

            st.session_state.role = USERS[username]["role"]
            st.session_state.user = username

            # Redirect after login
            if USERS[username]["role"] == "counsellor":
                st.session_state.page = "counselling"
            else:
                st.session_state.page = "main"

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid username or password")


# ── Sidebar Navigation ─────────────────────────────────────────
def sidebar():

    with st.sidebar:

        st.write(f"👤 Logged in as: **{st.session_state.user}**")
        st.write(f"Role: **{st.session_state.role}**")

        if st.button("🏠 Risk Prediction"):
            st.session_state.page = "main"
            st.rerun()

        if st.button("📋 Government Schemes"):
            st.session_state.page = "schemes"
            st.rerun()

        if st.button("💬 Message"):
            st.session_state.page = "message"
            st.rerun()

        if st.button("🧠 Counselling"):
            st.session_state.page = "counselling"
            st.rerun()

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()


# ── Router ─────────────────────────────────────────────────────
page = st.session_state.page
role = st.session_state.role

# 1️⃣ Login Page
if page == "login":
    login_page()

# 2️⃣ Counsellor Portal (restricted access)
elif role == "counsellor":

    st.info("Counsellor Portal — Submit student counselling feedback")

    page_counselling.show()

# 3️⃣ Teacher / Admin Dashboard
else:

    sidebar()

    if page == "main":
        page_predict.show()

    elif page == "schemes":
        page_schemes.show()

    elif page == "scheme_detail":
        page_scheme_detail.show()

    elif page == "message":
        page_message.show()

    elif page == "counselling":
        page_counselling.show()

    elif page == "cohort":
        page_cohort.show()

    elif page == "heatmap":
        page_heatmap.show()

    else:
        st.session_state.page = "main"
        st.rerun()