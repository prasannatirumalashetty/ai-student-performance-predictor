import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

data = {
    "Attendance": [90, 75, 95, 60, 85],
    "Study_Hours": [4, 2, 5, 1, 3],
    "Assignment_Score": [85, 65, 92, 50, 78],
    "Final_Marks": [88, 68, 95, 45, 80]
}

df = pd.DataFrame(data)

X = df[["Attendance", "Study_Hours", "Assignment_Score"]]
y = df["Final_Marks"]

model = LinearRegression()
model.fit(X, y)

st.title("🤖 AI Student Performance Predictor")
st.write("Enter student details to predict final marks.")

attendance = st.number_input("Attendance (%)", 0, 100, 75)
study_hours = st.number_input("Study Hours per Day", 0.0, 24.0, 3.0)
assignment_score = st.number_input("Assignment Score", 0, 100, 70)

if st.button("Predict Marks 🚀"):
    new_student = pd.DataFrame({
        "Attendance": [attendance],
        "Study_Hours": [study_hours],
        "Assignment_Score": [assignment_score]
    })

    prediction = model.predict(new_student)

    st.success(f"Predicted Final Marks: {prediction[0]:.2f}")
