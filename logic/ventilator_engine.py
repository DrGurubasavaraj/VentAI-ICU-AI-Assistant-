def _pf_band(po2, fio2):
    if fio2 <= 0:
        return None, "unavailable"

    pf = po2 / fio2

    if pf <= 100:
        return pf, "severe"
    elif pf <= 200:
        return pf, "moderate"
    elif pf <= 300:
        return pf, "mild"
    else:
        return pf, "preserved"


def ventilator_considerations(
    pco2,
    po2,
    rr,
    tv,
    fio2,
    peep,
    abg=None,
    hco3=None
):
    """
    Generate clinician-facing review prompts only.
    No direct ventilator-setting instructions are produced.
    """
    considerations = []
    primary = (abg or {}).get("primary", "")

    # Handle mixed disorders before generic PaCO2 rules.
    if primary == "Mixed Respiratory + Metabolic Acidosis":
        considerations.append(
            "Combined respiratory and metabolic acidifying processes are present; "
            "review ventilation adequacy while addressing the metabolic driver."
        )

    elif primary == "Mixed Respiratory + Metabolic Alkalosis":
        considerations.append(
            "Combined respiratory and metabolic alkalinizing processes are present; "
            "review the drivers of both processes before considering any ventilator change."
        )

    elif primary == "Metabolic Acidosis" and hco3 is not None:
        expected = (1.5 * hco3) + 8
        low, high = expected - 2, expected + 2

        if low <= pco2 <= high:
            considerations.append(
                "Observed PaCO2 is within the expected respiratory compensatory range; "
                "avoid interpreting compensatory hypocapnia as isolated overventilation."
            )
        elif pco2 > high:
            considerations.append(
                "PaCO2 is above the expected compensatory range for metabolic acidosis; "
                "review ventilation adequacy and concurrent respiratory acidosis."
            )
        else:
            considerations.append(
                "PaCO2 is below the expected compensatory range; review for a concurrent "
                "respiratory alkalosis process."
            )

    elif primary == "Metabolic Alkalosis" and hco3 is not None:
        expected = 40 + 0.7 * (hco3 - 24)
        low, high = expected - 5, expected + 5

        if low <= pco2 <= high:
            considerations.append(
                "Observed PaCO2 is compatible with expected respiratory compensation for "
                "metabolic alkalosis; avoid interpreting the compensatory rise in PaCO2 "
                "in isolation as inadequate ventilation."
            )
        elif pco2 > high:
            considerations.append(
                "PaCO2 exceeds the expected compensatory range for metabolic alkalosis; "
                "review for an additional respiratory acidosis process."
            )
        else:
            considerations.append(
                "PaCO2 is below the expected compensatory range for metabolic alkalosis; "
                "review for an additional respiratory alkalosis process."
            )

    elif pco2 > 45:
        considerations.append(
            "Review adequacy of minute ventilation in the full clinical context."
        )

        if rr >= 20 and tv >= 500:
            considerations.append(
                "Hypercapnia persists despite relatively high set ventilation; consider "
                "dead-space burden, mechanics, synchrony and V/Q abnormalities."
            )

    elif pco2 < 35:
        considerations.append(
            "Review the cause of hypocapnia before considering any ventilator change."
        )

    # Harmonize oxygenation wording with the P/F classification shown in the UI.
    pf_ratio, pf_band = _pf_band(po2, fio2)

    if pf_ratio is not None and pf_band != "preserved":
        pao2_context = (
            "Marked hypoxemia by PaO2 is also present. "
            if po2 < 60
            else ""
        )

        considerations.append(
            f"{pao2_context}P/F ratio ({pf_ratio:.1f}) indicates {pf_band} "
            "oxygenation impairment; correlate with SpO2, FiO2 requirement, "
            "clinical target and underlying cause."
        )

    elif po2 < 80:
        considerations.append(
            "Low PaO2 is present despite a relatively preserved P/F ratio; "
            "verify entered FiO2 and correlate with the clinical context."
        )

    if peep >= 12:
        considerations.append(
            "Elevated PEEP requirement noted; review hemodynamic tolerance and lung mechanics."
        )

    if not considerations:
        considerations.append(
            "No major ventilator-specific prompt generated from the entered ABG and settings; "
            "continue clinical reassessment."
        )

    return considerations


def prioritize_recommendations(considerations):
    high_priority = []
    general = []

    high_markers = (
        "severe oxygenation impairment",
        "combined respiratory and metabolic acidifying",
        "combined respiratory and metabolic alkalinizing",
        "above the expected compensatory range",
        "exceeds the expected compensatory range",
    )

    for item in considerations:
        if any(marker in item.lower() for marker in high_markers):
            high_priority.append(item)
        else:
            general.append(item)

    return high_priority, general
