def calculate_pf_ratio(po2, fio2):

    if fio2 <= 0:
        return None, "Invalid FiO₂"

    pf_ratio = po2 / fio2

    # -------------------------
    # Classification
    # -------------------------

    if pf_ratio < 100:

        severity = "Severe oxygenation impairment"

    elif pf_ratio < 200:

        severity = "Moderate oxygenation impairment"

    elif pf_ratio < 300:

        severity = "Mild oxygenation impairment"

    else:

        severity = "Relatively preserved oxygenation"

    return round(pf_ratio, 1), severity

def ards_classification(pf_ratio):

    if pf_ratio < 100:

        return "Severe ARDS Pattern"

    elif pf_ratio < 200:

        return "Moderate ARDS Pattern"

    elif pf_ratio < 300:

        return "Mild ARDS Pattern"

    else:

        return "No major ARDS pattern detected"