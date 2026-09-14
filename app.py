"""
European Bank Customer Analytics
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""

import base64
import io

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="European Bank Customer Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COLOR PALETTE (Enterprise Bloomberg / Modern Financial Theme)
# =========================================================

BG_DARK = "#0B0F17"          # Deep near-black background
SURFACE = "#121824"          # Card & panel surface
SURFACE_HOVER = "#182030"    # Hover surface
BORDER = "#1E293B"           # Subtle container border

RED = "#E52335"              # Primary European Bank Accent Red
RED_MUTED = "rgba(229, 35, 53, 0.15)"

WHITE = "#F8FAFC"            # Primary text
TEXT_MUTED = "#94A3B8"       # Secondary labels & subtitles
TEXT_DARK = "#64748B"        # Captions & quiet text

SLATE_BAR = "#334155"       # Base bar color for neutral/stayed metrics
BLUE_ACCENT = "#3B82F6"      # Positive / secondary accent


# =========================================================
# HTML RENDERING HELPERS
# =========================================================

def _clean_html(content: str) -> str:
    lines = []
    for line in content.strip().splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def html(content: str) -> None:
    """Render a normalized HTML string safely without markdown codeblock triggering."""
    st.markdown(_clean_html(content), unsafe_allow_html=True)


# =========================================================
# SVG ICON SYSTEM (Inline crisp SVG icons)
# =========================================================

ICONS = {
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "user": '<circle cx="12" cy="7" r="4"/><path d="M5.5 21a6.5 6.5 0 0 1 13 0"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "chart": '<line x1="4" y1="19" x2="4" y2="10"/><line x1="10" y1="19" x2="10" y2="5"/><line x1="16" y1="19" x2="16" y2="8"/><line x1="22" y1="19" x2="22" y2="3"/>',
    "trend": '<polyline points="3 17 9 11 13 15 21 7"/><polyline points="15 7 21 7 21 13"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
    "wallet": '<path d="M20 7H5a3 3 0 0 1 0-6h14a2 2 0 0 1 2 2v15a4 4 0 0 1-4 4H5a3 3 0 0 1-3-3V4"/><path d="M16 13h4"/>',
    "heart": '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 0 20"/><path d="M12 2a15.3 15.3 0 0 0 0 20"/>',
    "search": '<circle cx="11" cy="11" r="7"/><line x1="20" y1="20" x2="16.65" y2="16.65"/>',
    "filter": '<line x1="4" y1="6" x2="20" y2="6"/><line x1="7" y1="12" x2="17" y2="12"/><line x1="10" y1="18" x2="14" y2="18"/>',
    "lightbulb": '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.56.46-1.09.91-1.54A5.5 5.5 0 1 0 8 12.46c.45.45.73.98.91 1.54"/><path d="M9 14h6"/>',
    "document": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/><path d="M4 12v7c0 1.66 3.58 3 8 3s8-1.34 8-3v-7"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="9" y1="6" x2="9" y2="6"/><line x1="15" y1="6" x2="15" y2="6"/><line x1="9" y1="10" x2="9" y2="10"/><line x1="15" y1="10" x2="15" y2="10"/><line x1="9" y1="14" x2="9" y2="14"/><line x1="15" y1="14" x2="15" y2="14"/><line x1="9" y1="18" x2="15" y2="18"/>',
}


def icon(name: str, size: int = 16, color: str = RED) -> str:
    """Return a single-line inline SVG icon string."""
    body = ICONS.get(name, "")
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round">{body}</svg>'
    )


# =========================================================
# CHART HELPERS (High-DPI Matplotlib PNGs)
# =========================================================

def fig_to_png(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight", transparent=True)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def _style_axes(ax) -> None:
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.spines["bottom"].set_linewidth(1)
    ax.tick_params(colors=TEXT_MUTED, labelsize=8.5, length=0, pad=4)
    ax.grid(axis="y", color=BORDER, linewidth=0.8, alpha=0.4)
    ax.set_axisbelow(True)


def bar_chart_png(series, color=RED, figsize=(5.5, 2.1), fmt="{:.1f}%") -> str:
    """Render a clean vertical bar chart as a base64 PNG string."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    _style_axes(ax)

    labels = [str(i) for i in series.index]
    values = [float(v) for v in series.values]
    bar_colors = color if isinstance(color, (list, tuple)) else color

    bars = ax.bar(labels, values, color=bar_colors, width=0.45, zorder=3)
    top = max(values) if values else 1.0

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + (top * 0.03 if top > 0 else 0.1),
            fmt.format(value),
            ha="center",
            va="bottom",
            color=WHITE,
            fontsize=8.5,
            fontweight="bold",
        )

    ax.set_ylim(0, top * 1.24 if top > 0 else 1)
    return fig_to_png(fig)


def donut_png(values, labels, center_value, center_label,
              colors=(SLATE_BAR, RED)) -> str:
    """Render a compact donut chart as a base64 PNG string."""
    fig, ax = plt.subplots(figsize=(4.0, 2.0))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.36, "edgecolor": SURFACE, "linewidth": 2.0},
        colors=list(colors),
        autopct="%1.1f%%",
        pctdistance=0.76,
        textprops={"color": WHITE, "fontsize": 8.0, "fontweight": "bold"},
    )

    for text in texts:
        text.set_color(TEXT_MUTED)
        text.set_fontsize(8.0)

    ax.text(0, 0.08, center_value, ha="center", va="center",
            color=WHITE, fontsize=15, fontweight="bold")
    ax.text(0, -0.15, center_label, ha="center", va="center",
            color=TEXT_MUTED, fontsize=8.0)
    return fig_to_png(fig)


# =========================================================
# UI BUILDERS (Structured Layout Rhythm & Spacing)
# =========================================================

def panel_heading(icon_name, title, subtitle=""):
    sub = f"<div class='section-subtitle'>{subtitle}</div>" if subtitle else ""
    return (
        "<div class='section-heading'>"
        f"<div class='section-icon'>{icon(icon_name, 14, RED)}</div>"
        f"<div><div class='section-title'>{title}</div>{sub}</div>"
        "</div>"
    )


def chart_panel(icon_name, title, subtitle, image, img_class="", panel_class=""):
    html(f"""
    <div class="panel {panel_class.strip()}">
        {panel_heading(icon_name, title, subtitle)}
        <div class="chart-fit {img_class.strip()}">
            <img src="data:image/png;base64,{image}" alt="{title}">
        </div>
    </div>
    """)


def table_panel(icon_name, title, subtitle, table_html, panel_class=""):
    html(f"""
    <div class="panel {panel_class.strip()}">
        {panel_heading(icon_name, title, subtitle)}
        {table_html}
    </div>
    """)


def html_table(df, numeric_cols=()):
    """Convert a DataFrame into a structured enterprise HTML table string."""
    headers = []
    for col in df.columns:
        cls = " class='num'" if col in numeric_cols else ""
        headers.append(f"<th{cls}>{col}</th>")

    rows = []
    for _, row in df.iterrows():
        cells = []
        for col in df.columns:
            cls = " class='num'" if col in numeric_cols else ""
            cells.append(f"<td{cls}>{row[col]}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")

    return (
        "<div class='table-wrapper'><table class='data-table'><thead><tr>"
        + "".join(headers)
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def kpi_card(icon_name, label, value, note, tag="METRIC", is_risk=False):
    """Return one compact enterprise KPI card with 16px internal padding."""
    card_class = "kpi-card risk-card" if is_risk else "kpi-card"
    tag_class = "kpi-tag risk-tag" if is_risk else "kpi-tag"

    return f"""
    <div class="{card_class}">
        <div class="kpi-header">
            <span class="kpi-label">{label}</span>
            <span class="{tag_class}">{tag}</span>
        </div>
        <div class="kpi-body">
            <div class="kpi-value">{value}</div>
            <div class="kpi-icon-badge">{icon(icon_name, 16, RED)}</div>
        </div>
        <div class="kpi-note">{note}</div>
    </div>
    """


def insight_card(icon_name, title, text, tag="INSIGHT", is_risk=False):
    """Return one actionable insight card with structured 16px internal padding."""
    card_class = "insight-card risk-insight" if is_risk else "insight-card"
    tag_class = "insight-tag risk-tag" if is_risk else "insight-tag"

    return f"""
    <div class="{card_class}">
        <div class="insight-header">
            <div class="insight-icon-wrapper">{icon(icon_name, 14, RED)}</div>
            <span class="{tag_class}">{tag}</span>
        </div>
        <div class="insight-title">{title}</div>
        <div class="insight-text">{text}</div>
    </div>
    """


# =========================================================
# SYSTEMATIC SPACING & LAYOUT STYLESHEET
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, button, input, select, textarea {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background-color: #0B0F17;
    color: #F8FAFC;
}

[data-testid="stHeader"] { background: transparent; }

/* 28px - 32px Horizontal Page Margin */
[data-testid="stMainBlockContainer"] {
    padding: 1.25rem 2rem 2.5rem;
    max-width: 1580px;
}

/* Horizontal Grid Gutter System (22px horizontal gap between cards) */
div[data-testid="stHorizontalBlock"] { gap: 1.35rem; align-items: stretch; }
div[data-testid="stHorizontalBlock"] > div {
    display: flex;
    flex-direction: column;
}
div[data-testid="stHorizontalBlock"] > div > div { flex: 1 1 auto; }

/* Main Vertical Block Gap (20px vertical spacing) */
div[data-testid="stVerticalBlock"] { gap: 1.25rem; }

/* =====================================================
   SIDEBAR - Systematic Navigation & Filter Spacing
   ===================================================== */
[data-testid="stSidebar"] {
    min-width: 255px;
    max-width: 255px;
    background-color: #0E131F;
    border-right: 1px solid #1E293B;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0 16px 0;
    border-bottom: 1px solid #1E293B;
    margin-bottom: 18px;
}

.brand-mark {
    width: 34px;
    height: 34px;
    border-radius: 6px;
    background: #E52335;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(229, 35, 53, 0.3);
}

.brand-name {
    color: #F8FAFC;
    font-size: 13.5px;
    font-weight: 700;
    letter-spacing: -0.2px;
    line-height: 1.15;
}

.brand-sub {
    color: #94A3B8;
    font-size: 8.5px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    font-weight: 600;
}

.side-label {
    font-size: 9.5px;
    letter-spacing: 1.3px;
    color: #64748B;
    text-transform: uppercase;
    font-weight: 700;
    margin: 10px 0 8px 2px;
}

/* Radio Group (Navigation Items with 4px gap) */
div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

div[role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-left: 3px solid transparent;
    border-radius: 5px;
    padding: 7px 12px;
    margin: 0;
    transition: all 0.15s ease;
    cursor: pointer;
}

div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.03);
}

div[role="radiogroup"] label p {
    color: #94A3B8;
    font-size: 12px;
    font-weight: 500;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #162032;
    border-left: 3px solid #E52335;
}

div[role="radiogroup"] label:has(input:checked) p {
    color: #F8FAFC;
    font-weight: 600;
}

[data-testid="stSidebar"] label {
    color: #94A3B8;
    font-size: 10.5px;
    font-weight: 500;
    margin-bottom: 6px;
}

/* Sidebar Widgets: 20px Vertical Buffer Between Filter Groups */
[data-testid="stSidebar"] div.stMultiSelect,
[data-testid="stSidebar"] div.stSelectbox,
[data-testid="stSidebar"] div.stSlider {
    margin-bottom: 20px;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #121824;
    border-color: #1E293B;
    border-radius: 5px;
    color: #F8FAFC;
    font-size: 11.5px;
    min-height: 34px;
}

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #1E293B;
    border-radius: 3px;
    padding: 2px 7px;
    margin-top: 4px;
}

[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #F8FAFC;
    font-size: 10.5px;
}

[data-testid="stSidebar"] [data-baseweb="slider"] {
    padding-top: 4px;
}

/* TOP BAR (20px Margin to Page Header) */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 12px;
    padding-bottom: 14px;
    border-bottom: 1px solid #1E293B;
}

.search-box {
    flex: 1 1 auto;
    max-width: 480px;
    height: 36px;
    border: 1px solid #1E293B;
    border-radius: 6px;
    background: #121824;
    display: flex;
    align-items: center;
    padding: 0 12px;
    color: #64748B;
    font-size: 11.5px;
    transition: border-color 0.15s ease;
}

.search-box:hover {
    border-color: #334155;
}

.profile {
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(59, 130, 246, 0.08);
    border: 1px solid rgba(59, 130, 246, 0.22);
    padding: 4px 10px;
    border-radius: 16px;
    color: #60A5FA;
    font-size: 10.5px;
    font-weight: 500;
}

.status-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: #3B82F6;
    box-shadow: 0 0 6px #3B82F6;
}

.avatar {
    width: 30px;
    height: 30px;
    border-radius: 6px;
    background: #1E293B;
    border: 1px solid #334155;
    color: #F8FAFC;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 10.5px;
    letter-spacing: 0.5px;
}

/* PAGE HERO HEADER (22px Margin to KPI Row) */
.hero {
    padding: 0 0 22px 0;
}

.eyebrow {
    color: #E52335;
    font-size: 9.5px;
    letter-spacing: 1.8px;
    font-weight: 700;
    margin-bottom: 4px;
    text-transform: uppercase;
}

.hero-title {
    color: #F8FAFC;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.4px;
    line-height: 1.15;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 4px;
    font-weight: 400;
}

/* ENTERPRISE KPI CARDS (16px Card Padding, 22px Bottom Margin) */
.kpi-card {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 112px;
    padding: 14px 16px;
    border: 1px solid #1E293B;
    border-radius: 8px;
    background: #121824;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
    box-sizing: border-box;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.kpi-card:hover {
    transform: translateY(-1px);
    border-color: #334155;
}

.kpi-card.risk-card {
    border-color: rgba(229, 35, 53, 0.28);
    background: linear-gradient(180deg, rgba(229, 35, 53, 0.04) 0%, #121824 100%);
}

.kpi-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
}

.kpi-label {
    color: #94A3B8;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-tag {
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
    background: rgba(148, 163, 184, 0.1);
    color: #94A3B8;
    letter-spacing: 0.4px;
}

.kpi-tag.risk-tag {
    background: rgba(229, 35, 53, 0.14);
    color: #F87171;
    border: 1px solid rgba(229, 35, 53, 0.25);
}

.kpi-body {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 8px;
    margin-top: 6px;
}

.kpi-value {
    color: #F8FAFC;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: -0.5px;
    font-variant-numeric: tabular-nums;
    line-height: 1;
}

.kpi-icon-badge {
    width: 30px;
    height: 30px;
    border-radius: 6px;
    background: rgba(229, 35, 53, 0.08);
    border: 1px solid rgba(229, 35, 53, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.kpi-note {
    color: #64748B;
    font-size: 10.5px;
    margin-top: 8px;
    line-height: 1.25;
}

/* PANELS & CONTAINER CARDS (16px Internal Padding, 22px Bottom Margin) */
.panel {
    background: #121824;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 22px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
    box-sizing: border-box;
    height: 100%;
    transition: border-color 0.15s ease;
}

.panel:hover {
    border-color: #334155;
}

.panel-tall { min-height: 260px; }

.section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}

.section-heading > div:last-child { flex: 1 1 auto; min-width: 0; }

.section-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: rgba(229, 35, 53, 0.1);
    border: 1px solid rgba(229, 35, 53, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.section-title {
    color: #F8FAFC;
    font-size: 13.5px;
    font-weight: 600;
    letter-spacing: -0.2px;
    line-height: 1.2;
}

.section-subtitle {
    color: #94A3B8;
    font-size: 10.5px;
    margin-top: 3px;
}

.chart-fit {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 6px;
    height: 190px;
}

.chart-fit img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
}

.chart-fit.donut-fit img {
    object-fit: contain;
    max-width: 100%;
}

/* CUSTOMER SUMMARY TABLE (Structured Spacing) */
.table-wrapper {
    width: 100%;
    overflow-x: auto;
    margin-top: 14px;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
}

.data-table th {
    text-align: left;
    color: #94A3B8;
    font-size: 9.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 7.5px 10px;
    border-bottom: 1px solid #1E293B;
    background: rgba(255, 255, 255, 0.012);
}

.data-table td {
    color: #E2E8F0;
    padding: 7.5px 10px;
    border-bottom: 1px solid rgba(30, 41, 59, 0.5);
}

.data-table tr:hover td {
    background: rgba(255, 255, 255, 0.02);
}

.data-table tr:last-child td { border-bottom: none; }
.data-table td.num, .data-table th.num { text-align: right; font-variant-numeric: tabular-nums; }

/* ACTIONABLE INSIGHT CARDS (16px Padding, 28px Gap Above Section) */
.insight-section-wrapper {
    margin-top: 28px;
}

.insight-card {
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 14px 16px;
    background: #121824;
    height: 100%;
    box-sizing: border-box;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.insight-card:hover {
    transform: translateY(-1px);
    border-color: #334155;
}

.insight-card.risk-insight {
    border-color: rgba(229, 35, 53, 0.28);
    background: linear-gradient(180deg, rgba(229, 35, 53, 0.04) 0%, #121824 100%);
}

.insight-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.insight-icon-wrapper {
    width: 26px;
    height: 26px;
    border-radius: 5px;
    background: rgba(229, 35, 53, 0.08);
    display: flex;
    align-items: center;
    justify-content: center;
}

.insight-tag {
    font-size: 8.5px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
    background: rgba(59, 130, 246, 0.12);
    color: #60A5FA;
    letter-spacing: 0.4px;
}

.insight-tag.risk-tag {
    background: rgba(229, 35, 53, 0.14);
    color: #F87171;
}

.insight-title {
    color: #F8FAFC;
    font-size: 12.5px;
    font-weight: 600;
    margin-bottom: 6px;
}

.insight-text {
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.45;
}

/* FOOTER */
.footer {
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #1E293B;
    text-align: center;
    color: #64748B;
    font-size: 10.5px;
    font-weight: 500;
}

/* RESPONSIVE BREAKPOINTS */
@media (max-width: 1024px) {
    div[data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 100%;
        min-width: 0;
    }
}

@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        width: 220px;
        min-width: 220px;
        max-width: 220px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/European_Bank.csv")


df = load_data().copy()


# =========================================================
# DERIVED FEATURES (Analytics logic unchanged)
# =========================================================

high_balance_threshold = df["Balance"].quantile(0.75)
df["HighBalance"] = df["Balance"] >= high_balance_threshold


def relationship_category(row):
    if row["NumOfProducts"] >= 3:
        return "Product-Risk"
    elif row["IsActiveMember"] == 1 and row["NumOfProducts"] == 2:
        return "Strong"
    elif row["IsActiveMember"] == 1 and row["NumOfProducts"] == 1:
        return "Moderate"
    else:
        return "Weak"


df["RelationshipCategory"] = df.apply(relationship_category, axis=1)


# =========================================================
# SIDEBAR: BRAND + NAVIGATION + FILTERS
# =========================================================

with st.sidebar:

    html(f"""
    <div class="brand">
        <div class="brand-mark">{icon("building", 18, "#FFFFFF")}</div>
        <div>
            <div class="brand-name">European Bank</div>
            <div class="brand-sub">Customer Analytics</div>
        </div>
    </div>
    """)

    html("""
    <div class="side-label">Navigation</div>
    """)

    page = st.radio(
        "Dashboard Navigation",
        [
            "Overview",
            "Engagement Analysis",
            "Product Analysis",
            "High-Value Customers",
            "Relationship Strength",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin: 22px 0 18px 0; border-top: 1px solid #1E293B;'></div>", unsafe_allow_html=True)

    html(f"""
    <div class="side-label" style="display:flex;align-items:center;gap:6px;color:#94A3B8;margin-bottom:12px;">
        {icon("filter", 13, RED)}
        <span>Filter Parameters</span>
    </div>
    """)

    geography = st.multiselect(
        "Geography",
        sorted(df["Geography"].unique()),
        default=sorted(df["Geography"].unique()),
    )

    gender = st.multiselect(
        "Gender",
        sorted(df["Gender"].unique()),
        default=sorted(df["Gender"].unique()),
    )

    age_range = st.slider(
        "Age Range",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max())),
    )

    product_range = st.slider(
        "Number of Products",
        int(df["NumOfProducts"].min()),
        int(df["NumOfProducts"].max()),
        (int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max())),
    )

    activity = st.selectbox(
        "Engagement",
        ["All", "Active", "Inactive"],
    )

    balance_range = st.slider(
        "Balance Range",
        float(df["Balance"].min()),
        float(df["Balance"].max()),
        (float(df["Balance"].min()), float(df["Balance"].max())),
    )


# =========================================================
# APPLY FILTERS (Filtering logic unchanged)
# =========================================================

filtered_df = df[
    (df["Geography"].isin(geography))
    & (df["Gender"].isin(gender))
    & (df["Age"].between(age_range[0], age_range[1]))
    & (df["NumOfProducts"].between(product_range[0], product_range[1]))
    & (df["Balance"].between(balance_range[0], balance_range[1]))
].copy()

if activity == "Active":
    filtered_df = filtered_df[filtered_df["IsActiveMember"] == 1]
elif activity == "Inactive":
    filtered_df = filtered_df[filtered_df["IsActiveMember"] == 0]

if filtered_df.empty:
    st.warning(
        "No customers match the current filters. "
        "Adjust the sidebar filters to see results."
    )
    st.stop()


# =========================================================
# TOP BAR + HERO (Shared across all pages)
# =========================================================

html(f"""
<div class="topbar">
    <div class="search-box">
        {icon("search", 14, "#64748B")}
        <span style="margin-left:8px;">Search customer ID, segment, geography...</span>
    </div>
    <div class="profile">
        <div class="status-pill">
            <span class="status-dot"></span>
            <span>2025 Analytics Active</span>
        </div>
        <div class="avatar">EA</div>
    </div>
</div>
""")

html("""
<div class="hero">
    <div class="eyebrow">CUSTOMER ANALYTICS</div>
    <div class="hero-title">European Bank Customer Analytics</div>
    <div class="hero-subtitle">Customer Engagement &amp; Product Utilization Analytics for Retention Strategy</div>
</div>
""")


# =========================================================
# PAGE: OVERVIEW
# =========================================================

if page == "Overview":

    total_customers = len(filtered_df)
    churned_customers = int(filtered_df["Exited"].sum())
    churn_rate = filtered_df["Exited"].mean() * 100
    active_customers = int((filtered_df["IsActiveMember"] == 1).sum())
    inactive_customers = int((filtered_df["IsActiveMember"] == 0).sum())
    high_value_disengaged = filtered_df[
        (filtered_df["Balance"] >= high_balance_threshold)
        & (filtered_df["IsActiveMember"] == 0)
    ]

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        html(kpi_card(
            "users", "Total Customers", f"{total_customers:,}",
            "Customers in selection",
            tag="SELECTION"
        ))
    with k2:
        html(kpi_card(
            "trend", "Churn Rate", f"{churn_rate:.2f}%",
            f"{churned_customers:,} exited members",
            tag="RISK METRIC", is_risk=True
        ))
    with k3:
        html(kpi_card(
            "activity", "Active Customers", f"{active_customers:,}",
            f"{inactive_customers:,} inactive members",
            tag="ENGAGEMENT"
        ))
    with k4:
        html(kpi_card(
            "wallet", "High-Value Disengaged", f"{len(high_value_disengaged):,}",
            f"Balance ≥ €{high_balance_threshold:,.0f}",
            tag="PRIORITY RISK", is_risk=True
        ))

    left, right = st.columns(2)

    with left:
        stayed = total_customers - churned_customers
        chart_panel(
            "users",
            "Customer Status",
            "Stayed versus churned customers proportion",
            donut_png(
                [stayed, churned_customers],
                ["Stayed", "Churned"],
                f"{total_customers:,}",
                "Total Customers",
                colors=(SLATE_BAR, RED),
            ),
            img_class="donut-fit",
        )

    with right:
        engagement_churn = (
            filtered_df.groupby("IsActiveMember")["Exited"]
            .mean().mul(100)
            .reindex([0, 1]).fillna(0)
        )
        engagement_churn.index = ["Inactive", "Active"]
        chart_panel(
            "chart",
            "Churn by Engagement",
            "Churn rate comparison between active and inactive members",
            bar_chart_png(engagement_churn, color=[RED, SLATE_BAR], figsize=(5.5, 2.1)),
        )

    left, right = st.columns(2)

    with left:
        geo_churn = (
            filtered_df.groupby("Geography")["Exited"]
            .mean().mul(100).sort_values(ascending=False)
        )
        chart_panel(
            "globe",
            "Churn by Geography",
            "Churn rate across customer regional markets",
            bar_chart_png(geo_churn, color=RED, figsize=(5.5, 2.1)),
            panel_class="panel-tall",
        )

    with right:
        avg_balance = filtered_df["Balance"].mean()
        summary = pd.DataFrame({
            "Metric": [
                "Total Customers",
                "Churned Customers",
                "Churn Rate",
                "Active Customers",
                "Inactive Customers",
                "High-Value Disengaged",
                "Average Balance (€)",
            ],
            "Value": [
                f"{total_customers:,}",
                f"{churned_customers:,}",
                f"{churn_rate:.2f}%",
                f"{active_customers:,}",
                f"{inactive_customers:,}",
                f"{len(high_value_disengaged):,}",
                f"€{avg_balance:,.0f}",
            ],
        })
        table_panel(
            "document",
            "Customer Summary",
            "Key baseline statistics for current selection",
            html_table(summary),
            panel_class="panel-tall",
        )

    html(f"""
    <div class="insight-section-wrapper">
        <div class="section-heading" style="margin-bottom:14px;">
            <div class="section-icon">{icon("lightbulb", 14, RED)}</div>
            <div>
                <div class="section-title">Key Insights & Executive Summary</div>
                <div class="section-subtitle">Critical retention drivers and risk indicators</div>
            </div>
        </div>
    </div>
    """)

    i1, i2, i3 = st.columns(3)
    with i1:
        html(insight_card(
            "activity",
            "Engagement Matters",
            "Active customers demonstrate substantially lower churn rates compared to inactive members, confirming engagement as a primary retention lever.",
            tag="RETENTION LEVER", is_risk=False
        ))
    with i2:
        html(insight_card(
            "wallet",
            "High-Value Risk",
            f"{len(high_value_disengaged):,} customers maintain high balances (top quartile) yet remain disengaged, posing significant revenue capital risk.",
            tag="HIGH PRIORITY", is_risk=True
        ))
    with i3:
        html(insight_card(
            "trend",
            "Overall Churn Concentration",
            f"{churn_rate:.2f}% overall churn rate indicates critical segments require targeted retention workflows and structured customer outreach.",
            tag="KEY METRIC", is_risk=False
        ))


# =========================================================
# PAGE: ENGAGEMENT ANALYSIS
# =========================================================

elif page == "Engagement Analysis":

    engagement_summary = (
        filtered_df.groupby("IsActiveMember")
        .agg(
            Customers=("CustomerId", "count"),
            Churned=("Exited", "sum"),
            Churn_Rate=("Exited", "mean"),
        )
        .reset_index()
    )
    engagement_summary["Engagement"] = engagement_summary["IsActiveMember"].map(
        {0: "Inactive", 1: "Active"}
    )
    engagement_summary["Churn_Rate"] *= 100

    active_row = engagement_summary[engagement_summary["Engagement"] == "Active"]
    inactive_row = engagement_summary[engagement_summary["Engagement"] == "Inactive"]

    active_count = int(active_row["Customers"].iloc[0]) if not active_row.empty else 0
    active_churn = float(active_row["Churn_Rate"].iloc[0]) if not active_row.empty else 0.0
    inactive_count = int(inactive_row["Customers"].iloc[0]) if not inactive_row.empty else 0
    inactive_churn = float(inactive_row["Churn_Rate"].iloc[0]) if not inactive_row.empty else 0.0

    e1, e2, e3, e4 = st.columns(4)
    with e1:
        html(kpi_card("activity", "Active Members", f"{active_count:,}",
                      "Currently engaged account holders", tag="ENGAGED"))
    with e2:
        html(kpi_card("trend", "Active Churn", f"{active_churn:.2f}%",
                      "Churn rate among active members", tag="STABLE"))
    with e3:
        html(kpi_card("user", "Inactive Members", f"{inactive_count:,}",
                      "Disengaged account holders", tag="DISENGAGED", is_risk=True))
    with e4:
        html(kpi_card("chart", "Inactive Churn", f"{inactive_churn:.2f}%",
                      "Churn rate among inactive members", tag="HIGH CHURN", is_risk=True))

    left, right = st.columns(2)

    with left:
        distribution = (
            engagement_summary.set_index("Engagement")["Customers"]
            .reindex(["Active", "Inactive"]).fillna(0)
        )
        chart_panel(
            "users",
            "Customer Distribution by Engagement",
            "Total volume of active versus inactive account holders",
            bar_chart_png(distribution, color=[BLUE_ACCENT, SLATE_BAR], fmt="{:,.0f}"),
        )

    with right:
        churn_by_engagement = (
            engagement_summary.set_index("Engagement")["Churn_Rate"]
            .reindex(["Active", "Inactive"]).fillna(0)
        )
        chart_panel(
            "chart",
            "Churn Rate by Engagement Group",
            "Comparative churn rate across active and inactive cohorts",
            bar_chart_png(churn_by_engagement, color=[SLATE_BAR, RED]),
        )

    display_engagement = engagement_summary.copy()
    display_engagement["Churn_Rate"] = display_engagement["Churn_Rate"].round(2)
    display_engagement = display_engagement[[
        "Engagement", "Customers", "Churned", "Churn_Rate"
    ]]
    display_engagement.columns = [
        "Engagement Status", "Total Customers", "Churned Count", "Churn Rate (%)"
    ]
    table_panel(
        "document",
        "Engagement Performance Metrics",
        "Detailed statistical breakdown by member activity level",
        html_table(
            display_engagement,
            numeric_cols=("Total Customers", "Churned Count", "Churn Rate (%)"),
        ),
    )

    st.info(
        f"Inactive customers present a churn rate of **{inactive_churn:.2f}%**, "
        f"compared with **{active_churn:.2f}%** for active customers "
        f"(a difference of **{inactive_churn - active_churn:.2f} percentage points**). "
        "Re-engagement initiatives represent the most direct opportunity for retention enhancement."
    )


# =========================================================
# PAGE: PRODUCT ANALYSIS
# =========================================================

elif page == "Product Analysis":

    product_analysis = (
        filtered_df.groupby("NumOfProducts")
        .agg(
            Customers=("CustomerId", "count"),
            Churned=("Exited", "sum"),
            Churn_Rate=("Exited", "mean"),
        )
        .reset_index()
    )
    product_analysis["Churn_Rate"] *= 100

    most_common = (
        int(filtered_df["NumOfProducts"].mode()[0])
        if not filtered_df.empty else 0
    )
    avg_products = (
        filtered_df["NumOfProducts"].mean() if not filtered_df.empty else 0
    )
    three_plus = int((filtered_df["NumOfProducts"] >= 3).sum())

    p1, p2, p3 = st.columns(3)
    with p1:
        html(kpi_card("box", "Primary Holding Count", f"{most_common} Products",
                      "Modal product holding level", tag="MOST COMMON"))
    with p2:
        html(kpi_card("chart", "Average Products", f"{avg_products:.2f}",
                      "Mean products held per customer", tag="AVERAGE"))
    with p3:
        html(kpi_card("wallet", "3+ Product Customers", f"{three_plus:,}",
                      "High product count, elevated churn risk", tag="RISK GROUP", is_risk=True))

    product_chart = product_analysis.set_index("NumOfProducts")["Churn_Rate"]
    chart_panel(
        "box",
        "Churn Rate by Number of Products Held",
        "Evaluating customer retention across product portfolio depth",
        bar_chart_png(product_chart, color=[SLATE_BAR, SLATE_BAR, RED, RED], figsize=(6.2, 2.3)),
    )

    product_engagement = (
        filtered_df.groupby(["NumOfProducts", "IsActiveMember"])
        .agg(
            Customers=("CustomerId", "count"),
            Churned=("Exited", "sum"),
            Churn_Rate=("Exited", "mean"),
        )
        .reset_index()
    )
    product_engagement["Engagement"] = product_engagement["IsActiveMember"].map(
        {0: "Inactive", 1: "Active"}
    )
    product_engagement["Churn_Rate"] *= 100
    product_engagement["Churn_Rate"] = product_engagement["Churn_Rate"].round(2)
    display_pe = product_engagement[[
        "NumOfProducts", "Engagement", "Customers", "Churned", "Churn_Rate"
    ]]
    display_pe.columns = [
        "Product Count", "Engagement", "Customers", "Churned", "Churn Rate (%)"
    ]
    table_panel(
        "activity",
        "Product Depth & Engagement Cross-Analysis",
        "Detailed matrix combining product utilization and active membership status",
        html_table(
            display_pe,
            numeric_cols=("Product Count", "Customers", "Churned", "Churn Rate (%)"),
        ),
    )

    st.info(
        "Customers holding 2 products exhibit substantially lower churn than single-product holders. "
        "However, customers with 3 or 4 products represent an unusually high-churn segment requiring "
        "dedicated product simplification and relationship review."
    )


# =========================================================
# PAGE: HIGH-VALUE CUSTOMERS
# =========================================================

elif page == "High-Value Customers":

    high_value = filtered_df[
        (filtered_df["Balance"] >= high_balance_threshold)
        & (filtered_df["IsActiveMember"] == 0)
    ].copy()

    high_value_churn = (
        high_value["Exited"].mean() * 100 if not high_value.empty else 0
    )

    h1, h2, h3 = st.columns(3)
    with h1:
        html(kpi_card("wallet", "High-Balance Threshold",
                      f"€{high_balance_threshold:,.0f}",
                      "75th percentile of balance distribution", tag="THRESHOLD"))
    with h2:
        html(kpi_card("user", "High-Value Disengaged",
                      f"{len(high_value):,}",
                      "Top quartile balance & disengaged", tag="AT-RISK COUNT", is_risk=True))
    with h3:
        html(kpi_card("trend", "At-Risk Segment Churn",
                      f"{high_value_churn:.2f}%",
                      "Churn rate within disengaged high-balance cohort", tag="SEGMENT CHURN", is_risk=True))

    high_balance_customers = filtered_df[
        filtered_df["Balance"] >= high_balance_threshold
    ]
    active_high_balance = high_balance_customers[
        high_balance_customers["IsActiveMember"] == 1
    ]

    comparison = pd.DataFrame({
        "Group": ["High Balance + Active", "High Balance + Inactive"],
        "Customers": [len(active_high_balance), len(high_value)],
        "Churn Rate (%)": [
            round(active_high_balance["Exited"].mean() * 100, 2)
            if not active_high_balance.empty else 0.0,
            round(high_value_churn, 2),
        ],
    })

    table_panel(
        "document",
        "High-Balance Cohort Comparison",
        "Performance evaluation between active and disengaged high-balance customers",
        html_table(
            comparison,
            numeric_cols=("Customers", "Churn Rate (%)"),
        ),
    )

    chart_panel(
        "chart",
        "Churn Rate: Active vs. Inactive High-Balance Cohorts",
        "Demonstrating that balance size alone does not substitute for active member engagement",
        bar_chart_png(
            comparison.set_index("Group")["Churn Rate (%)"],
            color=[BLUE_ACCENT, RED],
            figsize=(6.5, 2.3),
        ),
    )

    html(f"""
    <div class="section-heading" style="margin-top:14px;">
        <div class="section-icon">{icon("users", 14, RED)}</div>
        <div>
            <div class="section-title">At-Risk High-Value Customer Register</div>
            <div class="section-subtitle">Individual account records for high-balance inactive members</div>
        </div>
    </div>
    """)

    customer_columns = [
        "CustomerId", "Surname", "Geography", "Gender", "Age",
        "Balance", "NumOfProducts", "EstimatedSalary", "Exited",
    ]

    if not high_value.empty:

        st.dataframe(
            high_value[customer_columns].sort_values(
                "Balance", ascending=False
            ),
            width="stretch",
            hide_index=True,
            height=360,
        )

        csv = high_value[customer_columns].to_csv(index=False)

        st.download_button(
            "Export At-Risk High-Value Records (CSV)",
            csv,
            "high_value_disengaged_customers.csv",
            "text/csv",
            type="primary",
        )

    else:

        st.success(
            "No high-value disengaged customers match the current filter selection."
        )

    st.info(
        "High-balance account holders should not be presumed loyal. "
        "Financial capital depth must be monitored alongside account activity patterns."
    )


# =========================================================
# PAGE: RELATIONSHIP STRENGTH
# =========================================================

elif page == "Relationship Strength":

    relationship_analysis = (
        filtered_df.groupby("RelationshipCategory")
        .agg(
            Customers=("CustomerId", "count"),
            Churned=("Exited", "sum"),
            Churn_Rate=("Exited", "mean"),
            Avg_Balance=("Balance", "mean"),
        )
        .reset_index()
    )
    relationship_analysis["Churn_Rate"] *= 100
    relationship_analysis["Avg_Balance"] = (
        relationship_analysis["Avg_Balance"].round(0)
    )

    strongest = filtered_df[
        filtered_df["RelationshipCategory"] == "Strong"
    ]
    strongest_churn = (
        strongest["Exited"].mean() * 100 if not strongest.empty else 0
    )

    product_risk = filtered_df[
        filtered_df["RelationshipCategory"] == "Product-Risk"
    ]
    product_risk_churn = (
        product_risk["Exited"].mean() * 100 if not product_risk.empty else 0
    )

    r1, r2, r3 = st.columns(3)
    with r1:
        html(kpi_card("heart", "Strong Relationship Members",
                      f"{len(strongest):,}",
                      "Active members holding exactly 2 products", tag="STRONG"))
    with r2:
        html(kpi_card("trend", "Strong Segment Churn",
                      f"{strongest_churn:.2f}%",
                      "Churn rate within the strong cohort", tag="BENCHMARK"))
    with r3:
        html(kpi_card("chart", "Product-Risk Churn",
                      f"{product_risk_churn:.2f}%",
                      "Churn rate for members holding 3+ products", tag="HIGH RISK", is_risk=True))

    relationship_chart = (
        relationship_analysis.set_index("RelationshipCategory")["Churn_Rate"]
        .sort_values()
    )
    chart_panel(
        "heart",
        "Churn Rate by Relationship Strength Tier",
        "Correlation between multi-product engagement tiers and retention outcomes",
        bar_chart_png(relationship_chart, color=[BLUE_ACCENT, SLATE_BAR, SLATE_BAR, RED], figsize=(6.2, 2.3)),
    )

    display_rel = relationship_analysis[[
        "RelationshipCategory", "Customers", "Churned",
        "Churn_Rate", "Avg_Balance",
    ]]
    display_rel["Churn_Rate"] = display_rel["Churn_Rate"].round(2)
    display_rel.columns = [
        "Relationship Category", "Total Customers", "Churned Count",
        "Churn Rate (%)", "Avg Balance (€)",
    ]
    table_panel(
        "document",
        "Relationship Category Breakdown",
        "Distribution, churn metrics, and balance profiles across relationship tiers",
        html_table(
            display_rel,
            numeric_cols=("Total Customers", "Churned Count", "Churn Rate (%)", "Avg Balance (€)"),
        ),
    )

    st.info(
        "Strong relationship customers (Active members holding 2 products) exhibit the highest retention stability. "
        "Conversely, the Product-Risk tier highlights that excessive product stacking without active management "
        "correlates with elevated account exit rates."
    )


# =========================================================
# FOOTER
# =========================================================

html("""
<div class="footer">
    European Bank Customer Analytics &nbsp;&bull;&nbsp;
    Customer Engagement &amp; Product Utilization Platform &nbsp;&bull;&nbsp;
    Enterprise Intelligence System
</div>
""")
