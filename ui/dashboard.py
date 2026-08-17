import os
import tempfile
from datetime import datetime
import streamlit as st

from logic.abg_engine import analyze_abg, calculate_anion_gap, calculate_delta_ratio
from logic.severity_engine import calculate_instability
from logic.ml_predictor import predict_patient
from logic.model_safety_engine import reconcile_model_signal
from logic.ventilator_engine import ventilator_considerations, prioritize_recommendations
from logic.oxygenation_engine import calculate_pf_ratio, oxygenation_band
from logic.trajectory_engine import trajectory_analysis, detect_deterioration
from logic.teaching_engine import teaching_points
from logic.reporting_engine import generate_summary
from ui.cards import clinical_card, metric_card, status_card
from ui.charts import abg_trend_chart
from ui.sidebar import render_sidebar
from data.patient_history import save_abg_entry, get_history
from utils.presets import presets
from utils.report_generator import generate_report


def _risk_status(severity):
    return {"Critical":"critical", "High Risk":"high", "Moderate":"moderate", "Low Risk":"low", "Stable":"low"}.get(severity, "neutral")


def _render_product_header():
    header_html = (
        '<div class="vai-product-header">'
        '<div class="vai-brand-block">'
        '<div class="vai-kicker">EXPLAINABLE CRITICAL-CARE DECISION SUPPORT</div>'
        '<div class="vai-product-title">VentAI Insight</div>'
        '<div class="vai-product-subtitle">ABG interpretation, oxygenation assessment and ventilator review prompts</div>'
        '</div>'
        '<div class="vai-header-meta">'
        '<div class="vai-chip-wrap">'
        '<span class="vai-chip">RESEARCH PROTOTYPE</span>'
        '<span class="vai-chip vai-chip-safe">CLINICIAN IN THE LOOP</span>'
        '</div>'
        '<div class="vai-developed-by">Developed by <strong>Dr. Gurubasavaraj</strong></div>'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)


def _render_mode_css(presentation_mode, screenshot_mode):
    css = []
    if screenshot_mode:
        css.append(
            '[data-testid="stHeader"]{display:none !important;} '
            'footer{display:none !important;} '
            '.block-container{padding-top:0.55rem !important;}'
        )
    if presentation_mode:
        css.append(
            '.block-container{max-width:1540px !important;padding-top:0.55rem !important;padding-bottom:0.8rem !important;} '
            '.vai-product-header{margin-bottom:0.65rem !important;}'
        )
    if css:
        st.markdown(f"<style>{''.join(css)}</style>", unsafe_allow_html=True)


def _render_inputs(preset):
    with st.container(border=True):
        st.markdown("### Patient inputs")
        abg_col, vent_col = st.columns(2)
        with abg_col:
            st.markdown("**ABG parameters**")
            ph = st.number_input("Arterial pH", value=float(preset.get("ph", 7.28)), step=0.01, format="%.2f")
            pco2 = st.number_input("PaCO2 (mmHg)", value=float(preset.get("pco2", 58.0)), step=1.0)
            hco3 = st.number_input("HCO3 (mEq/L)", value=float(preset.get("hco3", 24.0)), step=1.0)
            po2 = st.number_input("PaO2 (mmHg)", value=float(preset.get("po2", 68.0)), step=1.0)
        with vent_col:
            st.markdown("**Ventilator parameters**")
            rr = st.number_input("Respiratory rate (/min)", value=int(preset.get("rr", 16)), step=1)
            tv = st.number_input("Tidal volume (mL)", value=int(preset.get("tv", 500)), step=10)
            fio2 = st.number_input("FiO2", min_value=0.21, max_value=1.0, value=float(preset.get("fio2", 0.50)), step=0.01, format="%.2f")
            peep = st.number_input("PEEP (cmH2O)", min_value=0, max_value=30, value=int(preset.get("peep", 6)), step=1)
        with st.expander("Optional chemistry for anion-gap assessment"):
            chem1, chem2 = st.columns(2)
            with chem1:
                na = st.number_input("Sodium / Na (mEq/L)", value=float(preset.get("na", 140.0)), step=1.0)
            with chem2:
                cl = st.number_input("Chloride / Cl (mEq/L)", value=float(preset.get("cl", 104.0)), step=1.0)
        analyze = st.button("Analyze patient", use_container_width=True, type="primary")
    return {"ph":ph,"pco2":pco2,"hco3":hco3,"po2":po2,"rr":rr,"tv":tv,"fio2":fio2,"peep":peep,"na":na,"cl":cl,"analyze":analyze}


def _run_analysis(inputs, context):
    ph,pco2,hco3,po2 = inputs["ph"],inputs["pco2"],inputs["hco3"],inputs["po2"]
    rr,tv,fio2,peep = inputs["rr"],inputs["tv"],inputs["fio2"],inputs["peep"]
    na,cl = inputs["na"],inputs["cl"]
    abg = analyze_abg(ph,pco2,hco3)
    score,severity,alerts = calculate_instability(ph,pco2,po2)
    raw_signal,confidence,confidence_label = predict_patient(ph,pco2,hco3,po2,rr,tv,fio2,peep)
    model_signal,model_status,model_note = reconcile_model_signal(raw_signal,abg,pco2,hco3)
    pf_ratio,pf_text = calculate_pf_ratio(po2,fio2)
    oxy_band = oxygenation_band(pf_ratio)
    considerations = ventilator_considerations(pco2,po2,rr,tv,fio2,peep,abg=abg,hco3=hco3)
    high_priority,general = prioritize_recommendations(considerations)
    ag,ag_text = calculate_anion_gap(na,cl,hco3)
    delta,delta_text = calculate_delta_ratio(ag,hco3)
    save_abg_entry(ph,pco2,hco3,po2,fio2,severity)
    result = {"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"inputs":inputs,"context":context,"abg":abg,"score":score,"severity":severity,"alerts":alerts,
              "model_signal":model_signal,"model_status":model_status,"model_note":model_note,"confidence":confidence,"confidence_label":confidence_label,
              "pf_ratio":pf_ratio,"pf_text":pf_text,"oxygen_band":oxy_band,"considerations":considerations,"high_priority":high_priority,"general_considerations":general,
              "anion_gap":ag,"anion_gap_text":ag_text,"delta_ratio":delta,"delta_text":delta_text}
    st.session_state["latest_analysis"] = result
    return result


def _executive_impression(result):
    abg = result["abg"]
    compensation = abg.get("compensation_status") or abg.get("compensation")
    return (f"{abg['primary']} with {abg['state'].lower()}. ABG risk index is {result['severity'].lower()} ({result['score']}/100). "
            f"{compensation}. Oxygenation: P/F {result['pf_ratio']}, {result['pf_text'].lower()}.")


def _render_primary_row(result, presentation=False):
    ratios = [0.9, 1.35, 1.35, 1.05] if presentation else [1.0, 1.25, 1.25, 1.1]
    c1,c2,c3,c4 = st.columns(ratios)
    with c1:
        status_card(
            "ABG risk index",
            f"{result['severity']} · {result['score']}/100",
            status=_risk_status(result["severity"]),
            helper=None if presentation else "Derived from pH, PaCO2 and PaO2; excludes FiO2/PF and context vitals."
        )
    with c2:
        clinical_card("Primary disorder", result["abg"]["primary"], compact=True)
    with c3:
        clinical_card("Compensation", result["abg"].get("compensation_status") or "Review full context", compact=True)
    with c4:
        clinical_card("Oxygenation", f"P/F {result['pf_ratio']} · {result['pf_text']}", compact=True)


def _render_hero(result, presentation=False):
    left,right = st.columns([1.6,1])
    with left:
        with st.container(border=True):
            st.markdown("### Executive clinical impression")
            st.write(_executive_impression(result))
            if not presentation:
                st.caption(f"Latest analysis: {result['timestamp']} · Prototype decision support; clinician interpretation remains primary.")
            if result["model_status"] == "Physiology-model conflict":
                st.warning("Secondary model signal withheld because it conflicted with the physiological rule layer.")
            elif not presentation:
                st.caption(f"Secondary model signal: {result['model_signal']} ({result['confidence_label'].lower()}).")
    with right:
        with st.container(border=True):
            st.markdown("### Prioritized considerations")
            shown = 0
            for item in result["high_priority"]:
                st.markdown(f"- {item}")
                shown += 1
                if presentation and shown >= 2:
                    break
            if (not presentation or shown < 2):
                for item in result["general_considerations"]:
                    st.markdown(f"- {item}")
                    shown += 1
                    if presentation and shown >= 2:
                        break
            if not presentation:
                st.caption("Clinical consideration prompts only - not direct treatment instructions.")


def _render_context_strip(result):
    st.markdown("#### Physiological context")
    c1,c2,c3,c4 = st.columns(4)
    ctx=result["context"]
    with c1: metric_card("SpO2", f"{ctx['spo2']}%")
    with c2: metric_card("Heart rate", f"{ctx['heart_rate']} bpm")
    with c3: metric_card("MAP", f"{ctx['map_pressure']} mmHg")
    with c4: metric_card("Temperature", f"{ctx['temperature']:.1f} C")
    st.caption("Context vitals are shown for clinical orientation and are not included in the ABG risk index index.")


def _render_reasoning_tab(result):
    st.markdown("### Physiological reasoning")
    for index,item in enumerate(result["abg"]["reasoning"],start=1):
        with st.container(border=True):
            st.markdown(f"**Step {index}**")
            st.write(item)
    if result["alerts"]:
        st.markdown("#### Risk flags")
        for alert in result["alerts"]: st.write(f"- {alert}")
    st.markdown("#### Compensation detail")
    st.write(result["abg"]["compensation"])
    st.markdown("#### Chemistry")
    chem1,chem2=st.columns(2)
    with chem1: clinical_card("Anion gap", f"{result['anion_gap']:.1f} · {result['anion_gap_text']}", compact=True)
    with chem2:
        delta=result["delta_ratio"]
        value=f"{delta:.2f} · {result['delta_text']}" if delta is not None else result["delta_text"]
        clinical_card("Delta ratio", value, compact=True)
    st.markdown("#### Secondary model signal")
    clinical_card("Model pattern", result["model_signal"], compact=True)
    st.caption(f"{result['model_status']} · {result['confidence_label']} ({result['confidence']*100:.1f}%).")
    st.write(result["model_note"])
    points = teaching_points(result["abg"]["primary"])
    if points and points != ["No teaching pearls available."]:
        with st.expander("Teaching notes"):
            for point in points:
                st.write(f"- {point}")


def _render_trajectory_tab(result):
    history=get_history()
    st.caption(f"Current session: {len(history)} stored ABG analyses.")
    fig=abg_trend_chart(history, compact=False)
    if fig: st.plotly_chart(fig,use_container_width=True)
    else: st.info("Analyze at least two readings in this session to display trajectory.")
    trajectory=trajectory_analysis(history)
    deterioration=detect_deterioration(history)
    if trajectory:
        st.markdown("#### Trajectory interpretation")
        for item in trajectory: st.write(f"- {item}")
    if deterioration:
        st.markdown("#### Deterioration flags")
        for item in deterioration: st.warning(item)


def _render_ventilator_tab(result):
    st.caption("Ventilator outputs are review prompts only. They do not constitute autonomous ventilator-setting instructions.")
    if result["high_priority"]:
        st.markdown("### Higher-priority review")
        for item in result["high_priority"]: st.warning(item)
    st.markdown("### Additional considerations")
    for item in result["general_considerations"]: st.info(item)


def _render_report_tab(result):
    st.markdown("### Clinical report")
    summary=generate_summary(result["abg"],result["severity"],result["model_signal"],result["pf_ratio"],result["considerations"],
                             model_status=result["model_status"],model_note=result["model_note"],oxygenation_text=result["pf_text"],risk_score=result["score"])
    temp_path=None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf",delete=False) as tmp: temp_path=tmp.name
        generate_report(temp_path,summary)
        with open(temp_path,"rb") as f: pdf_bytes=f.read()
        st.download_button("Download clinical report",data=pdf_bytes,file_name="VentAI_Insight_Clinical_Report.pdf",mime="application/pdf",use_container_width=True)
    finally:
        if temp_path and os.path.exists(temp_path):
            try: os.remove(temp_path)
            except OSError: pass
    st.caption("Report generated from the current prototype analysis. Not a substitute for a clinical record or clinician judgment.")


def _render_presentation_view(result):
    st.markdown('<div class="vai-presentation-label">CONFERENCE VIEW</div>', unsafe_allow_html=True)
    _render_primary_row(result, presentation=True)
    _render_hero(result, presentation=True)

    history=get_history()
    fig=abg_trend_chart(history, compact=True)
    if fig:
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.caption("Add a second analysis to include serial trajectory in Presentation Mode.")

    st.markdown(
        '<div class="vai-presentation-footer">'
        'VentAI Insight · Research prototype · Clinician-in-the-loop decision support · '
        'Developed by Dr. Gurubasavaraj'
        '</div>',
        unsafe_allow_html=True
    )


def render_dashboard():
    selected_preset,presentation_mode,screenshot_mode,spo2,heart_rate,map_pressure,temperature=render_sidebar()
    _render_mode_css(presentation_mode,screenshot_mode)
    _render_product_header()
    preset={} if selected_preset=="Custom" else presets[selected_preset]
    context={"spo2":spo2,"heart_rate":heart_rate,"map_pressure":map_pressure,"temperature":temperature}

    if presentation_mode:
        result=st.session_state.get("latest_analysis")
        if result is None:
            st.info("Analyze a case first, then enable Presentation Mode.")
            return
        _render_presentation_view(result)
        return

    inputs=_render_inputs(preset)
    result=_run_analysis(inputs,context) if inputs["analyze"] else st.session_state.get("latest_analysis")
    if result is None:
        st.caption("Enter or load a scenario and select Analyze patient to generate the clinical cockpit.")
        return

    st.markdown("---")
    _render_primary_row(result)
    _render_hero(result)
    _render_context_strip(result)

    reasoning_tab,trajectory_tab,vent_tab,report_tab=st.tabs(["Clinical reasoning","Trajectory","Ventilator considerations","Report"])
    with reasoning_tab: _render_reasoning_tab(result)
    with trajectory_tab: _render_trajectory_tab(result)
    with vent_tab: _render_ventilator_tab(result)
    with report_tab: _render_report_tab(result)

    st.markdown("---")
    st.caption("VentAI Insight is a research and educational clinical decision-support prototype. It is not intended for autonomous diagnosis or treatment. Final decisions remain the responsibility of qualified clinicians.")
