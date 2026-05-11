def trajectory_analysis(history):

    if len(history) < 2:

        return []

    insights = []

    latest = history[-1]
    previous = history[-2]

    # -------------------------
    # pH Trend
    # -------------------------

    if latest["pH"] < previous["pH"]:

        insights.append(
            "Acidemia appears to be worsening over time."
        )

    else:

        insights.append(
            "Acid-base status shows relative improvement."
        )

    # -------------------------
    # Oxygenation
    # -------------------------

    if latest["PaO2"] < previous["PaO2"]:

        insights.append(
            "Oxygenation trajectory appears unfavorable."
        )

    else:

        insights.append(
            "Oxygenation profile shows interval improvement."
        )

    # -------------------------
    # FiO2 Escalation
    # -------------------------

    if latest["FiO2"] > previous["FiO2"]:

        insights.append(
            "Increasing FiO₂ requirements detected."
        )

    return insights

def detect_deterioration(history):

    if len(history) < 3:

        return []

    warnings = []

    latest = history[-1]
    previous = history[-2]

    # -------------------------
    # Progressive Acidemia
    # -------------------------

    if latest["pH"] < previous["pH"]:

        warnings.append(
            "Progressive worsening acidemia detected."
        )

    # -------------------------
    # Oxygenation
    # -------------------------

    if latest["PaO2"] < previous["PaO2"]:

        warnings.append(
            "Declining oxygenation trajectory detected."
        )

    # -------------------------
    # Escalating FiO2
    # -------------------------

    if latest["FiO2"] > previous["FiO2"]:

        warnings.append(
            "Increasing oxygen requirements detected."
        )

    return warnings