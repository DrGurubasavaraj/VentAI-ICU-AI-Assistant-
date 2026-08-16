from datetime import datetime


def generate_summary(abg, severity, model_signal, pf_ratio, vent_considerations, model_status=None, model_note=None, oxygenation_text=None, risk_score=None):
    summary = []
    summary.append(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("<b>System:</b> VentAI Insight - research prototype / clinician-in-the-loop")
    summary.append(f"<b>Primary Disorder:</b> {abg['primary']}")
    summary.append(f"<b>Acid-Base State:</b> {abg['state']}")
    summary.append(f"<b>Compensation:</b> {abg.get('compensation_status', abg.get('compensation', ''))}")
    risk_text = severity if risk_score is None else f"{severity} ({risk_score}/100)"
    summary.append(f"<b>ABG / Oxygenation Risk:</b> {risk_text}")
    if oxygenation_text:
        summary.append(f"<b>Oxygenation:</b> P/F ratio {pf_ratio} - {oxygenation_text}")
    else:
        summary.append(f"<b>P/F Ratio:</b> {pf_ratio}")
    summary.append(f"<b>Secondary Model Signal:</b> {model_signal}")
    if model_status:
        summary.append(f"<b>Model Safety Status:</b> {model_status}")
    if model_note:
        summary.append(f"<b>Model Safety Note:</b> {model_note}")
    summary.append("<b>Clinical Consideration Prompts:</b>")
    for item in vent_considerations:
        summary.append(f"- {item}")
    summary.append("<b>Safety:</b> Decision-support / educational prototype only. Not for autonomous treatment decisions.")
    return summary
