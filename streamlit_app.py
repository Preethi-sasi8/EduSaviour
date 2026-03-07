import streamlit as st
import requests

st.title("AI Student Dropout Early Warning System")

st.header("Enter Student Information")

gender = st.selectbox("Gender",["Male","Female"])

caste = st.selectbox("Caste Category",["General","OBC","SC","ST"])

standard = st.selectbox("Standard",[6,7,8,9,10])

age = st.slider("Age",10,18)

income = st.selectbox("Family Income Level",
["Low","Medium","High"])

father_edu = st.selectbox("Father Education",
["None","Primary","Secondary","Graduate"])

mother_edu = st.selectbox("Mother Education",
["None","Primary","Secondary","Graduate"])

siblings = st.number_input("Number of Siblings",0,10)

attendance = st.slider("Attendance Percentage",0,100,70)

marks = st.slider("Previous Year Marks",0,100,60)

failed = st.number_input("Failed Subjects Count",0,10)

distance = st.slider("Distance to School (km)",0,20,5)

internet = st.selectbox("Internet Access",["Yes","No"])

smartphone = st.selectbox("Smartphone Access",["Yes","No"])

if st.button("Predict Risk"):


   data = {
    "Gender": gender,
    "Caste_Category": caste,
    "Standard": standard,
    "Age": age,
    "Family_Income_Level": income,
    "Father_Education": father_edu,
    "Mother_Education": mother_edu,
    "No_of_Siblings": siblings,
    "Attendance_Percentage": attendance,
    "Previous_Year_Marks": marks,
    "Failed_Subjects_Count": failed,
    "Distance_to_School_km": distance,
    "Internet_Access": internet,
    "Smartphone_Access": smartphone
     }

   response = requests.post(
    "http://127.0.0.1:5000/predict",
    json=data
    )

   result = response.json()

   st.subheader("Prediction Result")

   st.write("Risk Level:", result["Risk_Level"])

   if result["Risk_Level"] != "Low":
       st.write("Recommended Scheme:",
             result["Recommended_Scheme"])

       st.write("Top Influencing Factors")

   for factor in result["Top_Influencing_Factors"]:
         st.write("-",factor)

