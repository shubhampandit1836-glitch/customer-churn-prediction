import streamlit as st
import joblib
import pandas as pd

# Page config
st.set_page_config(page_title="Churn Prediction", layout="wide")

# Load model
model = joblib.load("churn_model.pkl")
scaler = joblib.load("scaler.pkl")

# Title
st.markdown("<h1 style='text-align: center;'>📊 Customer Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown("### Predict whether a customer will churn or stay")

# Layout (2 columns)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Customer Info")
    tenure = st.slider("Tenure (months)", 1, 72, 24)
    monthly = st.number_input("Monthly Charges", value=70.0)
    total = st.number_input("Total Charges", value=1500.0)

    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    st.subheader("📌 Services & Plan")
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])
    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])

    Contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], index=2)
    PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
    PaymentMethod = st.selectbox("Payment Method", ["Credit card", "Electronic check", "Mailed check"])

# Predict button
st.markdown("---")
if st.button("🚀 Predict Churn"):

    columns = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
               'gender_Male', 'Partner_Yes', 'Dependents_Yes', 'PhoneService_Yes',
               'MultipleLines_No phone service', 'MultipleLines_Yes',
               'InternetService_Fiber optic', 'InternetService_No',
               'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
               'OnlineBackup_No internet service', 'OnlineBackup_Yes',
               'DeviceProtection_No internet service', 'DeviceProtection_Yes',
               'TechSupport_No internet service', 'TechSupport_Yes',
               'StreamingTV_No internet service', 'StreamingTV_Yes',
               'StreamingMovies_No internet service', 'StreamingMovies_Yes',
               'Contract_One year', 'Contract_Two year',
               'PaperlessBilling_Yes',
               'PaymentMethod_Credit card (automatic)',
               'PaymentMethod_Electronic check',
               'PaymentMethod_Mailed check']

    df = pd.DataFrame([[0]*len(columns)], columns=columns)

    # Fill values
    df['tenure'] = tenure
    df['MonthlyCharges'] = monthly
    df['TotalCharges'] = total
    df['SeniorCitizen'] = SeniorCitizen

    if gender == "Male": df['gender_Male'] = 1
    if Partner == "Yes": df['Partner_Yes'] = 1
    if Dependents == "Yes": df['Dependents_Yes'] = 1
    if PhoneService == "Yes": df['PhoneService_Yes'] = 1

    if Contract == "One year": df['Contract_One year'] = 1
    elif Contract == "Two year": df['Contract_Two year'] = 1

    if PaperlessBilling == "Yes": df['PaperlessBilling_Yes'] = 1

    if PaymentMethod == "Credit card":
        df['PaymentMethod_Credit card (automatic)'] = 1
    elif PaymentMethod == "Electronic check":
        df['PaymentMethod_Electronic check'] = 1
    elif PaymentMethod == "Mailed check":
        df['PaymentMethod_Mailed check'] = 1

    # Scale
    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    df[numeric_cols] = scaler.transform(df[numeric_cols])

    # Prediction
    probability = model.predict_proba(df)[0][1]
    prediction = 1 if probability > 0.4 else 0

    # Output UI
    st.markdown("## 🔍 Prediction Result")

    st.metric("Churn Probability", f"{probability:.2f}")

    # Risk level
    if probability < 0.3:
        st.success("🟢 Low Risk Customer")
    elif probability < 0.6:
        st.warning("🟡 Medium Risk Customer")
    else:
        st.error("🔴 High Risk Customer")

    # Final decision
    if prediction == 1:
        st.error("⚠ Customer likely to churn")
        st.info("💡 Suggestion: Offer discount or long-term plan")
    else:
        st.success("✅ Customer likely to stay")
        st.info("💡 Suggestion: Upsell premium services")

st.markdown("### 📊 Key Insight")

if st.button("🟢 Load Low Risk Customer"):
    st.session_state.tenure = 48
    st.session_state.monthly = 60

if st.button("🔴 Load High Risk Customer"):
    st.session_state.tenure = 2
    st.session_state.monthly = 100

    if probability > 0.6:
    st.write("Customer is high risk due to:")
    if Contract == "Month-to-month":
        st.write("- Short-term contract")
    if MonthlyCharges > 80:
        st.write("- High monthly charges")
    if Partner == "No":
        st.write("- No partner support")
else:
    st.write("Customer is stable due to:")
    if tenure > 24:
        st.write("- Long tenure")
    if Contract != "Month-to-month":
        st.write("- Long-term contract")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Shubham")
