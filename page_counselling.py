import streamlit as st
from datetime import timedelta

def show():

    st.title("🧑‍⚕️ Counselling Assignment")

    student = st.session_state.student_data
    result = st.session_state.result

    role = st.session_state.get("role", "teacher")
    user = st.session_state.get("user", "")

    student_name = student.get("name", "Not Provided")
    student_id = student.get("id", "Not Provided")
    risk = result.get("Risk_Level", "Unknown")

    # ── Student Details ─────────────────────────────

    st.subheader("Student Details")

    col1, col2, col3 = st.columns(3)

    col1.metric("Student Name", student_name)
    col2.metric("Student ID", student_id)
    col3.metric("Risk Level", risk)

    st.divider()

    # ── Storage ─────────────────────────────────────

    if "assigned_counsellor" not in st.session_state:
        st.session_state.assigned_counsellor = None

    if "counselling_records" not in st.session_state:
        st.session_state.counselling_records = []

    # =================================================
    # 👩‍🏫 TEACHER / ADMIN VIEW
    # =================================================

    if role in ["administrator", "teacher"]:

        st.subheader("Assign Counsellor")

        if st.session_state.assigned_counsellor is None:

            counsellor = st.selectbox(
                "Select Counsellor",
                [
                    "Mrs. Lakshmi (School Counsellor)",
                    "Dr. Kumar (Psychologist)",
                    "Mr. Rajesh (Academic Mentor)",
                    "Ms. Priya (Social Worker)"
                ]
            )

        else:
            counsellor = st.session_state.assigned_counsellor
            st.success(f"Assigned Counsellor: {counsellor}")

        session_date = st.date_input("First Session Date")

        end_date = session_date + timedelta(days=30)
        st.write("Counselling End Date:", end_date)

        if st.button("Assign Counselling"):

            if st.session_state.assigned_counsellor is None:
                st.session_state.assigned_counsellor = counsellor

            record = {
                "Student Name": student_name,
                "Student ID": student_id,
                "Counsellor": st.session_state.assigned_counsellor,
                "Day": 0,
                "Feedback": "Session Scheduled",
                "Progress Status": "Session Scheduled",
                "Next Session Date": session_date,
                "Updated By": user
            }

            st.session_state.counselling_records.append(record)

            st.success("Counselling assigned successfully")

    # =================================================
    # 🧑‍⚕️ COUNSELLOR VIEW
    # =================================================

    if role == "counsellor":

        st.subheader("Counsellor Feedback")

        assigned = st.session_state.assigned_counsellor

        if assigned is None:

            st.warning("No student assigned yet.")

        else:

            st.success(f"Student: {student_name}")

            day = st.number_input(
                "Counselling Day (1–30)",
                min_value=1,
                max_value=30
            )

            feedback = st.text_area("Session Feedback")

            progress_status = st.selectbox(
                "Progress Status",
                [
                    "Improving",
                    "No Change",
                    "Needs Attention"
                ]
            )

            next_session = st.date_input("Next Session Date")

            if st.button("Submit Feedback"):

                record = {
                    "Student Name": student_name,
                    "Student ID": student_id,
                    "Counsellor": assigned,
                    "Day": day,
                    "Feedback": feedback,
                    "Progress Status": progress_status,
                    "Next Session Date": next_session,
                    "Updated By": user
                }

                st.session_state.counselling_records.append(record)

                st.success("Feedback submitted successfully")

    st.divider()

    # ── Teacher Tracking Dashboard ─────────────────

    st.subheader("Teacher Tracking Dashboard")

    if st.session_state.counselling_records:

        st.dataframe(
            st.session_state.counselling_records,
            use_container_width=True
        )

    else:
        st.info("No counselling records yet.")

    # ── Navigation Buttons ─────────────────────────

    col1, col2 = st.columns(2)

    if col1.button("⬅ Back to Prediction"):

        st.session_state.page = "main"
        st.rerun()

    if col2.button("📩 Send Parent Message"):

        st.session_state.page = "message"
        st.rerun()