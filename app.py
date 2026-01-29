import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("LP_Train.csv")

# -----------------------------
# Data Cleaning (your logic)
# -----------------------------
df.Dependents = df.Dependents.replace('[+]','',regex=True).astype('float')
df.Dependents = df.Dependents.fillna(0)
df.Gender = df.Gender.fillna('Male')
df.Self_Employed = df.Self_Employed.fillna('No')
df.LoanAmount = df.LoanAmount.fillna(128.0)
df.Loan_Amount_Term = df.Loan_Amount_Term.fillna(360.0)
df.Credit_History = df.Credit_History.fillna(1.0)
df.Married = df.Married.fillna('Yes')
df['Loan_Status'] = df['Loan_Status'].replace({'Y': 1, 'N': 0})

# -----------------------------
# Encoding
# -----------------------------
df_encoded = pd.get_dummies(df, drop_first=True)

X = df_encoded.drop('Loan_Status', axis=1)
y = df_encoded['Loan_Status']

# -----------------------------
# Train Model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🏦 Loan Approval Prediction App")

st.write("Check loan approval chances based on applicant details")

# Sidebar Inputs
st.sidebar.header("Applicant Details")

name = st.sidebar.text_input("Applicant Name")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
married = st.sidebar.selectbox("Married", ["Yes", "No"])
education = st.sidebar.selectbox("Education", ["Graduate", "Not Graduate"])
self_emp = st.sidebar.selectbox("Self Employed", ["Yes", "No"])
property_area = st.sidebar.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

dependents = st.sidebar.slider("Dependents", 0, 3, 0)
app_income = st.sidebar.number_input("Applicant Income", min_value=1000, value=5000)
co_income = st.sidebar.number_input("Co-applicant Income", min_value=0, value=0)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=50, value=150)
loan_term = st.sidebar.selectbox("Loan Term", [360, 180, 240, 120])
credit_history = st.sidebar.selectbox("Credit History", [1.0, 0.0])

# -----------------------------
# Prediction
# -----------------------------
if st.sidebar.button("Check Loan Approval"):

    user_data = {
        'ApplicantIncome': app_income,
        'CoapplicantIncome': co_income,
        'LoanAmount': loan_amount,
        'Loan_Amount_Term': loan_term,
        'Credit_History': credit_history,
        'Dependents': dependents,
        'Gender_Male': 1 if gender == "Male" else 0,
        'Married_Yes': 1 if married == "Yes" else 0,
        'Education_Not Graduate': 1 if education == "Not Graduate" else 0,
        'Self_Employed_Yes': 1 if self_emp == "Yes" else 0,
        'Property_Area_Semiurban': 1 if property_area == "Semiurban" else 0,
        'Property_Area_Urban': 1 if property_area == "Urban" else 0,
    }

    user_df = pd.DataFrame([user_data])
    user_df = user_df.reindex(columns=X.columns, fill_value=0)

    prob = model.predict_proba(user_df)[0][1] * 100

    st.subheader(f"Hello {name} 👋")

    st.write(f"### ✅ Loan Approval Chance: **{prob:.2f}%**")

    if prob >= 60:
        st.success("High chance of loan approval 🎉")
    else:
        st.warning("Low chance of loan approval ⚠️")

# -----------------------------
# EDA Section
# -----------------------------
st.header("📊 Exploratory Data Analysis")

option = st.selectbox(
    "Select Analysis",
    [
        "Loan Status by Gender",
        "Loan Status by Married",
        "Loan Status by Education",
        "Loan Status by Property Area",
        "Income vs Loan Status"
    ]
)

plt.figure()

if option == "Loan Status by Gender":
    sb.barplot(x=df.Gender, y=df.Loan_Status)
elif option == "Loan Status by Married":
    sb.barplot(x=df.Married, y=df.Loan_Status)
elif option == "Loan Status by Education":
    sb.barplot(x=df.Education, y=df.Loan_Status)
elif option == "Loan Status by Property Area":
    sb.barplot(x=df.Property_Area, y=df.Loan_Status)
elif option == "Income vs Loan Status":
    sb.barplot(x=df.Loan_Status, y=df.ApplicantIncome)

st.pyplot(plt)
