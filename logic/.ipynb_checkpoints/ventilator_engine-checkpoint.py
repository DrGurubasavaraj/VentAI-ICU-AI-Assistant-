def ventilator_considerations(
    pco2,
    po2,
    rr,
    tv,
    fio2,
    peep
):

    considerations = []

    # -------------------------
    # Ventilation Logic
    # -------------------------

    if pco2 > 45:

        considerations.append(
            "Consider evaluating adequacy of minute ventilation"
        )

        if rr >= 20 and tv >= 500:

            considerations.append(
                "Persistent hypercapnia despite elevated ventilatory support may suggest dead-space physiology or severe V/Q mismatch"
            )

    elif pco2 < 35:

        considerations.append(
            "Consider reviewing potential causes of hyperventilation physiology"
        )

    # -------------------------
    # Oxygenation Logic
    # -------------------------

    if po2 < 60:

        considerations.append(
            "Severe oxygenation impairment detected"
        )

        if fio2 >= 0.6:

            considerations.append(
                "Refractory hypoxemia may warrant evaluation of recruitment strategies in clinical context"
            )

        else:

            considerations.append(
                "Consider reviewing oxygen delivery strategy"
            )

    elif po2 < 80:

        considerations.append(
            "Borderline oxygenation profile detected"
        )

    # -------------------------
    # PEEP
    # -------------------------

    if peep >= 12:

        considerations.append(
            "Elevated PEEP requirements noted"
        )

    return considerations

def prioritize_recommendations(
    considerations
):

    critical = []
    moderate = []

    for item in considerations:

        if (
            "Severe" in item
            or "Refractory" in item
        ):

            critical.append(item)

        else:

            moderate.append(item)

    return critical, moderate