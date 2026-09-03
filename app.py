        import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="AI Student Performance Predictor",
    page_icon="🤖"
)

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

st.write(
    "Predict a student's final marks using "
    "attendance, study hours, and assignment score."
)

st.divider()

student_name = st.text_input(
    "👤 Student Name",
    placeholder="Enter student name"
)

attendance = st.number_input(
    "📅 Attendance (%)",
    min_value=0,
    max_value=100,
    value=75
)

study_hours = st.number_input(
    "📚 Study Hours per Day",
    min_value=0.0,
    max_value=24.0,
    value=3.0,
    step=0.5
)

assignment_score = st.number_input(
    "📝 Assignment Score",
    min_value=0,
    max_value=100,
    value=70
)

if st.button("🚀 Predict Final Marks", use_container_width=True):

    if not student_name.strip():
        st.warning("Please enter the student's name.")

    else:
        new_student = pd.DataFrame({
            "Attendance": [attendance],
            "Study_Hours": [study_hours],
            "Assignment_Score": [assignment_score]
        })

        prediction = model.predict(new_student)[0]
        prediction = max(0, min(100, prediction))

        st.divider()

        st.subheader(f"📊 Result for {student_name}")

        st.metric(
            "Predicted Final Marks",
            f"{prediction:.2f} / 100"
        )

        if prediction >= 85:
            category = "🏆 Excellent"
            advice = "Keep maintaining the same consistency."

        elif prediction >= 70:
            category = "🟢 Good"
            advice = "A little more consistency can improve the marks."

        elif prediction >= 50:
            category = "🟡 Average"
            advice = "Focus more on study hours and assignments."

        else:
            category = "🔴 Needs Improvement"
            advice = "Increase study time, attendance and assignment performance."

        st.success(f"Performance: {category}")
        st.info(f"💡 Recommendation: {advice}")
