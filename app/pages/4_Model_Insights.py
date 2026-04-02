from __future__ import annotations

from pathlib import Path
import sys

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.ui_theme import apply_theme, render_sidebar

st.set_page_config(page_title="Model Insights", page_icon="🔬", layout="wide")

theme = apply_theme()
render_sidebar()

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Model Insights</div>', unsafe_allow_html=True)

try:
    bundle = joblib.load(PROJECT_ROOT / "models" / "rain_model.pkl")
    model = bundle["model"]
    feature_names = bundle["feature_names"]

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame(
            {"Feature": feature_names, "Importance": model.feature_importances_}
        ).sort_values("Importance", ascending=False)
    else:
        importance_df = pd.DataFrame(
            {"Feature": feature_names, "Importance": [0] * len(feature_names)}
        )

    top1, top2, top3 = st.columns(3)
    cards = [
        ("Model Type", model.__class__.__name__),
        ("Features Used", str(len(feature_names))),
        ("Output", "Rain Tomorrow"),
    ]

    for col, (title, value) in zip([top1, top2, top3], cards):
        with col:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div style="font-size:1.2rem; font-weight:800; color:{theme["text_main"]};">{value}</div>
                    <div class="soft-label" style="margin-top:6px;">{title}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 0.9])

    with left:
        fig = go.Figure(
            go.Bar(
                x=importance_df["Importance"],
                y=importance_df["Feature"],
                orientation="h"
            )
        )
        fig.update_layout(
            height=420,
            title="Feature Importance",
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text_main"]),
            xaxis=dict(showgrid=True, gridcolor=theme["plot_grid"]),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown(
            """
            <div class="glass-card">
                <div class="section-title">Interpretation</div>
                <div class="soft-label" style="margin-top:10px;">
                    This page highlights how the trained Random Forest model prioritizes meteorological
                    features when making a rain classification. Higher importance values indicate stronger
                    influence on the model’s decision boundary.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="glass-card">
                <div class="section-title">Training Context</div>
                <div class="soft-label" style="margin-top:10px;">
                    Dataset: Kaggle weatherAUS<br>
                    Target: RainTomorrow<br>
                    Model family: Ensemble tree-based classification<br>
                    Deployment: Live API data transformed into training-compatible feature space
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.dataframe(importance_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Could not load model insights: {e}")