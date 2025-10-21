import streamlit as st
import altair as alt

# Brand tokens
COLORS = {
    "bg": "#0F172A",
    "card": "#111827",
    "text": "#E5E7EB",
    "muted": "#94A3B8",
    "accent": "#38BDF8",   # sky
    "success": "#34D399",  # mint
    "danger": "#F87171"    # coral/red
}

def inject_css():
    st.markdown(
        f"""
        <style>
        /* Global */
        .block-container {{
            padding-top: 2.0rem;
            padding-bottom: 4rem;
            max-width: 1200px;
        }}
        h1, h2, h3, h4, h5, h6 {{ letter-spacing: 0.2px; }}
        /* Buttons */
        .stButton>button {{
            border-radius: 10px;
            border: 1px solid rgba(56,189,248,.35);
            background: {COLORS["accent"]};
            color: #0B1221;
            font-weight: 700;
            transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
        }}
        .stButton>button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(56,189,248,.25);
        }}
        /* Metric cards */
        div[data-testid="stMetric"] {{
            background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,0));
            border: 1px solid rgba(148,163,184,.18);
            padding: 14px 16px;
            border-radius: 14px;
        }}
        /* Tables */
        .stDataFrame, .stTable {{
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(148,163,184,.18);
        }}
        /* File uploader */
        section[data-testid="stFileUploader"] > div {{
            background: {COLORS["card"]};
            border: 1px dashed rgba(148,163,184,.35);
            border-radius: 14px;
        }}
        /* Subtle link style */
        a {{
            color: {COLORS["accent"]};
            text-decoration: none;
        }}
        a:hover {{ text-decoration: underline; }}
        </style>
        """,
        unsafe_allow_html=True
    )

def banner(title: str, subtitle: str, emoji: str = "✨"):
    st.markdown(
        f"""
        <div style="
            border: 1px solid rgba(148,163,184,.18);
            border-radius: 18px;
            padding: 22px 20px;
            margin-bottom: 18px;
            background: linear-gradient(135deg, rgba(56,189,248,.10), rgba(52,211,153,.08));
        ">
          <h1 style="margin:0; font-size: 1.9rem;">{emoji} {title}</h1>
          <p style="margin: 6px 0 0; color:{COLORS['muted']};">
            {subtitle}
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def set_altair_theme():
    # Unified chart theme
    def _theme():
        return {
            "config": {
                "view": {"strokeOpacity": 0, "continuousWidth": 400, "continuousHeight": 300},
                "background": "transparent",
                "axis": {
                    "labelColor": COLORS["muted"],
                    "titleColor": COLORS["muted"],
                    "gridColor": "#1F2937"
                },
                "legend": {"labelColor": COLORS["text"], "titleColor": COLORS["text"]},
                "range": {
                    "category": [COLORS["accent"], COLORS["success"], COLORS["muted"], "#F59E0B", "#A78BFA"]
                }
            }
        }
    alt.themes.register("ms_insight", _theme)
    alt.themes.enable("ms_insight")
