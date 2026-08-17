import os
import pickle
import streamlit as st


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model.pkl"
)


@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


model = load_model()


def _neutralize_model_label(raw_prediction):
    """
    Convert treatment-like model classes into non-prescriptive research signals.
    """
    raw_text = str(raw_prediction).strip()
    normalized = raw_text.lower()

    label_map = {
        "increase ventilation": "Higher ventilatory-demand pattern",
        "decrease ventilation": "Lower ventilatory-demand pattern",
        "maintain ventilation": "No major ventilatory-change pattern",
        "no change": "No major ventilatory-change pattern",
        "improve oxygenation": "Oxygenation-support review pattern",
        "stable": "No major model-defined support-change pattern",
    }

    if normalized in label_map:
        return label_map[normalized]

    return f"Model classification: {raw_text}"


def predict_patient(
    ph,
    pco2,
    hco3,
    po2,
    rr,
    tv,
    fio2,
    peep
):
    input_data = [[
        ph,
        pco2,
        hco3,
        po2,
        rr,
        tv,
        fio2,
        peep
    ]]

    raw_prediction = model.predict(input_data)[0]
    prediction = _neutralize_model_label(raw_prediction)

    probs = model.predict_proba(input_data)[0]
    confidence = float(max(probs))

    if confidence > 0.85:
        label = "High model confidence"
    elif confidence > 0.65:
        label = "Moderate model confidence"
    else:
        label = "Low model confidence"

    return prediction, confidence, label
