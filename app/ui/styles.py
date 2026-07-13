"""Global Uber-inspired styling."""
import streamlit as st

from config import APP_CITY, APP_TITLE, FONT_FAMILY, GOOGLE_FONT_URL, THEME


def inject_global_styles() -> None:
    t = THEME
    st.markdown(f'<link href="{GOOGLE_FONT_URL}" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: {FONT_FAMILY};
        }}

        .stApp {{
            background-color: {t.bg};
            color: {t.text_primary};
        }}

        #MainMenu, footer, header[data-testid="stHeader"], .stDeployButton {{
            visibility: hidden;
            height: 0;
        }}

        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1320px;
        }}

        div[data-testid="stTabs"] button {{
            background: transparent;
            color: {t.text_secondary};
            border: none;
            border-bottom: 2px solid transparent;
            border-radius: 0;
            font-weight: 600;
            padding: 0.7rem 1.2rem;
        }}

        div[data-testid="stTabs"] button[aria-selected="true"] {{
            color: {t.text_primary};
            border-bottom-color: {t.text_primary};
        }}

        div[data-testid="stTabs"] button:hover {{
            color: {t.text_primary};
            background: {t.surface};
        }}

        .stButton > button {{
            border-radius: 8px;
            font-weight: 600;
            border: 1px solid {t.border};
        }}

        .stButton > button[kind="primary"] {{
            background-color: {t.accent};
            color: #FFFFFF;
            border: none;
        }}

        .stButton > button[kind="primary"]:hover {{
            background-color: #222222;
            color: #FFFFFF;
        }}

        .stButton > button:disabled {{
            background-color: {t.surface_alt} !important;
            color: {t.text_muted} !important;
        }}

        div[data-testid="stRadio"] > div {{
            flex-direction: column;
            gap: 0.45rem;
        }}

        div[data-testid="stRadio"] label {{
            background: {t.bg};
            border: 1px solid {t.border};
            border-radius: 10px;
            padding: 0.8rem 1rem !important;
            font-weight: 500;
            width: 100%;
            color: {t.text_primary} !important;
        }}

        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label span,
        div[data-testid="stRadio"] label div {{
            color: {t.text_primary} !important;
        }}

        div[data-testid="stRadio"] label:hover {{
            border-color: {t.text_secondary};
            background: {t.surface};
        }}

        div[data-testid="stRadio"] label[data-checked="true"],
        div[data-testid="stRadio"] label:has(input:checked) {{
            border-color: {t.text_primary};
            background: {t.surface};
            font-weight: 600;
        }}

        div[data-testid="stRadio"] label > div:first-child {{
            display: none;
        }}

        .app-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid {t.border};
            margin-bottom: 1.25rem;
        }}

        .app-logo {{
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.04em;
        }}

        .app-city {{
            font-size: 0.8rem;
            font-weight: 600;
            color: {t.text_secondary};
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .panel-title {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: {t.text_muted};
            margin: 1rem 0 0.6rem 0;
        }}

        .panel-title:first-child {{
            margin-top: 0;
        }}

        .map-card, .side-card {{
            background: {t.bg};
            border: 1px solid {t.border};
            border-radius: 14px;
            padding: 1rem 1.1rem;
        }}

        .map-hint {{
            font-size: 0.88rem;
            color: {t.text_secondary};
            margin-bottom: 0.75rem;
        }}

        .location-row {{
            display: flex;
            align-items: flex-start;
            gap: 0.7rem;
            padding: 0.35rem 0;
        }}

        .location-dot {{
            width: 10px;
            height: 10px;
            margin-top: 0.3rem;
            flex-shrink: 0;
        }}

        .location-dot.pickup {{
            background: {t.pickup};
            border-radius: 50%;
        }}

        .location-dot.dropoff {{
            background: {t.dropoff};
            border-radius: 2px;
        }}

        .location-label {{
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {t.text_muted};
        }}

        .location-coords {{
            font-size: 0.82rem;
            color: {t.text_secondary};
            font-variant-numeric: tabular-nums;
        }}

        .location-divider {{
            border-left: 2px dashed {t.border};
            margin-left: 4px;
            height: 10px;
        }}

        .fare-panel {{
            background: {t.surface};
            border: 1px solid {t.border};
            border-radius: 12px;
            padding: 1.2rem;
            margin-top: 0.75rem;
        }}

        .fare-amount {{
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1;
        }}

        .fare-meta {{
            font-size: 0.95rem;
            color: {t.text_secondary};
            margin-top: 0.35rem;
        }}

        .fare-range {{
            font-size: 0.82rem;
            color: {t.text_muted};
            margin-top: 0.45rem;
        }}

        .surge-banner {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 0.75rem;
            padding: 0.6rem 0.8rem;
            background: #FDF2F0;
            border: 1px solid #F0C4BE;
            border-radius: 8px;
            font-size: 0.82rem;
            color: {t.warning};
            font-weight: 600;
        }}

        .surge-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: {t.warning};
        }}

        .empty-state {{
            text-align: center;
            padding: 1.75rem 1rem;
            color: {t.text_muted};
            font-size: 0.88rem;
            border: 1px dashed {t.border};
            border-radius: 12px;
            margin-top: 0.75rem;
            background: {t.surface};
        }}

        .stat-card {{
            background: {t.surface};
            border: 1px solid {t.border};
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }}

        .stat-value {{
            font-size: 1.45rem;
            font-weight: 800;
        }}

        .stat-label {{
            font-size: 0.72rem;
            color: {t.text_muted};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.2rem;
        }}

        .stNumberInput input, .stDateInput input, .stTimeInput input {{
            background-color: {t.bg} !important;
            color: {t.text_primary} !important;
            border: 1px solid {t.border} !important;
        }}

        div[data-baseweb="input"] {{
            background-color: {t.bg};
            border-color: {t.border};
        }}
            display: inline-block;
            padding: 0.5rem 0.9rem;
            background: #EEFBF4;
            border: 1px solid #B8E8CC;
            border-radius: 8px;
            color: {t.success};
            font-size: 0.88rem;
            font-weight: 600;
            margin-top: 0.75rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        f"""
        <div class="app-header">
            <span class="app-logo">{APP_TITLE}</span>
            <span class="app-city">{APP_CITY}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
