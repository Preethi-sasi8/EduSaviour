# ═══════════════════════════════════════════════════════════════
# data.py — Scheme Database & Factor Explanations
# ═══════════════════════════════════════════════════════════════

FACTOR_EXPLANATIONS = {
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

SCHEME_DATA = {
    "PM POSHAN (Mid-Day Meal)": {
        "description": "Provides free nutritious meals daily to students in government and aided schools to improve attendance, nutrition, and reduce dropout caused by hunger and financial burden.",
        "eligibility_rules": lambda d: d.get("School_Type") == "Government",
        "eligibility_display": ["Student studies in a Government school", "Student is enrolled (automatic benefit)"],
        "documents": ["School Enrollment Proof", "Aadhar Card"],
        "benefit": "Free meals daily",
        "website": "https://pmposhan.education.gov.in"
    },
    "Pre-Matric Scholarship SC/ST": {
        "description": "Financial scholarship for SC/ST students in Class 9-10 to reduce dropout due to economic burden.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") in ["SC", "ST"] and
            int(d.get("Standard", 0)) in [9, 10] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["SC or ST caste category", "Class 9 or 10", "Family income ≤ ₹2,50,000/year"],
        "documents": ["Caste Certificate", "Income Certificate", "Mark Sheet", "Aadhar Card", "Bank Passbook"],
        "benefit": "₹3,500–₹7,000/year",
        "website": "https://scholarships.gov.in"
    },
    "Post-Matric Scholarship SC/ST": {
        "description": "Supports SC/ST students in Class 11-12 to prevent dropout at the higher secondary transition stage.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") in ["SC", "ST"] and
            int(d.get("Standard", 0)) in [11, 12] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["SC or ST caste category", "Class 11 or 12", "Family income ≤ ₹2,50,000/year"],
        "documents": ["Caste Certificate", "Income Certificate", "Mark Sheet", "Aadhar Card"],
        "benefit": "₹6,000–₹12,000/year",
        "website": "https://scholarships.gov.in"
    },
    "OBC Pre-Matric Scholarship": {
        "description": "Financial assistance for OBC students in Class 9-10 facing financial hardship.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") == "OBC" and
            int(d.get("Standard", 0)) in [9, 10] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["OBC caste category", "Class 9 or 10", "Family income ≤ ₹1,00,000/year"],
        "documents": ["OBC Certificate", "Income Certificate", "Aadhar Card", "Mark Sheet"],
        "benefit": "₹2,500–₹4,500/year",
        "website": "https://scholarships.gov.in"
    },
    "NMMS Scholarship": {
        "description": "National Means-cum-Merit Scholarship for meritorious students from low-income families in government schools.",
        "eligibility_rules": lambda d: (
            int(d.get("Standard", 0)) in [9, 10, 11, 12] and
            d.get("School_Type") == "Government" and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line", "Middle Income"]
        ),
        "eligibility_display": ["Government school", "Class 9–12", "Family income ≤ ₹3,50,000/year"],
        "documents": ["Class 8 Mark Sheet", "Income Certificate", "Aadhar Card"],
        "benefit": "₹12,000/year (₹1,000/month)",
        "website": "https://scholarships.gov.in"
    },
    "KGBV Residential School": {
        "description": "Free residential schooling for SC/ST/OBC/Minority girls in Classes 9-12.",
        "eligibility_rules": lambda d: (
            d.get("Gender") == "Female" and
            d.get("Caste_Category") in ["SC", "ST", "OBC", "Minority"] and
            int(d.get("Standard", 0)) in [9, 10, 11, 12]
        ),
        "eligibility_display": ["Female", "SC / ST / OBC / Minority", "Class 9–12"],
        "documents": ["Caste Certificate", "Income Proof", "Transfer Certificate", "Aadhar Card"],
        "benefit": "Free boarding + tuition + uniform + books",
        "website": "https://samagra.education.gov.in"
    },
    "Beti Bachao Beti Padhao": {
        "description": "National campaign providing awareness and cash incentives to prevent gender discrimination and early marriage.",
        "eligibility_rules": lambda d: d.get("Gender") == "Female",
        "eligibility_display": ["Female", "Any caste / income level"],
        "documents": ["Birth Certificate", "Bank Account", "Aadhar Card"],
        "benefit": "Awareness + conditional cash transfers",
        "website": "https://wcd.nic.in"
    },
    "Free Bicycle Scheme": {
        "description": "State scheme providing free bicycles to students living more than 3 km from school.",
        "eligibility_rules": lambda d: (
            float(d.get("Distance_to_School_km", 0)) >= 3 and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"] and
            int(d.get("Standard", 0)) in [9, 10]
        ),
        "eligibility_display": ["Lives > 3 km from school", "BPL or Low Income", "Class 9 or 10"],
        "documents": ["Distance Proof", "Enrollment Certificate", "Aadhar Card"],
        "benefit": "Free bicycle (₹3,000–₹4,500 value)",
        "website": "https://www.tn.gov.in"
    },
    "National Child Labour Project (NCLP)": {
        "description": "Rehabilitates children in labour through bridge education, nutrition support, and vocational training.",
        "eligibility_rules": lambda d: (
            d.get("Child_Labour") == "Yes" and
            int(d.get("Age", 20)) <= 14 and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Involved in child labour", "Age ≤ 14", "BPL or Low Income"],
        "documents": ["Family Income Proof", "ID Proof", "School Certificate"],
        "benefit": "₹150/month + bridge education",
        "website": "https://labour.gov.in"
    },
    "EWS Central Scholarship": {
        "description": "Scholarship for EWS General category students in Class 11-12.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") == "EWS" and
            int(d.get("Standard", 0)) in [11, 12] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["EWS (General) category", "Class 11 or 12", "Family income ≤ ₹4,50,000/year"],
        "documents": ["EWS Certificate", "Class 10 Mark Sheet", "Aadhar Card"],
        "benefit": "₹10,000/year",
        "website": "https://scholarships.gov.in"
    },
    "Minority Pre-Matric Scholarship": {
        "description": "Financial scholarship for Minority community students in Class 9-10.",
        "eligibility_rules": lambda d: (
            d.get("Caste_Category") == "Minority" and
            int(d.get("Standard", 0)) in [9, 10] and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Minority community", "Class 9 or 10", "Family income ≤ ₹1,00,000/year"],
        "documents": ["Minority Certificate", "Income Certificate", "Mark Sheet", "Aadhar Card"],
        "benefit": "₹5,000–₹6,000/year",
        "website": "https://scholarships.gov.in"
    },
    "Pudhumai Penn Scheme (TN)": {
        "description": "Tamil Nadu scheme providing monthly support to girl students in government schools.",
        "eligibility_rules": lambda d: (
            d.get("Gender") == "Female" and
            d.get("School_Type") == "Government" and
            int(d.get("Standard", 0)) in [9, 10, 11, 12]
        ),
        "eligibility_display": ["Female", "Tamil Nadu Government school", "Class 9–12"],
        "documents": ["Enrollment Proof", "Bank Account", "Aadhar Card"],
        "benefit": "₹12,000/year (₹1,000/month)",
        "website": "https://www.tn.gov.in"
    },
    "State Social Welfare Scholarship": {
        "description": "State scheme for BPL single-parent families to reduce financial stress.",
        "eligibility_rules": lambda d: (
            d.get("Single_Parent_Family") == "Yes" and
            d.get("Family_Income_Level") in ["Low Income", "Below Poverty Line"]
        ),
        "eligibility_display": ["Single Parent Family", "BPL or Low Income"],
        "documents": ["Income Certificate", "Single Parent Proof", "Aadhar Card"],
        "benefit": "₹3,000–₹8,000/year",
        "website": "https://www.tn.gov.in"
    },
    "Family Education Counselling (NIOS)": {
        "description": "Free bridge courses and counselling for students with sibling dropout history.",
        "eligibility_rules": lambda d: int(d.get("Siblings_Dropout_Count", 0)) >= 1,
        "eligibility_display": ["1 or more siblings who dropped out"],
        "documents": ["Enrollment Proof", "Family Details"],
        "benefit": "Free bridge courses + counselling",
        "website": "https://nios.ac.in"
    },
    "Samagra Shiksha Remedial Support": {
        "description": "Remedial classes and teacher support for low-performing students.",
        "eligibility_rules": lambda d: (
            float(d.get("Previous_Year_Marks", 100)) < 50 or
            int(d.get("Failed_Subjects_Count", 0)) >= 2
        ),
        "eligibility_display": ["Previous Year Marks < 50%, OR Failed ≥ 2 subjects"],
        "documents": ["School Enrollment Proof"],
        "benefit": "Free remedial classes + teacher support",
        "website": "https://samagra.education.gov.in"
    },
    "General Counselling & RTE Support": {
        "description": "Universal support under the Right to Education Act for any at-risk student.",
        "eligibility_rules": lambda d: True,
        "eligibility_display": ["Any student needing support", "No income or caste restriction"],
        "documents": ["School Enrollment Proof"],
        "benefit": "Free — under Right to Education Act",
        "website": "https://rte.gov.in"
    },
}