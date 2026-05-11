def teaching_points(primary):

    pearls = {

        "Respiratory Acidosis": [
            "Respiratory acidosis usually reflects alveolar hypoventilation.",
            "Evaluate for airway, CNS, or neuromuscular causes."
        ],

        "Metabolic Acidosis": [
            "Always assess anion gap in metabolic acidosis.",
            "Winter’s formula helps identify mixed disorders."
        ],

        "Respiratory Alkalosis": [
            "Common causes include sepsis, anxiety, and pulmonary embolism."
        ],

        "Metabolic Alkalosis": [
            "Consider vomiting, diuretics, or volume depletion."
        ]
    }

    return pearls.get(
        primary,
        ["No teaching pearls available."]
    )