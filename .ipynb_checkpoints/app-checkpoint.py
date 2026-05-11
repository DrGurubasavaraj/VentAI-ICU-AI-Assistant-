import streamlit as st

from styles.theme_loader import load_theme

from ui.dashboard import render_dashboard
from data.patient_history import (
    initialize_history
)

st.set_page_config(
    page_title="ICU AI Assistant",
    layout="wide"
)

theme = st.sidebar.selectbox(
    "🎨 Theme",
    ["dark", "light"]
)

load_theme(theme)
initialize_history()

render_dashboard()