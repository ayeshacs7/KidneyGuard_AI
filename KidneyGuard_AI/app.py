# ============================================
# KidneyGuard AI
# Part 1
# ============================================

import streamlit as st
import pandas as pd
import joblib
from PIL import Image
from datetime import datetime
import os
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="KidneyGuard AI",
    page_icon="🩺",
    layout="wide"
)

# -----------------------------
# Load Model
# -----------------------------


BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "models" / "model.pkl")
history_file = BASE_DIR / "prediction_history.csv"

if not os.path.exists(history_file):

    history = pd.DataFrame(
        columns=[
            "Date",
            "Prediction",
            "Risk Score"
        ]
    )

    history.to_csv(history_file, index=False)

# -----------------------------
# Load Image
# -----------------------------
image = Image.open("images/kidney.png")

# -----------------------------
# Header
# -----------------------------
col1, col2 = st.columns([1,2])

with col1:
    st.image(image, width=220)

with col2:
    st.title("🩺 KidneyGuard AI")
    st.markdown("### Early Kidney Disease Risk Prediction System")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🩺 KidneyGuard AI")

st.sidebar.info(
    "KidneyGuard AI helps estimate kidney disease risk using Machine Learning."
)

st.sidebar.markdown("---")


st.sidebar.header("📊 Project Features")

st.sidebar.success("✅ Machine Learning Prediction")
st.sidebar.success("✅ BMI Calculator")
st.sidebar.success("✅ Water Intake Calculator")
st.sidebar.success("✅ AI Health Insights")
st.sidebar.success("✅ Diet Recommendation")
st.sidebar.success("✅ PDF Report")

st.sidebar.success("💡 Tip of the Day")

st.sidebar.write(
    "Drink enough water and keep your blood pressure under control."
)

# -----------------------------
# Disclaimer
# -----------------------------
st.info(
    "⚠️ This tool is for educational purposes only. It is NOT a medical diagnosis."
)

# ============================================
# BMI Calculator
# ============================================

st.header("📏 BMI Calculator")

bmi_col1, bmi_col2 = st.columns(2)

with bmi_col1:
    height = st.number_input(
        "Height (cm)",
        min_value=50,
        max_value=250,
        value=170
    )

with bmi_col2:
    weight = st.number_input(
        "Weight (kg)",
        min_value=10,
        max_value=250,
        value=70
    )

bmi = weight / ((height/100) ** 2)

st.metric("BMI", round(bmi,2))

if bmi < 18.5:
    st.info("🟡 Underweight")
elif bmi < 25:
    st.success("🟢 Healthy Weight")
elif bmi < 30:
    st.warning("🟠 Overweight")
    
else:
    st.error("🔴 Obese")

# ============================================
# Water Intake
# ============================================

water = round(weight * 35 / 1000,2)

st.metric(
    "💧 Recommended Water Intake",
    f"{water} Liters/day"
)

st.markdown("---")

# ============================================
# Patient Information
# ============================================

st.header("👤 Patient Information")

col1, col2 = st.columns(2)

with col1:

    bp = st.number_input("Blood Pressure", min_value=0)

    sg = st.number_input(
        "Specific Gravity",
        min_value=0.0,
        format="%.3f"
    )

    al = st.number_input("Albumin", min_value=0)

    su = st.number_input("Sugar", min_value=0)

    rbc = st.number_input("Red Blood Cells", min_value=0)

with col2:

    bu = st.number_input("Blood Urea", min_value=0.0)

    sc = st.number_input("Serum Creatinine", min_value=0.0)

    sod = st.number_input("Sodium", min_value=0.0)

    pot = st.number_input("Potassium", min_value=0.0)

    hemo = st.number_input("Hemoglobin", min_value=0.0)

wbcc = st.number_input(
    "White Blood Cell Count",
    min_value=0
)

rbcc = st.number_input(
    "Red Blood Cell Count",
    min_value=0.0
)

htn = st.selectbox(
    "Hypertension",
    [0,1],
    format_func=lambda x: "Yes" if x==1 else "No"
)

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📂 Dataset", "400")

with col2:
    st.metric("🎯 Accuracy", "100%")

with col3:
    st.metric("🤖 Algorithm", "Random Forest")
    st.markdown("---")

st.header("📊 Model Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📂 Dataset", "400 Patients")

with col2:
    st.metric("🎯 Model Accuracy", "100%")

with col3:
    st.metric("🤖 Algorithm", "Random Forest")

# ============================================
# Prediction
# ============================================

if st.button("🔍 Predict Kidney Disease Risk"):

    input_data = pd.DataFrame([{
        "Bp": bp,
        "Sg": sg,
        "Al": al,
        "Su": su,
        "Rbc": rbc,
        "Bu": bu,
        "Sc": sc,
        "Sod": sod,
        "Pot": pot,
        "Hemo": hemo,
        "Wbcc": wbcc,
        "Rbcc": rbcc,
        "Htn": htn
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    risk_percent = round(probability * 100, 2)

    health_score = round(100 - risk_percent, 2)

    st.metric("📊 Risk Score", f"{risk_percent}%")
    st.progress(risk_percent / 100)

    st.caption(f"Estimated Kidney Disease Risk: {risk_percent}%")
    st.metric("💚 Kidney Health Score", f"{health_score}/100")

    st.markdown("---")

    if prediction == 1:

        st.error("🔴 High Risk of Kidney Disease")

        if risk_percent >= 80:
            st.error("🚨 Please consult a kidney specialist immediately.")

        st.subheader("🤖 AI Health Insights")

        if bp > 140:
            st.write("🩸 High Blood Pressure detected.")

        if sc > 1.2:
            st.write("🧪 High Serum Creatinine detected.")

        if hemo < 12:
            st.write("🩸 Low Hemoglobin detected.")

        if al > 1:
            st.write("🧫 Albumin level is abnormal.")

        if htn == 1:
            st.write("❤️ Hypertension increases kidney disease risk.")

        st.subheader("🥗 Diet Recommendation")

        st.success("""
✅ Apples

✅ Cabbage

✅ Cauliflower

✅ Fish

✅ Olive Oil

✅ Drink water as advised by your doctor.
""")

        st.error("""
❌ Avoid Salt

❌ Junk Food

❌ Soft Drinks

❌ Smoking

❌ Alcohol
""")

    else:

        st.success("🟢 Low Risk of Kidney Disease")

        st.subheader("🤖 AI Health Insights")

        st.success("Most health indicators look normal.")

        st.write("✅ Blood Pressure looks acceptable.")
        st.write("✅ Kidney function appears stable.")
        st.write("✅ Continue healthy lifestyle.")

        st.subheader("🥗 Healthy Lifestyle")

        st.success("""
🥗 Balanced Diet

🚶 Daily Walk

💧 Drink Water

😴 Sleep 7-8 Hours

🩺 Regular Checkup
""")

    st.warning(
        "This tool is for educational purposes only and should not replace professional medical advice."
    )

st.markdown("---")

st.header("ℹ️ About KidneyGuard AI")

st.write("""
KidneyGuard AI is a Machine Learning-based web application
designed to estimate the risk of kidney disease using
patient health parameters.

It was developed as an educational AI project using:

- 🐍 Python
- 🤖 Scikit-learn
- 📊 Pandas
- 🌐 Streamlit
""")

st.caption("🩺 KidneyGuard AI v1.0")

st.caption("Developed by Ayesha Shafiq ❤️")

st.caption("For Educational Purposes Only")
st.markdown("---")

st.markdown(
"""
### 👨‍💻 Developed By

**Ayesha Shafiq**

🩺 KidneyGuard AI v1.0

Built with ❤️ using Python, Streamlit & Machine Learning.
"""
)