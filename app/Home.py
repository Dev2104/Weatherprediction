from __future__ import annotations

from pathlib import Path
import sys
from datetime import datetime

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Make project root importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.weather_api import get_current_weather, get_forecast


st.set_page_config(
    page_title="Weather Hub",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_theme_tokens(theme_mode: str) -> dict:
    """
    Return theme colors for the selected mode.
    'System' currently falls back to dark styling.
    """
    if theme_mode == "Light":
        return {
            "bg_main": "#f3f6fb",
            "bg_grad_1": "rgba(79,124,255,0.10)",
            "bg_grad_2": "rgba(0,153,255,0.06)",
            "sidebar_bg_1": "#eef3fb",
            "sidebar_bg_2": "#e7edf8",
            "card_bg_1": "rgba(255,255,255,0.94)",
            "card_bg_2": "rgba(246,249,255,0.92)",
            "border": "rgba(15,23,42,0.08)",
            "text_main": "#0f172a",
            "text_soft": "#5b6b83",
            "pill_bg": "rgba(79,124,255,0.10)",
            "pill_border": "rgba(79,124,255,0.22)",
            "pill_text": "#2141a8",
            "input_bg": "rgba(255,255,255,0.92)",
            "button_grad_1": "#4f7cff",
            "button_grad_2": "#2d55ff",
            "shadow": "0 8px 28px rgba(15,23,42,0.08)",
            "nav_bg": "rgba(79,124,255,0.06)",
        }

    # Dark + System fallback
    return {
        "bg_main": "#060914",
        "bg_grad_1": "rgba(49,89,255,0.18)",
        "bg_grad_2": "rgba(0,153,255,0.10)",
        "sidebar_bg_1": "#0d1222",
        "sidebar_bg_2": "#0a0f1c",
        "card_bg_1": "rgba(22,28,45,0.90)",
        "card_bg_2": "rgba(15,19,34,0.88)",
        "border": "rgba(255,255,255,0.08)",
        "text_main": "#f5f7fb",
        "text_soft": "#9aa7bd",
        "pill_bg": "rgba(95,125,255,0.18)",
        "pill_border": "rgba(124,150,255,0.25)",
        "pill_text": "#dfe8ff",
        "input_bg": "rgba(255,255,255,0.04)",
        "button_grad_1": "#4f7cff",
        "button_grad_2": "#2d55ff",
        "shadow": "0 8px 30px rgba(0,0,0,0.28)",
        "nav_bg": "rgba(255,255,255,0.04)",
    }


if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

theme_tokens = get_theme_tokens(st.session_state.theme_mode)

st.markdown(
    f"""
    <style>
    header[data-testid="stHeader"] {{
        display: none;
    }}

    div[data-testid="stToolbar"] {{
        display: none;
    }}

    div[data-testid="stDecoration"] {{
        display: none;
    }}

    div[data-testid="stStatusWidget"] {{
        display: none;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    .stApp {{
        background:
            radial-gradient(circle at top left, {theme_tokens["bg_grad_1"]}, transparent 28%),
            radial-gradient(circle at top right, {theme_tokens["bg_grad_2"]}, transparent 22%),
            linear-gradient(180deg, {theme_tokens["bg_main"]} 0%, {theme_tokens["bg_main"]} 100%);
        color: {theme_tokens["text_main"]};
    }}

    div[data-testid="stSidebarNav"] {{
        display: none;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {theme_tokens["sidebar_bg_1"]} 0%, {theme_tokens["sidebar_bg_2"]} 100%);
        border-right: 1px solid {theme_tokens["border"]};
    }}

    section[data-testid="stSidebar"] > div:first-child {{
        padding-top: 1rem;
    }}

    .block-container {{
        padding-top: 0.7rem !important;
        padding-bottom: 1rem;
        max-width: 1450px;
    }}

    .top-card,
    .glass-card,
    .mini-card,
    .feature-card {{
        background: linear-gradient(180deg, {theme_tokens["card_bg_1"]}, {theme_tokens["card_bg_2"]});
        border: 1px solid {theme_tokens["border"]};
        border-radius: 22px;
        box-shadow: {theme_tokens["shadow"]};
        backdrop-filter: blur(12px);
    }}

    .top-card {{
        padding: 24px 28px;
        min-height: 210px;
    }}

    .glass-card {{
        padding: 20px 22px 16px 22px;
        min-height: 420px;
    }}

    .mini-card {{
        padding: 18px 16px;
        text-align: center;
        min-height: 150px;
    }}

    .feature-card {{
        padding: 18px 20px;
        min-height: 105px;
    }}

    .soft-label {{
        color: {theme_tokens["text_soft"]};
        font-size: 0.95rem;
    }}

    .section-title {{
        font-size: 1.55rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: {theme_tokens["text_main"]};
    }}

    .hero-title {{
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        color: {theme_tokens["text_main"]};
    }}

    .weather-emoji {{
        font-size: 5.6rem;
        line-height: 1;
    }}

    .pill {{
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: {theme_tokens["pill_bg"]};
        border: 1px solid {theme_tokens["pill_border"]};
        color: {theme_tokens["pill_text"]};
        font-size: 0.88rem;
        margin-right: 0.45rem;
        margin-top: 0.35rem;
    }}

    .sidebar-brand {{
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: {theme_tokens["text_main"]};
    }}

    .feature-title {{
        font-weight: 700;
        font-size: 1.12rem;
        margin-bottom: 0.25rem;
        color: {theme_tokens["text_main"]};
    }}

    .footer-note {{
        text-align: center;
        color: {theme_tokens["text_soft"]};
        font-size: 0.9rem;
        margin-top: 0.8rem;
    }}

    .stTextInput > div > div,
    .stSelectbox > div > div,
    .stButton > button {{
        border-radius: 14px !important;
    }}

    .stTextInput input {{
        background: {theme_tokens["input_bg"]} !important;
        color: {theme_tokens["text_main"]} !important;
        border: 1px solid {theme_tokens["border"]} !important;
    }}

    .stSelectbox div[data-baseweb="select"] > div {{
        background: {theme_tokens["input_bg"]} !important;
        color: {theme_tokens["text_main"]} !important;
        border: 1px solid {theme_tokens["border"]} !important;
    }}

    .stRadio > div {{
        background: transparent !important;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, {theme_tokens["button_grad_1"]}, {theme_tokens["button_grad_2"]}) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
    }}

    .stButton > button:hover {{
        filter: brightness(1.06);
    }}

    a[data-testid="stPageLink-NavLink"] {{
        background: {theme_tokens["nav_bg"]};
        border: 1px solid {theme_tokens["border"]};
        border-radius: 14px;
        margin-bottom: 0.45rem;
        padding: 0.25rem 0.45rem;
    }}

    a[data-testid="stPageLink-NavLink"] p {{
        color: {theme_tokens["text_main"]} !important;
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def weather_emoji(description: str) -> str:
    desc = description.lower()
    if "thunder" in desc:
        return "⛈️"
    if "snow" in desc:
        return "❄️"
    if "rain" in desc or "drizzle" in desc:
        return "🌧️"
    if "cloud" in desc:
        return "☁️"
    if "mist" in desc or "fog" in desc or "haze" in desc:
        return "🌫️"
    if "clear" in desc:
        return "☀️"
    return "🌤️"


@st.cache_data(show_spinner=False, ttl=900)
def fetch_dashboard_data(city: str):
    current = get_current_weather(city)
    forecast = get_forecast(city)
    return current, forecast


def build_daily_cards(forecast_list: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for item in forecast_list:
        date_key = item["dt_txt"].split(" ")[0]
        grouped.setdefault(date_key, []).append(item)

    cards = []
    for date_key, items in list(grouped.items())[:3]:
        representative = min(
            items,
            key=lambda x: abs(int(x["dt_txt"].split(" ")[1].split(":")[0]) - 12)
        )
        temps = [x["main"]["temp"] for x in items]
        hums = [x["main"]["humidity"] for x in items]
        cards.append(
            {
                "date": date_key,
                "temp": round(representative["main"]["temp"]),
                "min": round(min(temps)),
                "max": round(max(temps)),
                "humidity": round(sum(hums) / len(hums)),
                "desc": representative["weather"][0]["description"],
            }
        )
    return cards


def build_forecast_table_cards(forecast_list: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for item in forecast_list:
        date_key = item["dt_txt"].split(" ")[0]
        grouped.setdefault(date_key, []).append(item)

    cards = []
    for date_key, items in list(grouped.items())[:7]:
        representative = min(
            items,
            key=lambda x: abs(int(x["dt_txt"].split(" ")[1].split(":")[0]) - 12)
        )
        temps = [x["main"]["temp"] for x in items]
        hums = [x["main"]["humidity"] for x in items]
        rain_values = [x.get("pop", 0) for x in items]
        cards.append(
            {
                "date": date_key,
                "label": datetime.strptime(date_key, "%Y-%m-%d").strftime("%a"),
                "icon": weather_emoji(representative["weather"][0]["description"]),
                "temp": round(representative["main"]["temp"]),
                "min": round(min(temps)),
                "max": round(max(temps)),
                "humidity": round(sum(hums) / len(hums)),
                "rain_prob": round(max(rain_values) * 100),
            }
        )
    return cards


def get_rain_probability_series(forecast_list: list[dict]) -> pd.DataFrame:
    model_bundle = joblib.load(PROJECT_ROOT / "models" / "rain_model.pkl")
    model = model_bundle["model"]
    features = model_bundle["feature_names"]

    rows = []
    for item in forecast_list[:10]:
        model_input = {
            "MinTemp": item["main"]["temp_min"],
            "MaxTemp": item["main"]["temp_max"],
            "Humidity9am": item["main"]["humidity"],
            "Humidity3pm": item["main"]["humidity"],
            "Pressure9am": item["main"]["pressure"],
            "Pressure3pm": item["main"]["pressure"],
            "WindSpeed9am": item.get("wind", {}).get("speed", 0),
            "WindSpeed3pm": item.get("wind", {}).get("speed", 0),
        }

        df = pd.DataFrame([model_input])[features]
        probability = model.predict_proba(df)[0][1] * 100

        rows.append(
            {
                "time": datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%d %b\n%H:%M"),
                "temperature": item["main"]["temp"],
                "rain_probability": probability,
            }
        )

    return pd.DataFrame(rows)


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🌦️ WEATHER HUB</div>', unsafe_allow_html=True)

        st.markdown("### Theme")
        theme_choice = st.radio(
            "Choose theme",
            ["Dark", "Light", "System"],
            index=["Dark", "Light", "System"].index(st.session_state.theme_mode),
            horizontal=True,
            label_visibility="collapsed",
            key="theme_picker",
        )

        if theme_choice != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_choice
            st.rerun()

        st.markdown("---")

        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/1_Current_Weather.py", label="Current Weather", icon="📅")
        st.page_link("pages/2_Rain_Prediction.py", label="Model Predictions", icon="🧠")
        st.page_link("pages/3_Forecast_Analysis.py", label="Forecast Analysis", icon="📈")
        st.page_link("pages/4_Model_Insights.py", label="Model Insights", icon="🔬")
        st.page_link("pages/5_About_Project.py", label="About Project", icon="⚙️")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("Welcome to your ML-powered weather dashboard.")


render_sidebar()
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

if "city" not in st.session_state:
    st.session_state.city = "Berlin"

header_left, header_mid, header_right = st.columns([4, 4, 1.8])

with header_left:
    st.markdown('<div class="section-title">Home</div>', unsafe_allow_html=True)

with header_mid:
    city_input = st.text_input(
        "Search city",
        value=st.session_state.city,
        label_visibility="collapsed",
        placeholder="Search city..."
    )

with header_right:
    forecast_mode = st.selectbox(
        "Mode",
        ["Animated forecast", "Static forecast"],
        label_visibility="collapsed"
    )

search_col1, _ = st.columns([1, 6])
with search_col1:
    if st.button("Load city"):
        st.session_state.city = city_input.strip() or "Berlin"

city = st.session_state.city

try:
    current_weather, forecast_data = fetch_dashboard_data(city)

    top_cards = build_daily_cards(forecast_data)
    weekly_cards = build_forecast_table_cards(forecast_data)
    rain_df = get_rain_probability_series(forecast_data)

    hero_left, hero_right = st.columns([5.2, 2.3])

    with hero_left:
        emoji = weather_emoji(current_weather["weather"][0]["description"])
        location = f'{current_weather["name"]}, {current_weather["sys"]["country"]}'
        temp = round(current_weather["main"]["temp"])
        desc = current_weather["weather"][0]["description"].title()
        humidity = current_weather["main"]["humidity"]
        wind = current_weather.get("wind", {}).get("speed", 0)

        st.markdown(
            f"""
            <div class="top-card">
                <div style="display:flex; gap:22px; align-items:center; justify-content:space-between;">
                    <div style="display:flex; gap:24px; align-items:center;">
                        <div class="weather-emoji">{emoji}</div>
                        <div>
                            <div class="soft-label">{location}</div>
                            <div class="hero-title">{temp}°C, {desc}</div>
                            <div class="soft-label">Humidity: {humidity}% &nbsp;&nbsp;•&nbsp;&nbsp; Wind: {wind} m/s</div>
                            <div style="margin-top:10px;">
                                <span class="pill">Feels like {round(current_weather["main"]["feels_like"])}°C</span>
                                <span class="pill">Pressure {current_weather["main"]["pressure"]} hPa</span>
                                <span class="pill">Clouds {current_weather.get("clouds", {}).get("all", 0)}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_right:
        cols = st.columns(3)
        for idx, card in enumerate(top_cards):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class="mini-card">
                        <div class="soft-label">{datetime.strptime(card["date"], "%Y-%m-%d").strftime("%d %b")}</div>
                        <div style="font-size:2rem; margin:0.35rem 0;">{weather_emoji(card["desc"])}</div>
                        <div style="font-weight:700; font-size:1.35rem; color:{theme_tokens["text_main"]};">{card["temp"]}°C</div>
                        <div class="soft-label">{card["humidity"]}% humidity</div>
                        <div class="soft-label">{card["min"]}° / {card["max"]}°</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1.05, 1.1])

    with left_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Current Forecast</div>', unsafe_allow_html=True)
        st.markdown('<div class="soft-label">7-day style preview from the live forecast feed</div>', unsafe_allow_html=True)
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        day_cols = st.columns(7)
        for idx, card in enumerate(weekly_cards):
            with day_cols[idx]:
                st.markdown(
                    f"""
                    <div style="text-align:center;">
                        <div style="font-weight:700; color:{theme_tokens["text_main"]};">{card["label"]}</div>
                        <div style="font-size:1.8rem; margin:0.4rem 0;">{card["icon"]}</div>
                        <div style="font-size:1.05rem; font-weight:700; color:{theme_tokens["text_main"]};">{card["temp"]}°C</div>
                        <div class="soft-label">{card["min"]}° / {card["max"]}°</div>
                        <div class="soft-label">💧 {card["rain_prob"]}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Machine Learning Rain Outlook</div>', unsafe_allow_html=True)
        st.markdown('<div class="soft-label">Live forecast transformed into model-ready features</div>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=rain_df["time"],
                y=rain_df["rain_probability"],
                mode="lines+markers",
                name="Rain Probability",
                line=dict(width=3),
                fill="tozeroy",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=rain_df["time"],
                y=rain_df["temperature"],
                mode="lines+markers",
                name="Temperature",
                line=dict(width=3, dash="dot"),
                yaxis="y2",
            )
        )

        fig.update_layout(
            height=315,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme_tokens["text_main"]),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title="Rain %",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)" if st.session_state.theme_mode != "Light" else "rgba(15,23,42,0.08)",
                range=[0, 100]
            ),
            yaxis2=dict(
                title="Temp °C",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Features</div>', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    feature_data = [
        ("📡", "Live Data Sources", "OpenWeather current + forecast endpoints"),
        ("🧠", "Model Insights", "Random Forest model trained on Kaggle weather data"),
        ("⬇️", "Download Ready", "Exportable insights can be added on next page"),
        ("🔗", "Shareable UI", "Dashboard-style presentation for portfolio use"),
    ]

    for col, (icon, title, text) in zip([f1, f2, f3, f4], feature_data):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div style="font-size:1.8rem;">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="soft-label">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="footer-note">
            Powered by OpenWeather API + WeatherML • Modern dashboard UI built with Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )

except Exception as e:
    st.error(f"Could not load dashboard: {e}")
    st.info("Check your API key, internet connection, and model file.")