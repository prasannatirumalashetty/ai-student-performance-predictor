
# 🤖 AI Student Performance Predictor

An AI-powered web application that predicts student final marks based on attendance, study hours, and assignment scores using Machine Learning.

## 📌 Project Overview

The AI Student Performance Predictor is designed to analyze student academic information and predict their expected final marks.

The application uses Machine Learning to provide:
- Predicted final marks
- Performance category
- Grade
- Student analytics
- At-risk student identification
- Downloadable prediction reports

## ✨ Features

- 🔐 Admin Login
- 📊 Student Performance Dashboard
- 🤖 Machine Learning based prediction
- 👥 Multiple student analysis
- 📁 CSV file upload
- 📈 Performance analytics
- 🏆 Grade calculation
- ⚠️ Students needing attention
- 💡 Smart recommendations
- 📥 Download prediction results

## 🧠 Machine Learning

The project uses **Linear Regression** from Scikit-learn.

### Input Features

- Attendance (%)
- Study Hours per Day
- Assignment Score

### Output

- Predicted Final Marks

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Streamlit
- GitHub

## ⚙️ How It Works

1. Admin logs into the application.
2. Student academic information is provided.
3. The Machine Learning model processes the input data.
4. The model predicts the student's final marks.
5. The application assigns a grade and performance category.
6. The system provides recommendations.
7. Results can be downloaded as a CSV report.

## 📂 Project Structure

```text
AI-Student-Performance-Predictor/
│
├── app.py
├── requirements.txt
└── README.md
