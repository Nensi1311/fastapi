import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Prediction")

st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=0, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0)
height = st.number_input("Height (cm)", min_value=0.0, value=170.0)
income = st.number_input("Income (LPA)", min_value=0.0, value=5.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox("Occupation", options=['Teacher', 'Clerk', 'Lawyer', 'Engineer', 'Doctor', 'Manager'])


if st.button("Predict Premium Category"):
    user_data = {
        "Age": age,
        "Weight": weight,
        "Height": height,
        "Income_LPA": income,
        "Smoker": smoker,
        "City": city,
        "Occupation": occupation
    }
    
    try:
        response = requests.post(API_URL, json=user_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Premium Category: **{result['predicted_category']}**")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Please ensure the FastAPI server is running on port 8000.")