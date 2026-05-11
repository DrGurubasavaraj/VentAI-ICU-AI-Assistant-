import plotly.graph_objects as go


def instability_gauge(score):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=score,

        title={
            'text': "Physiological Instability Index"
        },

        gauge={

            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'color': "#1f77ff"
            },

            'steps': [

                {
                    'range': [0, 30],
                    'color': "#52c41a"
                },

                {
                    'range': [30, 55],
                    'color': "#faad14"
                },

                {
                    'range': [55, 80],
                    'color': "#ff7a45"
                },

                {
                    'range': [80, 100],
                    'color': "#ff4d4f"
                }
            ]
        }
    ))
    gauge = {}
    bgcolor="#0d1b2a",
    borderwidth=2,
    bordercolor="#1f2d3d",

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="#0d1b2a",
        font_color="white"
    )

    return fig

def pf_ratio_gauge(pf_ratio):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=pf_ratio,

        title={
            'text': "P/F Ratio"
        },

        gauge={

            'axis': {
                'range': [0, 500]
            },

            'bar': {
                'color': "#1f77ff"
            },

            'steps': [

                {
                    'range': [0, 100],
                    'color': "#ff4d4f"
                },

                {
                    'range': [100, 200],
                    'color': "#ff7a45"
                },

                {
                    'range': [200, 300],
                    'color': "#faad14"
                },

                {
                    'range': [300, 500],
                    'color': "#52c41a"
                }
            ]
        }
    ))
    gauge = {}
    bgcolor="#0d1b2a",
    borderwidth=2,
    bordercolor="#1f2d3d",

    fig.update_layout(
        height=280,
        paper_bgcolor="#0d1b2a",
        font_color="white"
    )

    return fig

def explainability_gauge(score):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=score,

        title={
            'text': "Explainability Index"
        },

        gauge={

            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'color': "#722ed1"
            },

            'steps': [

                {
                    'range': [0, 50],
                    'color': "#ff7875"
                },

                {
                    'range': [50, 75],
                    'color': "#faad14"
                },

                {
                    'range': [75, 100],
                    'color': "#52c41a"
                }
            ],

            "bgcolor": "#0d1b2a",

            "borderwidth": 2,

            "bordercolor": "#1f2d3d"
        }
    ))

    fig.update_layout(

        height=280,

        paper_bgcolor="#0d1b2a",

        font_color="white"
    )

    return fig