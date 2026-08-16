import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def abg_trend_chart(history, compact=False):
    """
    Serial ABG trajectory using separate scales for pH, PaCO2 and PaO2.
    Compact mode is optimized for conference/presentation screenshots.
    """
    if len(history) < 2:
        return None

    df = pd.DataFrame(history)

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06 if compact else 0.08,
        subplot_titles=(
            "Arterial pH",
            "PaCO2 (mmHg)",
            "PaO2 (mmHg)",
        ),
    )

    traces = [
        ("pH", "pH", 1, "pH %{y:.2f}"),
        ("PaCO2", "PaCO2", 2, "PaCO2 %{y:.0f} mmHg"),
        ("PaO2", "PaO2", 3, "PaO2 %{y:.0f} mmHg"),
    ]

    for column, name, row, hover_text in traces:
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df[column],
                mode="lines+markers",
                name=name,
                line=dict(width=2.6),
                marker=dict(size=7),
                hovertemplate=f"Time %{{x}}<br>{hover_text}<extra></extra>",
            ),
            row=row,
            col=1,
        )

        # Emphasize the latest observation.
        fig.add_trace(
            go.Scatter(
                x=[df["time"].iloc[-1]],
                y=[df[column].iloc[-1]],
                mode="markers",
                showlegend=False,
                marker=dict(
                    size=13,
                    symbol="circle-open",
                    line=dict(width=3),
                ),
                hoverinfo="skip",
            ),
            row=row,
            col=1,
        )

    # Clinical reference bands.
    fig.add_hrect(
        y0=7.35,
        y1=7.45,
        line_width=0,
        opacity=0.11,
        row=1,
        col=1,
    )
    fig.add_hrect(
        y0=35,
        y1=45,
        line_width=0,
        opacity=0.10,
        row=2,
        col=1,
    )

    max_pao2 = max(120, float(df["PaO2"].max()) + 20)
    fig.add_hrect(
        y0=80,
        y1=max_pao2,
        line_width=0,
        opacity=0.08,
        row=3,
        col=1,
    )

    fig.update_yaxes(
        title_text="pH",
        range=[
            min(7.0, float(df["pH"].min()) - 0.05),
            max(7.6, float(df["pH"].max()) + 0.05),
        ],
        row=1,
        col=1,
    )
    fig.update_yaxes(
        title_text="mmHg",
        rangemode="tozero",
        row=2,
        col=1,
    )
    fig.update_yaxes(
        title_text="mmHg",
        rangemode="tozero",
        row=3,
        col=1,
    )

    # Explicit title text prevents Plotly/renderer from displaying "undefined".
    chart_title = (
        "Serial physiological trajectory"
        if compact
        else "Serial ABG trajectory"
    )

    fig.update_layout(
        title=dict(
            text=chart_title,
            x=0.01,
            xanchor="left",
            font=dict(size=13 if compact else 16),
        ),
        height=390 if compact else 600,
        showlegend=False,
        margin=dict(
            l=35,
            r=20,
            t=42 if compact else 60,
            b=24,
        ),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11 if compact else 12),
    )

    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=9 if compact else 11),
    )
    fig.update_yaxes(
        gridcolor="rgba(128,128,128,0.16)",
        tickfont=dict(size=9 if compact else 11),
        title_font=dict(size=10 if compact else 11),
    )

    for annotation in fig.layout.annotations:
        annotation.font.size = 11 if compact else 13

    return fig
