def reconcile_model_signal(model_signal, abg, pco2, hco3):
    """
    Physiology-first safety reconciliation.

    Rule-based physiology takes precedence over the ML pattern classifier.
    """
    display_signal = model_signal
    status = "Secondary model signal"
    note = (
        "Machine-learning output is displayed as a non-prescriptive pattern "
        "classification and does not override physiological reasoning."
    )

    primary = abg.get("primary", "")
    signal_lower = str(model_signal).lower()

    # Mixed disorders are deliberately withheld from model-directed messaging.
    # A single model class is too reductive for two simultaneous primary processes.
    if primary.startswith("Mixed Respiratory + Metabolic"):
        return (
            "Model signal suppressed",
            "Complex physiology — model signal withheld",
            "The model signal was withheld because a mixed acid-base disorder was "
            "identified. The physiological rule layer takes precedence."
        )

    # Metabolic acidosis: appropriate respiratory compensation should not be
    # interpreted as excessive ventilation.
    if primary == "Metabolic Acidosis":
        expected = (1.5 * hco3) + 8
        low, high = expected - 2, expected + 2

        if low <= pco2 <= high and "lower ventilatory-demand" in signal_lower:
            return (
                "Model signal suppressed",
                "Physiology-model conflict",
                "The model signal was withheld because PaCO2 is within the expected "
                "compensatory range for metabolic acidosis. The physiological rule "
                "layer takes precedence."
            )

    # Metabolic alkalosis: appropriate compensatory rise in PaCO2 should not
    # be interpreted as a generic need for greater ventilation.
    if primary == "Metabolic Alkalosis":
        expected = 40 + 0.7 * (hco3 - 24)
        low, high = expected - 5, expected + 5

        if low <= pco2 <= high and "higher ventilatory-demand" in signal_lower:
            return (
                "Model signal suppressed",
                "Physiology-model conflict",
                "The model signal was withheld because PaCO2 is compatible with "
                "expected respiratory compensation for metabolic alkalosis. "
                "The physiological rule layer takes precedence."
            )

    return display_signal, status, note
