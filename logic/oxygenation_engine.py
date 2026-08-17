def calculate_pf_ratio(po2, fio2):
    if fio2 <= 0:
        return None, "Invalid FiO2"

    pf_ratio = po2 / fio2

    # Inclusive boundary handling:
    # severe <=100; moderate >100 to <=200;
    # mild >200 to <=300; preserved >300.
    if pf_ratio <= 100:
        severity = "Severe oxygenation impairment"
    elif pf_ratio <= 200:
        severity = "Moderate oxygenation impairment"
    elif pf_ratio <= 300:
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

    if pf_ratio <= 100:
        return "Severe impairment band (P/F <= 100)"
    elif pf_ratio <= 200:
        return "Moderate impairment band (P/F > 100 to <= 200)"
    elif pf_ratio <= 300:
        return "Mild impairment band (P/F > 200 to <= 300)"
    else:
        return "Preserved range (P/F > 300)"


def ards_classification(pf_ratio):
    """
    Backward-compatible wrapper.
    The output is intentionally framed as an oxygenation range rather than
    an ARDS diagnosis.
    """
    band = oxygenation_band(pf_ratio)
    return (
        f"ARDS-compatible oxygenation range: {band}; "
        "full clinical criteria required"
    )
