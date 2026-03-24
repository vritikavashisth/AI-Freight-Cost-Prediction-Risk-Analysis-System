import streamlit as st
import pandas as pd
import joblib
import sqlite3
import plotly.express as px


# ======================
# LOAD MODEL
# ======================
model = joblib.load("freight_model.pkl")

# ======================
# UI
# ======================

st.markdown("""
<style>

/* ===== BACKGROUND ===== */
body {
    background: linear-gradient(135deg, #0E1117, #111827);
}

*:focus {
    outline: none !important;
    box-shadow: none !important;
}

.title-clean {
    font-size: 30px;
    font-weight: 800;
    text-align: center;
    letter-spacing: 1px;
    margin-bottom: 8px;

    background: linear-gradient(90deg, #60A5FA, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    /* Softer glow  */
    text-shadow: 0px 0px 6px rgba(99,102,241,0.15);
}
/* ===== SUBTITLE ===== */
.subtitle {
    text-align:center;
    color:#9CA3AF;
    font-size:18px;
    margin-bottom: 10px;
}

/* ===== CARD ===== */
.card {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 16px;
    border: 4px solid #E5E7EB;
    transition: 0.3s;
}


.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 0px 20px rgba(99,102,241,0.25);
}

            
/* ===== METRIC ===== */
.metric {
    font-size: 30px;
    font-weight: bold;
    color: #2563EB;
}

.label {
    font-size: 17px;
    color: #9CA3AF;
}

/* ===== BUTTON ===== */
div.stButton > button {
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    transform: scale(1.05);
}

/* ===== TABS ===== */
button[kind="tab"] {
    font-size: 20px;
    font-weight: 600;
    color: #9CA3AF;
}

button[kind="tab"][aria-selected="true"] {
    color: white;
    border-bottom: 3px solid #6366F1;
}

</style>
""", unsafe_allow_html=True)
# ======================
# LOAD DATA
# ======================
conn = sqlite3.connect("inventory.db")
df = pd.read_sql("SELECT * FROM vendor_invoice", conn)

df.columns = df.columns.str.strip().str.replace(" ", "")

# ======================
# FEATURE ENGINEERING
# ======================
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
# AI ASSISTANT (UPGRADED)
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
    elif "anomaly" in q:
        st.sidebar.write("Anomaly means unusual or suspicious transaction.")
    else:
        st.sidebar.write("Try asking about freight, vendor, risk, trend, anomaly.")

# ======================
# MAIN TITLE
# ======================
st.markdown("""
<div style="text-align:center; margin-top:20px; margin-bottom:40px;">

<div class="title-clean">
AI Freight Cost Prediction & Risk Analysis System
</div>

<div class="subtitle">
Smart Cost Prediction • Risk Detection • Vendor Insights
</div>

</div>
""", unsafe_allow_html=True)

# ======================
# TABS
# ======================
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "📈 Analysis",
    "🎯 AI Prediction"
])

# ======================
# DASHBOARD
# ======================
with tab1:

    st.subheader("📊 Business Overview")
    st.markdown("""

This dashboard provides a high-level summary of logistics performance.  

- Displays total invoices, average freight cost, and total quantity  
- Helps monitor overall business performance  
- Useful for quick decision-making and tracking KPIs  

It gives a snapshot of how efficiently the freight system is operating.
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="label">Total Invoices</div>
            <div class="metric">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="label">Avg Freight</div>
            <div class="metric">{round(df["Freight"].mean(),2)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="label">Total Quantity</div>
            <div class="metric">{int(df["Quantity"].sum())}</div>
        </div>
        """, unsafe_allow_html=True)
# ======================
# ANALYSIS (CLEAN + FIXED)
# ======================
with tab2:

    st.subheader("📈 Freight Analysis")
    st.markdown("""

This section provides detailed insights into freight data using visualizations.  

- Analyzes relationship between quantity and freight cost  
- Evaluates vendor performance  
- Identifies trends over time  
- Detects anomalies and unusual transactions  

It helps in understanding patterns and improving logistics strategy.
""")

    # GRAPH
    fig = px.scatter(
        df,
        x="Quantity",
        y="Freight",
        color="Freight",
        color_continuous_scale="viridis"
    )

    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#EAEDF0",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    # VENDOR
    st.subheader("🏆 Vendor Performance")

    with st.expander("ℹ️ What is Vendor Performance?"):
        st.write("""
        Vendor Performance ranks vendors based on freight efficiency.

    - Low cost → better vendor  
    - High cost → expensive vendor 
        """)

    vendor_rank = df.groupby("VendorName")["Freight"].mean().sort_values()
    st.dataframe(vendor_rank.head(10))

    # TREND
    st.subheader("📅 Freight Trend Analysis")
    with st.expander("ℹ️ What is Freight Trend Analysis?"):
        st.write("""
    Freight Trend Analysis shows how freight cost changes over time.

    - Identifies monthly variations  
    - Detects trends  
    - Helps in forecasting  
    """)

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    trend = df.groupby(df["InvoiceDate"].dt.month)["Freight"].mean()
    st.line_chart(trend)

    # ANOMALY
    st.subheader("🚨 Anomaly Detection")
    with st.expander("ℹ️ What is Anomaly Detection?"):
        st.write("""
    Detects unusual transactions using statistical methods.

    - Helps find fraud  
    - Identifies abnormal cost  
    """)

    df["z_score"] = (df["Freight"] - df["Freight"].mean()) / df["Freight"].std()
    st.dataframe(df[df["z_score"].abs() > 2].head())

# ======================
# PREDICTION
# ======================
with tab3:

    if module == "Freight Prediction":

        st.subheader("🚚 Freight Cost Prediction")
        st.markdown("""

This module uses Machine Learning to predict freight cost and detect risks.  

- Predicts expected freight cost  
- Compares actual vs predicted values  
- Identifies risk level (Safe / Medium / High)  
- Helps in fraud detection and decision-making  

It automates invoice validation and reduces manual effort.
""")

        quantity = st.number_input("Quantity", value=100)
        dollars = st.number_input("Invoice Value ($)", value=1000.0)
        actual_cost = st.number_input("Actual Freight Cost", value=10.0)

        if st.button("Predict"):

            vendor_avg = df["Freight"].mean()

            input_data = pd.DataFrame([{
                "Quantity": quantity,
                "Dollars": dollars,
                "vendor_avg_freight": vendor_avg,
                "cost_per_unit": actual_cost / quantity,
                "freight_ratio": actual_cost / dollars,
                "deviation": actual_cost - vendor_avg
            }])

            prediction = model.predict(input_data)[0]

            ratio = actual_cost / prediction if prediction != 0 else 0

            st.metric("Predicted Cost", round(prediction, 2))

            if ratio > 2:
                st.error("🔴 HIGH RISK")
            elif ratio > 1.5:
                st.warning("🟠 MEDIUM RISK")
            else:
                st.success("🟢 SAFE")

            # AI Insight
            st.subheader("🧠 AI Insight")

            if ratio > 1.5:
                st.warning("Cost is higher than expected ⚠️")
            else:
                st.success("Cost is within expected range ✅")

            # GRAPH
            st.bar_chart(pd.DataFrame({
                "Type": ["Actual", "Predicted"],
                "Cost": [actual_cost, prediction]
            }).set_index("Type"))

    else:

        st.subheader("🚨 Risk Detection")
        st.markdown("""

This module analyzes invoice data to identify risky or abnormal transactions.  

- Compares freight cost with invoice value and quantity  
- Detects unusually high or low cost patterns  
- Classifies transactions into Safe, Medium Risk, or High Risk  
- Helps in preventing fraud and financial loss  

This system enables automated monitoring and reduces the need for manual verification.
""")

        quantity = st.number_input("Quantity", value=50)
        dollars = st.number_input("Invoice Value", value=500.0)
        freight = st.number_input("Freight Cost", value=20.0)

        if st.button("Check Risk"):

            ratio = freight / (dollars / quantity)

            if ratio > 2:
                st.error("🔴 HIGH RISK")
            elif ratio > 1.5:
                st.warning("🟠 MEDIUM RISK")
            else:
                st.success("🟢 SAFE")


