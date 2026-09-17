from flask import Blueprint, request, jsonify
from database import connection, cursor
import pandas as pd
import joblib

predict_bp = Blueprint("predict", __name__)

# Load model
model = joblib.load("bank_model.pkl")

# Load encoders
location_encoder = joblib.load("location_encoder.pkl")
device_encoder = joblib.load("device_encoder.pkl")
time_encoder = joblib.load("time_encoder.pkl")


@predict_bp.route("/predict", methods=["POST"])
def predict():

    data = request.json

    amount = float(data["amount"])
    frequency = int(data["frequency"])
    location = location_encoder.transform([data["location"]])[0]
    device = device_encoder.transform([data["device"]])[0]
    time = time_encoder.transform([data["time"]])[0]
    account_age = int(data["account_age"])

    df = pd.DataFrame([{
        "Amount": amount,
        "Frequency": frequency,
        "Location": location,
        "Device": device,
        "Time": time,
        "AccountAge": account_age
    }])

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    # Status
    status = "Fraud" if prediction == 1 else "Safe"

    # Save transaction
    cursor.execute("""
        INSERT INTO transactions(
            amount,
            frequency,
            location,
            device,
            time,
            account_age,
            prediction,
            probability,
            status
        )
        VALUES (?,?,?,?,?,?,?,?,?)
    """,
    (
        amount,
        frequency,
        data["location"],
        data["device"],
        data["time"],
        account_age,
        int(prediction),
        float(probability) * 100,
        status
    ))

    connection.commit()

    return jsonify({
        "prediction": int(prediction),
        "probability": round(float(probability) * 100, 2),
        "status": status
    })