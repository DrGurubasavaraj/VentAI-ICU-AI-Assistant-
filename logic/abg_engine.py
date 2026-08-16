def analyze_abg(ph, pco2, hco3):
    result = {"state":"", "primary":"", "compensation":"", "compensation_status":"", "reasoning":[], "mixed":False}

    if ph < 7.35:
        result["state"] = "Acidemia"
    elif ph > 7.45:
        result["state"] = "Alkalemia"
    else:
        result["state"] = "Near-normal pH"

    if ph < 7.35:
        if pco2 > 45 and hco3 < 22:
            result["primary"] = "Mixed Respiratory + Metabolic Acidosis"
            result["mixed"] = True
            result["reasoning"].append("PaCO2 is acidifying while HCO3 is also reduced: two acidifying processes are present.")
        elif pco2 > 45:
            result["primary"] = "Respiratory Acidosis"
        elif hco3 < 22:
            result["primary"] = "Metabolic Acidosis"
        else:
            result["primary"] = "Acidemia - primary process unclear"
    elif ph > 7.45:
        if pco2 < 35 and hco3 > 26:
            result["primary"] = "Mixed Respiratory + Metabolic Alkalosis"
            result["mixed"] = True
            result["reasoning"].append("PaCO2 is alkalinizing while HCO3 is also elevated: two alkalinizing processes are present.")
        elif pco2 < 35:
            result["primary"] = "Respiratory Alkalosis"
        elif hco3 > 26:
            result["primary"] = "Metabolic Alkalosis"
        else:
            result["primary"] = "Alkalemia - primary process unclear"
    else:
        if pco2 > 45 and hco3 > 26:
            result["primary"] = "Compensated / Mixed Respiratory Acidosis Pattern"
        elif pco2 < 35 and hco3 < 22:
            result["primary"] = "Compensated / Mixed Respiratory Alkalosis Pattern"
        elif pco2 > 45 and hco3 < 22:
            result["primary"] = "Mixed Respiratory + Metabolic Acidosis"
            result["mixed"] = True
        elif pco2 < 35 and hco3 > 26:
            result["primary"] = "Mixed Respiratory + Metabolic Alkalosis"
            result["mixed"] = True
        else:
            result["primary"] = "No dominant acid-base disorder identified"

    primary = result["primary"]

    if primary == "Metabolic Acidosis":
        expected = (1.5 * hco3) + 8
        low, high = expected - 2, expected + 2
        result["compensation"] = f"Expected PaCO2 ~= {expected:.1f} mmHg (acceptable range {low:.1f}-{high:.1f}; Winter's formula)"
        result["reasoning"].append("Reduced HCO3 identifies a metabolic acidifying process.")
        if low <= pco2 <= high:
            result["compensation_status"] = "Respiratory compensation broadly appropriate"
            result["reasoning"].append("Observed PaCO2 is within the expected compensatory range.")
        elif pco2 > high:
            result["compensation_status"] = "Additional respiratory acidosis suspected"
            result["mixed"] = True
            result["reasoning"].append("Observed PaCO2 is above the expected compensatory range.")
        else:
            result["compensation_status"] = "Additional respiratory alkalosis suspected"
            result["mixed"] = True
            result["reasoning"].append("Observed PaCO2 is below the expected compensatory range.")

    elif primary == "Metabolic Alkalosis":
        expected = 40 + 0.7 * (hco3 - 24)
        low, high = expected - 5, expected + 5
        result["compensation"] = f"Expected PaCO2 ~= {expected:.1f} mmHg (approximate range {low:.1f}-{high:.1f})"
        result["reasoning"].append("Elevated HCO3 identifies a metabolic alkalinizing process.")
        if low <= pco2 <= high:
            result["compensation_status"] = "Respiratory compensation broadly appropriate"
        elif pco2 > high:
            result["compensation_status"] = "Additional respiratory acidosis suspected"
            result["mixed"] = True
        else:
            result["compensation_status"] = "Additional respiratory alkalosis suspected"
            result["mixed"] = True

    elif primary == "Respiratory Acidosis":
        delta = pco2 - 40
        acute_hco3 = 24 + (delta / 10) * 1
        chronic_hco3 = 24 + (delta / 10) * 4
        result["compensation"] = f"Expected HCO3: acute ~= {acute_hco3:.1f} mEq/L; chronic ~= {chronic_hco3:.1f} mEq/L"
        result["reasoning"].append("Elevated PaCO2 identifies a respiratory acidifying process.")
        lower = min(acute_hco3, chronic_hco3) - 2
        upper = max(acute_hco3, chronic_hco3) + 2
        if lower <= hco3 <= upper:
            result["compensation_status"] = "Compensation compatible with acute-to-chronic respiratory acidosis"
        elif hco3 < lower:
            result["compensation_status"] = "Additional metabolic acidosis suspected"
            result["mixed"] = True
        else:
            result["compensation_status"] = "Additional metabolic alkalosis suspected"
            result["mixed"] = True

    elif primary == "Respiratory Alkalosis":
        delta = 40 - pco2
        acute_hco3 = 24 - (delta / 10) * 2
        chronic_hco3 = 24 - (delta / 10) * 5
        result["compensation"] = f"Expected HCO3: acute ~= {acute_hco3:.1f} mEq/L; chronic ~= {chronic_hco3:.1f} mEq/L"
        result["reasoning"].append("Reduced PaCO2 identifies a respiratory alkalinizing process.")
        lower = min(acute_hco3, chronic_hco3) - 2
        upper = max(acute_hco3, chronic_hco3) + 2
        if lower <= hco3 <= upper:
            result["compensation_status"] = "Compensation compatible with acute-to-chronic respiratory alkalosis"
        elif hco3 < lower:
            result["compensation_status"] = "Additional metabolic acidosis suspected"
            result["mixed"] = True
        else:
            result["compensation_status"] = "Additional metabolic alkalosis suspected"
            result["mixed"] = True

    elif primary == "Mixed Respiratory + Metabolic Acidosis":
        result["compensation"] = "Compensation formula is not used as the primary interpretation because both PaCO2 and HCO3 are contributing to acidemia."
        result["compensation_status"] = "Mixed acidifying processes detected"

    elif primary == "Mixed Respiratory + Metabolic Alkalosis":
        result["compensation"] = "Compensation formula is not used as the primary interpretation because both PaCO2 and HCO3 are contributing to alkalemia."
        result["compensation_status"] = "Mixed alkalinizing processes detected"

    else:
        result["compensation"] = "No single compensation rule is sufficient for this pattern."
        result["compensation_status"] = "Review full clinical context"

    return result


def calculate_anion_gap(na, cl, hco3):
    ag = na - (cl + hco3)
    if ag > 14:
        interpretation = "High anion gap"
    elif ag < 8:
        interpretation = "Low anion gap"
    else:
        interpretation = "Normal anion gap"
    return ag, interpretation


def calculate_delta_ratio(ag, hco3):
    if hco3 >= 24:
        return None, "Delta ratio not applicable"
    denominator = 24 - hco3
    if denominator <= 0:
        return None, "Delta ratio not applicable"
    delta = (ag - 12) / denominator
    if delta < 0.4:
        interpretation = "Predominantly normal-anion-gap metabolic acidosis pattern"
    elif delta < 0.8:
        interpretation = "Mixed high- and normal-anion-gap metabolic acidosis pattern"
    elif delta <= 2:
        interpretation = "High-anion-gap metabolic acidosis pattern"
    else:
        interpretation = "High-anion-gap acidosis with concurrent metabolic alkalosis pattern"
    return delta, interpretation
