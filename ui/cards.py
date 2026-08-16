import html
import streamlit as st


def _safe(value):
    return html.escape(str(value))


def clinical_card(
    title,
    value,
    border_color="var(--accent)",
    eyebrow=None,
    compact=False
):
    eyebrow_html = (
        f'<div class="vai-card-eyebrow">{_safe(eyebrow)}</div>'
        if eyebrow else ""
    )
    compact_class = " vai-card--compact" if compact else ""

    card_html = (
        f'<div class="vai-card{compact_class}" style="--card-accent:{border_color};">'
        f'{eyebrow_html}'
        f'<div class="vai-card-title">{_safe(title)}</div>'
        f'<div class="vai-card-value">{_safe(value)}</div>'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)


def metric_card(
    title,
    value,
    delta=None,
    color="var(--accent)"
):
    delta_html = (
        f'<div class="vai-metric-note">{_safe(delta)}</div>'
        if delta is not None else ""
    )

    card_html = (
        f'<div class="vai-metric" style="--metric-accent:{color};">'
        f'<div class="vai-metric-title">{_safe(title)}</div>'
        f'<div class="vai-metric-value">{_safe(value)}</div>'
        f'{delta_html}'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)


def status_card(
    label,
    value,
    status="neutral",
    helper=None
):
    helper_html = (
        f'<div class="vai-status-helper">{_safe(helper)}</div>'
        if helper else ""
    )

    card_html = (
        f'<div class="vai-status-card vai-status-{_safe(status)}">'
        f'<div class="vai-status-label">{_safe(label)}</div>'
        f'<div class="vai-status-value">{_safe(value)}</div>'
        f'{helper_html}'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)


def executive_impression_card(text):
    card_html = (
        '<div class="vai-card" style="--card-accent:var(--accent);">'
        '<div class="vai-card-title">Executive Clinical Impression</div>'
        f'<div class="vai-card-value">{_safe(text)}</div>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)


def risk_badge(severity):
    status_map = {
        "Critical": "critical",
        "High Risk": "high",
        "Moderate": "moderate",
        "Low Risk": "low",
        "Stable": "low",
    }
    status = status_map.get(str(severity), "neutral")

    badge_html = (
        f'<div class="vai-risk-badge vai-risk-{status}">'
        f'{_safe(severity)}'
        f'</div>'
    )

    st.markdown(badge_html, unsafe_allow_html=True)
