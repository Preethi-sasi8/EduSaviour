# ═══════════════════════════════════════════════════════════════
# utils.py — Helper Functions
# ═══════════════════════════════════════════════════════════════

import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import GMAIL_SENDER, GMAIL_APP_PASS, FLASK_API_URL
from data import SCHEME_DATA, FACTOR_EXPLANATIONS


# ── Prediction ─────────────────────────────────────────────────
def predict_risk(data):
    """Try Flask API first, fallback to local scoring."""
    try:
        response = requests.post(FLASK_API_URL, json=data, timeout=5)
        result = response.json()
        return result
    except Exception:
        return _local_predict(data)


def _local_predict(data):
    attendance   = float(data.get("Attendance_Percentage", 75))
    marks        = float(data.get("Previous_Year_Marks", 60))
    failed_subj  = int(data.get("Failed_Subjects_Count", 0))
    child_labour = data.get("Child_Labour", "No")
    early_mar    = data.get("Early_Marriage_Risk", "No")
    distance     = float(data.get("Distance_to_School_km", 3))
    income       = data.get("Family_Income_Level", "Middle Income")
    siblings_d   = int(data.get("Siblings_Dropout_Count", 0))
    mental       = data.get("Mental_Health_Concern", "No")
    bullying     = data.get("Bullying_Experience", "No")

    score = 0
    if attendance < 60:   score += 30
    elif attendance < 75: score += 15
    if marks < 40:        score += 25
    elif marks < 55:      score += 12
    if failed_subj >= 3:  score += 20
    elif failed_subj >= 1: score += 10
    if child_labour == "Yes":  score += 20
    if early_mar == "Yes":     score += 15
    if distance > 10:  score += 10
    elif distance > 5: score += 5
    if income == "Below Poverty Line": score += 10
    if siblings_d >= 2:    score += 10
    if mental == "Yes":    score += 8
    if bullying == "Yes":  score += 7

    if score >= 50:   risk = "High"
    elif score >= 25: risk = "Moderate"
    else:             risk = "Low"

    return {
        "Risk_Level": risk,
        "Top_Influencing_Factors": get_top_factors(data, risk),
    }


# ── Factor Scoring ──────────────────────────────────────────────
def get_top_factors(data, risk):
    scores = {}
    scores["Attendance_Percentage"]  = (100 - float(data.get("Attendance_Percentage", 75))) / 100
    scores["Previous_Year_Marks"]    = (100 - float(data.get("Previous_Year_Marks", 60))) / 100
    scores["Failed_Subjects_Count"]  = min(int(data.get("Failed_Subjects_Count", 0)) / 5, 1.0)
    scores["Distance_to_School_km"]  = min(float(data.get("Distance_to_School_km", 3)) / 20, 1.0)
    scores["Child_Labour"]           = 1.0 if data.get("Child_Labour") == "Yes" else 0.0
    scores["Early_Marriage_Risk"]    = 1.0 if data.get("Early_Marriage_Risk") == "Yes" else 0.0
    income_map = {"Below Poverty Line": 1.0, "Low Income": 0.7, "Middle Income": 0.3, "High Income": 0.0}
    scores["Family_Income_Level"]    = income_map.get(data.get("Family_Income_Level", "Low Income"), 0.5)
    scores["Siblings_Dropout_Count"] = min(int(data.get("Siblings_Dropout_Count", 0)) / 3, 1.0)
    scores["Single_Parent_Family"]   = 1.0 if data.get("Single_Parent_Family") == "Yes" else 0.0
    involvement_map = {"High": 0.0, "Moderate": 0.4, "Low": 0.8, "None": 1.0}
    scores["Parental_Involvement"]   = involvement_map.get(data.get("Parental_Involvement", "Moderate"), 0.4)
    scores["Mental_Health_Concern"]  = 1.0 if data.get("Mental_Health_Concern") == "Yes" else 0.0
    scores["Bullying_Experience"]    = 1.0 if data.get("Bullying_Experience") == "Yes" else 0.0
    scores["Learning_Difficulty"]    = 1.0 if data.get("Learning_Difficulty") == "Yes" else 0.0
    dom_map = {"High": 1.0, "Moderate": 0.5, "Low": 0.1, "None": 0.0}
    scores["Domestic_Responsibility"] = dom_map.get(data.get("Domestic_Responsibility", "Low"), 0.1)
    peer_map = {"Negative": 1.0, "Neutral": 0.3, "Positive": 0.0}
    scores["Peer_Influence"]         = peer_map.get(data.get("Peer_Influence", "Neutral"), 0.3)
    esteem_map = {"Low": 1.0, "Moderate": 0.4, "High": 0.0}
    scores["Self_Esteem_Level"]      = esteem_map.get(data.get("Self_Esteem_Level", "Moderate"), 0.4)
    return sorted(scores, key=scores.get, reverse=True)[:3]


# ── Scheme Eligibility ─────────────────────────────────────────
def get_eligible_schemes(data):
    eligible = []
    for name, info in SCHEME_DATA.items():
        try:
            if info["eligibility_rules"](data):
                eligible.append(name)
        except Exception:
            pass
    return eligible


# ── Tamil Message Generator ────────────────────────────────────
def generate_tamil_message(data, risk):
    standard   = data.get("Standard", "")
    attendance = data.get("Attendance_Percentage", "")
    marks      = data.get("Previous_Year_Marks", "")
    gender     = data.get("Gender", "Male")
    pronoun    = "அவள்"   if gender == "Female" else "அவன்"
    child_word = "மகளின்" if gender == "Female" else "மகனின்"

    if risk == "Moderate":
        return (
            f"அன்பான பெற்றோருக்கு,\n\n"
            f"வணக்கம். உங்கள் {child_word} கல்வி நலனில் ஆர்வமுள்ள நாங்கள் உங்களுடன் சில "
            f"முக்கியமான தகவல்களை பகிர்ந்துகொள்ள விரும்புகிறோம்.\n\n"
            f"உங்கள் பிள்ளை தற்போது {standard}-ஆம் வகுப்பில் படிக்கிறார். கடந்த சில வாரங்களாக "
            f"{pronoun} பள்ளி வருகையில் சிறிது மாற்றம் காணப்படுகிறது. வருகை சதவிகிதம் "
            f"{attendance}% ஆகவும், கடந்த ஆண்டு மதிப்பெண் {marks} ஆகவும் உள்ளது.\n\n"
            f"உங்கள் பிள்ளை மிகவும் திறமையானவர். இந்த சிறிய இடைவெளியை சரி செய்தால், "
            f"{pronoun} எதிர்காலம் இன்னும் பிரகாசமாக இருக்கும்.\n\n"
            f"தினமும் பள்ளிக்கு வருவதை உறுதி செய்யுங்கள். படிக்க வீட்டில் அமைதியான நேரம் "
            f"ஒதுக்குங்கள். ஏதாவது சிரமம் இருந்தால் ஆசிரியரிடம் நேரடியாக தெரிவியுங்கள்.\n\n"
            f"உங்கள் ஒத்துழைப்புக்கு நன்றி.\n\nமரியாதையுடன்,\nபள்ளி நலன் குழு"
        )
    else:
        return (
            f"அன்பான பெற்றோருக்கு,\n\n"
            f"வணக்கம். உங்கள் {child_word} நலனில் ஆழமான அக்கறையுடன் இந்த செய்தியை அனுப்புகிறோம்.\n\n"
            f"உங்கள் பிள்ளை {standard}-ஆம் வகுப்பில் படிக்கிறார். தற்போது {pronoun} பள்ளி வருகை "
            f"{attendance}% மட்டுமே உள்ளது மற்றும் கடந்த ஆண்டு மதிப்பெண் {marks} ஆக இருக்கிறது. "
            f"இது {pronoun} கல்வி வாழ்க்கையில் தொடர்ந்தால் நீண்ட கால பாதிப்பை உண்டாக்கலாம்.\n\n"
            f"உடனடியாக பள்ளியை தொடர்பு கொண்டு ஆசிரியருடன் சந்திப்பு ஏற்பாடு செய்யுங்கள். "
            f"உங்கள் பிள்ளையிடம் அன்புடன் பேசி {pronoun} மனசுக்குள் என்ன நடக்கிறது என்று "
            f"புரிந்துகொள்ளுங்கள். பள்ளியில் கிடைக்கும் அரசு உதவித்தொகை திட்டங்களை "
            f"பயன்படுத்திக்கொள்ளுங்கள். {pronoun} தினமும் பள்ளிக்கு வருவதை நேரில் உறுதிப்படுத்துங்கள்.\n\n"
            f"நினைவில் வையுங்கள்: ஒரு குழந்தையின் எதிர்காலம் பெற்றோரின் ஒரு நிமிட "
            f"கவனிப்பில் மாறலாம். நாங்கள் உங்களோடு இருக்கிறோம்.\n\n"
            f"மரியாதையுடன்,\nபள்ளி நலன் குழு"
        )


# ── Gmail Email Sender ─────────────────────────────────────────
def send_email_gmail(to_email, message, risk):
    """
    Sends Tamil parent message as a styled HTML email via Gmail SMTP.
    Returns (success: bool, message: str)
    """
    subject = (
        "⚠️ உங்கள் பிள்ளையின் கல்வி நலன் தொடர்பான முக்கிய தகவல்"
        if risk == "Moderate"
        else "🚨 உங்கள் பிள்ளைக்கு உடனடி கவனிப்பு தேவை — பள்ளி அறிவிப்பு"
    )
    border_color = "#f0ad4e" if risk == "Moderate" else "#d9534f"
    heading_color = "#e67e22" if risk == "Moderate" else "#c0392b"
    heading_text = "⚠️ கவனிப்பு தேவை" if risk == "Moderate" else "🚨 உடனடி கவனிப்பு தேவை"

    html_body = f"""
    <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
      <div style="max-width:600px;margin:auto;background:white;border-radius:10px;
                  padding:30px;border-left:6px solid {border_color};">
        <h2 style="color:{heading_color};">{heading_text}</h2>
        <hr style="border:none;border-top:1px solid #eee;"/>
        <div style="font-size:15px;line-height:2;color:#333;white-space:pre-wrap;">{message}</div>
        <hr style="border:none;border-top:1px solid #eee;"/>
        <p style="font-size:12px;color:#aaa;">
          இந்த செய்தி பள்ளி மாணவர் நலன் கணினி மூலம் தானாக அனுப்பப்பட்டது.
        </p>
      </div>
    </body></html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = GMAIL_SENDER
        msg["To"]      = to_email
        msg.attach(MIMEText(message,   "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html",  "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_SENDER, to_email, msg.as_string())

        return True, "Email sent successfully."

    except smtplib.SMTPAuthenticationError:
        return False, "AUTH_FAILED"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"