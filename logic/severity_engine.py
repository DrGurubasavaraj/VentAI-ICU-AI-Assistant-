def calculate_instability(ph, pco2, po2):
    """
    ABG / oxygenation risk index.

    IMPORTANT:
    - This is not a whole-patient ICU severity score.
    - HR, MAP, SpO2, temperature and other clinical variables are not included here.
    """

    score = 0
    alerts = []

    # -------------------------
    # pH risk
    # -------------------------
    if ph < 7.10:
        score += 50
        alerts.append("Profound acidemia detected")
    elif ph < 7.20:
        score += 40
        alerts.append("Marked acidemia detected")
    elif ph < 7.30:
        score += 30
        alerts.append("Moderate acidemia detected")
    elif ph < 7.35:
        score += 15
        alerts.append("Mild acidemia detected")
    elif ph > 7.60:
        score += 40
        alerts.append("Marked alkalemia detected")
    elif ph > 7.55:
        score += 30
        alerts.append("Moderate alkalemia detected")
    elif ph > 7.45:
        score += 15
        alerts.append("Mild alkalemia detected")

    # -------------------------
    # PaCO2 risk
    # -------------------------
    if pco2 >= 70:
        score += 20
        alerts.append("Marked hypercapnia detected")
    elif pco2 > 45:
        score += 10
        alerts.append("Hypercapnia detected")
    elif pco2 <= 20:
        score += 20
        alerts.append("Marked hypocapnia detected")
    elif pco2 < 35:
        score += 10
        alerts.append("Hypocapnia detected")

    # -------------------------
    # PaO2 risk
    # -------------------------
    if po2 < 60:
        score += 30
        alerts.append("Severe hypoxemia detected")
    elif po2 < 80:
        score += 15
        alerts.append("Impaired oxygenation detected")

    score = min(score, 100)

    # -------------------------
    # Final ABG / O2 risk band
    # -------------------------
    if score >= 70:
        severity = "Critical"
    elif score >= 35:
        severity = "High Risk"
    elif score >= 15:
        severity = "Moderate"
    else:
        severity = "Low Risk"

    return score, severity, alerts
