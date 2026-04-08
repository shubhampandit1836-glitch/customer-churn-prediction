import streamlit as st
import requests

st.title("📊 Customer Churn Prediction App")

# Inputs
tenure = st.slider("Tenure", 1, 72, value=24)
monthly = st.number_input("Monthly Charges", value=70.0)
total = st.number_input("Total Charges", value=1500.0)

SeniorCitizen = st.selectbox("Senior Citizen", [0, 1], index=0)
gender = st.selectbox("Gender", ["Male", "Female"], index=0)
Partner = st.selectbox("Partner", ["Yes", "No"], index=0)
Dependents = st.selectbox("Dependents", ["Yes", "No"], index=1)
PhoneService = st.selectbox("Phone Service", ["Yes", "No"], index=0)

Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"], index=2)

PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"], index=0)

PaymentMethod = st.selectbox(
    "Payment Method",
    ["Credit card", "Electronic check", "Mailed check"],
    index=0
)

if st.button("Predict"):

    data = {
        "tenure": tenure,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
        "SeniorCitizen": SeniorCitizen,
        "gender": gender,
        "Partner": Partner,
        "Dependents": Dependents,
        "PhoneService": PhoneService,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)
    result = response.json()

    if "error" in result:
        st.error(result["error"])
    else:
        st.write(f"Churn Probability: {result['churn_probability']:.2f}")

        if result['churn_prediction'] == 1:
            st.error("⚠ Customer likely to churn")
        else:
            st.success("✅ Customer likely to stay")