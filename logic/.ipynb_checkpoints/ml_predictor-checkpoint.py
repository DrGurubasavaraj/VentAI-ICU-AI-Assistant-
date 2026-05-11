import os
import pickle
import streamlit as st


# -----------------------------------
# PROJECT ROOT
# -----------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

# -----------------------------------
# MODEL PATH
# -----------------------------------

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model.pkl"
)

# -----------------------------------
# LOAD MODEL
# -----------------------------------

@st.cache_resource
def load_model():

    with open(MODEL_PATH, "rb") as f:

        return pickle.load(f)


model = load_model()


# -----------------------------------
# PREDICTION ENGINE
# -----------------------------------

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

    prediction = model.predict(input_data)[0]

    probs = model.predict_proba(input_data)[0]

    confidence = max(probs)

    # -----------------------------------
    # CONFIDENCE LABELS
    # -----------------------------------

    if confidence > 0.85:

        label = "High interpretive confidence"

    elif confidence > 0.65:

        label = "Moderate interpretive confidence"

    else:

        label = (
            "Complex physiology detected"
        )

    return prediction, confidence, label