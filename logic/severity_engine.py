def calculate_instability(ph, pco2, po2):

    score = 0
    alerts = []

    # -------------------------
    # pH Severity
    # -------------------------

    if ph < 7.1:
        score += 40
        alerts.append("Severe acidemia detected")

    elif ph < 7.25:
        score += 25
        alerts.append("Moderate acidemia detected")

    elif ph > 7.55:
        score += 30
        alerts.append("Severe alkalemia detected")

    # -------------------------
    # CO2 Severity
    # -------------------------

    if pco2 > 60:
        score += 25
        alerts.append("Severe hypercapnia")

    elif pco2 > 45:
        score += 15
        alerts.append("Hypercapnia detected")

    elif pco2 < 25:
        score += 20
        alerts.append("Severe hypocapnia")

    # -------------------------
    # Oxygenation Severity
    # -------------------------

    if po2 < 60:
        score += 30
        alerts.append("Severe hypoxemia")

    elif po2 < 80:
        score += 15
        alerts.append("Mild hypoxemia")

    # -------------------------
    # Final Severity
    # -------------------------

    if score >= 80:
        severity = "Critical"

    elif score >= 55:
        severity = "High Risk"

    elif score >= 30:
        severity = "Moderate"

    else:
        severity = "Stable"

    return score, severity, alerts