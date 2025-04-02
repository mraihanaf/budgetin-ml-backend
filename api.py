from flask import Flask, request, jsonify
import joblib
from sklearn.preprocessing import FunctionTransformer
import pandas as pd
import os

app =  Flask(__name__)

model = joblib.load("model_rf.joblib")
scaler = joblib.load('scaler.joblib')
ordinal_encoder_mix = joblib.load('credit_mix_encoder.joblib')
label_encoder_payment = joblib.load('payment_encoder.joblib')
label_encoder_score = joblib.load('credit_score_encoder.joblib')
imputation_mean = joblib.load('imputer.joblib')
log_transformation = joblib.load('log_transformer.joblib')

def preprocess_data(new_data):


@app.route("/")
def index():
    return "Machine Learning Backend"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    result = collection.insert_one(data)
    return jsonify({"message": "Data stored successfully", "id": str(result.inserted_id)}), 201