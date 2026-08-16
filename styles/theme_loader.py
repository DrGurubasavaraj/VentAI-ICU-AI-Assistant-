import os
import streamlit as st


def load_theme(theme="dark"):
    base_dir=os.path.dirname(os.path.dirname(__file__))
    paths=[os.path.join(base_dir,"styles",f"{theme}_theme.css"), os.path.join(base_dir,"styles","v2_cockpit.css")]
    for css_path in paths:
        with open(css_path,encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
