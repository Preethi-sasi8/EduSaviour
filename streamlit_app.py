import streamlit as st
import requests
import urllib.parse

# ─────────────────────────────────────────────
# GMAIL SMTP CREDENTIALS
# Use your Gmail address + App Password
# Get App Password: myaccount.google.com →
# Security → 2-Step Verification → App Passwords
# ─────────────────────────────────────────────
GMAIL_SENDER     = "preethisasikumar811@gmail.com"       # ← உங்கள் Gmail
GMAIL_APP_PASS   = "gpsq yirc jucg sajb"        # ← 16-digit App Password

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "page": "main",
    "scheme": "",
    "result": None,
    "student_data": {},
    "show_schemes": False,
}
for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────
# FACTOR DESCRIPTIONS
# ─────────────────────────────────────────────
factor_explanations = {
    "Attendance_Percentage": {
        "Low":      "✅ Good attendance shows strong commitment to education and reduces dropout risk significantly.",
        "Moderate": "⚠️ Irregular attendance is breaking academic continuity and may signal hidden barriers to schooling.",
        "High":     "🚨 Critically low attendance is the single strongest predictor of imminent dropout — immediate intervention needed."
    },
    "Previous_Year_Marks": {
        "Low":      "✅ Strong academic marks reflect confidence and motivation that protect against dropout.",
        "Moderate": "⚠️ Average performance may indicate learning gaps that, if unaddressed, increase dropout likelihood.",
        "High":     "🚨 Very poor academic results are demoralising students and making them disengage from school entirely."
    },
    "Failed_Subjects_Count": {
        "Low":      "✅ No failed subjects demonstrate academic stability and consistent progress.",
        "Moderate": "⚠️ Failing in some subjects creates frustration and may push students toward dropping out.",
        "High":     "🚨 Multiple subject failures severely undermine academic confidence and are strongly linked to dropout."
    },
    "Distance_to_School_km": {
        "Low":      "✅ Short school distance removes a major logistical barrier to daily attendance.",
        "Moderate": "⚠️ Moderate travel distance is adding fatigue and cost pressure that strains attendance.",
        "High":     "🚨 Long commute distance is a critical dropout driver, especially without safe transport available."
    },
    "Child_Labour": {
        "Low":      "✅ No child labour involvement means the student can focus entirely on education.",
        "Moderate": "⚠️ Part-time labour is creating time and energy conflicts that affect school performance.",
        "High":     "🚨 Active child labour is directly displacing schooling — urgent economic and legal intervention needed."
    },
    "Early_Marriage_Risk": {
        "Low":      "✅ No early marriage risk ensures the student can continue education without social pressure.",
        "Moderate": "⚠️ Emerging social pressure around marriage may soon interrupt schooling for this student.",
        "High":     "🚨 High early marriage risk is one of the leading causes of permanent female dropout — immediate family counselling needed."
    },
    "Family_Income_Level": {
        "Low":      "✅ Stable family income removes financial stress and supports uninterrupted schooling.",
        "Moderate": "⚠️ Low family income is creating resource constraints that may force the student to prioritise earning over learning.",
        "High":     "🚨 Extreme poverty (BPL) severely limits access to books, uniforms, and transport — financial support is critical."
    },
    "Siblings_Dropout_Count": {
        "Low":      "✅ No sibling dropouts suggest a positive family attitude toward education.",
        "Moderate": "⚠️ Having a sibling who dropped out normalises the behaviour and increases this student's risk.",
        "High":     "🚨 Multiple sibling dropouts create a strong behavioural pattern that significantly raises dropout probability."
    },
    "Single_Parent_Family": {
        "Low":      "✅ Both parents present provides stable emotional and financial support for education.",
        "Moderate": "⚠️ Single-parent household increases domestic responsibilities that can interfere with studying.",
        "High":     "🚨 Single-parent families face compounded financial and emotional pressures strongly linked to dropout."
    },
    "Parental_Involvement": {
        "Low":      "✅ High parental involvement creates accountability and encouragement that drives school retention.",
        "Moderate": "⚠️ Limited parental engagement reduces monitoring of academic progress and early warning signs.",
        "High":     "🚨 Absent parental involvement leaves students without guidance when they face school challenges."
    },
    "Mental_Health_Concern": {
        "Low":      "✅ Good mental health allows the student to cope with academic and social pressures effectively.",
        "Moderate": "⚠️ Mental health challenges are reducing motivation and concentration, affecting performance.",
        "High":     "🚨 Serious mental health concerns are creating significant barriers to school attendance and engagement."
    },
    "Bullying_Experience": {
        "Low":      "✅ Absence of bullying creates a safe school environment that encourages continued attendance.",
        "Moderate": "⚠️ Occasional bullying is damaging self-esteem and making school feel unwelcoming.",
        "High":     "🚨 Severe bullying is making school a hostile environment — students cannot learn or thrive under such conditions."
    },
    "Learning_Difficulty": {
        "Low":      "✅ No learning difficulties allow the student to keep pace with curriculum and stay engaged.",
        "Moderate": "⚠️ Undiagnosed or unsupported learning difficulties are causing frustration and disengagement.",
        "High":     "🚨 Significant learning difficulties without remedial support are pushing the student toward disengagement."
    },
    "Domestic_Responsibility": {
        "Low":      "✅ Minimal home duties allow the student adequate time for studying and rest.",
        "Moderate": "⚠️ Growing domestic responsibilities are eating into study time and causing fatigue.",
        "High":     "🚨 Heavy domestic burden is acting as a hidden barrier to education, especially for girls."
    },
    "Peer_Influence": {
        "Low":      "✅ Positive peer influence reinforces the value of staying in school.",
        "Moderate": "⚠️ Mixed peer influence may normalise absenteeism or disengagement from academics.",
        "High":     "🚨 Negative peer pressure is actively discouraging school participation and academic effort."
    },
    "Self_Esteem_Level": {
        "Low":      "✅ High self-esteem equips students to handle setbacks and persist through academic challenges.",
        "Moderate": "⚠️ Wavering self-esteem reduces resilience and makes the student vulnerable to dropout triggers.",
        "High":     "🚨 Very low self-esteem is a major psychological barrier — students stop believing education can help them."
    },
}

# ─────────────────────────────────────────────
# SCHEME DATABASE
# ─────────────────────────────────────────────
scheme_data = {
    "PM POSHAN (Mid-Day Meal)": {
        "description": "Provides free nutritious meals daily to students in government and aided schools to improve attendance, nutrition, and reduce dropout caused by hunger and financial burden.",
        "eligibility_rules": lambda d: d.get("School_Type") == "Government",
        "eligibility_display": ["Student studies in a Government school", "Student is enrolled (automatic benefit)"],
        "documents": ["School Enrollment Proof", "Aadhar Card"],
        "benefit": "Free meals daily",
        "website": "pmposhan.education.gov.in"
    },
    "Pre-Matric Scholarship SC/ST": {
        "description": "Financial scholarship for SC/ST students in Class 9-10 to reduce dropout due to economic burden.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") in ["SC", "ST"] and
            int(d.get("Standard", 0)) in [9, 10] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Belongs to SC or ST caste category", "Studying in Class 9 or 10", "Family income <= Rs.2,50,000 per year"],
        "documents": ["Caste Certificate", "Income Certificate", "Mark Sheet", "Aadhar Card", "Bank Passbook"],
        "benefit": "Rs.3,500-Rs.7,000/year",
        "website": "scholarships.gov.in"
    },
    "Post-Matric Scholarship SC/ST": {
        "description": "Supports SC/ST students in Class 11-12 to prevent dropout at the higher secondary transition stage.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") in ["SC", "ST"] and
            int(d.get("Standard", 0)) in [11, 12] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Belongs to SC or ST caste category", "Studying in Class 11 or 12", "Family income <= Rs.2,50,000 per year"],
        "documents": ["Caste Certificate", "Income Certificate", "Mark Sheet", "Aadhar Card"],
        "benefit": "Rs.6,000-Rs.12,000/year",
        "website": "scholarships.gov.in"
    },
    "OBC Pre-Matric Scholarship": {
        "description": "Financial assistance for OBC students in Class 9-10 facing financial hardship.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") == "OBC" and
            int(d.get("Standard", 0)) in [9, 10] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Belongs to OBC caste category", "Studying in Class 9 or 10", "Family income <= Rs.1,00,000 per year"],
        "documents": ["OBC Certificate", "Income Certificate", "Aadhar Card", "Mark Sheet"],
        "benefit": "Rs.2,500-Rs.4,500/year",
        "website": "scholarships.gov.in"
    },
    "NMMS Scholarship": {
        "description": "National Means-cum-Merit Scholarship for meritorious students from low-income families in government schools.",
        "eligibility_rules": lambda d: (
            int(d.get("Standard", 0)) in [9, 10, 11, 12] and
            d.get("School_Type") == "Government" and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line", "Middle Income"]
        ),
        "eligibility_display": ["Studying in Class 9-12 in a government school", "Family income <= Rs.3,50,000 per year"],
        "documents": ["Class 7 Mark Sheet", "Income Certificate", "Aadhar Card"],
        "benefit": "Rs.12,000/year (Rs.1,000/month)",
        "website": "scholarships.gov.in"
    },
    "KGBV Residential School": {
        "description": "Free residential schooling for SC/ST/OBC/Minority girls in Classes 9-12.",
        "eligibility_rules": lambda d: (
            d.get("Gender") == "Female" and
            d.get("Caste_Category") in ["SC", "ST", "OBC", "Minority"] and
            int(d.get("Standard", 0)) in [9, 10, 11, 12]
        ),
        "eligibility_display": ["Gender: Female", "Caste: SC / ST / OBC / Minority", "Studying in Class 9-12"],
        "documents": ["Caste Certificate", "Income Proof", "Transfer Certificate", "Aadhar Card"],
        "benefit": "Free boarding + tuition + uniform + books",
        "website": "samagra.education.gov.in"
    },
    "Beti Bachao Beti Padhao": {
        "description": "National campaign providing awareness and cash incentives to prevent gender discrimination and early marriage.",
        "eligibility_rules": lambda d: d.get("Gender") == "Female",
        "eligibility_display": ["Gender: Female", "Any caste / income level"],
        "documents": ["Birth Certificate", "Bank Account", "Aadhar Card"],
        "benefit": "Awareness + conditional cash transfers",
        "website": "wcd.nic.in"
    },
    "Free Bicycle Scheme": {
        "description": "State scheme providing free bicycles to students living more than 3 km from school.",
        "eligibility_rules": lambda d: (
            float(d.get("Distance_to_School_km", 0)) >= 3 and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"] and
            int(d.get("Standard", 0)) in [9, 10]
        ),
        "eligibility_display": ["Lives more than 3 km from school", "BPL or Low Income family", "Studying in Class 9 or 10"],
        "documents": ["Distance Proof", "Enrollment Certificate", "Aadhar Card"],
        "benefit": "Free bicycle (Rs.3,000-Rs.4,500 value)",
        "website": "State Education Portal"
    },
    "National Child Labour Project (NCLP)": {
        "description": "Rehabilitates children in labour through bridge education, nutrition support, and vocational training.",
        "eligibility_rules": lambda d: (
            d.get("Child_Labour") == "Yes" and
            int(d.get("Age", 20)) <= 14 and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Child is involved in labour", "Age 14 or below", "BPL or Low Income family"],
        "documents": ["Family Income Proof", "ID Proof", "School Certificate"],
        "benefit": "Rs.150/month + bridge education",
        "website": "labour.gov.in"
    },
    "EWS Central Scholarship": {
        "description": "Scholarship for EWS General category students in Class 11-12.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") == "EWS" and
            int(d.get("Standard", 0)) in [11, 12] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Caste Category: EWS (General)", "Studying in Class 11 or 12", "Family income <= Rs.4,50,000 per year"],
        "documents": ["EWS Certificate", "Class 10 Mark Sheet", "Aadhar Card"],
        "benefit": "Rs.10,000/year",
        "website": "scholarships.gov.in"
    },
    "Minority Pre-Matric Scholarship": {
        "description": "Financial scholarship for Minority community students in Class 9-10.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") == "Minority" and
            int(d.get("Standard", 0)) in [9, 10] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Caste Category: Minority", "Studying in Class 9 or 10", "Family income <= Rs.1,00,000 per year"],
        "documents": ["Minority Certificate", "Income Certificate", "Mark Sheet", "Aadhar Card"],
        "benefit": "Rs.5,000-Rs.6,000/year",
        "website": "scholarships.gov.in"
    },
    "Pudhumai Penn Scheme (TN)": {
        "description": "Tamil Nadu scheme providing monthly support to girl students in government schools.",
        "eligibility_rules": lambda d: (
            d.get("Gender") == "Female" and
            d.get("School_Type") == "Government" and
            int(d.get("Standard", 0)) in [9, 10, 11, 12]
        ),
        "eligibility_display": ["Gender: Female", "Studying in a Tamil Nadu Government school", "Studying in Class 9-12"],
        "documents": ["Enrollment Proof", "Bank Account", "Aadhar Card"],
        "benefit": "Rs.12,000/year (Rs.1,000/month)",
        "website": "TN Education Portal"
    },
    "State Social Welfare Scholarship": {
        "description": "State scheme for BPL single-parent families to reduce financial stress.",
        "eligibility_rules": lambda d: (
            d.get("Single_Parent_Family") == "Yes" and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Single Parent Family: Yes", "BPL or Low Income family"],
        "documents": ["Income Certificate", "Single Parent Proof", "Aadhar Card"],
        "benefit": "Rs.3,000-Rs.8,000/year",
        "website": "State Social Welfare Portal"
    },
    "Family Education Counselling (NIOS)": {
        "description": "Free bridge courses and counselling for students with sibling dropout history.",
        "eligibility_rules": lambda d: int(d.get("Siblings_Dropout_Count", 0)) >= 1,
        "eligibility_display": ["Has 1 or more siblings who dropped out"],
        "documents": ["Enrollment Proof", "Family Details"],
        "benefit": "Free bridge courses + counselling",
        "website": "nios.ac.in"
    },
    "Samagra Shiksha Remedial Support": {
        "description": "Remedial classes and teacher support for low-performing students.",
        "eligibility_rules": lambda d: (
            float(d.get("Previous_Year_Marks", 100)) < 50 or
            int(d.get("Failed_Subjects_Count", 0)) >= 2
        ),
        "eligibility_display": ["Previous Year Marks below 50%, OR Failed 2 or more subjects"],
        "documents": ["School Enrollment Proof"],
        "benefit": "Free remedial classes + teacher support",
        "website": "samagra.education.gov.in"
    },
    "General Counselling & RTE Support": {
        "description": "Universal support under the Right to Education Act for any at-risk student.",
        "eligibility_rules": lambda d: True,
        "eligibility_display": ["Any student needing support", "No income or caste restriction"],
        "documents": ["School Enrollment Proof"],
        "benefit": "Free; under Right to Education Act",
        "website": "rte.gov.in"
    },
}

# ─────────────────────────────────────────────
# TAMIL MESSAGE TEMPLATES
# ─────────────────────────────────────────────
def generate_tamil_message(data, risk):
    student_standard = data.get("Standard", "")
    attendance = data.get("Attendance_Percentage", "")
    marks = data.get("Previous_Year_Marks", "")
    gender = data.get("Gender", "Male")
    child_pronoun = "அவள்" if gender == "Female" else "அவன்"
    child_word = "மகளின்" if gender == "Female" else "மகனின்"

    if risk == "Moderate":
        message = (
            f"அன்பான பெற்றோருக்கு,\n\n"
            f"வணக்கம். உங்கள் {child_word} கல்வி நலனில் ஆர்வமுள்ள நாங்கள் உங்களுடன் சில முக்கியமான தகவல்களை பகிர்ந்துகொள்ள விரும்புகிறோம்.\n\n"
            f"உங்கள் பிள்ளை தற்போது {student_standard}-ஆம் வகுப்பில் படிக்கிறார். கடந்த சில வாரங்களாக {child_pronoun} பள்ளி வருகையில் சிறிது மாற்றம் காணப்படுகிறது. "
            f"வருகை சதவிகிதம் {attendance}% ஆகவும், கடந்த ஆண்டு மதிப்பெண் {marks} ஆகவும் உள்ளது.\n\n"
            f"உங்கள் பிள்ளை மிகவும் திறமையானவர். இந்த சிறிய இடைவெளியை சரி செய்தால், {child_pronoun} எதிர்காலம் இன்னும் பிரகாசமாக இருக்கும்.\n\n"
            f"தினமும் பள்ளிக்கு வருவதை உறுதி செய்யுங்கள். படிக்க வீட்டில் அமைதியான நேரம் ஒதுக்குங்கள். "
            f"ஏதாவது சிரமம் இருந்தால் ஆசிரியரிடம் நேரடியாக தெரிவியுங்கள்.\n\n"
            f"உங்கள் ஒத்துழைப்புக்கு நன்றி.\n\n"
            f"மரியாதையுடன்,\nபள்ளி நலன் குழு"
        )
    else:
        message = (
            f"அன்பான பெற்றோருக்கு,\n\n"
            f"வணக்கம். உங்கள் {child_word} நலனில் ஆழமான அக்கறையுடன் இந்த செய்தியை அனுப்புகிறோம்.\n\n"
            f"உங்கள் பிள்ளை {student_standard}-ஆம் வகுப்பில் படிக்கிறார். தற்போது {child_pronoun} பள்ளி வருகை {attendance}% மட்டுமே உள்ளது மற்றும் "
            f"கடந்த ஆண்டு மதிப்பெண் {marks} ஆக இருக்கிறது. இது {child_pronoun} கல்வி வாழ்க்கையில் தொடர்ந்தால் நீண்ட கால பாதிப்பை உண்டாக்கலாம்.\n\n"
            f"உடனடியாக பள்ளியை தொடர்பு கொண்டு ஆசிரியருடன் சந்திப்பு ஏற்பாடு செய்யுங்கள். "
            f"உங்கள் பிள்ளையிடம் அன்புடன் பேசி {child_pronoun} மனசுக்குள் என்ன நடக்கிறது என்று புரிந்துகொள்ளுங்கள். "
            f"பள்ளியில் கிடைக்கும் அரசு உதவித்தொகை திட்டங்களை பயன்படுத்திக்கொள்ளுங்கள். "
            f"{child_pronoun} தினமும் பள்ளிக்கு வருவதை நேரில் உறுதிப்படுத்துங்கள்.\n\n"
            f"நினைவில் வையுங்கள்: ஒரு குழந்தையின் எதிர்காலம் பெற்றோரின் ஒரு நிமிட கவனிப்பில் மாறலாம். நாங்கள் உங்களோடு இருக்கிறோம்.\n\n"
            f"மரியாதையுடன்,\nபள்ளி நலன் குழு"
        )
    return message



# ─────────────────────────────────────────────
# SEND EMAIL via Gmail SMTP
# ─────────────────────────────────────────────
def send_email_gmail(to_email, message, risk):
    """
    Sends Tamil parent message as email via Gmail SMTP.
    Completely free — unlimited emails.
    Returns (success: bool, response_message: str)
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    subject = (
        "⚠️ உங்கள் பிள்ளையின் கல்வி நலன் தொடர்பான முக்கிய தகவல்"
        if risk == "Moderate"
        else "🚨 உங்கள் பிள்ளைக்கு உடனடி கவனிப்பு தேவை — பள்ளி அறிவிப்பு"
    )

    # Build HTML email with Tamil content
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f9f9f9; padding:20px;">
        <div style="max-width:600px; margin:auto; background:white; border-radius:10px;
                    padding:30px; border-left: 6px solid {'#f0ad4e' if risk == 'Moderate' else '#d9534f'};">
            <h2 style="color:{'#e67e22' if risk == 'Moderate' else '#c0392b'};">
                {'⚠️ கவனிப்பு தேவை' if risk == 'Moderate' else '🚨 உடனடி கவனிப்பு தேவை'}
            </h2>
            <hr/>
            <div style="font-size:15px; line-height:2; color:#333; white-space:pre-wrap;">
{message}
            </div>
            <hr/>
            <p style="font-size:12px; color:#999;">
                இந்த செய்தி பள்ளி மாணவர் நலன் கணினி மூலம் அனுப்பப்பட்டது.
            </p>
        </div>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = GMAIL_SENDER
        msg["To"]      = to_email
        msg.attach(MIMEText(message, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_SENDER, to_email, msg.as_string())

        return True, f"Email sent to {to_email}"

    except smtplib.SMTPAuthenticationError:
        return False, "AUTH_FAILED"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        return False, f"ERROR: {str(e)}"

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_eligible_schemes(data):
    eligible = []
    for name, info in scheme_data.items():
        try:
            if info["eligibility_rules"](data):
                eligible.append(name)
        except Exception:
            pass
    return eligible

def get_top_factors(data, risk):
    scores = {}
    scores["Attendance_Percentage"] = (100 - float(data.get("Attendance_Percentage", 75))) / 100
    scores["Previous_Year_Marks"] = (100 - float(data.get("Previous_Year_Marks", 60))) / 100
    scores["Failed_Subjects_Count"] = min(int(data.get("Failed_Subjects_Count", 0)) / 5, 1.0)
    scores["Distance_to_School_km"] = min(float(data.get("Distance_to_School_km", 3)) / 20, 1.0)
    scores["Child_Labour"] = 1.0 if data.get("Child_Labour") == "Yes" else 0.0
    scores["Early_Marriage_Risk"] = 1.0 if data.get("Early_Marriage_Risk") == "Yes" else 0.0
    income_map = {"Below Poverty Line": 1.0, "Low Income": 0.7, "Middle Income": 0.3, "High Income": 0.0}
    scores["Family_Income_Level"] = income_map.get(data.get("Family_Income_Level", "Low Income"), 0.5)
    scores["Siblings_Dropout_Count"] = min(int(data.get("Siblings_Dropout_Count", 0)) / 3, 1.0)
    scores["Single_Parent_Family"] = 1.0 if data.get("Single_Parent_Family") == "Yes" else 0.0
    involvement_map = {"High": 0.0, "Moderate": 0.4, "Low": 0.8, "None": 1.0}
    scores["Parental_Involvement"] = involvement_map.get(data.get("Parental_Involvement", "Moderate"), 0.4)
    scores["Mental_Health_Concern"] = 1.0 if data.get("Mental_Health_Concern") == "Yes" else 0.0
    scores["Bullying_Experience"] = 1.0 if data.get("Bullying_Experience") == "Yes" else 0.0
    scores["Learning_Difficulty"] = 1.0 if data.get("Learning_Difficulty") == "Yes" else 0.0
    dom_map = {"High": 1.0, "Moderate": 0.5, "Low": 0.1, "None": 0.0}
    scores["Domestic_Responsibility"] = dom_map.get(data.get("Domestic_Responsibility", "Low"), 0.1)
    peer_map = {"Negative": 1.0, "Neutral": 0.3, "Positive": 0.0}
    scores["Peer_Influence"] = peer_map.get(data.get("Peer_Influence", "Neutral"), 0.3)
    esteem_map = {"Low": 1.0, "Moderate": 0.4, "High": 0.0}
    scores["Self_Esteem_Level"] = esteem_map.get(data.get("Self_Esteem_Level", "Moderate"), 0.4)
    return sorted(scores, key=scores.get, reverse=True)[:3]

# ═══════════════════════════════════════════════════════════════
# PAGE: MAIN
# ═══════════════════════════════════════════════════════════════
if st.session_state.page == "main":
    st.title("🎓 AI Student Dropout Early Warning System")
    st.markdown("Fill in the student details below and click **Predict Dropout Risk**.")

    st.header("👤 Student Demographics")
    c1, c2 = st.columns(2)
    with c1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        standard = st.selectbox("Standard (Class)", [9, 10, 11, 12])
        caste = st.selectbox("Caste Category", ["General", "SC", "ST", "OBC", "EWS", "Minority"])
    with c2:
        age = st.number_input("Age", min_value=10, max_value=20, value=14)
        income = st.selectbox("Family Income Level", ["Below Poverty Line", "Low Income", "Middle Income", "High Income"])

    st.header("🏠 Family Background")
    c1, c2 = st.columns(2)
    with c1:
        father_edu = st.selectbox("Father's Education", ["Illiterate", "Primary", "Secondary", "Higher Secondary", "Graduate", "Post Graduate"])
        mother_edu = st.selectbox("Mother's Education", ["Illiterate", "Primary", "Secondary", "Higher Secondary", "Graduate", "Post Graduate"])
        siblings = st.number_input("Number of Siblings", min_value=0, max_value=10, value=1)
        siblings_dropout = st.number_input("Siblings Dropout Count", min_value=0, max_value=10, value=0)
    with c2:
        siblings_reason = st.selectbox("Siblings Dropout Reason", ["N/A", "Financial", "Marriage", "Labour", "Distance", "Academic Failure", "Family Pressure"])
        siblings_edu = st.selectbox("Siblings Highest Education", ["N/A", "Primary", "Secondary", "Higher Secondary", "Graduate"])
        siblings_school = st.selectbox("Siblings Currently In School", ["Yes", "No", "N/A"])
        sibling_impact = st.slider("Sibling Dropout Impact Score (0-10)", 0, 10, 3)
    single_parent = st.selectbox("Single Parent Family", ["Yes", "No"])

    st.header("📚 Academic Performance")
    c1, c2 = st.columns(2)
    with c1:
        attendance = st.slider("Attendance Percentage", 0, 100, 70)
        marks = st.slider("Previous Year Marks", 0, 100, 55)
        failed_subj = st.number_input("Failed Subjects Count", min_value=0, max_value=10, value=0)
    with c2:
        homework = st.selectbox("Homework Completion", ["Always", "Often", "Sometimes", "Rarely", "Never"])
        grade_rep = st.selectbox("Grade Repetition History", ["Yes", "No"])
        learning_diff = st.selectbox("Learning Difficulty", ["Yes", "No"])

    st.header("🚌 School & Transport")
    c1, c2 = st.columns(2)
    with c1:
        distance = st.slider("Distance to School (km)", 0, 30, 5)
        transport = st.selectbox("Transport Available", ["Yes", "No"])
    with c2:
        school_type = st.selectbox("School Type", ["Government", "Private", "Aided"])
        mid_day = st.selectbox("Mid-Day Meal Beneficiary", ["Yes", "No"])
    scholarship = st.selectbox("Scholarship Received", ["Yes", "No"])

    st.header("🧠 Social & Psychological Factors")
    c1, c2 = st.columns(2)
    with c1:
        bullying = st.selectbox("Bullying Experience", ["Yes", "No"])
        teacher_rel = st.selectbox("Teacher-Student Relationship", ["Excellent", "Good", "Average", "Poor"])
        peer_inf = st.selectbox("Peer Influence", ["Positive", "Neutral", "Negative"])
        self_esteem = st.selectbox("Self Esteem Level", ["High", "Moderate", "Low"])
    with c2:
        mental_health = st.selectbox("Mental Health Concern", ["Yes", "No"])
        parental_inv = st.selectbox("Parental Involvement", ["High", "Moderate", "Low", "None"])
        child_labour = st.selectbox("Child Labour", ["Yes", "No"])
        early_marriage = st.selectbox("Early Marriage Risk", ["Yes", "No"])
    c1, c2 = st.columns(2)
    with c1:
        domestic = st.selectbox("Domestic Responsibility", ["None", "Low", "Moderate", "High"])
        smartphone = st.selectbox("Smartphone Access", ["Yes", "No"])
    with c2:
        internet = st.selectbox("Internet Access", ["Yes", "No"])

    st.markdown("---")
    if st.button("🔍 Predict Dropout Risk", use_container_width=True, type="primary"):
        st.session_state.show_schemes = False
        data = {
            "Gender": gender, "Caste_Category": caste, "Standard": standard,
            "Age": age, "Family_Income_Level": income,
            "Father_Education": father_edu, "Mother_Education": mother_edu,
            "No_of_Siblings": siblings, "Siblings_Dropout_Count": siblings_dropout,
            "Siblings_Dropout_Reason": siblings_reason, "Siblings_Highest_Education": siblings_edu,
            "Siblings_Currently_In_School": siblings_school, "Sibling_Dropout_Impact_Score": sibling_impact,
            "Single_Parent_Family": single_parent, "Attendance_Percentage": attendance,
            "Previous_Year_Marks": marks, "Failed_Subjects_Count": failed_subj,
            "Homework_Completion": homework, "Grade_Repetition_History": grade_rep,
            "Learning_Difficulty": learning_diff, "Distance_to_School_km": distance,
            "Transport_Available": transport, "School_Type": school_type,
            "Mid_Day_Meal_Beneficiary": mid_day, "Scholarship_Received": scholarship,
            "Bullying_Experience": bullying, "Teacher_Student_Relationship": teacher_rel,
            "Peer_Influence": peer_inf, "Self_Esteem_Level": self_esteem,
            "Mental_Health_Concern": mental_health, "Parental_Involvement": parental_inv,
            "Child_Labour": child_labour, "Early_Marriage_Risk": early_marriage,
            "Domestic_Responsibility": domestic, "Smartphone_Access": smartphone,
            "Internet_Access": internet,
        }
        try:
            response = requests.post("http://127.0.0.1:5000/predict", json=data, timeout=5)
            result = response.json()
        except Exception:
            score = 0
            if attendance < 60: score += 30
            elif attendance < 75: score += 15
            if marks < 40: score += 25
            elif marks < 55: score += 12
            if failed_subj >= 3: score += 20
            elif failed_subj >= 1: score += 10
            if child_labour == "Yes": score += 20
            if early_marriage == "Yes": score += 15
            if distance > 10: score += 10
            elif distance > 5: score += 5
            if income == "Below Poverty Line": score += 10
            if siblings_dropout >= 2: score += 10
            if mental_health == "Yes": score += 8
            if bullying == "Yes": score += 7
            risk_val = "High" if score >= 50 else ("Moderate" if score >= 25 else "Low")
            result = {
                "Risk_Level": risk_val,
                "Top_Influencing_Factors": get_top_factors(data, risk_val),
                "Recommended_Scheme": "General Counselling & RTE Support"
            }
        st.session_state.result = result
        st.session_state.student_data = data

    # ── RESULTS ──
    if st.session_state.result:
        result = st.session_state.result
        data = st.session_state.student_data
        risk = result.get("Risk_Level", "Low")

        st.markdown("---")
        st.subheader("📊 Prediction Result")

        if risk == "Low":
            st.success("### ✅ Risk Level: **LOW**\nThis student shows a low concern level. Continue monitoring academic progress.")
        elif risk == "Moderate":
            st.warning("### ⚠️ Risk Level: **MODERATE**\nThis student needs attention. Targeted support is recommended.")
        else:
            st.error("### 🚨 Risk Level: **HIGH**\nThis student needs immediate support and intervention.")

        st.subheader("🔍 Top 3 Influencing Factors")
        factors = result.get("Top_Influencing_Factors", get_top_factors(data, risk))[:3]
        for i, factor in enumerate(factors, 1):
            desc = factor_explanations.get(factor, {}).get(risk, "This factor influences the prediction.")
            label = factor.replace("_", " ")
            if risk == "Low":
                st.success(f"**{i}. {label}**\n\n{desc}")
            elif risk == "Moderate":
                st.warning(f"**{i}. {label}**\n\n{desc}")
            else:
                st.error(f"**{i}. {label}**\n\n{desc}")

        if risk != "Low":
            st.markdown("---")
            st.subheader("📋 Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📌 View Eligible Government Schemes", use_container_width=True):
                    st.session_state.show_schemes = True
            with col2:
                if st.button("✉️ Send Message to Parents (Tamil)", use_container_width=True):
                    st.session_state.page = "message"
                    st.rerun()

            if st.session_state.show_schemes:
                st.markdown("---")
                st.subheader("🏛️ Eligible Government Schemes")
                eligible_schemes = get_eligible_schemes(data)
                if eligible_schemes:
                    st.success(f"✅ This student is automatically eligible for **{len(eligible_schemes)} scheme(s)**.")
                    for scheme_name in eligible_schemes:
                        with st.expander(f"📋 {scheme_name}", expanded=False):
                            info = scheme_data[scheme_name]
                            st.markdown(f"**📖 Description:** {info['description']}")
                            st.markdown(f"**💰 Benefit:** {info['benefit']}")
                            st.markdown(f"**🌐 Apply at:** [{info['website']}](https://{info['website']})")
                            st.markdown("**✅ Eligibility Met:**")
                            for crit in info["eligibility_display"]:
                                st.markdown(f"  - ✅ {crit}")
                            st.markdown("**📋 Documents Required:**")
                            for doc in info["documents"]:
                                st.markdown(f"  - 📄 {doc}")
                            if st.button(f"View Full Details — {scheme_name}", key=f"btn_{scheme_name}"):
                                st.session_state.scheme = scheme_name
                                st.session_state.page = "scheme"
                                st.rerun()
                else:
                    st.info("No specific schemes matched. Showing universal support.")
                    if st.button("📌 View General RTE Support"):
                        st.session_state.scheme = "General Counselling & RTE Support"
                        st.session_state.page = "scheme"
                        st.rerun()

# ═══════════════════════════════════════════════════════════════
# PAGE: MESSAGE GENERATOR
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "message":
    data = st.session_state.student_data
    result = st.session_state.result
    risk = result.get("Risk_Level", "Moderate") if result else "Moderate"

    st.title("✉️ பெற்றோர் செய்தி உருவாக்கி")
    st.markdown("##### Parent Message Generator — Tamil")
    st.markdown("---")

    if risk == "Moderate":
        st.warning("⚠️ நிலை: கவனிப்பு தேவை")
    else:
        st.error("🚨 நிலை: உடனடி கவனிப்பு தேவை")

    st.subheader("📝 செய்தி வார்ப்புரு")
    st.caption("கீழே உள்ள செய்தியை தேவைப்பட்டால் திருத்தலாம்.")

    default_msg = generate_tamil_message(data, risk)
    message = st.text_area(
        "செய்தி:",
        value=default_msg,
        height=420,
        label_visibility="collapsed"
    )

    # Character count info
    char_count = len(message)
    sms_count = max(1, -(-char_count // 160))  # ceiling division
    st.caption(f"📊 Characters: {char_count} | Estimated SMS parts: {sms_count} (Unicode may use more credits)")

    st.markdown("---")
    st.subheader("📧 பெற்றோர் மின்னஞ்சல் முகவரி")
    st.caption("🆓 Gmail மூலம் இலவசமாக எத்தனை email வேண்டுமானாலும் அனுப்பலாம்.")

    parent_email = st.text_input(
        "பெற்றோரின் Email முகவரி உள்ளிடுக:",
        placeholder="உதாரணம்: parent@gmail.com",
    )

    email_valid = bool(
        parent_email and "@" in parent_email and "." in parent_email.split("@")[-1]
    )

    if parent_email and not email_valid:
        st.error("❌ சரியான email முகவரியை உள்ளிடுக.")

    st.markdown("---")
    st.subheader("⚙️ உங்கள் Gmail அமைப்பு")

    col1, col2 = st.columns(2)
    with col1:
        sender_email = st.text_input(
            "உங்கள் Gmail முகவரி:",
            value=GMAIL_SENDER,
            placeholder="yourschool@gmail.com"
        )
    with col2:
        app_password = st.text_input(
            "Gmail App Password (16 digits):",
            value=GMAIL_APP_PASS,
            type="password",
            placeholder="xxxx xxxx xxxx xxxx"
        )

    with st.expander("❓ App Password எப்படி பெறுவது?"):
        st.markdown("""
1. **myaccount.google.com** → Security
2. **2-Step Verification** இயக்கவும் (enable)
3. Security → **App Passwords** → Select app: Mail → Generate
4. 16-digit password கிடைக்கும் → அதை மேலே paste செய்யவும்
        """)

    st.markdown("")

    send_clicked = st.button(
        "📧 Email அனுப்பு",
        use_container_width=True,
        type="primary",
        disabled=not (email_valid and sender_email and app_password),
    )

    # ── Gmail send handler ──
    if send_clicked and email_valid:
        # Override globals with user-entered values
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        subject = (
            "⚠️ உங்கள் பிள்ளையின் கல்வி நலன் தொடர்பான முக்கிய தகவல்"
            if risk == "Moderate"
            else "🚨 உங்கள் பிள்ளைக்கு உடனடி கவனிப்பு தேவை — பள்ளி அறிவிப்பு"
        )

        with st.spinner("📧 Email அனுப்புகிறோம்..."):
            success, result_msg = send_email_gmail(
                to_email=parent_email,
                message=message,
                risk=risk,
            )

        if success:
            st.success(f"✅ Email வெற்றிகரமாக அனுப்பப்பட்டது! 📧 **{parent_email}** க்கு சென்றது.")
            st.balloons()
            with st.expander("📄 அனுப்பப்பட்ட செய்தி காண்க"):
                st.markdown(f"**📧 அனுப்பப்பட்டது:** {parent_email}")
                st.text(message)

        elif result_msg == "AUTH_FAILED":
            st.error("❌ Gmail login தவறானது!")
            st.markdown("""
**சரிசெய்ய:**
- Gmail முகவரி சரியாக உள்ளதா?
- **App Password** பயன்படுத்துகிறீர்களா? (உங்கள் Gmail password அல்ல!)
- myaccount.google.com → Security → App Passwords → புதிதாக generate செய்யவும்
            """)
        else:
            st.error(f"❌ பிழை ஏற்பட்டது: {result_msg}")

    st.markdown("---")
    if st.button("⬅️ முந்தைய பக்கம் / Back to Results"):
        st.session_state.page = "main"
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# PAGE: SCHEME DETAIL
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "scheme":
    scheme = st.session_state.scheme
    data = st.session_state.student_data

    st.title("📚 Government Scheme Details")

    if scheme in scheme_data:
        info = scheme_data[scheme]
        st.header(f"🏛️ {scheme}")
        st.subheader("📖 About This Scheme")
        st.write(info["description"])
        st.info(f"💰 **Benefit:** {info['benefit']}   |   🌐 **Website:** {info['website']}")

        st.subheader("✅ Eligibility Status")
        try:
            is_eligible = info["eligibility_rules"](data)
        except Exception:
            is_eligible = False

        if is_eligible:
            st.success("🎉 **This student IS ELIGIBLE for this scheme** based on the information provided!")
        else:
            st.error("❌ This student does not currently meet the eligibility criteria for this scheme.")

        st.markdown("**Eligibility Criteria:**")
        for crit in info["eligibility_display"]:
            st.markdown(f"  {'✅' if is_eligible else '⚪'} {crit}")

        st.subheader("📋 Document Checklist")
        for doc in info["documents"]:
            st.checkbox(f"📄 {doc}", key=f"doc_{doc}")

        st.markdown("---")
        st.markdown(f"🌐 **Apply online at:** [https://{info['website']}](https://{info['website']})")
    else:
        st.error("Scheme details not found.")

    if st.button("⬅️ Back to Prediction Results"):
        st.session_state.page = "main"
        st.rerun()
