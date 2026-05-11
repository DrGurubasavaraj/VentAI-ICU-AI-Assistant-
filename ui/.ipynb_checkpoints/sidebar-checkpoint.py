import streamlit as st

from utils.presets import presets


def render_sidebar():

    st.sidebar.title("🩺 ICU Monitor")

    st.sidebar.markdown("---")

    selected_preset = st.sidebar.selectbox(
        "Load ICU Scenario",
        ["Custom"] + list(presets.keys())
    )
    presentation_mode = st.sidebar.toggle(
        "🎤 Presentation Mode"
    )
    screenshot_mode = st.sidebar.toggle(
        "📸 Screenshot Mode"
    )
    st.sidebar.markdown("---")

    spo2 = st.sidebar.number_input(
        "SpO₂ (%)",
        value=92
    )

    heart_rate = st.sidebar.number_input(
        "Heart Rate (bpm)",
        value=118
    )

    map_pressure = st.sidebar.number_input(
        "MAP (mmHg)",
        value=68
    )

    temperature = st.sidebar.number_input(
        "Temperature (°C)",
        value=38.4
    )

    return (
        selected_preset,
        presentation_mode,
        screenshot_mode,
        spo2,
        heart_rate,
        map_pressure,
        temperature
    )

    
if st.sidebar.button("🗑 Clear Session"):

    st.session_state.abg_history = []

    st.sidebar.success(
        "Session history cleared."
    )