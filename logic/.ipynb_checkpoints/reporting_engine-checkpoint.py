from datetime import datetime

def generate_summary(
    abg,
    severity,
    prediction,
    pf_ratio,
    vent_considerations
):


    summary = []

    summary.append(
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    summary.append(
        f"<b>Primary Disorder:</b> {abg['primary']}"
    )

    summary.append(
        f"<b>Acid-Base State:</b> {abg['state']}"
    )

    summary.append(
        f"<b>Severity Classification:</b> {severity}"
    )

    summary.append(
        f"<b>AI Interpretation:</b> {prediction}"
    )

    summary.append(
        f"<b>P/F Ratio:</b> {pf_ratio}"
    )

    summary.append(
        f"<b>Compensation:</b> {abg['compensation']}"
    )

    summary.append(
        "<b>Ventilator Considerations:</b>"
    )

    for item in vent_considerations:

        summary.append(f"• {item}")

    return summary