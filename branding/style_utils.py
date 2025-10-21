import streamlit as st
import altair as alt

COLORS = {
    "bg": "#FFFFFF",
    "card": "#E8EEF1",
    "text": "#2F3437",
    "muted": "#6B7280",
    "accent": "#4A90E2",
    "border": "#B0BEC5"
}

def inject_css():
    st.markdown(
        f"""
        <style>
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
            color: {COLORS['text']};
        }}

        h1, h2, h3, h4 {{
            color: {COLORS['text']};
            letter-spacing: 0.2px;
        }}

        /* Buttons */
        .stButton>button {{
            border-radius: 8px;
            border: 1px solid {COLORS['border']};
            background: {COLORS['accent']};
            color: white;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .stButton>button:hover {{
            background: #3D7CC3;
            transform: translateY(-1px);
        }}

        /* Metric boxes */
        div[data-testid="stMetric"] {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            padding: 12px 16px;
        }}

        /* Table borders */
        .stDataFrame, .stTable {{
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
        }}

        /* File uploader */
        section[data-testid="stFileUploader"] > div {{
            background: {COLORS['card']};
            border: 1px dashed {COLORS['border']};
            border-radius: 10px;
        }}

        /* Subtle link */
        a {{
            color: {COLORS['accent']};
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def banner(title: str, subtitle: str, emoji: str = "✨"):
    st.markdown(
        f"""
        <div style="
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 22px;
            background: linear-gradient(135deg, rgba(74,144,226,0.08), rgba(232,238,241,0.9));
        ">
          <h1 style="margin:0; font-size: 1.9rem;">{emoji} {title}</h1>
          <p style="margin-top:6px; color:{COLORS['muted']};">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def set_altair_theme():
    def _theme():
        return {
            "config": {
                "view": {"strokeOpacity": 0, "continuousWidth": 400, "continuousHeight": 300},
                "background": "transparent",
                "axis": {
                    "labelColor": COLORS["muted"],
                    "titleColor": COLORS["muted"],
                    "gridColor": COLORS["border"]
                },
                "legend": {"labelColor": COLORS["text"], "titleColor": COLORS["text"]},
                "range": {
                    "category": [COLORS["acce]()]()
