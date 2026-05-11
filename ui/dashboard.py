
import streamlit as st

from logic.abg_engine import analyze_abg
from logic.severity_engine import calculate_instability

from logic.ml_predictor import predict_patient

from logic.ventilator_engine import (
    ventilator_considerations
)

from logic.oxygenation_engine import (
    calculate_pf_ratio
)

from ui.gauges import (
    instability_gauge,
    pf_ratio_gauge
)

from ui.cards import (
    clinical_card,
    metric_card
)
from ui.sidebar import render_sidebar

from utils.presets import presets
from ui.charts import abg_trend_chart
from data.patient_history import (initialize_history)
from logic.trajectory_engine import (trajectory_analysis)
from logic.oxygenation_engine import (
    ards_classification
)
from data.patient_history import (
    save_abg_entry,
    get_history
)

from logic.explainability_engine import (
    explainability_score
)

from ui.gauges import explainability_gauge
from logic.trajectory_engine import (
    detect_deterioration
)
from logic.teaching_engine import (
    teaching_points
)
from ui.cards import risk_badge
from utils.report_generator import (
    generate_report
)

from logic.reporting_engine import (
    generate_summary
)
from logic.ventilator_engine import (
    prioritize_recommendations
)

st.markdown(
    """
    <div style="
        background-color:#0d1b2a;
        padding:14px;
        border-radius:14px;
        border:1px solid #1f2d3d;
        margin-bottom:20px;
    ">

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
    ">

    <div>
        <h3 style="margin:0;">
            ICU AI Monitoring System
        </h3>

        <p style="
            margin:0;
            color:#8c8c8c;
        ">
            Real-time ABG + Ventilator Analysis
        </p>
    </div>

    <div style="
        color:#52c41a;
        font-weight:bold;
        font-size:18px;
    ">
        ● LIVE SYSTEM
    </div>

    </div>

    </div>
    """,

    unsafe_allow_html=True
)



def render_dashboard():

    # -----------------------------------
    # SIDEBAR
    # -----------------------------------

    (
        selected_preset,
        presentation_mode,
        screenshot_mode,
        spo2,
        heart_rate,
        map_pressure,
        temperature
    ) = render_sidebar()

    # -----------------------------------
    # HEADER
    # -----------------------------------

    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0d1b2a, #102840);
            padding:28px;
            border-radius:18px;
            border:1px solid #1f2d3d;
            margin-bottom:20px;
        ">

        <h1 style="
            margin-bottom:5px;
            color:white;
            font-size:46px;
        ">
            🫁 VentAI (ICU AI Assistant)
        </h1>

        <p style="
            color:#d9d9d9;
            font-size:18px;
            margin-bottom:12px;
        ">
            Explainable ABG + Ventilator Clinical Decision Support
        </p>

        <p style="
            color:#8c8c8c;
            font-size:14px;
            margin:0;
        ">
            Developed by <b>Dr. Gurubasavaraj</b><br>
            Clinical AI & Critical Care Innovator
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
    status1, status2, status3, status4 = st.columns(4)

    with status1:

        st.success("🟢 AI Engine Active")

    with status2:

        st.info("📡 Monitoring Enabled")

    with status3:

        st.warning("🧠 Explainability Mode")

    with status4:

        st.error("⚡ ICU Decision Support")
    
    st.markdown("---")

    # -----------------------------------
    # LOAD PRESET
    # -----------------------------------

    preset = {}

    if selected_preset != "Custom":

        preset = presets[selected_preset]

    if screenshot_mode:

        st.markdown(
            """
            <style>

            footer {
                visibility: hidden;
            }

            header {
                visibility: hidden;
            }

            .block-container {
                padding-top: 1rem;
            }

            </style>
            """,

            unsafe_allow_html=True
        )

    # -----------------------------------
    # INPUT SECTION
    # -----------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("ABG Parameters")

        ph = st.number_input(
            "Arterial pH",
            value=preset.get("ph", 7.28)
        )

        pco2 = st.number_input(
            "PaCO₂ (mmHg)",
            value=preset.get("pco2", 58.0)
        )

        hco3 = st.number_input(
            "HCO₃⁻ (mEq/L)",
            value=preset.get("hco3", 24.0)
        )

        po2 = st.number_input(
            "PaO₂ (mmHg)",
            value=preset.get("po2", 68.0)
        )

    with col2:

        st.subheader("Ventilator Parameters")

        rr = st.number_input(
            "Respiratory Rate",
            value=preset.get("rr", 16)
        )

        tv = st.number_input(
            "Tidal Volume (mL)",
            value=preset.get("tv", 500)
        )

        fio2 = st.number_input(
            "FiO₂",
            value=preset.get("fio2", 0.5)
        )

        peep = st.number_input(
            "PEEP",
            value=preset.get("peep", 6)
        )

    # -----------------------------------
    # ANALYZE BUTTON
    # -----------------------------------

    analyze = st.button(
        "🔍 Analyze Patient",
        use_container_width=True
    )

    # -----------------------------------
    # MAIN ANALYSIS
    # -----------------------------------

    if analyze:

        # -----------------------------------
        # ABG ANALYSIS
        # -----------------------------------

        abg = analyze_abg(
            ph,
            pco2,
            hco3
        )

        # -----------------------------------
        # SEVERITY
        # -----------------------------------

        score, severity, alerts = (
            calculate_instability(
                ph,
                pco2,
                po2
            )
        )

        # -----------------------------------
        # SAVE SESSION
        # -----------------------------------

        save_abg_entry(
            ph,
            pco2,
            hco3,
            po2,
            fio2,
            severity
        )

        # -----------------------------------
        # ML PREDICTION
        # -----------------------------------

        prediction, confidence, conf_label = (
            predict_patient(
                ph,
                pco2,
                hco3,
                po2,
                rr,
                tv,
                fio2,
                peep
            )
        )

        # -----------------------------------
        # OXYGENATION
        # -----------------------------------

        pf_ratio, pf_text = (
            calculate_pf_ratio(
                po2,
                fio2
            )
        )

        ards_status = (
            ards_classification(
                pf_ratio
            )
        )

        # -----------------------------------
        # VENTILATOR CONSIDERATIONS
        # -----------------------------------

        vent_considerations = (
            ventilator_considerations(
                pco2,
                po2,
                rr,
                tv,
                fio2,
                peep
            )
        )

        # -----------------------------------
        # ALERT BANNER
        # -----------------------------------

        if severity == "Critical":

            st.error(
                "🔴 CRITICAL PHYSIOLOGICAL INSTABILITY"
            )

        elif severity == "High Risk":

            st.warning(
                "🟠 HIGH RISK ABG PROFILE"
            )

        elif severity == "Moderate":

            st.info(
                "🟡 MODERATE PHYSIOLOGICAL DISTURBANCE"
            )

        else:

            st.success(
                "🟢 RELATIVELY STABLE PROFILE"
            )

        # -----------------------------------
        # METRIC STRIP
        # -----------------------------------

        from ui.cards import metric_card

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:

            metric_card(
                "Arterial pH",
                ph,
                color="#ff4d4f"
            )

        with metric2:

            metric_card(
                "PaCO₂ (mmHg)",
                f"{pco2}",
                color="#faad14"
            )

        with metric3:

            metric_card(
                "PaO₂ (mmHg)",
                f"{po2}",
                color="#52c41a"
            )

        with metric4:

            metric_card(
                "Instability Level",
                severity,
                color="#1f77ff"
            )

        st.markdown("---")

        # -----------------------------------
        # AI SUMMARY
        # -----------------------------------

        st.subheader("🤖 AI Clinical Summary")

        ai1, ai2, ai3 = st.columns(3)

        with ai1:

            clinical_card(
                "AI Interpretation",
                prediction
            )

        with ai2:

            clinical_card(
                "Interpretive Confidence",
                conf_label
            )

        with ai3:

            clinical_card(
                "P/F Ratio",
                f"{pf_ratio} → {pf_text}"
            )

            clinical_card(
                "ARDS Pattern",
                ards_status
            )

        st.markdown("---")

        st.subheader("🩺 Executive Clinical Impression")

        summary_text = f"""

        Primary physiology suggests
        {abg['primary']} with
        {abg['state'].lower()}.

        Current instability level is classified as
        {severity}.

        Oxygenation profile demonstrates
        {pf_text.lower()} with a P/F ratio of
        {pf_ratio}.

        Interpretation confidence:
        {conf_label.lower()}.
        """

        st.markdown(
            f"""
            <div style="
                background-color:#0d1b2a;
                padding:22px;
                border-radius:16px;
                border-left:6px solid #1f77ff;
                line-height:1.8;
                font-size:18px;
            ">
            {summary_text}
            </div>
            """,

            unsafe_allow_html=True
        )

        # -----------------------------------
        # MAIN OUTPUT
        # -----------------------------------

        left, right = st.columns([2, 1])

        with left:

            clinical_card(
                "Primary Disorder",
                abg["primary"]
            )

            clinical_card(
                "Acid-Base State",
                abg["state"]
            )

            clinical_card(
                "Compensation",
                abg["compensation"]
            )

        with right:

            fig = instability_gauge(score)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            pf_fig = pf_ratio_gauge(
                pf_ratio
            )

            st.plotly_chart(
                pf_fig,
                use_container_width=True
            )

        # -----------------------------------
        # SESSION HISTORY
        # -----------------------------------

        history = get_history()

        st.markdown("---")

        st.markdown(
            f"""
            <div style="
                background-color:#0d1b2a;
                padding:14px;
                border-radius:12px;
                border-left:5px solid #1f77ff;
                margin-bottom:15px;
            ">

            <h4 style="margin-bottom:5px;">
                🗂 Current ICU Session
            </h4>

            <p style="margin:0;">
                Stored ABG Analyses: <b>{len(history)}</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------------
        # TREND CHARTS
        # -----------------------------------

        st.subheader("📈 Serial ABG Trends")

        trend_fig = abg_trend_chart(history)

        if trend_fig:

            st.plotly_chart(
                trend_fig,
                use_container_width=True
            )

        else:

            st.info(
                "At least two analyses are required to display trends."
            )

        # -----------------------------------
        # TRAJECTORY INSIGHTS
        # -----------------------------------

        trajectory = trajectory_analysis(history)

        if trajectory:

            st.markdown("---")

            st.subheader(
                "📊 ICU Trajectory Insights"
            )

            for item in trajectory:

                st.warning(f"• {item}")

        # -----------------------------------
        # REASONING PANEL
        # -----------------------------------

        with st.expander(
            "🧠 AI Clinical Reasoning"
        ):

            step = 1

            for item in abg["reasoning"]:

                st.markdown(
                    f"""
                    <div style="
                        background-color:#0d1b2a;
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:10px;
                        border-left:4px solid #1f77ff;
                    ">

                    <b>Step {step}</b><br>
                    {item}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                step += 1

            for alert in alerts:

                st.warning(alert)

        # -----------------------------------
        # VENTILATOR CONSIDERATIONS
        # -----------------------------------

        st.markdown("---")

        st.subheader(
            "🫁 Ventilator Considerations"
        )

        for item in vent_considerations:

            st.info(f"• {item}")

        # -----------------------------------
        # CLINICAL PEARLS
        # -----------------------------------

        st.markdown("---")

        st.subheader("📚 Clinical Pearls")

        pearls = [

            "Respiratory acidosis commonly reflects hypoventilation physiology.",

            "P/F ratio below 200 suggests significant oxygenation impairment.",

            "Compensation patterns help identify mixed acid-base disorders.",

            "Persistent hypercapnia despite high ventilation may indicate increased dead space."
        ]

        for pearl in pearls:

            st.success(f"• {pearl}")

        # -----------------------------------
        # PDF REPORT EXPORT
        # -----------------------------------

        st.markdown("---")

        st.subheader("📄 Export Clinical Report")

        summary = generate_summary(
            abg,
            severity,
            prediction,
            pf_ratio,
            vent_considerations
        )

        report_path = "icu_ai_report.pdf"

        generate_report(
            report_path,
            summary
        )

        with open(report_path, "rb") as pdf_file:

            st.download_button(

                label="⬇ Download ICU Clinical Report",

                data=pdf_file,

                file_name="icu_ai_report.pdf",

                mime="application/pdf",

                use_container_width=True
            )

        st.markdown("---")

        st.caption(
            """
            This platform is intended for clinical decision support,
            physiological interpretation assistance,
            and educational use only.

            Final medical decisions remain the responsibility
            of licensed clinicians.
            """
        )
