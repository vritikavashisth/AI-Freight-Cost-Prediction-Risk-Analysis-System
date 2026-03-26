# 🚀 AI Freight Cost Prediction & Risk Analysis System

A machine learning-based web application that helps analyze freight costs, compare vendor performance, predict expenses, and detect risky invoices using interactive dashboards.

---

## 🎯 Project Impact

This project is useful for businesses and logistics teams that deal with large volumes of vendor invoices and freight costs. Managing such data manually is time-consuming and often leads to errors or missed insights.

This system helps by:

* **Reducing costs:** It identifies invoices where freight charges are higher than expected, helping businesses control expenses.
* **Improving vendor decisions:** By comparing vendor performance, it becomes easier to choose cost-efficient vendors.
* **Detecting risks:** The system highlights unusual or abnormal transactions that may indicate errors or potential fraud.
* **Saving time:** Automated analysis replaces manual checking of data, making the process faster and more reliable.
* **Supporting data-driven decisions:** Instead of guesswork, decisions are based on actual data insights and model predictions.

Overall, this project helps improve operational efficiency, reduce unnecessary costs, and make smarter business decisions.

---

## 📌 Features

* 📊 Dashboard with key insights
* 📈 Freight trend analysis
* 🏆 Vendor performance comparison
* 🤖 Freight cost prediction
* 🚨 Risk detection system

---

## 🖼️ Application Overview

### 📊 Dashboard

This page shows overall business insights like total invoices, average freight cost, and quantity.
It helps users quickly understand system performance.

👉 Built using: Pandas + Streamlit (columns & metrics)

<p align="center">
  <img src="assets/dashboard.png.png" width="600">
</p>

---

### 📈 Analysis

This section displays graphs for freight trends and vendor comparison.
It helps in identifying patterns and unusual cost behavior.

👉 Built using: Pandas (groupby) + Plotly charts

<p align="center">
  <img src="assets/analysis1.png.png" width="600">
</p>

<p align="center">
  <img src="assets/analysis2.png.png" width="600">
</p>

<p align="center">
  <img src="assets/analysis3.png.png" width="600">
</p>

<p align="center">
  <img src="assets/analysis4.png.png" width="600">
</p>

---

### 🎯 Prediction & Risk Detection

Users enter inputs like quantity and invoice value.
The system predicts freight cost and classifies risk as Safe / Medium / High.

👉 Built using: Scikit-learn model + Joblib

<p align="center">
  <img src="assets/prediction1.png.png" width="600">
</p>

<p align="center">
  <img src="assets/prediction2.png.png" width="600">
</p>

---

### ⚙️ Model Selection & AI Assistant

This section lets users choose between **Freight Prediction** and **Risk Detection**.

It also includes an AI assistant where users can ask queries like *highest vendor* or *most expensive vendor*, and get instant insights.

👉 Built using: Pandas + Streamlit

<p align="center">
  <img src="assets/ai&model.png.png" width="400" height="700">
</p>


## ⚙️ How It Works

* Data is processed using Pandas
* Features like cost ratio and deviation are created
* ML model predicts freight cost
* Risk is calculated based on difference
* Results are displayed using Streamlit

---
## 🗄️ Database

This project uses an SQLite database (`inventory.db`) to store vendor invoice data.

It contains details such as vendor name, quantity, and freight cost, which are used for analysis and model predictions.

👉 Used for:

* Data storage
* Dashboard metrics
* Vendor analysis
* Input for ML model

👉 Integrated using: Pandas + SQLite

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Plotly

---

## ▶️ Run Locally

```bash id="1q9zkl"
git clone https://github.com/vritikavashisth/AI-Freight-Cost-Prediction-Risk-Analysis-System.git
cd AI-Freight-Cost-Prediction-Risk-Analysis-System
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## 🌐 Live Demo

https://ai-freight-cost-prediction-risk-analysis-system-ipztyoxfkebtfb.streamlit.app

---

## 👤 Author

**Vritika**
AI/ML Enthusiast | Building Real-World Intelligent Systems

🔗 GitHub: https://github.com/vritikavashisth
🔗 LinkedIn: https://linkedin.com/in/vritikasharmaa

---
