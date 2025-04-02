from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained components
model = joblib.load("model_rf.joblib")
scaler = joblib.load("scaler.joblib")
ordinal_encoder_mix = joblib.load("credit_mix_encoder.joblib")
label_encoder_payment = joblib.load("payment_encoder.joblib")
label_encoder_score = joblib.load("credit_score_encoder.joblib")
imputation_mean = joblib.load("imputer.joblib")
log_transformation = joblib.load("log_transformer.joblib")

def preprocess_data(new_data):
    """Preprocess input JSON data without using Pandas."""
    # Convert input JSON dictionary to NumPy array
    raw_values = np.array([list(new_data.values())], dtype=np.float64)

    # Handle missing values (imputation)
    processed_values = imputation_mean.transform(raw_values)

    # Apply log transformation if needed
    processed_values = log_transformation.transform(processed_values)

    # Encode categorical features (assuming indexes 2, 3, and 4 are categorical)
    processed_values[:, 2] = ordinal_encoder_mix.transform(processed_values[:, 2].reshape(-1, 1)).flatten()
    processed_values[:, 3] = label_encoder_payment.transform(processed_values[:, 3].reshape(-1, 1)).flatten()
    processed_values[:, 4] = label_encoder_score.transform(processed_values[:, 4].reshape(-1, 1)).flatten()

    # Scale numerical features
    processed_values = scaler.transform(processed_values)

    return processed_values

@app.route("/")
def index():
    return "Machine Learning Backend"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        # Preprocess input data
        processed_data = preprocess_data(data)

        # Make prediction
        prediction = model.predict(processed_data)
        
        return jsonify({"prediction": int(prediction[0])})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
