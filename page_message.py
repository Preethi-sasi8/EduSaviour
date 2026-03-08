# ═══════════════════════════════════════════════════════════════
# page_message.py — Tamil Parent Message + Email Sender
# ═══════════════════════════════════════════════════════════════

import urllib.parse
import streamlit as st
from utils import generate_tamil_message, send_email_gmail


def show():
    data   = st.session_state.get("student_data", {})
    result = st.session_state.get("result", {})
    risk   = result.get("Risk_Level", "Moderate") if result else "Moderate"

    st.title("✉️ பெற்றோர் செய்தி உருவாக்கி")
    st.markdown("##### Parent Message Generator — Tamil")
    st.markdown("---")

    # Risk badge
    if risk == "High":
        st.error("🚨 நிலை: உடனடி கவனிப்பு தேவை (High Risk)")
    else:
        st.warning("⚠️ நிலை: கவனிப்பு தேவை (Moderate Risk)")

    # ── Editable Message ───────────────────────────────────────
    st.subheader("📝 செய்தி")
    st.caption("தேவைப்பட்டால் கீழே உள்ள செய்தியை திருத்தலாம்.")

    default_msg = generate_tamil_message(data, risk)
    message = st.text_area(
        "Message",
        value=default_msg,
        height=380,
        label_visibility="collapsed"
    )
    st.caption(f"📊 Characters: {len(message)}")

    st.markdown("---")

    # ── Parent Email Input ─────────────────────────────────────
    st.subheader("📧 பெற்றோர் மின்னஞ்சல்")

    parent_email = st.text_input(
        "பெற்றோரின் Email முகவரி:",
        placeholder="parent@gmail.com",
    )
    email_valid = bool(
        parent_email
        and "@" in parent_email
        and "." in parent_email.split("@")[-1]
    )
    if parent_email and not email_valid:
        st.error("❌ சரியான email முகவரியை உள்ளிடுக.")

    st.markdown("---")

    # ── Send Buttons ───────────────────────────────────────────
    col_email, col_wa = st.columns(2)

    with col_email:
        send_clicked = st.button(
            "📧 Email அனுப்பு",
            use_container_width=True,
            type="primary",
            disabled=not email_valid,
        )

    with col_wa:
        if email_valid:
            # WhatsApp link as backup — use phone number if available
            encoded = urllib.parse.quote(message)
            st.link_button(
                "💬 WhatsApp மூலம் அனுப்பு",
                f"https://wa.me/?text={encoded}",
                use_container_width=True,
            )
        else:
            st.button("💬 WhatsApp மூலம் அனுப்பு", disabled=True, use_container_width=True)

    # ── Email Send Handler ─────────────────────────────────────
    if send_clicked and email_valid:
        with st.spinner("📧 Email அனுப்புகிறோம்..."):
            success, result_msg = send_email_gmail(
                to_email=parent_email,
                message=message,
                risk=risk,
            )

        if success:
            st.success(f"✅ Email வெற்றிகரமாக அனுப்பப்பட்டது! 📧 **{parent_email}** க்கு சென்றது.")

            with st.expander("📄 அனுப்பப்பட்ட செய்தி காண்க"):
                st.markdown(f"**To:** {parent_email}")
                st.text(message)

        elif result_msg == "AUTH_FAILED":
            st.error("❌ Gmail login தவறானது!")
            with st.expander("🔧 சரிசெய்வது எப்படி?"):
                st.markdown("""
**App Password பயன்படுத்துகிறீர்களா?** (உங்கள் Gmail password அல்ல)

**App Password பெற:**
1. **myaccount.google.com** → Security
2. **2-Step Verification** enable செய்யவும்
3. Security → **App Passwords** → Mail → Generate
4. 16-digit password-ஐ `config.py`-ல் paste செய்யவும்
                """)
        else:
            st.error(f"❌ பிழை ஏற்பட்டது:")
            st.code(result_msg, language="text")

    st.markdown("---")

    # ── Navigation ─────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Results", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()
