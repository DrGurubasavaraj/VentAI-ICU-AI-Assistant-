import streamlit as st


def clinical_card(title, value, border_color="#1f77ff"):

    st.markdown(
        f"""
        <div style="
            background-color:#0d1b2a;
            padding:18px;
            border-radius:14px;
            border-left:6px solid {border_color};
            margin-bottom:15px;
        ">

        <h4 style="margin-bottom:10px;">
            {title}
        </h4>

        <p style="font-size:18px;">
            {value}
        </p>

        </div>
        """,

        unsafe_allow_html=True
    )

def metric_card(
    title,
    value,
    delta=None,
    color="#1f77ff"
):

    delta_html = ""

    if delta:

        delta_html = f"""
        <p style="
            color:{color};
            margin-top:8px;
            font-size:14px;
        ">
            {delta}
        </p>
        """

    st.markdown(
        f"""
        <div style="
            background-color:#0d1b2a;
            padding:18px;
            border-radius:16px;
            border:1px solid #1f2d3d;
            text-align:center;
            margin-bottom:12px;
        ">

        <h4 style="
            font-size:20px;
            margin-bottom:10px;
            color:#d9d9d9;
        ">

        <h1 style="
            font-size:38px;
            font-weight:700;
            margin-bottom:0px;
            color:{color};
        ">
            {value}
        </h2>

        {delta_html}

        </div>
        """,

        unsafe_allow_html=True
    )

def risk_badge(severity):

    colors = {

        "Critical": "#ff4d4f",

        "High Risk": "#ff7a45",

        "Moderate": "#faad14",

        "Stable": "#52c41a"
    }

    color = colors.get(
        severity,
        "#1f77ff"
    )

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:10px;
            border-radius:10px;
            text-align:center;
            font-weight:bold;
            color:white;
            margin-bottom:15px;
        ">
            {severity}
        </div>
        """,

        unsafe_allow_html=True
    )