from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("churn_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.get("/")
def home():
    return {"message": "Churn Prediction API Running"}

@app.post("/predict")
def predict(data: dict):
    try:
        # Step 1: Create full feature template (all columns = 0)
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

        # Step 2: Fill numeric values
        df['tenure'] = data['tenure']
        df['MonthlyCharges'] = data['MonthlyCharges']
        df['TotalCharges'] = data['TotalCharges']
        df['SeniorCitizen'] = data['SeniorCitizen']

        # Step 3: Handle categorical (ONE HOT)
        if data['gender'] == "Male":
            df['gender_Male'] = 1

        if data['Partner'] == "Yes":
            df['Partner_Yes'] = 1

        if data['Dependents'] == "Yes":
            df['Dependents_Yes'] = 1

        if data['PhoneService'] == "Yes":
            df['PhoneService_Yes'] = 1

        if data['Contract'] == "One year":
            df['Contract_One year'] = 1
        elif data['Contract'] == "Two year":
            df['Contract_Two year'] = 1

        if data['PaperlessBilling'] == "Yes":
            df['PaperlessBilling_Yes'] = 1

        # Payment Method
        if data['PaymentMethod'] == "Credit card":
            df['PaymentMethod_Credit card (automatic)'] = 1
        elif data['PaymentMethod'] == "Electronic check":
            df['PaymentMethod_Electronic check'] = 1
        elif data['PaymentMethod'] == "Mailed check":
            df['PaymentMethod_Mailed check'] = 1

        # Step 4: Scale numeric
        numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
        df[numeric_cols] = scaler.transform(df[numeric_cols])

        # Step 5: Predict
        probability = model.predict_proba(df)[0][1]

        # Apply custom threshold
        threshold = 0.4
        prediction = 1 if probability > threshold else 0

        return {
            "churn_prediction": int(prediction),
            "churn_probability": float(probability)
        }

    except Exception as e:
        return {"error": str(e)}
