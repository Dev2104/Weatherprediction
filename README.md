# 🌦️ WeatherML — AI-Powered Weather Intelligence Dashboard

An end-to-end **Machine Learning + Data Visualization web application** that combines real-time weather data with predictive modeling to deliver actionable insights.

---

## 🚀 Overview

WeatherML is a modern Streamlit-based dashboard that:

* Fetches **live weather data** using OpenWeather API
* Uses a **trained Machine Learning model** to predict rain probability
* Provides **interactive visual analytics**
* Delivers a **clean, dashboard-style UI** suitable for real-world applications

---

## 🧠 Key Features

* 📡 **Live Weather Integration**

  * Real-time weather data using OpenWeather API

* 🧠 **Machine Learning Predictions**

  * Rain prediction using a trained Random Forest model
  * Feature engineering based on real-world meteorological data

* 📊 **Interactive Dashboard**

  * Forecast visualization
  * Rain probability trends
  * Temperature analytics

* 🎨 **Custom UI/UX**

  * Fully designed Streamlit dashboard (not default UI)
  * Dark/Light theme toggle
  * Glassmorphism-style cards

* 🔄 **Multi-page Application**

  * Home Dashboard
  * Current Weather
  * Model Predictions
  * Forecast Analysis
  * Model Insights

---

## 🏗️ Project Structure

```
weather_ml_app/
│
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 1_Current_Weather.py
│       ├── 2_Rain_Prediction.py
│       ├── 3_Forecast_Analysis.py
│       ├── 4_Model_Insights.py
│       └── 5_About_Project.py
│
├── src/
│   ├── weather_api.py
│   ├── preprocess.py
│   ├── features.py
│   ├── train.py
│   └── train_model.py
│
├── data/
│   └── raw/
│       └── weatherAUS.csv
│
├── models/
│   └── rain_model.pkl
│
├── .env
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Tech Stack

* **Python**
* **Streamlit**
* **Scikit-learn**
* **Pandas / NumPy**
* **Plotly**
* **OpenWeather API**

---

## 🧪 Machine Learning Details

* Model: **Random Forest Classifier**
* Dataset: **Kaggle Weather Dataset (weatherAUS)**
* Target: `RainTomorrow`
* Features:

  * Temperature (min/max)
  * Humidity
  * Pressure
  * Wind speed

---

## 🔑 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/weather-ml-app.git
cd weather-ml-app
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API key

Create a `.env` file:

```
OPENWEATHER_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
streamlit run app/Home.py
```

---

## 📈 Future Improvements

* Advanced time-series forecasting (LSTM / Prophet)
* Model explainability (SHAP / XAI)
* Deployment (Streamlit Cloud / Docker)
* Real-time alert system

---

## 💡 Author

**Dev Tailor**
Aspiring Data Scientist | AI + Analytics Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
