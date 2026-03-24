import streamlit as st
import pandas as pd
import joblib
import sqlite3
import plotly.express as px
import os

# ======================
# LOAD MODEL (SAFE)
# ======================
if os.path.exists("freight_model.pkl"):
    model = joblib.load("freight_model.pkl")
else:
    model = None
    st.warning("⚠️ Model file not found. Prediction disabled.")

# ======================
# LOAD DATA (SAFE)
# ======================
if os.path.exists("inventory.db"):
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql("SELECT * FROM vendor_invoice", conn)
else:
    st.warning("⚠️ Database not found. Using sample data.")
    df = pd.DataFrame({
        "VendorName": ["Vendor A", "Vendor B", "Vendor C"],
        "Freight": [50, 120, 80],
        "Quantity": [10, 20, 15],
        "Dollars": [500, 2000, 1200],
        "InvoiceDate": pd.date_range(start="2024-01-01", periods=3)
    })

df.columns = df.columns.str.strip().str.replace(" ", "")

# ======================
# FEATURE ENGINEERING (SAFE)
# ======================
df["Quantity"] = df["Quantity"].replace(0, 1)
df["cost_per_unit"] = df["Freight"] / df["Quantity"]
df["vendor_avg_freight"] = df.groupby("VendorName")["Freight"].transform("mean")
df["freight_ratio"] = df["Freight"] / df["Dollars"]
df["deviation"] = df["Freight"] - df["vendor_avg_freight"]

# ======================
# SIDEBAR
# ======================
st.sidebar.title("⚙️ Model Selection")

module = st.sidebar.radio(
    "Choose Module",
    ["Freight Prediction", "Risk Detection"]
)

# ======================
# AI ASSISTANT
# ======================
st.sidebar.title("🤖 AI Assistant")

query = st.sidebar.text_input("Ask something")

if query:
    q = query.lower()

    if "freight" in q:
        st.sidebar.write("Freight is the transportation cost of goods.")
    elif "vendor" in q:
        best = df.groupby("VendorName")["Freight"].mean().idxmin()
        worst = df.groupby("VendorName")["Freight"].mean().idxmax()
        st.sidebar.write(f"Best Vendor: {best}")
        st.sidebar.write(f"Most Expensive Vendor: {worst}")
    elif "average" in q:
        st.sidebar.write(f"Average Freight: {round(df['Freight'].mean(),2)}")
    elif "trend" in q:
        st.sidebar.write("Freight trend shows how cost changes over time.")
    elif "risk" in q:
        st.sidebar.write("Risk increases when actual cost is higher than predicted.")
    else:
        st.sidebar.write("Try asking about freight, vendor, risk.")

# ======================
# TITLE
# ======================
st.title("🚀 AI Freight Cost Prediction & Risk Analysis System")
st.caption("Smart Cost Prediction • Risk Detection • Vendor Insights")

# ======================
# TABS
# ======================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Analysis", "🎯 AI Prediction"])

# ======================
# DASHBOARD
# ======================
with tab1:

    st.subheader("📊 Business Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Invoices", len(df))
    col2.metric("Avg Freight", round(df["Freight"].mean(), 2))
    col3.metric("Total Quantity", int(df["Quantity"].sum()))

# ======================
# ANALYSIS
# ======================
with tab2:

    st.subheader("📈 Freight Analysis")

    fig = px.scatter(df, x="Quantity", y="Freight", color="Freight")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Vendor Performance")
    vendor_rank = df.groupby("VendorName")["Freight"].mean().sort_values()
    st.dataframe(vendor_rank.head(10))

    st.subheader("📅 Trend")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    trend = df.groupby(df["InvoiceDate"].dt.month)["Freight"].mean()
    st.line_chart(trend)

# ======================
# PREDICTION
# ======================
with tab3:

    if module == "Freight Prediction":

        st.subheader("🚚 Prediction")

        quantity = st.number_input("Quantity", value=100)
        dollars = st.number_input("Invoice Value ($)", value=1000.0)
        actual_cost = st.number_input("Actual Freight", value=10.0)

        if st.button("Predict"):

            if model is None:
                st.error("Model not available")
            else:
                vendor_avg = df["Freight"].mean()

                input_data = pd.DataFrame([{
                    "Quantity": quantity,
                    "Dollars": dollars,
                    "vendor_avg_freight": vendor_avg,
                    "cost_per_unit": actual_cost / max(quantity,1),
                    "freight_ratio": actual_cost / max(dollars,1),
                    "deviation": actual_cost - vendor_avg
                }])

                prediction = model.predict(input_data)[0]

                st.success(f"Predicted Cost: {round(prediction,2)}")

    else:

        st.subheader("🚨 Risk Detection")

        quantity = st.number_input("Quantity", value=50)
        dollars = st.number_input("Invoice Value", value=500.0)
        freight = st.number_input("Freight Cost", value=20.0)

        if st.button("Check Risk"):

            ratio = freight / (dollars / max(quantity,1))

            if ratio > 2:
                st.error("🔴 HIGH RISK")
            elif ratio > 1.5:
                st.warning("🟠 MEDIUM RISK")
            else:
                st.success("🟢 SAFE")