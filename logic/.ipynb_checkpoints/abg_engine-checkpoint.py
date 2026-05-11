def analyze_abg(ph, pco2, hco3):

    result = {}

    # ---------------------------
    # STEP 1 — pH Classification
    # ---------------------------

    if ph < 7.35:
        result["state"] = "Acidemia"

    elif ph > 7.45:
        result["state"] = "Alkalemia"

    else:
        result["state"] = "Near Normal / Compensated"

    # ---------------------------
    # STEP 2 — Primary Disorder
    # ---------------------------

    if ph < 7.35:

        if pco2 > 45:
            result["primary"] = "Respiratory Acidosis"

        elif hco3 < 22:
            result["primary"] = "Metabolic Acidosis"

        else:
            result["primary"] = "Mixed Disorder"

    elif ph > 7.45:

        if pco2 < 35:
            result["primary"] = "Respiratory Alkalosis"

        elif hco3 > 26:
            result["primary"] = "Metabolic Alkalosis"

        else:
            result["primary"] = "Mixed Disorder"

    else:
        result["primary"] = "Compensated Disorder"

    # ---------------------------
    # STEP 3 — Compensation
    # ---------------------------

    compensation = ""
    reasoning = []

    if result["primary"] == "Metabolic Acidosis":

        expected_pco2 = (1.5 * hco3) + 8

        compensation = (
            f"Expected PaCO₂ ≈ {round(expected_pco2,1)} "
            "(Winter’s Formula)"
        )

        reasoning.append(
            "Low HCO₃ suggests metabolic acidosis physiology"
        )

        if abs(pco2 - expected_pco2) > 2:

            compensation += " → Mixed disorder suspected"

            reasoning.append(
                "Observed PaCO₂ deviates from expected compensation"
            )

    elif result["primary"] == "Respiratory Acidosis":

        delta = pco2 - 40

        acute_hco3 = 24 + (delta / 10) * 1
        chronic_hco3 = 24 + (delta / 10) * 4

        compensation = (
            f"Expected HCO₃: Acute ≈ {round(acute_hco3,1)} | "
            f"Chronic ≈ {round(chronic_hco3,1)}"
        )

        reasoning.append(
            "Elevated PaCO₂ suggests hypoventilation physiology"
        )

        if acute_hco3 <= hco3 <= chronic_hco3:

            reasoning.append(
                "Compensation appears physiologically appropriate"
            )

        elif hco3 < acute_hco3:

            reasoning.append(
                "Additional metabolic acidosis may be present"
            )

        elif hco3 > chronic_hco3:

            reasoning.append(
                "Additional metabolic alkalosis may be present"
            )

    elif result["primary"] == "Respiratory Alkalosis":

        delta = 40 - pco2

        acute_hco3 = 24 - (delta / 10) * 2
        chronic_hco3 = 24 - (delta / 10) * 5

        compensation = (
            f"Expected HCO₃: Acute ≈ {round(acute_hco3,1)} | "
            f"Chronic ≈ {round(chronic_hco3,1)}"
        )

        reasoning.append(
            "Low PaCO₂ suggests hyperventilation physiology"
        )

    elif result["primary"] == "Metabolic Alkalosis":

        expected_pco2 = (0.7 * hco3) + 20

        compensation = (
            f"Expected PaCO₂ ≈ {round(expected_pco2,1)}"
        )

        reasoning.append(
            "Elevated HCO₃ suggests metabolic alkalosis"
        )

    result["compensation"] = compensation
    result["reasoning"] = reasoning

    return result

def calculate_anion_gap(na, cl, hco3):

    ag = na - (cl + hco3)

    if ag > 14:
        interpretation = (
            "High anion gap metabolic process detected"
        )

    elif ag < 8:
        interpretation = (
            "Low anion gap detected"
        )

    else:
        interpretation = (
            "Normal anion gap"
        )

    return ag, interpretation


def calculate_delta_ratio(ag, hco3):

    if hco3 >= 24:
        return None, "Delta ratio not applicable"

    delta = (ag - 12) / (24 - hco3)

    if delta < 1:

        interpretation = (
            "Possible mixed high and normal anion gap acidosis"
        )

    elif 1 <= delta <= 2:

        interpretation = (
            "Pattern consistent with pure high anion gap acidosis"
        )

    else:

        interpretation = (
            "Possible concurrent metabolic alkalosis"
        )

    return delta, interpretation