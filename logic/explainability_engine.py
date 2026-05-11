def explainability_score(
    confidence,
    reasoning_count,
    alerts_count
):

    score = 50

    # -------------------------
    # Confidence Contribution
    # -------------------------

    score += int(confidence * 30)

    # -------------------------
    # Reasoning Depth
    # -------------------------

    score += reasoning_count * 3

    # -------------------------
    # Complexity Penalty
    # -------------------------

    score -= alerts_count * 2

    # -------------------------
    # Clamp
    # -------------------------

    score = max(0, min(score, 100))

    # -------------------------
    # Label
    # -------------------------

    if score >= 85:

        label = "Highly Explainable"

    elif score >= 65:

        label = "Moderately Explainable"

    else:

        label = "Complex Physiological Pattern"

    return score, label