import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="AI Student Performance Predictor",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Admin Login")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("🚀 Login", use_container_width=True):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 AI Dashboard")
st.sidebar.success("🟢 Admin Logged In")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- SAMPLE DATA ----------------
data = {
    "Student": ["Rahul", "Priya", "Kiran", "Anu", "Ravi"],
    "Attendance": [90, 75, 95, 60, 85],
    "Study_Hours": [4, 2, 5, 1, 3],
    "Assignment_Score": [85, 65, 92, 50, 78],
    "Final_Marks": [88, 68, 95, 45, 80]
}

df = pd.DataFrame(data)

# ---------------- CSV UPLOAD ----------------
st.sidebar.subheader("📁 Student Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    required = [
        "Student",
        "Attendance",
        "Study_Hours",
        "Assignment_Score",
        "Final_Marks"
    ]

    if all(col in uploaded_df.columns for col in required):
        df = uploaded_df
        st.sidebar.success("✅ CSV loaded successfully!")
    else:
        st.sidebar.error(
            "CSV must contain: Student, Attendance, "
            "Study_Hours, Assignment_Score, Final_Marks"
        )

# ---------------- MODEL ----------------
X = df[
    ["Attendance", "Study_Hours", "Assignment_Score"]
]

y = df["Final_Marks"]

model = LinearRegression()
model.fit(X, y)

# ---------------- TITLE ----------------
st.title("🤖 AI Student Performance Predictor")
st.write(
    "Multiple Student AI Performance Analysis Dashboard"
)

st.divider()

# ---------------- DASHBOARD ----------------
st.subheader("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Students", len(df))

with col2:
    st.metric(
        "📈 Average Marks",
        f"{df['Final_Marks'].mean():.1f}"
    )

with col3:
    st.metric(
        "🏆 Highest",
        f"{df['Final_Marks'].max():.0f}"
    )

with col4:
    st.metric(
        "📉 Lowest",
        f"{df['Final_Marks'].min():.0f}"
    )

# ---------------- CHART ----------------
st.subheader("📈 Student Marks")

st.bar_chart(
    df.set_index("Student")["Final_Marks"]
)

# ---------------- AUTOMATIC PREDICTION ----------------
st.divider()

st.subheader("🤖 Automatic AI Predictions")

prediction_input = df[
    ["Attendance", "Study_Hours", "Assignment_Score"]
]

predictions = model.predict(prediction_input)

predictions = [
    max(0, min(100, value))
    for value in predictions
]

result_df = df.copy()

result_df["Predicted_Marks"] = [
    round(value, 2)
    for value in predictions
]

# ---------------- GRADES ----------------
def get_grade(mark):

    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"


def get_performance(mark):

    if mark >= 85:
        return "🏆 Excellent"
    elif mark >= 70:
        return "🟢 Good"
    elif mark >= 50:
        return "🟡 Average"
    else:
        return "🔴 Needs Improvement"


result_df["Grade"] = result_df["Predicted_Marks"].apply(
    get_grade
)

result_df["Performance"] = result_df[
    "Predicted_Marks"
].apply(get_performance)

# ---------------- DISPLAY RESULTS ----------------
st.dataframe(
    result_df,
    use_container_width=True
)

# ---------------- AT RISK STUDENTS ----------------
st.subheader("⚠️ Students Needing Attention")

at_risk = result_df[
    result_df["Predicted_Marks"] < 50
]

if len(at_risk) > 0:

    st.warning(
        f"{len(at_risk)} student(s) may need additional support."
    )

    st.dataframe(
        at_risk[
            [
                "Student",
                "Attendance",
                "Study_Hours",
                "Assignment_Score",
                "Predicted_Marks",
                "Grade"
            ]
        ],
        use_container_width=True
    )

else:

    st.success(
        "✅ No students are currently in the high-risk category."
    )

# ---------------- DOWNLOAD ----------------
st.divider()

csv = result_df.to_csv(index=False)

st.download_button(
    "📥 Download All Prediction Results",
    data=csv,
    file_name="student_prediction_results.csv",
    mime="text/csv",
    use_container_width=True
)

# ---------------- SINGLE STUDENT PREDICTION ----------------
st.divider()

st.subheader("🔮 Predict New Student")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "👤 Student Name",
        placeholder="Enter name"
    )

    attendance = st.number_input(
        "📅 Attendance (%)",
        0,
        100,
        75
    )

with col2:

    study_hours = st.number_input(
        "📚 Study Hours / Day",
        0.0,
        24.0,
        3.0,
        step=0.5
    )

    assignment_score = st.number_input(
        "📝 Assignment Score",
        0,
        100,
        70
    )

if st.button(
    "🚀 Predict New Student",
    use_container_width=True
):

    if not name.strip():

        st.warning("⚠️ Enter student name.")

    else:

        new_data = pd.DataFrame({
            "Attendance": [attendance],
            "Study_Hours": [study_hours],
            "Assignment_Score": [assignment_score]
        })

        prediction = model.predict(new_data)[0]

        prediction = max(
            0,
            min(100, prediction)
        )

        grade = get_grade(prediction)
        performance = get_performance(prediction)

        st.subheader(
            f"🎯 Result — {name}"
        )

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

# ---------------- MODEL INFO ----------------
st.divider()

with st.expander("🧠 About AI Model"):

    st.write(
        "The application uses Linear Regression "
        "from Scikit-learn."
    )

    st.write(
        "Features: Attendance, Study Hours and "
        "Assignment Score."
    )

st.caption(
    "Built with Python • Pandas • Scikit-learn • Streamlit 🤖"
)
