# Driver Sentiment Analytics Dashboard

A full-stack machine learning web application that collects driver feedback, performs automated sentiment analysis, and provides an interactive admin dashboard with rankings, performance trends, and real-time alerts.

---

## Project Overview

This system enables:

- Users to submit feedback for drivers  
- Automatic sentiment classification using machine learning  
- Real-time performance analytics  
- Driver ranking leaderboard  
- Low-performance alert monitoring  
- Admin-based driver management  
- Secure session-based authentication  

---

## Technology Stack

### Frontend

- React (Vite)  
- Axios  
- Recharts (Data Visualization)  
- CSS Animations  

### Backend

- Flask  
- MySQL  
- Flask-CORS  
- bcrypt (Password Hashing)  
- Joblib  

### Machine Learning

- Scikit-learn  
- TF-IDF Vectorizer  
- Logistic Regression Classifier  

---

## Features

### Public User Features

- Submit feedback for any driver  
- Automatic sentiment scoring (1–5 scale)  
- Automatic redirection after submission  

### Admin Features

- Secure login system  
- Add new drivers (duplicate prevention enabled)  
- Delete drivers  
- View performance trends (line graph)  
- View average score and total feedback count  
- Driver ranking leaderboard  
- Medal indicators for top 3 drivers  
- Real-time low performance alerts (polling-based)  
- Logout functionality  

---

## Sentiment Scoring Logic

| Sentiment | Score |
|-----------|--------|
| Positive  | 5      |
| Neutral   | 3      |
| Negative  | 1      |

Driver average score is recalculated dynamically after every feedback submission.

Low-score alert condition: average_score < 2.5

## Project Structure


driver-sentiment/
│
├── backend/
│ ├── app.py
│ ├── sentiment_model.pkl
│ ├── vectorizer.pkl
│
├── frontend/
│ ├── src/
│ │ ├── pages/
│ │ │ ├── AdminDashboard.jsx
│ │ │ ├── AdminLogin.jsx
│ │ │ ├── FeedbackPage.jsx
│ │ ├── components/
│ │ │ ├── FeedbackForm.jsx
│ │ ├── App.jsx
│ │ ├── main.jsx
│ │ ├── index.css
│
└── README.md


---

## Installation Guide

### 1. Clone the Repository

```
git clone <repository-url>
cd driver-sentiment
```

2. Backend Setup
```
cd backend
python -m venv myvenv
myvenv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```
Backend runs at:
```
http://127.0.0.1:5000
```
3. Frontend Setup
```
cd frontend
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

Database Requirements
drivers table
```
CREATE TABLE drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    total_feedbacks INT DEFAULT 0,
    cumulative_score INT DEFAULT 0,
    average_score FLOAT DEFAULT 0
);
```
feedback table
```
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT,
    feedback_text TEXT,
    sentiment_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES drivers(id)
);
```
admins table
```
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);
```

Note: Admin passwords must be stored as bcrypt-hashed values.

System Architecture

User submits feedback

Backend processes text using TF-IDF + Logistic Regression

Sentiment score (1, 3, or 5) is generated

Feedback is stored in MySQL

Driver statistics are updated

Admin dashboard fetches updated ranking, trends, and alerts
