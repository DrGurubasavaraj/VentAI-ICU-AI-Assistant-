import streamlit as st

from styles.theme_loader import load_theme
from ui.dashboard import render_dashboard
from data.patient_history import initialize_history


st.set_page_config(
    page_title="VentAI Insight",
    layout="wide",
)

try:
    active_theme = st.context.theme.type
except Exception:
    active_theme = "dark"

if active_theme not in ("dark", "light"):
    active_theme = "dark"

load_theme(active_theme)
initialize_history()
render_dashboard()
