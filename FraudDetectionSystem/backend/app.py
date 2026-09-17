from flask import Flask, request, jsonify
from flask_cors import CORS

from database import cursor
from routes.predict import predict_bp
from routes.transactions import transactions_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(predict_bp)
app.register_blueprint(transactions_bp)

@app.route("/")
def home():
    return {
        "message": "Fraud Detection API Running Successfully"
    }


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    cursor.execute(
        "SELECT name, role FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    if user:

        return jsonify({
            "success": True,
            "name": user[0],
            "role": user[1],
            "message": "Login Successful"
        })

    return jsonify({
        "success": False,
        "message": "Invalid Email or Password"
    }), 401


if __name__ == "__main__":
    app.run(debug=True, port=5000)