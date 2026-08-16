def ventilator_considerations(pco2, po2, rr, tv, fio2, peep, abg=None, hco3=None):
    considerations = []
    primary = (abg or {}).get("primary", "")

    if primary == "Metabolic Acidosis" and hco3 is not None:
        expected = (1.5 * hco3) + 8
        low, high = expected - 2, expected + 2
        if low <= pco2 <= high:
            considerations.append("Observed PaCO2 is within the expected respiratory compensatory range; avoid interpreting compensatory hypocapnia as isolated overventilation.")
        elif pco2 > high:
            considerations.append("PaCO2 is above the expected compensatory range for metabolic acidosis; review ventilation adequacy and concurrent respiratory acidosis.")
        else:
            considerations.append("PaCO2 is below the expected compensatory range; review for a concurrent respiratory alkalosis process.")
    elif "Mixed Respiratory + Metabolic Acidosis" in primary:
        considerations.append("Combined respiratory and metabolic acidifying processes are present; review ventilation adequacy while addressing the metabolic driver.")
    elif pco2 > 45:
        considerations.append("Review adequacy of minute ventilation in the full clinical context.")
        if rr >= 20 and tv >= 500:
            considerations.append("Hypercapnia persists despite relatively high set ventilation; consider dead-space burden, mechanics, synchrony and V/Q abnormalities.")
    elif pco2 < 35:
        considerations.append("Review the cause of hypocapnia before considering any ventilator change.")

    if po2 < 60:
        if fio2 >= 0.60:
            considerations.append("Severe oxygenation impairment persists at elevated FiO2; review PEEP/recruitment strategy, lung mechanics and underlying cause in clinical context.")
        else:
            considerations.append("Severe oxygenation impairment is present; review oxygen delivery and ventilatory strategy.")
    elif po2 < 80:
        considerations.append("Impaired oxygenation is present; correlate with SpO2, FiO2 requirement and clinical target.")

    if peep >= 12:
        considerations.append("Elevated PEEP requirement noted; review hemodynamic tolerance and lung mechanics.")

    if not considerations:
        considerations.append("No major ventilator-specific prompt generated from the entered ABG and settings; continue clinical reassessment.")

    return considerations


def prioritize_recommendations(considerations):
    high_priority = []
    general = []
    high_markers = ("severe oxygenation impairment", "combined respiratory and metabolic acidifying", "above the expected compensatory range")
    for item in considerations:
        if any(marker in item.lower() for marker in high_markers):
            high_priority.append(item)
        else:
            general.append(item)
    return high_priority, general
