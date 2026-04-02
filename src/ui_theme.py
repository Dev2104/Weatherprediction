from __future__ import annotations

import streamlit as st


def get_theme_tokens(theme_mode: str) -> dict:
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
            "plot_grid": "rgba(15,23,42,0.08)",
        }

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
        "plot_grid": "rgba(255,255,255,0.08)",
    }


def ensure_theme_state():
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Dark"


def apply_theme():
    ensure_theme_state()
    t = get_theme_tokens(st.session_state.theme_mode)

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
                radial-gradient(circle at top left, {t["bg_grad_1"]}, transparent 28%),
                radial-gradient(circle at top right, {t["bg_grad_2"]}, transparent 22%),
                linear-gradient(180deg, {t["bg_main"]} 0%, {t["bg_main"]} 100%);
            color: {t["text_main"]};
        }}
        div[data-testid="stSidebarNav"] {{
            display: none;
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {t["sidebar_bg_1"]} 0%, {t["sidebar_bg_2"]} 100%);
            border-right: 1px solid {t["border"]};
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            padding-top: 1rem;
        }}
        .block-container {{
            padding-top: 0.7rem !important;
            padding-bottom: 1rem;
            max-width: 1450px;
        }}
        .top-card, .glass-card, .mini-card, .feature-card {{
            background: linear-gradient(180deg, {t["card_bg_1"]}, {t["card_bg_2"]});
            border: 1px solid {t["border"]};
            border-radius: 22px;
            box-shadow: {t["shadow"]};
            backdrop-filter: blur(12px);
        }}
        .top-card {{
            padding: 24px 28px;
            min-height: 210px;
        }}
        .glass-card {{
            padding: 20px 22px 16px 22px;
            min-height: 200px;
        }}
        .mini-card {{
            padding: 18px 16px;
            text-align: center;
            min-height: 140px;
        }}
        .feature-card {{
            padding: 18px 20px;
            min-height: 105px;
        }}
        .soft-label {{
            color: {t["text_soft"]};
            font-size: 0.95rem;
        }}
        .section-title {{
            font-size: 1.55rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            color: {t["text_main"]};
        }}
        .hero-title {{
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
            color: {t["text_main"]};
        }}
        .weather-emoji {{
            font-size: 5.2rem;
            line-height: 1;
        }}
        .pill {{
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            background: {t["pill_bg"]};
            border: 1px solid {t["pill_border"]};
            color: {t["pill_text"]};
            font-size: 0.88rem;
            margin-right: 0.45rem;
            margin-top: 0.35rem;
        }}
        .sidebar-brand {{
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            color: {t["text_main"]};
        }}
        .feature-title {{
            font-weight: 700;
            font-size: 1.12rem;
            margin-bottom: 0.25rem;
            color: {t["text_main"]};
        }}
        .footer-note {{
            text-align: center;
            color: {t["text_soft"]};
            font-size: 0.9rem;
            margin-top: 0.8rem;
        }}
        .stTextInput > div > div,
        .stSelectbox > div > div,
        .stButton > button,
        .stNumberInput > div > div,
        .stSlider {{
            border-radius: 14px !important;
        }}
        .stTextInput input, .stNumberInput input {{
            background: {t["input_bg"]} !important;
            color: {t["text_main"]} !important;
            border: 1px solid {t["border"]} !important;
        }}
        .stSelectbox div[data-baseweb="select"] > div {{
            background: {t["input_bg"]} !important;
            color: {t["text_main"]} !important;
            border: 1px solid {t["border"]} !important;
        }}
        .stButton > button {{
            background: linear-gradient(90deg, {t["button_grad_1"]}, {t["button_grad_2"]}) !important;
            color: white !important;
            border: none !important;
            padding: 0.6rem 1rem !important;
            font-weight: 600 !important;
        }}
        .stButton > button:hover {{
            filter: brightness(1.06);
        }}
        a[data-testid="stPageLink-NavLink"] {{
            background: {t["nav_bg"]};
            border: 1px solid {t["border"]};
            border-radius: 14px;
            margin-bottom: 0.45rem;
            padding: 0.25rem 0.45rem;
        }}
        a[data-testid="stPageLink-NavLink"] p {{
            color: {t["text_main"]} !important;
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return t


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
            key="theme_picker_sidebar",
        )

        if theme_choice != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_choice
            st.rerun()

        st.markdown("---")
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/1_Current_Weather.py", label="Current Weather", icon="🌤️")
        st.page_link("pages/2_Rain_Prediction.py", label="Rain Prediction", icon="🧠")
        st.page_link("pages/3_Forecast_Analysis.py", label="Forecast Analysis", icon="📈")
        st.page_link("pages/4_Model_Insights.py", label="Model Insights", icon="🔬")
        st.page_link("pages/5_About_Project.py", label="About Project", icon="⚙️")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("WeatherML • Real-time insights with custom UI")


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