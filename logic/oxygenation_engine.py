def calculate_pf_ratio(po2, fio2):
    if fio2 <= 0:
        return None, "Invalid FiO2"

    pf_ratio = po2 / fio2

    if pf_ratio < 100:
        severity = "Severe oxygenation impairment"
    elif pf_ratio < 200:
        severity = "Moderate oxygenation impairment"
    elif pf_ratio < 300:
        severity = "Mild oxygenation impairment"
    else:
        severity = "Relatively preserved oxygenation"

    return round(pf_ratio, 1), severity


def oxygenation_band(pf_ratio):
    """
    P/F-based oxygenation band only.
    This does not diagnose ARDS.
    """
    if pf_ratio is None:
        return "Unavailable"

    if pf_ratio < 100:
        return "Severe impairment band (P/F < 100)"
    elif pf_ratio < 200:
        return "Moderate impairment band (P/F 100-199)"
    elif pf_ratio < 300:
        return "Mild impairment band (P/F 200-299)"
    else:
        return "Preserved range (P/F >= 300)"


def ards_classification(pf_ratio):
    """
    Backward-compatible wrapper for the existing dashboard.
    Kept temporarily so V1 imports do not break.

    V2 should label this as an oxygenation / ARDS-compatible band,
    not as a diagnosis of ARDS.
    """
    band = oxygenation_band(pf_ratio)
    return f"ARDS-compatible oxygenation range: {band}; full clinical criteria required"
