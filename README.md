# EduSaviour — AI-Powered Student Dropout Prevention System

EduSaviour is an intelligent web application that predicts student dropout risk using Machine Learning and provides actionable interventions — including government scheme recommendations, parent messaging, and counsellor assignment — to help schools save at-risk students before it's too late.

---

## 📌 Problem Statement
Student dropout is a serious issue across India, especially in government and rural schools. Teachers often lack the tools to identify which students are silently slipping away. EduSaviour bridges that gap — giving teachers, counsellors, and administrators a **data-driven early warning system** with built-in intervention tools.

---

## 👤 Workflow
1. **Login** (Administrator / Counsellor / Teacher)  
2. **Teacher enters student details** (Name, Age, Gender, Class, Attendance, Grades, Behaviour, Family Income, Caste)  
3. **Random Forest Model predicts dropout risk**  
🟢 LOW RISK 🟡 MODERATE RISK 🔴 HIGH RISK
→ Scheme Recommendations → Scheme Recommendations
→ Parent Message → Parent Message (Email/WhatsApp)
→ 30-Day Counselling Assignment

4. **Student Comparison View** – Risk student vs average vs safe student  
5. **District-wise Dropout Heatmap** – Visual hotspot map across districts/schools  
6. **Counsellor Dashboard** – View assigned students → Submit feedback → Track outcomes

---

## 🌟 Key Features
| Feature | Description |
|---------|-------------|
| 🔐 Role-based Login | Separate access for Admin, Teacher, Counsellor |
| 🤖 Risk Prediction | Low / Moderate / High dropout risk via Random Forest |
| 🔍 Factor Explanation | Top 3 influencing factors shown per prediction |
| 🏛️ Scheme Recommender | Eligible government schemes auto-matched to student profile |
| 💬 Message Generator | Personalised parent messages in Tamil |
| 📧 Direct Delivery | One-click Email & WhatsApp message sending |
| 🩺 Counselling Planner | 30-day counselling assignment with session scheduling |
| 📊 Comparison Charts | Risk student vs average vs safe student visualisation |
| 🗺️ District Heatmap | Geographic dropout hotspot map |
| 📝 Feedback Tracker | Counsellors submit feedback and track student outcomes |

---

## 🛠 Tech Stack
- Python (Flask)
- streamlit for frontend
- Random Forest ML model for prediction
- Parent Messaging: Automated personalized messages sent via SMTP

---

## ⚡ Installation & Usage
1. Clone this repo:  
```bash
git clone <your_repo_link>
