import streamlit as st
from utils.presets import presets


def render_sidebar():
    st.sidebar.title("VentAI Context")
    st.sidebar.caption("Physiological context + demo controls")

    selected_preset = st.sidebar.selectbox("ICU scenario", ["Custom"] + list(presets.keys()))
    presentation_mode = st.sidebar.toggle("Presentation Mode", help="Shows a condensed conference/demo layout using the latest analyzed case.")
    screenshot_mode = st.sidebar.toggle("Screenshot Mode", help="Reduces Streamlit chrome for cleaner captures.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Physiological context")
    spo2 = st.sidebar.number_input("SpO2 (%)", min_value=0, max_value=100, value=92)
    heart_rate = st.sidebar.number_input("Heart rate (bpm)", min_value=20, max_value=250, value=118)
    map_pressure = st.sidebar.number_input("MAP (mmHg)", min_value=20, max_value=180, value=68)
    temperature = st.sidebar.number_input("Temperature (C)", min_value=25.0, max_value=45.0, value=38.4, step=0.1)
    st.sidebar.caption("These context vitals are displayed separately and are not included in the ABG / oxygenation risk index.")

    st.sidebar.markdown("---")
    if st.sidebar.button("Clear current session", use_container_width=True):
        st.session_state.abg_history = []
        st.session_state.pop("latest_analysis", None)
        st.sidebar.success("Session cleared.")

    return selected_preset, presentation_mode, screenshot_mode, spo2, heart_rate, map_pressure, temperature
