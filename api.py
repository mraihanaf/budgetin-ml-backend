from flask import Flask, request, jsonify
import joblib
import traceback
import os
import numpy as np
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "model_rf.joblib"
SCALER_PATH = "scaler.joblib"
ENCODER_MIX_PATH = "credit_mix_encoder.joblib"
ENCODER_PAYMENT_PATH = "payment_encoder.joblib"
ENCODER_SCORE_PATH = "credit_score_encoder.joblib"
IMPUTER_PATH = "imputer.joblib"
LOG_TRANSFORMER_PATH = "log_transformer.joblib"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
ordinal_encoder_mix = joblib.load(ENCODER_MIX_PATH)
label_encoder_payment = joblib.load(ENCODER_PAYMENT_PATH)
label_encoder_score = joblib.load(ENCODER_SCORE_PATH)
imputation_mean = joblib.load(IMPUTER_PATH)
log_transformation = joblib.load(LOG_TRANSFORMER_PATH)

numeric_cols = [
    "Annual_Income", "Monthly_Inhand_Salary", "Num_Bank_Accounts", "Num_Credit_Card", "Interest_Rate", "Num_of_Loan", "Delay_from_due_date", "Num_of_Delayed_Payment",
    "Changed_Credit_Limit", "Num_Credit_Inquiries", "Outstanding_Debt", "Credit_Utilization_Ratio", "Total_EMI_per_month", "Amount_invested_monthly", "Monthly_Balance"
]
categoric_cols = ["Credit_Mix", "Payment_of_Min_Amount"]
log_transform_cols = ["Annual_Income", "Monthly_Inhand_Salary", "Outstanding_Debt", "Total_EMI_per_month", "Amount_invested_monthly", "Monthly_Balance"]

EXPECTED_KEYS = numeric_cols + categoric_cols

def preprocess_new_data(new_data):
    df = pd.DataFrame([new_data]) 
    df[numeric_cols] = imputation_mean.transform(df[numeric_cols])
    df[log_transform_cols] = log_transformation.transform(df[log_transform_cols])
    df["Credit_Mix"] = ordinal_encoder_mix.transform(df[["Credit_Mix"]])
    df["Payment_of_Min_Amount"] = label_encoder_payment.transform(df[["Payment_of_Min_Amount"]])
    df[numeric_cols] = scaler.transform(df[numeric_cols])
    df = df[model.feature_names_in_]
    return df

@app.route("/")
def index():
    return "Budgetin ML Service in Online!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        missing_keys = [key for key in EXPECTED_KEYS if key not in data]
        if missing_keys:
            return jsonify({"error": f"Missing keys: {missing_keys}"}), 400
        
        try:
            preprocessed_data = preprocess_new_data(data)
        except ValueError:
            return jsonify({"error": "Invalid input: Check feature values and types."}), 400

        prediction = model.predict(preprocessed_data)
        decoded_prediction = label_encoder_score.inverse_transform(prediction)
        return jsonify({"credit_score": decoded_prediction[0]})
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
