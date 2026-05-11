import streamlit as st


def load_theme(theme="dark"):

    css_path = f"styles/{theme}_theme.css"

    with open(css_path) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )