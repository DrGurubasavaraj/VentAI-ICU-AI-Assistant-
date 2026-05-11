import streamlit as st
from datetime import datetime


def initialize_history():

    if "abg_history" not in st.session_state:

        st.session_state.abg_history = []


def save_abg_entry(
    ph,
    pco2,
    hco3,
    po2,
    fio2,
    severity
):

    entry = {

        "time": datetime.now().strftime(
            "%H:%M:%S"
        ),

        "pH": ph,

        "PaCO2": pco2,

        "HCO3": hco3,

        "PaO2": po2,

        "FiO2": fio2,

        "Severity": severity
    }

    st.session_state.abg_history.append(entry)


def get_history():

    return st.session_state.abg_history