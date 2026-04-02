from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.weather_api import get_current_weather
from src.predict import predict_rain
from src.utils import transform_api_to_model_input
from src.ui_theme import apply_theme, render_sidebar, weather_emoji

st.set_page_config(page_title="Rain Prediction", page_icon="🧠", layout="wide")

theme = apply_theme()
render_sidebar()

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Rain Prediction</div>', unsafe_allow_html=True)

if "city" not in st.session_state:
    st.session_state.city = "Berlin"

col1, col2 = st.columns([4, 1.2])
with col1:
    city = st.text_input("City", value=st.session_state.city, label_visibility="collapsed", placeholder="Enter city for live prediction")
with col2:
    predict_btn = st.button("Predict")

if predict_btn:
    st.session_state.city = city.strip() or "Berlin"

city = st.session_state.city

try:
    weather = get_current_weather(city)
    model_input = transform_api_to_model_input(weather)
    prediction = predict_rain(model_input)

    temp = round(weather["main"]["temp"])
    desc = weather["weather"][0]["description"].title()
    emoji = weather_emoji(desc)
    result_text = "Rain Likely" if prediction == 1 else "No Rain Likely"
    result_emoji = "🌧️" if prediction == 1 else "☀️"
    result_color = "#4f7cff" if prediction == 1 else "#16a34a"

    hero_left, hero_right = st.columns([5.2, 2.3])

    with hero_left:
        st.markdown(
            f"""
            <div class="top-card">
                <div style="display:flex; gap:24px; align-items:center;">
                    <div class="weather-emoji">{emoji}</div>
                    <div>
                        <div class="soft-label">{weather["name"]}, {weather["sys"]["country"]}</div>
                        <div class="hero-title">{temp}°C, {desc}</div>
                        <div class="soft-label">Machine-learning rain classification using live weather input</div>
                        <div style="margin-top:14px;">
                            <span class="pill">Humidity {weather["main"]["humidity"]}%</span>
                            <span class="pill">Pressure {weather["main"]["pressure"]} hPa</span>
                            <span class="pill">Wind {weather.get("wind", {}).get("speed", 0)} m/s</span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_right:
        st.markdown(
            f"""
            <div class="mini-card">
                <div style="font-size:2rem;">{result_emoji}</div>
                <div style="font-size:1.35rem; font-weight:800; color:{result_color}; margin-top:8px;">
                    {result_text}
                </div>
                <div class="soft-label" style="margin-top:8px;">Prediction Output</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    a, b, c, d = st.columns(4)
    cards = [
        ("MinTemp", model_input["MinTemp"]),
        ("MaxTemp", model_input["MaxTemp"]),
        ("Humidity", model_input["Humidity9am"]),
        ("Pressure", model_input["Pressure9am"]),
    ]
    for col, (label, value) in zip([a, b, c, d], cards):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-title">{label}</div>
                    <div class="soft-label">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 0.9])

    with left:
        df = pd.DataFrame([model_input])
        st.markdown('<div class="section-title">Model Input Features</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with right:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-title">Prediction Logic</div>
                <div class="soft-label" style="margin-top:10px;">
                    The Random Forest model was trained on the Kaggle weatherAUS dataset to classify
                    whether rain is likely on the following day. For live predictions, current OpenWeather
                    conditions are transformed into the same feature structure used during training.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

except Exception as e:
    st.error(f"Could not generate prediction: {e}")