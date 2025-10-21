import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from branding.style_utils import inject_css, banner, set_altair_theme, COLORS

inject_css()
set_altair_theme()
banner(
    title="CX Sentiment Analyzer — Voice of Customer",
    subtitle="Upload customer feedback, classify sentiment, and explore insights.",
    emoji="💬"
)

st.markdown("""
Upload a CSV of customer feedback (or use the sample). The app will:
1) Label **sentiment** (Positive / Negative / Neutral)  
2) Classify **topics** (Onboarding, Billing, UI/UX, Performance, Support)  
3) Produce quick **charts** and a downloadable **labeled CSV**
""")

@st.cache_data
def load_sample():
    data = {
        "comment_text": [
            "I love how easy the setup was, super intuitive onboarding.",
            "Support was incredibly helpful and fast to respond.",
            "The app is slow and the interface feels confusing.",
            "I had a billing issue and the refund took too long.",
            "Amazing customer service and smooth experience."
        ]
    }
    return pd.DataFrame(data)

uploaded = st.file_uploader("Upload CSV (must include `comment_text` column)", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    df = load_sample()
    st.info("Using a small sample dataset — upload your own to replace.")

POS = {"love","great","awesome","helpful","fast","easy","intuitive","friendly","clear","smooth","reliable","fantastic","excellent","amazing","responsive","like","happy","satisfied","recommend","best"}
NEG = {"bug","slow","confusing","difficult","hate","bad","issue","error","broken","unhelpful","unclear","crash","complicated","annoying","frustrated","lag","problem","hard","wait"}

def simple_sentiment(text):
    toks = [t.strip(".,!?;:").lower() for t in str(text).split()]
    pos = sum(t in POS for t in toks)
    neg = sum(t in NEG for t in toks)
    score = pos - neg
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    return "Neutral"

df["sentiment"] = df["comment_text"].apply(simple_sentiment)

st.subheader("Labeled Preview")
st.dataframe(df, use_container_width=True)

chart = alt.Chart(df["sentiment"].value_counts().reset_index()).mark_bar().encode(
    x="index:N", y="sentiment:Q", color="index:N"
).properties(title="Sentiment Distribution")
st.altair_chart(chart, use_container_width=True)

st.download_button("⬇️ Download Labeled CSV", data=df.to_csv(index=False), file_name="sentiment_results.csv", mime="text/csv")
