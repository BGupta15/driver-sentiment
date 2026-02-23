from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
import joblib
import bcrypt
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"

CORS(app, supports_credentials=True)

# ML model
model = joblib.load("sentiment_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# MySQL connection (auto reconnect safe)
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yoshibinda",
        database="driver_sentiment",
        port=3305
    )

def predict_sentiment(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]

    if prediction == "positive":
        return 5
    elif prediction == "neutral":
        return 3
    else:
        return 1


@app.route("/")
def home():
    return "Backend running"

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route("/low-score-alerts")
def low_score_alerts():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, average_score
        FROM drivers
        WHERE average_score < 2.5
    """)

    return jsonify(cursor.fetchall())

@app.route("/public-drivers")
def public_drivers():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM drivers")
    return jsonify(cursor.fetchall())

@app.route("/admin-login", methods=["POST"])
def admin_login():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    data = request.json
    username = data["username"]
    password = data["password"]

    cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
    admin = cursor.fetchone()

    if admin and bcrypt.checkpw(password.encode(), admin["password"].encode()):
        session["admin_logged_in"] = True
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid credentials"}), 401


# ---------------- DRIVERS ---------------- #

@app.route("/drivers")
def get_drivers():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM drivers")
    return jsonify(cursor.fetchall())


@app.route("/add-driver", methods=["POST"])
def add_driver():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    db = get_db()
    cursor = db.cursor(dictionary=True)

    name = request.json["name"]

    # Check duplicate
    cursor.execute("SELECT * FROM drivers WHERE name=%s", (name,))
    existing = cursor.fetchone()

    if existing:
        return jsonify({"error": "Driver already exists"}), 400

    cursor.execute("""
        INSERT INTO drivers (name, total_feedbacks, cumulative_score, average_score)
        VALUES (%s, 0, 0, 0)
    """, (name,))

    db.commit()
    return jsonify({"message": "Driver added"})

@app.route("/driver-summary/<int:driver_id>")
def driver_summary(driver_id):
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT average_score, total_feedbacks
        FROM drivers
        WHERE id=%s
    """, (driver_id,))

    result = cursor.fetchone()
    return jsonify(result)

@app.route("/delete-driver/<int:driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM feedback WHERE driver_id=%s", (driver_id,))
    cursor.execute("DELETE FROM drivers WHERE id=%s", (driver_id,))

    db.commit()

    return jsonify({"message": "Driver deleted"})

@app.route("/driver-ranking")
def driver_ranking():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, average_score, total_feedbacks
        FROM drivers
        ORDER BY average_score DESC
    """)

    return jsonify(cursor.fetchall())

@app.route("/driver-history/<int:driver_id>")
def driver_history(driver_id):
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as created_at,
               sentiment_score
        FROM feedback
        WHERE driver_id=%s
        ORDER BY created_at
    """, (driver_id,))

    return jsonify(cursor.fetchall())



@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    data = request.json
    driver_id = data["driver_id"]
    text = data["text"]

    score = predict_sentiment(text)

    # Insert feedback
    cursor.execute("""
        INSERT INTO feedback (driver_id, feedback_text, sentiment_score)
        VALUES (%s, %s, %s)
    """, (driver_id, text, score))

    # Get driver current stats safely
    cursor.execute("""
        SELECT total_feedbacks, cumulative_score
        FROM drivers
        WHERE id=%s
    """, (driver_id,))

    driver = cursor.fetchone()

    current_total = driver["total_feedbacks"] or 0
    current_cumulative = driver["cumulative_score"] or 0

    new_total = current_total + 1
    new_cumulative = current_cumulative + score
    new_avg = new_cumulative / new_total

    # Update driver stats
    cursor.execute("""
        UPDATE drivers
        SET total_feedbacks=%s,
            cumulative_score=%s,
            average_score=%s
        WHERE id=%s
    """, (new_total, new_cumulative, new_avg, driver_id))

    db.commit()

    return jsonify({"message": "Feedback processed"})


if __name__ == "__main__":
    app.run(debug=True)