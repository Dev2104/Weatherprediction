from __future__ import annotations

from pathlib import Path
import sys
from datetime import datetime

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.weather_api import get_current_weather
from src.ui_theme import apply_theme, render_sidebar, weather_emoji

st.set_page_config(page_title="Current Weather", page_icon="🌤️", layout="wide")

theme = apply_theme()
render_sidebar()

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Current Weather</div>', unsafe_allow_html=True)

if "city" not in st.session_state:
    st.session_state.city = "Berlin"

search_col1, search_col2, search_col3 = st.columns([4, 1.2, 2])
with search_col1:
    city = st.text_input("City", value=st.session_state.city, label_visibility="collapsed", placeholder="Enter city")
with search_col2:
    load = st.button("Load Weather")
with search_col3:
    st.markdown('<div class="soft-label">Live current conditions using OpenWeather API</div>', unsafe_allow_html=True)

if load:
    st.session_state.city = city.strip() or "Berlin"

city = st.session_state.city

try:
    data = get_current_weather(city)

    location = f'{data["name"]}, {data["sys"]["country"]}'
    description = data["weather"][0]["description"].title()
    emoji = weather_emoji(description)
    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data.get("wind", {}).get("speed", 0)
    wind_deg = data.get("wind", {}).get("deg", 0)
    visibility = data.get("visibility", 0) / 1000
    clouds = data.get("clouds", {}).get("all", 0)
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    hero_left, hero_right = st.columns([5.2, 2.3])

    with hero_left:
        st.markdown(
            f"""
            <div class="top-card">
                <div style="display:flex; gap:24px; align-items:center;">
                    <div class="weather-emoji">{emoji}</div>
                    <div>
                        <div class="soft-label">{location}</div>
                        <div class="hero-title">{temp}°C, {description}</div>
                        <div class="soft-label">Real-time current conditions</div>
                        <div style="margin-top:12px;">
                            <span class="pill">Feels like {feels_like}°C</span>
                            <span class="pill">Humidity {humidity}%</span>
                            <span class="pill">Pressure {pressure} hPa</span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_right:
        c1, c2, c3 = st.columns(3)
        metrics = [
            ("💨", f"{wind_speed} m/s", "Wind"),
            ("☁️", f"{clouds}%", "Clouds"),
            ("👁️", f"{visibility:.1f} km", "Visibility"),
        ]
        for col, (icon, value, label) in zip([c1, c2, c3], metrics):
            with col:
                st.markdown(
                    f"""
                    <div class="mini-card">
                        <div style="font-size:2rem;">{icon}</div>
                        <div style="font-size:1.25rem; font-weight:700; color:{theme["text_main"]};">{value}</div>
                        <div class="soft-label">{label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    row1, row2, row3, row4 = st.columns(4)

    detail_cards = [
        ("🌡️", "Temperature Range", f'{round(data["main"]["temp_min"])}°C / {round(data["main"]["temp_max"])}°C'),
        ("🧭", "Wind Direction", f"{wind_deg}°"),
        ("🌅", "Sunrise", sunrise),
        ("🌇", "Sunset", sunset),
    ]

    for col, (icon, title, value) in zip([row1, row2, row3, row4], detail_cards):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div style="font-size:1.7rem;">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="soft-label">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    info_left, info_right = st.columns([1, 1])
    with info_left:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-title">Weather Summary</div>
                <div class="soft-label" style="margin-top:10px;">
                    {location} is currently experiencing <b>{description}</b> with a temperature of <b>{temp}°C</b>.
                    The air feels like <b>{feels_like}°C</b>, humidity is <b>{humidity}%</b>,
                    and wind speed is <b>{wind_speed} m/s</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with info_right:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-title">Operational Snapshot</div>
                <div class="soft-label" style="margin-top:10px;">
                    This page is powered by the live OpenWeather current-weather endpoint.
                    It is useful for checking real-time atmospheric conditions before using
                    the ML-based rain prediction and forecast analysis pages.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

except Exception as e:
    st.error(f"Could not load current weather: {e}")