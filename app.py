import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Page settings
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

# ---------------- TITLE ----------------
st.title("🤖 AI Student Performance Predictor")
st.write(
    "An AI-powered dashboard to predict and analyze student performance."
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Options")

uploaded_file = st.sidebar.file_uploader(
    "📁 Upload Student CSV",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        uploaded_df = pd.read_csv(uploaded_file)

        required_columns = [
            "Attendance",
            "Study_Hours",
            "Assignment_Score"
        ]

        if all(column in uploaded_df.columns for column in required_columns):
            df = uploaded_df
            st.sidebar.success("CSV uploaded successfully!")
        else:
            st.sidebar.error(
                "CSV must contain Attendance, Study_Hours and Assignment_Score."
            )

    except Exception:
        st.sidebar.error("Unable to read CSV file.")

# ---------------- MODEL ----------------
X = df[["Attendance", "Study_Hours", "Assignment_Score"]]

if "Final_Marks" in df.columns:
    y = df["Final_Marks"]

    model = LinearRegression()
    model.fit(X, y)

    model_ready = True
else:
    model_ready = False

# ---------------- DASHBOARD ----------------
st.subheader("📊 Student Performance Dashboard")

if "Final_Marks" in df.columns:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Students", len(df))

    with col2:
        st.metric("📈 Average Marks", f"{df['Final_Marks'].mean():.1f}")

    with col3:
        st.metric("🏆 Highest Marks", f"{df['Final_Marks'].max():.1f}")

    with col4:
        st.metric("📉 Lowest Marks", f"{df['Final_Marks'].min():.1f}")

    st.divider()

    # Charts
    st.subheader("📈 Marks Analysis")

    chart_data = df.set_index("Student")["Final_Marks"]

    st.bar_chart(chart_data)

    st.subheader("📋 Student Data")

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- PREDICT ----------------
st.divider()

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

if st.button(
    "🚀 Predict Final Marks",
    use_container_width=True
):

    if not student_name.strip():
        st.warning("⚠️ Please enter student name.")

    elif not model_ready:
        st.error(
            "❌ Prediction requires a CSV with Final_Marks column."
        )

    else:

        new_student = pd.DataFrame({
            "Attendance": [attendance],
            "Study_Hours": [study_hours],
            "Assignment_Score": [assignment_score]
        })

        prediction = model.predict(new_student)[0]

        prediction = max(0, min(100, prediction))

        st.divider()

        st.subheader(f"🎯 Result for {student_name}")

        st.metric(
            "Predicted Final Marks",
            f"{prediction:.2f} / 100"
        )

        st.progress(int(prediction))

        if prediction >= 85:
            st.success(
                "🏆 Excellent Performance! Keep it up!"
            )

        elif prediction >= 70:
            st.success(
                "🟢 Good Performance! A little more effort can make it excellent."
            )

        elif prediction >= 50:
            st.warning(
                "🟡 Average Performance. Focus more on study hours and assignments."
            )

        else:
            st.error(
                "🔴 Needs Improvement. Increase attendance and study time."
            )

        st.info(
            "💡 Recommendation: Maintain good attendance, "
            "increase study consistency and complete assignments regularly."
        )

# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "Built with Python • Pandas • Scikit-learn • Streamlit 🤖"
)
