from __future__ import annotations

from pathlib import Path
import sys
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.weather_api import get_forecast
from src.ui_theme import apply_theme, render_sidebar

st.set_page_config(page_title="Forecast Analysis", page_icon="📈", layout="wide")

theme = apply_theme()
render_sidebar()

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Forecast Analysis</div>', unsafe_allow_html=True)

if "city" not in st.session_state:
    st.session_state.city = "Berlin"

col1, col2 = st.columns([4, 1.2])
with col1:
    city = st.text_input("City", value=st.session_state.city, label_visibility="collapsed", placeholder="Enter city for forecast analysis")
with col2:
    load_btn = st.button("Analyze")

if load_btn:
    st.session_state.city = city.strip() or "Berlin"

city = st.session_state.city

try:
    forecast = get_forecast(city)

    rows = []
    for item in forecast:
        rows.append(
            {
                "datetime": datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S"),
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "wind_speed": item.get("wind", {}).get("speed", 0),
                "rain_probability": round(item.get("pop", 0) * 100, 2),
                "description": item["weather"][0]["description"].title(),
            }
        )

    df = pd.DataFrame(rows)

    hero1, hero2, hero3, hero4 = st.columns(4)
    summary_cards = [
        ("Avg Temp", f'{df["temperature"].mean():.1f}°C'),
        ("Max Temp", f'{df["temperature"].max():.1f}°C'),
        ("Avg Humidity", f'{df["humidity"].mean():.0f}%'),
        ("Peak Rain Prob.", f'{df["rain_probability"].max():.0f}%'),
    ]

    for col, (title, value) in zip([hero1, hero2, hero3, hero4], summary_cards):
        with col:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div style="font-size:1.15rem; font-weight:700; color:{theme["text_main"]};">{value}</div>
                    <div class="soft-label" style="margin-top:6px;">{title}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=df["datetime"], y=df["temperature"], mode="lines+markers", name="Temperature"))
        fig_temp.add_trace(go.Scatter(x=df["datetime"], y=df["feels_like"], mode="lines+markers", name="Feels Like"))
        fig_temp.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=30, b=10),
            title="Temperature Trend",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text_main"]),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor=theme["plot_grid"]),
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with right:
        fig_hum = go.Figure()
        fig_hum.add_trace(go.Scatter(x=df["datetime"], y=df["humidity"], mode="lines+markers", name="Humidity"))
        fig_hum.add_trace(go.Scatter(x=df["datetime"], y=df["rain_probability"], mode="lines+markers", name="Rain Probability"))
        fig_hum.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=30, b=10),
            title="Humidity vs Rain Probability",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text_main"]),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor=theme["plot_grid"]),
        )
        st.plotly_chart(fig_hum, use_container_width=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    lower_left, lower_right = st.columns([1, 1])

    with lower_left:
        fig_wind = go.Figure()
        fig_wind.add_trace(go.Bar(x=df["datetime"], y=df["wind_speed"], name="Wind Speed"))
        fig_wind.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=30, b=10),
            title="Wind Speed Distribution",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text_main"]),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor=theme["plot_grid"]),
        )
        st.plotly_chart(fig_wind, use_container_width=True)

    with lower_right:
        st.markdown('<div class="section-title">Forecast Table</div>', unsafe_allow_html=True)
        st.dataframe(
            df[["datetime", "temperature", "humidity", "pressure", "wind_speed", "rain_probability", "description"]],
            use_container_width=True,
            hide_index=True,
        )

except Exception as e:
    st.error(f"Could not analyze forecast: {e}")