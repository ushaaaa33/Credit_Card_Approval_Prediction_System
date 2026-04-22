import numpy as np
import pandas as pd
import joblib
import streamlit as st
from model import DecisionTreeClassifierCustom, Node

# Load trained model
def credit_card_prediction(input_data):
    model = joblib.load("custom_decision_tree.pkl")
    return model.predict(input_data)[0]

st.title("💳 Credit Card Approval Prediction")
# Input fields based on dataset features
gender = st.selectbox("Gender", ["F", "M"])
own_car = st.selectbox("Own Car", ["N", "Y"])
own_realty = st.selectbox("Own Realty", ["N", "Y"])
children = st.number_input("Number of Children", min_value=0, max_value=20, value=0)
total_income = st.number_input("Total Income", min_value=0.0, value=100000.0)
income_type = st.selectbox("Income Type", ["Working", "Commercial associate", "Pensioner", "State servant", "Student"])
education_type = st.selectbox("Education Type", ["Secondary / secondary special", "Higher education", "Incomplete higher", "Lower secondary", "Academic degree"])
family_status = st.selectbox("Family Status", ["Married", "Single / not married", "Civil marriage", "Separated", "Widow"])
housing_type = st.selectbox("Housing Type", ["House / apartment", "Rented apartment", "With parents", "Municipal apartment", "Office apartment", "Co-op apartment"])
age = st.number_input("Age", min_value=18, max_value=100, value=30)
experience = st.number_input("Years of Experience", min_value=0.0, max_value=50.0, value=5.0)
work_phone = st.selectbox("Work Phone", ["No", "Yes"])
occupation_type = st.selectbox("Occupation Type", ["Laborers", "Core staff", "Accountants", "Managers", "Drivers", "Sales staff", "Cleaning staff", "Cooking staff", "Private service staff", "Medicine staff", "Security staff", "High skill tech staff", "Waiters/barmen staff", "Low-skill Laborers", "Realty agents", "Secretaries", "IT staff", "HR staff", "Occupation Not Identified"])
fam_members = st.number_input("Family Members", min_value=1, max_value=20, value=2)

# Encoding mappings based on the notebook
gender_enc = {"F": 0, "M": 1}
own_car_enc = {"N": 0, "Y": 1}
own_realty_enc = {"N": 0, "Y": 1}
income_type_enc = {"Commercial associate": 0, "Pensioner": 1, "State servant": 2, "Student": 3, "Working": 4}
education_type_enc = {"Academic degree": 0, "Higher education": 1, "Incomplete higher": 2, "Lower secondary": 3, "Secondary / secondary special": 4}
family_status_enc = {"Civil marriage": 0, "Married": 1, "Separated": 2, "Single / not married": 3, "Widow": 4}
housing_type_enc = {"Co-op apartment": 0, "House / apartment": 1, "Municipal apartment": 2, "Office apartment": 3, "Rented apartment": 4, "With parents": 5}
work_phone_enc = {"No": 0, "Yes": 1}
occupation_type_enc = {"Accountants": 0, "Cleaning staff": 1, "Cooking staff": 2, "Core staff": 3, "Drivers": 4, "HR staff": 5, "High skill tech staff": 6, "IT staff": 7, "Laborers": 8, "Low-skill Laborers": 9, "Managers": 10, "Medicine staff": 11, "Occupation Not Identified": 12, "Private service staff": 13, "Realty agents": 14, "Sales staff": 15, "Secretaries": 16, "Security staff": 17, "Waiters/barmen staff": 18}

if st.button("Predict"):
    input_data = np.array([[
        0,  # index
        12345,  # ID (dummy)
        gender_enc[gender],
        own_car_enc[own_car],
        own_realty_enc[own_realty],
        children,
        total_income,
        income_type_enc[income_type],
        education_type_enc[education_type],
        family_status_enc[family_status],
        housing_type_enc[housing_type],
        age,
        experience,
        work_phone_enc[work_phone],
        occupation_type_enc[occupation_type],
        fam_members
    ]])
    prediction = credit_card_prediction(input_data)

    if prediction == 1:
        st.success("✅ Congratulations! Your credit card application is APPROVED.")
        st.balloons()
    else:
        st.warning("❌ Sorry, your credit card application was REJECTED.")
 