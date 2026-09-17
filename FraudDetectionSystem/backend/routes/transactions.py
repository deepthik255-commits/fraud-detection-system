from flask import Blueprint, jsonify
from database import cursor

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/transactions", methods=["GET"])
def get_transactions():

    cursor.execute("""
        SELECT
            id,
            amount,
            frequency,
            location,
            device,
            time,
            account_age,
            prediction,
            probability,
            status,
            created_at
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    transactions = []

    for row in rows:

        transactions.append({
            "id": row[0],
            "amount": row[1],
            "frequency": row[2],
            "location": row[3],
            "device": row[4],
            "time": row[5],
            "account_age": row[6],
            "prediction": row[7],
            "probability": row[8],
            "status": row[9],
            "created_at": row[10]
        })

    return jsonify(transactions)