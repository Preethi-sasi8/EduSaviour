# ═══════════════════════════════════════════════════════════════
# page_counselling.py — Counselling Assignment & 30-Day Tracker
# ═══════════════════════════════════════════════════════════════

import streamlit as st
from datetime import date, timedelta
from data import FACTOR_EXPLANATIONS
from utils import get_top_factors

# Display name → login username mapping
COUNSELLORS = {
    "Mrs. Lakshmi (School Counsellor)": "counsellor",
    "Dr. Kumar (Psychologist)":          "counsellor2",
    "Mr. Rajesh (Academic Mentor)":      "counsellor3",
    "Ms. Priya (Social Worker)":         "counsellor4",
}
COUNSELLOR_NAMES = list(COUNSELLORS.keys())

PROGRESS_OPTIONS = ["Improving", "Stable", "No Change", "Needs Attention", "Critical"]

# bg, border, text, emoji for each status
PROGRESS_STYLE = {
    "Improving":         ("#1a7a4a", "#13cf75", "#ffffff", "✅"),
    "Stable":            ("#1565c0", "#42a5f5", "#ffffff", "🔵"),
    "No Change":         ("#b8860b", "#ffd600", "#ffffff", "🟡"),
    "Needs Attention":   ("#c75000", "#ff7043", "#ffffff", "🟠"),
    "Critical":          ("#b71c1c", "#ef5350", "#ffffff", "🚨"),
    "Session Scheduled": ("#37474f", "#90a4ae", "#ffffff", "📅"),
    "Not Started":       ("#424242", "#757575", "#cccccc", "⬜"),
}

def _init():
    if "assignments" not in st.session_state:
        st.session_state.assignments = {}
    if "counselling_records" not in st.session_state:
        st.session_state.counselling_records = []

def show():
    _init()
    role = st.session_state.get("role", "teacher")
    if role in ["teacher", "administrator"]:
        _teacher_view()
    else:
        _counsellor_view()


# ═══════════════════════════════════════════════════════════════
# SHARED: coloured 30-day timeline grid
# ═══════════════════════════════════════════════════════════════
def _draw_timeline(student_id, assignment):
    records     = [r for r in st.session_state.counselling_records
                   if r["student_id"] == student_id and r["day"] > 0]
    by_day      = {r["day"]: r for r in records}

    # ── Legend ─────────────────────────────────────────────────
    legend_parts = []
    for status, (bg, border, fg, icon) in PROGRESS_STYLE.items():
        if status == "Not Started":
            continue
        legend_parts.append(
            f"<span style='display:inline-flex;align-items:center;margin-right:12px;"
            f"font-size:12px;color:#444;'>"
            f"<span style='width:14px;height:14px;border-radius:3px;background:{bg};"
            f"display:inline-block;margin-right:4px;'></span>{icon} {status}</span>"
        )
    st.markdown(
        "<div style='margin-bottom:10px;flex-wrap:wrap;display:flex;'>"
        + "".join(legend_parts) + "</div>",
        unsafe_allow_html=True
    )

    # ── Grid (5 rows × 6 cols) ─────────────────────────────────
    for row in range(5):
        cols = st.columns(6)
        for col_i in range(6):
            day = row * 6 + col_i + 1
            with cols[col_i]:
                if day in by_day:
                    rec = by_day[day]
                    bg, border, fg, icon = PROGRESS_STYLE.get(
                        rec["progress"], ("#37474f","#90a4ae","#fff","📅")
                    )
                    st.markdown(
                        f"<div style='background:{bg};border:2px solid {border};"
                        f"border-radius:10px;padding:8px 4px;text-align:center;"
                        f"margin:2px;min-height:80px;display:flex;flex-direction:column;"
                        f"justify-content:center;'>"
                        f"<div style='font-size:11px;font-weight:700;color:{fg};'>Day {day}</div>"
                        f"<div style='font-size:20px;margin:3px 0;'>{icon}</div>"
                        f"<div style='font-size:9px;color:{fg};font-weight:600;"
                        f"white-space:nowrap;overflow:hidden;'>{rec['progress'][:10]}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                else:
                    sdate    = assignment["start_date"] + timedelta(days=day - 1)
                    is_today = sdate == date.today()
                    bg       = "#f9a825" if is_today else "#2d3436"
                    border   = "#ffd600" if is_today else "#555"
                    fg       = "#1a1a1a" if is_today else "#8a8a8a"
                    icon     = "📍" if is_today else "○"
                    label    = "TODAY" if is_today else sdate.strftime("%d %b")
                    st.markdown(
                        f"<div style='background:{bg};border:2px solid {border};"
                        f"border-radius:10px;padding:8px 4px;text-align:center;"
                        f"margin:2px;min-height:80px;display:flex;flex-direction:column;"
                        f"justify-content:center;'>"
                        f"<div style='font-size:11px;font-weight:700;color:{fg};'>Day {day}</div>"
                        f"<div style='font-size:20px;margin:3px 0;'>{icon}</div>"
                        f"<div style='font-size:9px;color:{fg};font-weight:600;'>{label}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
    return records


# ═══════════════════════════════════════════════════════════════
# TEACHER VIEW
# ═══════════════════════════════════════════════════════════════
def _teacher_view():
    student = st.session_state.get("student_data", {})
    result  = st.session_state.get("result", {})
    user    = st.session_state.get("user", "Teacher")

    student_name = student.get("name", "Student")
    student_id   = student.get("id", "STU001")
    risk         = result.get("Risk_Level", "Unknown") if result else "Unknown"

    st.title("🧑‍⚕️ Counselling Assignment")

    # ── Student banner ─────────────────────────────────────────
    risk_styles = {
        "High":     ("#7f1d1d", "#ef4444", "🔴"),
        "Moderate": ("#78350f", "#f59e0b", "🟠"),
        "Low":      ("#14532d", "#22c55e", "🟢"),
    }
    rbg, rborder, ricon = risk_styles.get(risk, ("#1e293b","#64748b","⚪"))

    st.markdown(f"""
    <div style='background:{rbg};border-left:6px solid {rborder};border-radius:12px;
                padding:16px 22px;margin-bottom:16px;'>
      <div style='display:flex;justify-content:space-between;align-items:center;'>
        <div>
          <div style='font-size:20px;font-weight:800;color:#fff;'>👤 {student_name}</div>
          <div style='font-size:13px;color:#ccc;margin-top:4px;'>Student ID: {student_id}</div>
        </div>
        <div style='font-size:26px;font-weight:800;color:#fff;'>{ricon} {risk} Risk</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if student and risk != "Unknown":
        factors = get_top_factors(student, risk)
        tags_html = "".join([
            f"<span style='background:#334155;color:#e2e8f0;border-radius:20px;"
            f"padding:3px 11px;margin:3px;font-size:12px;display:inline-block;'>"
            f"🔸 {f.replace('_',' ')}</span>"
            for f in factors
        ])
        st.markdown(f"<div style='margin-bottom:12px;'>{tags_html}</div>",
                    unsafe_allow_html=True)

    st.divider()
    assignment = st.session_state.assignments.get(student_id)

    # ── Assign form ────────────────────────────────────────────
    if assignment is None:
        st.subheader("📋 Assign Counsellor")
        col1, col2 = st.columns(2)
        with col1:
            counsellor = st.selectbox("Select Counsellor", COUNSELLOR_NAMES)
        with col2:
            start_date = st.date_input("First Session Date", value=date.today())

        end_date = start_date + timedelta(days=29)
        st.info(f"📅 Period: **{start_date}** → **{end_date}** (30 days)")
        notes = st.text_area("Assignment Notes (optional)",
                             placeholder="Reason for counselling, specific concerns...")

        if st.button("✅ Assign Counselling", type="primary", use_container_width=True):
            # Store full student_data so counsellor can read it later
            st.session_state.assignments[student_id] = {
                "student_name":       student_name,
                "student_id":         student_id,
                "risk":               risk,
                "counsellor":         counsellor,
                "counsellor_username": COUNSELLORS[counsellor],  # ← login username
                "start_date":         start_date,
                "end_date":           end_date,
                "notes":              notes,
                "assigned_by":        user,
                "assigned_on":        date.today(),
                "status":             "Active",
                "student_data":       dict(student),
                "result":             dict(result) if result else {},
            }
            st.session_state.counselling_records.append({
                "student_id":   student_id,
                "student_name": student_name,
                "counsellor":   counsellor,
                "day":          0,
                "session_date": start_date,
                "feedback":     "Counselling session assigned.",
                "progress":     "Session Scheduled",
                "updated_by":   user,
            })
            st.success(f"✅ Assigned to **{counsellor}** from **{start_date}** to **{end_date}**")
            st.rerun()

    else:
        # ── Active assignment ──────────────────────────────────
        days_done = len([r for r in st.session_state.counselling_records
                         if r["student_id"] == student_id and r["day"] > 0])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Counsellor",    assignment["counsellor"].split("(")[0].strip())
        col2.metric("Start Date",    str(assignment["start_date"]))
        col3.metric("End Date",      str(assignment["end_date"]))
        col4.metric("Sessions Done", f"{days_done} / 30")

        pct = days_done / 30
        st.progress(pct, text=f"{days_done}/30 sessions  ({int(pct*100)}%)")
        st.divider()

        # Timeline
        st.subheader("📅 30-Day Session Timeline")
        records = _draw_timeline(student_id, assignment)

        st.divider()

        # Feedback log
        if records:
            st.subheader("📝 Session Feedback Log")
            for rec in sorted(records, key=lambda x: x["day"], reverse=True):
                bg, border, fg, icon = PROGRESS_STYLE.get(
                    rec["progress"], ("#37474f","#90a4ae","#fff","📅"))
                with st.expander(
                    f"{icon} Day {rec['day']} — {rec['session_date']} — {rec['progress']}"
                ):
                    st.markdown(
                        f"<div style='background:{bg};border-radius:8px;padding:10px 14px;"
                        f"border-left:4px solid {border};color:{fg};'>"
                        f"<b>Feedback:</b><br>{rec['feedback']}</div>",
                        unsafe_allow_html=True
                    )
                    if rec.get("interventions"):
                        st.markdown(f"🛠️ **Interventions:** {rec['interventions']}")
                    st.caption(f"By: {rec['updated_by']}")
        else:
            st.info("No sessions recorded yet.")

        # Reassign
        with st.expander("🔄 Reassign Counsellor"):
            new_c  = st.selectbox("New Counsellor", COUNSELLOR_NAMES, key="reassign_c")
            reason = st.text_input("Reason")
            if st.button("Confirm Reassignment"):
                st.session_state.assignments[student_id]["counsellor"] = new_c
                st.session_state.assignments[student_id]["counsellor_username"] = COUNSELLORS[new_c]
                st.session_state.counselling_records.append({
                    "student_id": student_id, "student_name": student_name,
                    "counsellor": new_c, "day": 0, "session_date": date.today(),
                    "feedback": f"Reassigned. Reason: {reason}",
                    "progress": "Session Scheduled", "updated_by": user,
                })
                st.success(f"Reassigned to {new_c}")
                st.rerun()

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⬅ Prediction", use_container_width=True):
            st.session_state.page = "main"; st.rerun()



# ═══════════════════════════════════════════════════════════════
# COUNSELLOR VIEW
# ═══════════════════════════════════════════════════════════════
def _counsellor_view():
    _init()
    user = st.session_state.get("user", "Counsellor")

    st.title(" Counsellor Dashboard")
    st.caption(f"Logged in as: **{user}**")
    st.divider()

    # Find assigned students — match by stored username, not display name substring
    my_assignments = {
        sid: asgn for sid, asgn in st.session_state.assignments.items()
        if asgn.get("counsellor_username") == user or user == "admin"
    }

    if not my_assignments:
        st.markdown("""
        <div style='background:#1e293b;border-radius:14px;padding:32px;
                    border:2px dashed #475569;text-align:center;'>
          <div style='font-size:42px;margin-bottom:10px;'>⏳</div>
          <div style='font-size:20px;font-weight:700;color:#f1f5f9;'>No Students Assigned Yet</div>
          <div style='font-size:14px;color:#94a3b8;margin-top:8px;'>
            The teacher/admin has not assigned any students to you.<br>
            Please check back after the teacher completes the assignment.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Student dropdown
    student_options = {
        sid: f"{asgn['student_name']} (ID: {sid}) — {asgn['risk']} Risk"
        for sid, asgn in my_assignments.items()
    }
    selected_sid = st.selectbox(
        "👤 Select Student",
        options=list(student_options.keys()),
        format_func=lambda x: student_options[x]
    )

    assignment          = my_assignments[selected_sid]
    student_name        = assignment["student_name"]
    student_id          = selected_sid
    risk                = assignment["risk"]
    assigned_counsellor = assignment["counsellor"]

    # Use full student data snapshot stored at assign time
    # Also fall back to current session_state if assignment snapshot is missing/empty
    student = assignment.get("student_data") or st.session_state.get("student_data") or {}
    result  = assignment.get("result")       or st.session_state.get("result")       or {"Risk_Level": risk}

    # ── Student info banner ────────────────────────────────────
    risk_styles = {
        "High":     ("#7f1d1d","#ef4444","🔴"),
        "Moderate": ("#78350f","#f59e0b","🟠"),
        "Low":      ("#14532d","#22c55e","🟢"),
    }
    rbg, rborder, ricon = risk_styles.get(risk, ("#1e293b","#64748b","⚪"))

    col_info, col_stats = st.columns([3, 1])
    with col_info:
        st.markdown(f"""
        <div style='background:{rbg};border-left:6px solid {rborder};border-radius:12px;
                    padding:16px 22px;'>
          <div style='font-size:20px;font-weight:800;color:#fff;'>👤 {student_name}</div>
          <div style='font-size:13px;color:#ccc;margin-top:4px;'>
            ID: {student_id} &nbsp;|&nbsp; {assigned_counsellor.split("(")[0].strip()}
          </div>
          <div style='font-size:13px;color:#ccc;margin-top:3px;'>
            📅 {assignment['start_date']} → {assignment['end_date']}
          </div>
          <div style='font-size:22px;font-weight:800;color:#fff;margin-top:8px;'>
            {ricon} {risk} Risk
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_stats:
        st.metric("Attendance",      f"{student.get('Attendance_Percentage','N/A')}%")
        st.metric("Last Yr Marks",   f"{student.get('Previous_Year_Marks','N/A')}")
        st.metric("Failed Subjects", f"{student.get('Failed_Subjects_Count','N/A')}")

    st.divider()

    # ── Risk factors ───────────────────────────────────────────
    st.subheader("🔍 Student Risk Analysis")
    if student:
        factors = get_top_factors(student, risk)
        for i, factor in enumerate(factors, 1):
            desc  = FACTOR_EXPLANATIONS.get(factor, {}).get(risk, "")
            label = factor.replace("_", " ")
            bg, border, fg, icon = PROGRESS_STYLE.get(
                "Critical" if risk == "High" else "Needs Attention",
                ("#7f1d1d","#ef4444","#fff","🚨")
            )
            st.markdown(
                f"<div style='background:{bg};border-radius:8px;padding:10px 14px;"
                f"margin-bottom:6px;border-left:4px solid {border};color:{fg};'>"
                f"<b>{i}. {label}</b>"
                f"<div style='font-size:13px;margin-top:3px;opacity:0.9;'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    with st.expander("📄 View Full Student Profile"):
        if not student:
            st.warning("Student profile data not available. Please re-assign after predicting.")
        else:
            # All 36 fields — group into readable sections
            SECTIONS = {
                " Demographics":       ["Gender","Caste_Category","Standard","Age","Family_Income_Level"],
                " Family Background":  ["Father_Education","Mother_Education","No_of_Siblings",
                                          "Siblings_Dropout_Count","Siblings_Dropout_Reason",
                                          "Siblings_Highest_Education","Siblings_Currently_In_School",
                                          "Sibling_Dropout_Impact_Score","Single_Parent_Family"],
                " Academic":           ["Attendance_Percentage","Previous_Year_Marks",
                                          "Failed_Subjects_Count","Homework_Completion",
                                          "Grade_Repetition_History","Learning_Difficulty"],
                "School & Transport": ["Distance_to_School_km","Transport_Available","School_Type",
                                          "Mid_Day_Meal_Beneficiary","Scholarship_Received"],
                "Social & Mental":    ["Bullying_Experience","Teacher_Student_Relationship",
                                          "Peer_Influence","Self_Esteem_Level","Mental_Health_Concern",
                                          "Parental_Involvement","Child_Labour","Early_Marriage_Risk",
                                          "Domestic_Responsibility","Smartphone_Access","Internet_Access"],
            }
            for section_title, keys in SECTIONS.items():
                st.markdown(f"**{section_title}**")
                c1, c2 = st.columns(2)
                for idx, k in enumerate(keys):
                    val = student.get(k, "—")
                    col = c1 if idx % 2 == 0 else c2
                    col.markdown(f"• **{k.replace('_',' ')}:** {val}")

    st.divider()

    # ── Progress overview ──────────────────────────────────────
    records    = [r for r in st.session_state.counselling_records
                  if r["student_id"] == student_id and r["day"] > 0]
    days_done  = len(records)
    last_prog  = records[-1]["progress"] if records else "Not Started"
    lbg, lborder, lfg, licon = PROGRESS_STYLE.get(last_prog,("#37474f","#90a4ae","#fff","⬜"))

    st.subheader("📊 Progress Overview")

    # Stats row
    c1, c2, c3 = st.columns(3)
    c1.metric("Sessions Done",  f"{days_done} / 30")
    c2.metric("Days Remaining", f"{30 - days_done}")
    c3.metric("Last Status",    f"{licon} {last_prog}")

    st.progress(days_done / 30, text=f"{days_done}/30 sessions completed")

    # Last status badge
    st.markdown(
        f"<div style='background:{lbg};border:2px solid {lborder};border-radius:10px;"
        f"padding:12px 18px;display:inline-block;margin:8px 0;color:{lfg};font-weight:700;'>"
        f"{licon} Current Status: {last_prog}</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # ── Timeline ───────────────────────────────────────────────
    st.subheader("📅 30-Day Session Timeline")
    _draw_timeline(student_id, assignment)

    st.divider()

    # ── Submit feedback ────────────────────────────────────────
    st.subheader("📝 Submit Session Feedback")
    recorded_days = {r["day"] for r in records}
    next_day      = max(recorded_days, default=0) + 1

    if next_day > 30:
        st.success("🎉 All 30 sessions completed!")
        _show_summary(records, student_name)
    else:
        session_date = assignment["start_date"] + timedelta(days=next_day - 1)
        c1, c2 = st.columns(2)
        with c1:
            day_input = st.number_input("Session Day", min_value=1, max_value=30, value=next_day)
        with c2:
            actual_date = st.date_input("Session Date", value=session_date)

        if day_input in recorded_days:
            st.warning(f"⚠️ Day {day_input} already has feedback.")

        feedback = st.text_area(
            "Session Feedback",
            placeholder="Student's mood, topics discussed, observations, follow-up actions...",
            height=120
        )

        c1, c2 = st.columns(2)
        with c1:
            progress_status = st.selectbox("Progress Status", PROGRESS_OPTIONS)
        with c2:
            next_session = st.date_input("Next Session Date",
                                         value=actual_date + timedelta(days=1))

        # Live status badge
        sbg, sborder, sfg, sicon = PROGRESS_STYLE.get(
            progress_status, ("#37474f","#90a4ae","#fff","📅"))
        st.markdown(
            f"<div style='background:{sbg};border:2px solid {sborder};border-radius:8px;"
            f"padding:8px 16px;display:inline-block;color:{sfg};font-weight:700;"
            f"margin-bottom:8px;'>{sicon} Status: {progress_status}</div>",
            unsafe_allow_html=True
        )

        intervention = st.multiselect("Interventions Used", [
            "Motivational Counselling", "Academic Support", "Family Involvement",
            "Peer Support", "Career Guidance", "Mental Health Support",
            "Financial Aid Referral", "Home Visit", "Group Session"
        ])

        if st.button("✅ Submit Feedback", type="primary", use_container_width=True,
                     disabled=not feedback.strip()):
            if day_input in recorded_days:
                st.error(f"Day {day_input} already submitted.")
            else:
                st.session_state.counselling_records.append({
                    "student_id":    student_id,
                    "student_name":  student_name,
                    "counsellor":    assigned_counsellor,
                    "day":           day_input,
                    "session_date":  actual_date,
                    "feedback":      feedback,
                    "progress":      progress_status,
                    "next_session":  next_session,
                    "interventions": ", ".join(intervention),
                    "updated_by":    user,
                })
                st.success(f"✅ Day {day_input} submitted! Next: {next_session}")
                st.rerun()

    st.divider()

    # ── Session history ────────────────────────────────────────
    if records:
        st.subheader("Full Session History")
        for rec in sorted(records, key=lambda x: x["day"], reverse=True):
            bg, border, fg, icon = PROGRESS_STYLE.get(
                rec["progress"], ("#37474f","#90a4ae","#fff","📅"))
            with st.expander(
                f"{icon} Day {rec['day']} — {rec['session_date']} — {rec['progress']}"
            ):
                st.markdown(
                    f"<div style='background:{bg};border-radius:8px;padding:12px 16px;"
                    f"border-left:4px solid {border};color:{fg};'>"
                    f"<b>📝 Feedback:</b><br><span style='opacity:0.95;'>{rec['feedback']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if rec.get("interventions"):
                    st.markdown(f"🛠️ **Interventions:** {rec['interventions']}")
                if rec.get("next_session"):
                    st.markdown(f"📅 **Next Session:** {rec['next_session']}")
                st.caption(f"Submitted by: {rec['updated_by']}")

    st.divider()
    if st.button("⬅ Back", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# 30-DAY SUMMARY
# ═══════════════════════════════════════════════════════════════
def _show_summary(records, student_name):
    st.subheader(f"📊 30-Day Summary — {student_name}")
    status_counts = {}
    for rec in records:
        p = rec["progress"]
        status_counts[p] = status_counts.get(p, 0) + 1

    cols = st.columns(max(len(status_counts), 1))
    for i, (status, count) in enumerate(status_counts.items()):
        bg, border, fg, icon = PROGRESS_STYLE.get(status, ("#37474f","#90a4ae","#fff","📅"))
        cols[i].markdown(
            f"<div style='background:{bg};border:2px solid {border};border-radius:12px;"
            f"padding:16px;text-align:center;'>"
            f"<div style='font-size:24px;'>{icon}</div>"
            f"<div style='font-size:28px;font-weight:800;color:{fg};'>{count}</div>"
            f"<div style='font-size:12px;color:{fg};font-weight:600;'>{status}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    final = records[-1]["progress"] if records else "Unknown"
    bg, border, fg, icon = PROGRESS_STYLE.get(final, ("#37474f","#90a4ae","#fff","📅"))
    msg = ("🎉 Great progress! Student has shown significant improvement."
           if final == "Improving"
           else "⚠️ Further intervention is recommended.")
    st.markdown(
        f"<div style='background:{bg};border:2px solid {border};border-radius:14px;"
        f"padding:20px;text-align:center;margin-top:16px;'>"
        f"<div style='font-size:32px;'>{icon}</div>"
        f"<div style='font-size:20px;font-weight:700;color:{fg};margin-top:8px;'>"
        f"Final Status: {final}</div>"
        f"<div style='font-size:14px;color:{fg};margin-top:6px;opacity:0.9;'>{msg}</div>"
        f"</div>",
        unsafe_allow_html=True
    )