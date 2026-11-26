"""Dark geospatial command theme for the Maritime Intelligence Engine.

Presentation-only layer. It does not alter AIS ingestion, engine state,
analytics, provenance, or collection lifecycle.
"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

DARK_MATTER_STYLE = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');
:root {
 --mie-bg:#0B1219; --mie-panel:#111C27; --mie-panel2:#162331;
 --mie-line:#263746; --mie-line2:#345064; --mie-text:#D9E4EA;
 --mie-muted:#8296A5; --mie-cyan:#3D9BDB; --mie-green:#39C98A;
 --mie-amber:#D4A017; --mie-red:#E45C62;
}
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:var(--mie-bg)!important;color:var(--mie-text)!important}
.block-container{max-width:1780px!important;padding:.75rem 1rem 2rem!important}
[data-testid="stSidebar"]{background:#0D1721!important;border-right:1px solid var(--mie-line)!important}
header[data-testid="stHeader"]{background:#0B1219!important}
h1,h2,h3,h4,p,label,span{color:var(--mie-text)}
h1{font-size:1.28rem!important;letter-spacing:.02em}
h2{font-size:1rem!important;letter-spacing:.04em}
h3{font-size:.86rem!important;letter-spacing:.06em}
[data-testid="stCaptionContainer"],.small-note,.data-label,.panel-title{color:var(--mie-muted)!important}
[data-testid="stMetric"],.panel,.ops-bar,div[data-testid="stExpander"]{background:linear-gradient(145deg,var(--mie-panel),#0E1822)!important;border:1px solid var(--mie-line)!important;border-radius:3px!important;box-shadow:inset 0 1px #ffffff08!important}
[data-testid="stMetricLabel"]{color:var(--mie-muted)!important;font-size:.6rem!important;letter-spacing:.09em;text-transform:uppercase}
[data-testid="stMetricValue"],.data-value,.ops-metric .val{color:var(--mie-text)!important;font-family:'IBM Plex Mono',monospace!important}
[data-testid="stDataFrame"]{border:1px solid var(--mie-line)!important;border-radius:3px!important;overflow:hidden}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,textarea{background:#0D1923!important;border-color:var(--mie-line2)!important;color:var(--mie-text)!important}
input,textarea{color:var(--mie-text)!important}
.stButton>button{background:#142432!important;color:var(--mie-text)!important;border:1px solid var(--mie-line2)!important;border-radius:3px!important;font-family:'IBM Plex Mono',monospace!important;font-size:.72rem!important;letter-spacing:.035em}
.stButton>button:hover{border-color:var(--mie-cyan)!important;color:var(--mie-cyan)!important;box-shadow:0 0 12px #3D9BDB22}
.stButton>button[kind="primary"]{background:#12364A!important;border-color:var(--mie-cyan)!important;color:#BCE8FF!important}
.operational-header{border-bottom:1px solid var(--mie-line2)!important;padding:.15rem 0 .65rem!important}
.brand{color:var(--mie-text)!important;font-family:'IBM Plex Mono',monospace!important;letter-spacing:.12em!important}
.brand small,.utc{color:var(--mie-muted)!important}
.status-pill{background:#0D1923!important;border-color:var(--mie-line2)!important;font-family:'IBM Plex Mono',monospace!important}
.status-live{color:var(--mie-green)!important;background:#0D241D!important;border-color:#24664B!important}
.status-connecting{color:var(--mie-amber)!important;background:#261F0E!important;border-color:#6A531C!important}
.status-disconnected{color:var(--mie-red)!important;background:#281519!important;border-color:#71313A!important}
.panel-title,.data-label,.ops-metric .lbl,.section-kicker,.side-section-title,.side-section-label{color:var(--mie-muted)!important}
.empty-state{background:#0D1923!important;border-color:#345064!important;color:var(--mie-muted)!important;border-radius:3px!important}
.empty-state strong{color:var(--mie-amber)!important}
.notice{background:#241F12!important;color:#E8D7A3!important;border-left-color:var(--mie-amber)!important}
.notice-red{background:#281519!important;color:#F0B9BD!important;border-left-color:var(--mie-red)!important}
.notice-green{background:#0D241D!important;color:#B5E7D0!important;border-left-color:var(--mie-green)!important}
.ops-bar,.intel-status{background:var(--mie-panel)!important;border-color:var(--mie-line)!important}
.intel-chip{background:#0D1923!important;border-color:var(--mie-line2)!important}
.intel-ready{color:var(--mie-green)!important;border-color:#24664B!important}
.intel-partial{color:var(--mie-amber)!important;border-color:#6A531C!important}
.intel-enabled{color:var(--mie-cyan)!important;border-color:#245778!important}
.intel-waiting,.intel-disabled{color:var(--mie-muted)!important}
.prov-live{color:var(--mie-green)!important;background:#0D241D!important;border-color:#24664B!important}
.prov-historical{color:var(--mie-cyan)!important;background:#102435!important;border-color:#245778!important}
.prov-derived{color:var(--mie-amber)!important;background:#261F0E!important;border-color:#6A531C!important}
.prov-insufficient{color:var(--mie-muted)!important;background:#0D1923!important;border-color:var(--mie-line)!important}
.side-header{border-bottom-color:var(--mie-line)!important}
.side-section-title{border-top-color:var(--mie-line)!important}
hr{border-top-color:var(--mie-line)!important}
[data-testid="stCheckbox"] label,[data-testid="stRadio"] label{color:var(--mie-text)!important}
[data-testid="stTabs"] button{color:var(--mie-muted)!important}
[data-testid="stTabs"] button[aria-selected="true"]{color:var(--mie-cyan)!important;border-bottom-color:var(--mie-cyan)!important}
[data-testid="stAlert"]{background:#111C27!important;border:1px solid var(--mie-line)!important}
.js-plotly-plot .plotly .modebar{background:transparent!important}
@media(max-width:980px){.ops-bar{grid-template-columns:1fr!important}.ops-meta{text-align:left!important}.ops-metrics{justify-content:flex-start!important}}
@media(max-width:760px){.block-container{padding:.65rem .55rem 1.5rem!important}.operational-header{align-items:flex-start!important;gap:.4rem}.brand small{display:block;margin:.12rem 0 0}}
</style>
"""

def _dark_plotly(fig):
    if not isinstance(fig, go.Figure):
        return fig
    fig.update_layout(
        paper_bgcolor="#111C27",
        plot_bgcolor="#0B1219",
        font={"family": "IBM Plex Mono, monospace", "color": "#D9E4EA", "size": 10},
        title={"font": {"size": 12, "color": "#D9E4EA"}, "x": 0},
        xaxis={"gridcolor": "#263746", "zerolinecolor": "#345064", "linecolor": "#345064"},
        yaxis={"gridcolor": "#263746", "zerolinecolor": "#345064", "linecolor": "#345064"},
        legend={"bgcolor": "rgba(17,28,39,.72)", "font": {"color": "#D9E4EA"}},
        hoverlabel={"bgcolor": "#162331", "font": {"color": "#D9E4EA"}},
        margin={"l": 35, "r": 15, "t": 35, "b": 30},
    )
    try:
        fig.update_geos(
            showland=True, landcolor="#182A32", showocean=True,
            oceancolor="#0A1B25", showcountries=True, countrycolor="#405765",
            coastlinecolor="#66808D", bgcolor="#0B1219",
        )
    except Exception:
        pass
    return fig

def _dark_deck(deck):
    if deck is not None and hasattr(deck, "map_style"):
        deck.map_style = DARK_MATTER_STYLE
    tooltip = getattr(deck, "tooltip", None) if deck is not None else None
    if isinstance(tooltip, dict):
        style = dict(tooltip.get("style") or {})
        style.update({"backgroundColor": "#111C27", "color": "#D9E4EA", "border": "1px solid #345064"})
        tooltip["style"] = style
        deck.tooltip = tooltip
    return deck

def inject_dark_theme():
    """Install presentation-only dark styles and chart adapters once per process."""
    if getattr(st, "_mie_dark_theme_installed", False):
        st.markdown(DARK_CSS, unsafe_allow_html=True)
        return
    original_plotly_chart = st.plotly_chart
    original_pydeck_chart = st.pydeck_chart

    def dark_plotly_chart(figure_or_data, *args, **kwargs):
        return original_plotly_chart(_dark_plotly(figure_or_data), *args, **kwargs)

    def dark_pydeck_chart(*args, **kwargs):
        if args:
            args = (_dark_deck(args[0]), *args[1:])
        elif "deck" in kwargs:
            kwargs["deck"] = _dark_deck(kwargs["deck"])
        return original_pydeck_chart(*args, **kwargs)

    st.plotly_chart = dark_plotly_chart
    st.pydeck_chart = dark_pydeck_chart
    st.session_state["map_style"] = "Dark Matter"
    st._mie_dark_theme_installed = True
    st.markdown(DARK_CSS, unsafe_allow_html=True)
