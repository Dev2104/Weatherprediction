from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.ui_theme import apply_theme, render_sidebar

st.set_page_config(page_title="About Project", page_icon="⚙️", layout="wide")

theme = apply_theme()
render_sidebar()

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">About Project</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="top-card">
        <div class="hero-title">WeatherML — AI-Powered Weather Dashboard</div>
        <div class="soft-label" style="margin-top:10px;">
            WeatherML is a full-stack Streamlit application that combines live OpenWeather API data,
            supervised machine learning, and premium dashboard styling to deliver practical weather intelligence.
        </div>
        <div style="margin-top:14px;">
            <span class="pill">OpenWeather API</span>
            <span class="pill">Random Forest Classifier</span>
            <span class="pill">Kaggle weatherAUS</span>
            <span class="pill">Streamlit + Plotly</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
blocks = [
    (
        "📡 Data Layer",
        "Real-time weather data is fetched from OpenWeather endpoints for current weather and multi-step forecast analysis."
    ),
    (
        "🧠 ML Layer",
        "A Random Forest model trained on historical weatherAUS data predicts likely rain outcomes using engineered meteorological inputs."
    ),
    (
        "🎨 Interface Layer",
        "A custom Streamlit dashboard replaces the default UI with themed cards, charts, and cohesive multi-page navigation."
    ),
]

for col, (title, text) in zip([c1, c2, c3], blocks):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-title">{title}</div>
                <div class="soft-label">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Project Goals</div>
            <div class="soft-label" style="margin-top:10px;">
                • Build a real-world weather application with live API integration<br>
                • Train and deploy a machine learning model for rain prediction<br>
                • Present insights through a portfolio-ready dashboard UI<br>
                • Demonstrate full workflow from data preprocessing to frontend delivery
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Tech Stack</div>
            <div class="soft-label" style="margin-top:10px;">
                Python<br>
                Streamlit<br>
                Pandas / NumPy<br>
                Scikit-learn<br>
                Plotly<br>
                OpenWeather API
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="glass-card">
        <div class="section-title">Future Improvements</div>
        <div class="soft-label" style="margin-top:10px;">
            Planned upgrades include exportable reports, city comparison tools, advanced model explainability,
            and improved forecast intelligence using richer historical data pipelines.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)