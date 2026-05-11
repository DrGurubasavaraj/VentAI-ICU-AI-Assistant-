import plotly.graph_objects as go
import pandas as pd


def abg_trend_chart(history):

    if len(history) < 2:

        return None

    df = pd.DataFrame(history)

    fig = go.Figure()

    # -------------------------
    # pH
    # -------------------------

    fig.add_trace(

        go.Scatter(

            x=df["time"],
            y=df["pH"],

            mode="lines+markers",

            name="pH"
        )
    )

    # -------------------------
    # PaCO2
    # -------------------------

    fig.add_trace(

        go.Scatter(

            x=df["time"],
            y=df["PaCO2"],

            mode="lines+markers",

            name="PaCO₂"
        )
    )

    # -------------------------
    # PaO2
    # -------------------------

    fig.add_trace(

        go.Scatter(

            x=df["time"],
            y=df["PaO2"],

            mode="lines+markers",

            name="PaO₂"
        )
    )

    fig.update_layout(

        title="Serial ABG Trajectory",

        height=400,

        paper_bgcolor="#0d1b2a",

        plot_bgcolor="#0d1b2a",

        font_color="white",

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig