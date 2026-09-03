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
    st.write("Login to access the AI Student Performance Dashboard.")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("🚀 Login", use_container_width=True):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

    st.stop()

# ---------------- DATA ----------------
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

# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 AI Dashboard")
st.sidebar.success("🟢 Admin Logged In")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- TITLE ----------------
st.title("🤖 AI Student Performance Predictor")
st.write("Machine Learning Based Student Analytics Dashboard")

st.divider()

# ---------------- OVERVIEW ----------------
st.subheader("📊 Performance Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Students", len(df))

with col2:
    st.metric("📈 Avg Marks", f"{df['Final_Marks'].mean():.1f}")

with col3:
    st.metric("📅 Avg Attendance", f"{df['Attendance'].mean():.1f}%")

with col4:
    st.metric("📚 Avg Study Hours", f"{df['Study_Hours'].mean():.1f}")

# ---------------- ANALYTICS ----------------
st.divider()
st.subheader("📈 Performance Analytics")

tab1, tab2, tab3 = st.tabs([
    "📊 Marks",
    "📅 Attendance",
    "📚 Study Hours"
])

with tab1:
    st.bar_chart(
        df.set_index("Student")["Final_Marks"]
    )

with tab2:
    st.bar_chart(
        df.set_index("Student")["Attendance"]
    )

with tab3:
    st.bar_chart(
        df.set_index("Student")["Study_Hours"]
    )

# ---------------- TOP PERFORMER ----------------
st.divider()
st.subheader("🏆 Top Performer")

top_student = df.loc[df["Final_Marks"].idxmax()]

st.success(
    f"🏆 **{top_student['Student']}** is the top performer "
    f"with **{top_student['Final_Marks']} marks**."
)

# ---------------- PERFORMANCE GROUPS ----------------
st.subheader("🎯 Performance Analysis")

excellent = len(df[df["Final_Marks"] >= 85])
good = len(df[(df["Final_Marks"] >= 70) & (df["Final_Marks"] < 85)])
average = len(df[(df["Final_Marks"] >= 50) & (df["Final_Marks"] < 70)])
needs_improvement = len(df[df["Final_Marks"] < 50])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏆 Excellent", excellent)

with col2:
    st.metric("🟢 Good", good)

with col3:
    st.metric("🟡 Average", average)

with col4:
    st.metric("🔴 Needs Improvement", needs_improvement)

# ---------------- STUDENT TABLE ----------------
st.divider()
st.subheader("📋 Student Records")

st.dataframe(
    df,
    use_container_width=True
)

# ---------------- PREDICTION ----------------
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

        # Grade
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

        # Smart recommendation
        recommendations = []

        if attendance < 75:
            recommendations.append(
                "Improve attendance."
            )

        if study_hours < 3:
            recommendations.append(
                "Increase daily study time."
            )

        if assignment_score < 70:
            recommendations.append(
                "Improve assignment scores."
            )

        if not recommendations:
            recommendations.append(
                "Excellent consistency. Keep it up!"
            )

        recommendation = " ".join(recommendations)

        # Result
        st.divider()
        st.subheader(f"🎯 Result for {student_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Predicted Marks",
                f"{prediction:.2f}/100"
            )

        with col2:
            st.metric("Grade", grade)

        with col3:
            st.metric("Performance", performance)

        st.progress(int(prediction))

        st.info(
            f"💡 **AI Recommendation:** {recommendation}"
        )

        # Report
        report = pd.DataFrame({
            "Student Name": [student_name],
            "Attendance (%)": [attendance],
            "Study Hours": [study_hours],
            "Assignment Score": [assignment_score],
            "Predicted Marks": [round(prediction, 2)],
            "Grade": [grade],
            "Performance": [performance],
            "Recommendation": [recommendation]
        })

        st.subheader("📄 Student Report")
        st.dataframe(report, use_container_width=True)

        csv = report.to_csv(index=False)

        st.download_button(
            "📥 Download Student Report",
            data=csv,
            file_name=f"{student_name}_report.csv",
            mime="text/csv",
            use_container_width=True
        )

# ---------------- MODEL INFO ----------------
st.divider()

with st.expander("🧠 About AI Model"):
    st.write(
        "The application uses Linear Regression from "
        "Scikit-learn."
    )

    st.write(
        "Features used: Attendance, Study Hours and "
        "Assignment Score."
    )

st.caption(
    "Built with Python • Pandas • Scikit-learn • Streamlit 🤖"
)
                    
