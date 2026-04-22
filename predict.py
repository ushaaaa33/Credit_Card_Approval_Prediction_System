import sys
import numpy as np
import joblib
from model import DecisionTreeClassifierCustom, Node

# Load the model
model = joblib.load("custom_decision_tree.pkl")
# Encodings from test.py
gender_enc = {"F": 0, "M": 1}
own_car_enc = {"N": 0, "Y": 1}
own_realty_enc = {"N": 0, "Y": 1}
income_type_enc = {"Commercial associate": 0, "Pensioner": 1, "State servant": 2, "Student": 3, "Working": 4}
education_type_enc = {"Academic degree": 0, "Higher education": 1, "Incomplete higher": 2, "Lower secondary": 3, "Secondary / secondary special": 4}
family_status_enc = {"Civil marriage": 0, "Married": 1, "Separated": 2, "Single / not married": 3, "Widow": 4}
housing_type_enc = {"Co-op apartment": 0, "House / apartment": 1, "Municipal apartment": 2, "Office apartment": 3, "Rented apartment": 4, "With parents": 5}
work_phone_enc = {"No": 0, "Yes": 1}
occupation_type_enc = {"Accountants": 0, "Cleaning staff": 1, "Cooking staff": 2, "Core staff": 3, "Drivers": 4, "HR staff": 5, "High skill tech staff": 6, "IT staff": 7, "Laborers": 8, "Low-skill Laborers": 9, "Managers": 10, "Medicine staff": 11, "Occupation Not Identified": 12, "Private service staff": 13, "Realty agents": 14, "Sales staff": 15, "Secretaries": 16, "Security staff": 17, "Waiters/barmen staff": 18}

if __name__ == "__main__":
    # Get arguments from PHP
    args = sys.argv[1:]
    if len(args) != 15:
        print("Error: Invalid number of arguments")
        sys.exit(1)

    try:
        gender = gender_enc[args[0]]
        own_car = own_car_enc[args[1]]
        own_realty = own_realty_enc[args[2]]
        children = int(args[3])
        total_income = float(args[4])
        income_type = income_type_enc[args[5]]
        education_type = education_type_enc[args[6]]
        family_status = family_status_enc[args[7]]
        housing_type = housing_type_enc[args[8]]
        age = int(args[9])
        experience = float(args[10])
        work_phone = work_phone_enc[args[11]]
        occupation_type = occupation_type_enc[args[12]]
        fam_members = int(args[13])
        # args[14] is user_id, not used in prediction

        # Prepare input array (same as in test.py)
        input_data = np.array([[0, 12345, gender, own_car, own_realty, children, total_income, income_type, education_type, family_status, housing_type, age, experience, work_phone, occupation_type, fam_members]])

        # Predict
        prediction = model.predict(input_data)[0]
        print(prediction)
    except Exception as e:
        print(f"Error: {str(e)}")
