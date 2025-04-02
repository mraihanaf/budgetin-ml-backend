# Budgetin Machine Learning
| This repo contains Machine Learning Model Development and Backend Implementation for [Budgetin](https://github.com/mraihanaf/capstone-fintech-budgeting-app) App.

# Usage
## Run locally with docker
You can run this service locally with docker
```bash
docker run -p 5000:5000 mraihanaf/budgetin-ml-backend
```
# Backend Development

## Dev shell using nix
You can enter dev shell using this command.
```
nix develop
```

# API Endpoints
## /predict

### Method: POST

**Description:** This endpoint receives a JSON payload with user data, processes the data using various machine learning preprocessing steps, and returns a predicted credit score.

### Request

Content-Type: application/json

Body: The JSON object should contain the following fields:
```
{
  "Annual_Income": 50000,
  "Monthly_Inhand_Salary": 4000,
  "Num_Bank_Accounts": 3,
  "Num_Credit_Card": 2,
  "Interest_Rate": 5.2,
  "Num_of_Loan": 1,
  "Delay_from_due_date": 2,
  "Num_of_Delayed_Payment": 1,
  "Changed_Credit_Limit": 500,
  "Num_Credit_Inquiries": 2,
  "Outstanding_Debt": 10000,
  "Credit_Utilization_Ratio": 30.5,
  "Total_EMI_per_month": 500,
  "Amount_invested_monthly": 200,
  "Monthly_Balance": 1000,
  "Credit_Mix": "Good",
  "Payment_of_Min_Amount": "Yes"
}
```

### Response

The response will be a JSON object containing the predicted credit score:
```
{
  "credit_score": "Good"
}
```
### Example cURL Request

To test the API with dummy data:
```bash
curl -X POST "http://localhost:5000/predict" \
     -H "Content-Type: application/json" \
     -d '{
        "Annual_Income": 50000,
        "Monthly_Inhand_Salary": 4000,
        "Num_Bank_Accounts": 3,
        "Num_Credit_Card": 2,
        "Interest_Rate": 5.2,
        "Num_of_Loan": 1,
        "Delay_from_due_date": 2,
        "Num_of_Delayed_Payment": 1,
        "Changed_Credit_Limit": 500,
        "Num_Credit_Inquiries": 2,
        "Outstanding_Debt": 10000,
        "Credit_Utilization_Ratio": 30.5,
        "Total_EMI_per_month": 500,
        "Amount_invested_monthly": 200,
        "Monthly_Balance": 1000,
        "Credit_Mix": "Good",
        "Payment_of_Min_Amount": "Yes"
     }'
```

### Error Handling
- 400 Bad Request: If the required fields are missing or the input data is malformed.
- 500 Internal Server Error: If the model fails to process the data.



