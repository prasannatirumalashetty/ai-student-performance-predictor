import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="AI Student Performance Predictor",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SAMPLE DATA ----------------
data = {
    "Student": ["Rahul", "Priya", "Kiran", "Anu", "Ravi"],
    "Attendance": [90, 75, 95, 60, 85],
    "Study_Hours": [4, 2, 5, 1, 3],
    "Assignment_Score": [85, 65, 92, 50, 78],
    "Final_Marks": [88, 68, 95, 45, 80]
}

df = pd.DataFrame(data)

# ---------------- MODEL ----------------
X = df[["Attendance", "Study_Hours", "Assignment_Score"]]
y = df["Final_Marks"]

model = LinearRegression()
model.fit(X, y)

# ---------------- TITLE ----------------
st.title("🤖 AI Student Performance Predictor")
st.write("Predict and analyze student performance using Machine Learning.")

st.divider()

# ---------------- DASHBOARD ----------------
st.subheader("📊 Performance Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Students", len(df))

with col2:
    st.metric("📈 Average Marks", f"{df['Final_Marks'].mean():.1f}")

with col3:
    st.metric("🏆 Highest", f"{df['Final_Marks'].max():.0f}")

with col4:
    st.metric("📉 Lowest", f"{df['Final_Marks'].min():.0f}")

st.bar_chart(
    df.set_index("Student")["Final_Marks"]
)

st.divider()

# ---------------- PREDICTION ----------------
st.subheader("🔮 Predict Student Performance")

col1, col2 = st.columns(2)

with col1:
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

with col2:
    study_hours = st.number_input(
        "📚 Study Hours / Day",
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
        st.warning("⚠️ Please enter student name.")

    else:
        new_student = pd.DataFrame({
            "Attendance": [attendance],
            "Study_Hours": [study_hours],
            "Assignment_Score": [assignment_score]
        })

        prediction = model.predict(new_student)[0]
        prediction = max(0, min(100, prediction))

        # ---------------- GRADE ----------------
        if prediction >= 90:
            grade = "A+"
            performance = "🏆 Excellent"

        elif prediction >= 80:
            grade = "A"
            performance = "🟢 Very Good"

        elif prediction >= 70:
            grade = "B"
            performance = "🟢 Good"

        elif prediction >= 60:
            grade = "C"
            performance = "🟡 Average"

        elif prediction >= 50:
            grade = "D"
            performance = "🟠 Below Average"

        else:
            grade = "F"
            performance = "🔴 Needs Improvement"

        # ---------------- SMART RECOMMENDATION ----------------
        if attendance < 75:
            recommendation = (
                "Improve attendance. Regular class attendance "
                "can help improve overall performance."
            )

        elif study_hours < 3:
            recommendation = (
                "Increase daily study time to at least 3 hours "
                "and maintain a consistent study schedule."
            )

        elif assignment_score < 70:
            recommendation = (
                "Focus on assignments and try to score above 70 "
                "to improve your final performance."
            )

        else:
            recommendation = (
                "Great consistency! Continue maintaining your "
                "attendance, study hours and assignment performance."
            )

        # ---------------- RESULT ----------------
        st.divider()

        st.subheader(f"🎯 Result for {student_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Predicted Marks",
                f"{prediction:.2f}/100"
            )

        with col2:
            st.metric(
                "Grade",
                grade
            )

        with col3:
            st.metric(
                "Performance",
                performance
            )

        st.progress(int(prediction))

        st.info(f"💡 **AI Recommendation:** {recommendation}")

        # ---------------- REPORT ----------------
        report = pd.DataFrame({
            "Student Name": [student_name],
            "Attendance (%)": [attendance],
            "Study Hours / Day": [study_hours],
            "Assignment Score": [assignment_score],
            "Predicted Marks": [round(prediction, 2)],
            "Grade": [grade],
            "Performance": [performance],
            "Recommendation": [recommendation]
        })

        st.subheader("📋 Student Report")
        st.dataframe(report, use_container_width=True)

        # ---------------- DOWNLOAD ----------------
        csv = report.to_csv(index=False)

        st.download_button(
            "📥 Download Student Report",
            data=csv,
            file_name=f"{student_name}_performance_report.csv",
            mime="text/csv",
            use_container_width=True
        )

st.divider()

# ---------------- MODEL INFO ----------------
with st.expander("🧠 About this AI Model"):
    st.write(
        "This application uses Linear Regression from Scikit-learn "
        "to predict final student marks."
    )

    st.write(
        "The model uses Attendance, Study Hours and Assignment Score "
        "as input features."
    )

st.caption(
    "Built with Python • Pandas • Scikit-learn • Streamlit 🤖"
)          
