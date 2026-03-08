# ═══════════════════════════════════════════════════════════════
# page_predict.py — Student Form + Prediction Results + Cohort
# ═══════════════════════════════════════════════════════════════

import streamlit as st
from data import FACTOR_EXPLANATIONS
from utils import predict_risk, get_top_factors

# ── Excel path ─────────────────────────────────────────────────
EXCEL_PATH = "student_dropout_with_schemes.xlsx"


# ══════════════════════════════════════════════════════════════
# MAIN PAGE
# ══════════════════════════════════════════════════════════════
def show():
    st.title("🎓 EduSaviour")
    st.markdown("Fill in the student details below and click **Predict Dropout Risk**.")

    # ── Section 1: Demographics ────────────────────────────────
    st.header("Student Details")
    c1, c2 = st.columns(2)
    with c1:
        student_name = st.text_input("Student Name")
        gender       = st.selectbox("Gender", ["Male", "Female"])
        standard     = st.selectbox("Standard (Class)", [9, 10, 11, 12])
        caste        = st.selectbox("Caste Category", ["General", "SC", "ST", "OBC", "EWS", "Minority"])
    with c2:
        student_id = st.text_input("Student ID")
        age        = st.number_input("Age", min_value=10, max_value=20, value=14)
        income     = st.selectbox("Family Income Level",
                                  ["Below Poverty Line", "Low Income", "Middle Income", "High Income"])

    # ── Section 2: Family Background ──────────────────────────
    st.header("Family Background")
    c1, c2 = st.columns(2)
    with c1:
        father_edu      = st.selectbox("Father's Education",
                                       ["Illiterate", "Primary", "Secondary", "Higher Secondary", "Graduate", "Post Graduate"])
        mother_edu      = st.selectbox("Mother's Education",
                                       ["Illiterate", "Primary", "Secondary", "Higher Secondary", "Graduate", "Post Graduate"])
        siblings        = st.number_input("Number of Siblings", min_value=0, max_value=10, value=1)
        siblings_drop   = st.number_input("Siblings Dropout Count", min_value=0, max_value=10, value=0)
    with c2:
        siblings_reason = st.selectbox("Siblings Dropout Reason",
                                       ["N/A", "Financial", "Marriage", "Labour", "Distance", "Academic Failure", "Family Pressure"])
        siblings_edu    = st.selectbox("Siblings Highest Education",
                                       ["N/A", "Primary", "Secondary", "Higher Secondary", "Graduate"])
        siblings_school = st.selectbox("Siblings Currently In School", ["Yes", "No", "N/A"])
        sibling_impact  = st.slider("Sibling Dropout Impact Score (0–10)", 0, 10, 3)
    single_parent = st.selectbox("Single Parent Family", ["Yes", "No"])

    # ── Section 3: Academic Performance ───────────────────────
    st.header("Academic Performance")
    c1, c2 = st.columns(2)
    with c1:
        attendance  = st.slider("Attendance Percentage", 0, 100, 70)
        marks       = st.slider("Previous Year Marks", 0, 100, 55)
        failed_subj = st.number_input("Failed Subjects Count", min_value=0, max_value=10, value=0)
    with c2:
        homework   = st.selectbox("Homework Completion", ["Always", "Often", "Sometimes", "Rarely", "Never"])
        grade_rep  = st.selectbox("Grade Repetition History", ["Yes", "No"])
        learn_diff = st.selectbox("Learning Difficulty", ["Yes", "No"])

    # ── Section 4: School & Transport ─────────────────────────
    st.header("School & Transport")
    c1, c2 = st.columns(2)
    with c1:
        distance    = st.slider("Distance to School (km)", 0, 30, 5)
        transport   = st.selectbox("Transport Available", ["Yes", "No"])
    with c2:
        school_type = st.selectbox("School Type", ["Government", "Private", "Aided"])
        mid_day     = st.selectbox("Mid-Day Meal Beneficiary", ["Yes", "No"])
    scholarship = st.selectbox("Scholarship Received", ["Yes", "No"])

    # ── Section 5: Social & Psychological ─────────────────────
    st.header("Social & Psychological Factors")
    c1, c2 = st.columns(2)
    with c1:
        bullying      = st.selectbox("Bullying Experience", ["Yes", "No"])
        teacher_rel   = st.selectbox("Teacher-Student Relationship", ["Excellent", "Good", "Average", "Poor"])
        peer_inf      = st.selectbox("Peer Influence", ["Positive", "Neutral", "Negative"])
        self_esteem   = st.selectbox("Self Esteem Level", ["High", "Moderate", "Low"])
    with c2:
        mental_health = st.selectbox("Mental Health Concern", ["Yes", "No"])
        parental_inv  = st.selectbox("Parental Involvement", ["High", "Moderate", "Low", "None"])
        child_labour  = st.selectbox("Child Labour", ["Yes", "No"])
        early_mar     = st.selectbox("Early Marriage Risk", ["Yes", "No"])
    c1, c2 = st.columns(2)
    with c1:
        domestic   = st.selectbox("Domestic Responsibility", ["None", "Low", "Moderate", "High"])
        smartphone = st.selectbox("Smartphone Access", ["Yes", "No"])
    with c2:
        internet = st.selectbox("Internet Access", ["Yes", "No"])

    # ── Build student_data dict ────────────────────────────────
    student_data = {
        "name": student_name, "id": student_id,
        "Gender": gender, "Caste_Category": caste, "Standard": standard,
        "Age": age, "Family_Income_Level": income,
        "Father_Education": father_edu, "Mother_Education": mother_edu,
        "No_of_Siblings": siblings, "Siblings_Dropout_Count": siblings_drop,
        "Siblings_Dropout_Reason": siblings_reason, "Siblings_Highest_Education": siblings_edu,
        "Siblings_Currently_In_School": siblings_school, "Sibling_Dropout_Impact_Score": sibling_impact,
        "Single_Parent_Family": single_parent, "Attendance_Percentage": attendance,
        "Previous_Year_Marks": marks, "Failed_Subjects_Count": failed_subj,
        "Homework_Completion": homework, "Grade_Repetition_History": grade_rep,
        "Learning_Difficulty": learn_diff, "Distance_to_School_km": distance,
        "Transport_Available": transport, "School_Type": school_type,
        "Mid_Day_Meal_Beneficiary": mid_day, "Scholarship_Received": scholarship,
        "Bullying_Experience": bullying, "Teacher_Student_Relationship": teacher_rel,
        "Peer_Influence": peer_inf, "Self_Esteem_Level": self_esteem,
        "Mental_Health_Concern": mental_health, "Parental_Involvement": parental_inv,
        "Child_Labour": child_labour, "Early_Marriage_Risk": early_mar,
        "Domestic_Responsibility": domestic, "Smartphone_Access": smartphone,
        "Internet_Access": internet,
    }

    st.markdown("---")
    btn_c1, btn_c2 ,btn_c3= st.columns([3, 1,1])
    with btn_c1:
        predict_clicked = st.button("🔍 Predict Dropout Risk",
                                    use_container_width=True, type="primary")
    with btn_c2:
        cohort_clicked = st.button("📊 Cohort Comparison",
                                   use_container_width=True)
    with btn_c3:
        heatmap_clicked = st.button(
            "🗺 District Heatmap",
            use_container_width=True
        )
    # ── Predict ────────────────────────────────────────────────
    if predict_clicked:
        st.session_state.student_data = student_data
        st.session_state.result       = predict_risk(student_data)

    # ── Cohort → navigate to dedicated page ────────────────────
    if cohort_clicked:
        st.session_state.student_data = student_data   # save current form values
        st.session_state.page         = "cohort"
        st.rerun()
    if heatmap_clicked:
        st.session_state.page = "heatmap"
        st.rerun()
    # ── Results ────────────────────────────────────────────────
    if st.session_state.result:
        _show_results()


# ── Results display ────────────────────────────────────────────
def _show_results():
    result = st.session_state.result
    data   = st.session_state.student_data
    risk   = result.get("Risk_Level", "Low")

    st.markdown("---")
    st.subheader("Prediction Result")

    if risk == "Low":
        st.success("### ✅ Risk Level: LOW\nThis student shows a low concern level. Continue monitoring progress.")
    elif risk == "Moderate":
        st.warning("### 🚨 Risk Level: MODERATE(SLIGHTLY HIGH)\nThis student needs attention. Targeted support is recommended.")
    else:
        st.error("### 🚨 Risk Level: HIGH\nThis student needs immediate support and intervention.")

    # Top 3 Factors
    st.subheader("🔍 Top 3 Influencing Factors")
    factors = result.get("Top_Influencing_Factors", get_top_factors(data, risk))[:3]
    for i, factor in enumerate(factors, 1):
        desc  = FACTOR_EXPLANATIONS.get(factor, {}).get(risk, "This factor influences the prediction.")
        label = factor.replace("_", " ")
        if risk == "Low":
            st.success(f"**{i}. {label}**\n\n{desc}")
        elif risk == "Moderate":
            st.warning(f"**{i}. {label}**\n\n{desc}")
        else:
            st.error(f"**{i}. {label}**\n\n{desc}")

    # Action buttons — only for Moderate / High
    if risk in ["Moderate", "High"]:
        st.markdown("---")
        st.subheader("Actions ")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📌 View Eligible Government Schemes", use_container_width=True):
                st.session_state.page = "schemes"
                st.rerun()
        with col2:
            if st.button("✉️ Send Message to Parents (Tamil)", use_container_width=True):
                st.session_state.page = "message"
                st.rerun()
        with col3:
            if st.button("🧑‍⚕️ Give Counselling", use_container_width=True, type="primary"):
                st.session_state.page = "counselling"
                st.rerun()