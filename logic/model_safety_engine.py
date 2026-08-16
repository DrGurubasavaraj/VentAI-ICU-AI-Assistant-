def reconcile_model_signal(
    model_signal,
    abg,
    pco2,
    hco3
):
    """
    Reconcile the ML pattern signal with the rule-based physiology layer.

    Returns:
        display_signal, status, note
    """

    display_signal = model_signal
    status = "Secondary model signal"
    note = (
        "Machine-learning output is displayed as a non-prescriptive pattern "
        "classification and does not override physiological reasoning."
    )

    primary = abg.get("primary", "")
    signal_lower = str(model_signal).lower()

    # Metabolic acidosis: assess respiratory compensation with Winter's formula.
    if primary == "Metabolic Acidosis":
        expected_pco2 = (1.5 * hco3) + 8
        compensation_gap = abs(pco2 - expected_pco2)

        # If respiratory compensation is broadly appropriate, a lower-ventilation
        # model signal could conflict with the physiology layer and is suppressed.
        if (
            compensation_gap <= 2
            and "lower ventilatory-demand" in signal_lower
        ):
            display_signal = "Model signal suppressed"
            status = "Physiology-model conflict"
            note = (
                "The model signal was withheld because PaCO2 is within the "
                "expected compensatory range for metabolic acidosis. "
                "The physiological rule layer takes precedence."
            )

    return display_signal, status, note
