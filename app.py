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
    page_title="European Bank Analytics",
    page_icon="EB",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COLOR PALETTE
# =========================================================

NAVY = "#161E2F"
NAVY_2 = "#242F49"
SLATE = "#384358"
PEACH = "#FFA586"
RED = "#D51A29"
BURGUNDY = "#541A2E"

WHITE = "#F5F7FA"
MUTED = "#8D98AB"
BORDER = "#29354A"
DARK = "#0D1421"


# =========================================================
# HTML RENDERING HELPERS
# ---------------------------------------------------------
# Streamlit runs every st.markdown string through its Markdown
# parser first. Lines indented 4+ spaces are parsed as an
# indented CODE BLOCK and printed as raw text, and blank lines
# between tags split the HTML into separate Markdown chunks.
# The helpers below normalize every HTML string before sending
# it to st.markdown(..., unsafe_allow_html=True):
#   - leading/trailing whitespace is stripped from every line
#   - blank lines are removed
# so HTML can never be mistaken for a code block again.
# =========================================================

def _clean_html(content: str) -> str:
    lines = []
    for line in content.strip().splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def html(content: str) -> None:
    """Render a normalized HTML string safely."""
    st.markdown(_clean_html(content), unsafe_allow_html=True)


# =========================================================
# SVG ICON SYSTEM (lucide-style inline icons, no dependencies)
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
}


def icon(name: str, size: int = 20, color: str = PEACH) -> str:
    """Return a single-line inline SVG icon string."""
    body = ICONS.get(name, "")
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round">{body}</svg>'
    )


# =========================================================
# CHART HELPERS (matplotlib rendered to base64 PNG so each
# panel is ONE complete HTML block - no split div tags)
# =========================================================

def fig_to_png(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=170, bbox_inches="tight", transparent=True)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def _style_axes(ax) -> None:
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(SLATE)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.grid(axis="y", color=BORDER, linewidth=0.8, alpha=0.55)
    ax.set_axisbelow(True)


def bar_chart_png(series, color=RED, figsize=(6.4, 3.2), fmt="{:.1f}%") -> str:
    """Render a vertical bar chart as a base64 PNG string."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    _style_axes(ax)
    labels = [str(i) for i in series.index]
    values = [float(v) for v in series.values]
    bars = ax.bar(labels, values, color=color, width=0.55, zorder=3)
    top = max(values) if values else 1.0
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            fmt.format(value),
            ha="center",
            va="bottom",
            color=WHITE,
            fontsize=9,
            fontweight="bold",
        )
    ax.set_ylim(0, top * 1.28 if top > 0 else 1)
    return fig_to_png(fig)


def donut_png(values, labels, center_value, center_label,
              colors=(PEACH, RED)) -> str:
    """Render a compact donut chart as a base64 PNG string."""
    fig, ax = plt.subplots(figsize=(4.6, 2.5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.pie(
        values,
        labels=labels,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.34, "edgecolor": DARK},
        colors=list(colors),
        autopct="%1.1f%%",
        textprops={"color": WHITE, "fontsize": 9},
    )
    ax.text(0, 0.07, center_value, ha="center", va="center",
            color=WHITE, fontsize=17, fontweight="bold")
    ax.text(0, -0.14, center_label, ha="center", va="center",
            color=MUTED, fontsize=8)
    return fig_to_png(fig)


# =========================================================
# UI BUILDERS (each returns/renders one COMPLETE html block)
# =========================================================

def panel_heading(icon_name, title, subtitle=""):
    sub = f"<div class='section-subtitle'>{subtitle}</div>" if subtitle else ""
    return (
        "<div class='section-heading'>"
        f"<div class='section-icon'>{icon(icon_name, 20, PEACH)}</div>"
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
    """Convert a small DataFrame into a styled HTML table string."""
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
        "<table class='data-table'><thead><tr>"
        + "".join(headers)
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )


def kpi_card(icon_name, label, value, note):
    """Return one complete KPI card HTML block."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            <div class="kpi-icon">{icon(icon_name, 20, PEACH)}</div>
        </div>
        <div class="kpi-note">{note}</div>
    </div>
    """


def insight_card(icon_name, title, text):
    """Return one complete insight card HTML block."""
    return f"""
    <div class="insight-card">
        <div class="insight-icon">{icon(icon_name, 18, PEACH)}</div>
        <div class="insight-title">{title}</div>
        <div class="insight-text">{text}</div>
    </div>
    """


# =========================================================
# CUSTOM CSS (plain string - passed with unsafe_allow_html)
# =========================================================

st.markdown("""
<style>
html, body, [class*="css"], .stApp, button, input, select, textarea {
    font-family: "Segoe UI", "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp {
    background:
        radial-gradient(1100px 520px at 75% -12%, rgba(84,26,46,0.30), rgba(0,0,0,0)),
        #0D1421;
    color: #F5F7FA;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"] {
    padding: 1.1rem 1.7rem 2.4rem;
}
div[data-testid="stHorizontalBlock"] { gap: 1rem; align-items: stretch; }
div[data-testid="stHorizontalBlock"] > div {
    display: flex;
    flex-direction: column;
}
div[data-testid="stHorizontalBlock"] > div > div { flex: 1 1 auto; }
div[data-testid="stVerticalBlock"] { gap: 0.65rem; }

/* =====================================================
   SIDEBAR - native Streamlit sidebar, fixed width
   ===================================================== */
[data-testid="stSidebar"] {
    min-width: 258px;
    max-width: 258px;
    background: linear-gradient(180deg, #161E2F 0%, #0D1421 100%);
    border-right: 1px solid #29354A;
}
.brand { display: flex; align-items: center; gap: 11px; padding: 4px 0 12px 0; }
.brand-mark {
    width: 38px;
    height: 38px;
    border-radius: 11px;
    background: linear-gradient(135deg, #D51A29, #541A2E);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 8px 18px rgba(213,26,41,0.25);
}
.brand-name { color: #F5F7FA; font-size: 14px; font-weight: 700; letter-spacing: -0.2px; }
.brand-sub { color: #8D98AB; font-size: 9.5px; letter-spacing: 1.5px; text-transform: uppercase; }
.side-label {
    font-size: 10px;
    letter-spacing: 1.5px;
    color: #69758A;
    text-transform: uppercase;
    margin: 2px 0 8px 4px;
}
div[role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 9px;
    padding: 6px 10px;
    margin: 1px 0;
    transition: 0.2s ease;
}
div[role="radiogroup"] label:hover { background: rgba(255,255,255,0.04); border-color: #29354A; }
div[role="radiogroup"] label p { color: #AEB7C6; font-size: 12px; }
div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, #D51A29, #541A2E);
    border-color: rgba(255,165,134,0.12);
}
div[role="radiogroup"] label:has(input:checked) p { color: #FFFFFF; font-weight: 600; }
[data-testid="stSidebar"] label {
    color: #9EA8B8;
    font-size: 11px;
}
[data-testid="stSidebar"] p {
    color: #AEB7C6;
    font-size: 12px;
}

/* TOP BAR */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
    flex-wrap: wrap;
    gap: 12px;
}
.search-box {
    flex: 1 1 auto;
    max-width: 62%;
    height: 40px;
    border: 1px solid #29354A;
    border-radius: 20px;
    background: rgba(9,15,26,0.65);
    display: flex;
    align-items: center;
    padding: 0 15px;
    color: #778398;
    font-size: 11px;
}
.profile { display: flex; align-items: center; gap: 11px; }
.profile-date { color: #AEB7C6; font-size: 10.5px; }
.profile-ring {
    width: 32px;
    height: 32px;
    border: 1px solid #29354A;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #FFA586;
    color: #541A2E;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 10.5px;
}

/* HERO */
.hero { padding: 2px 0 22px 0; }
.eyebrow { color: #D51A29; font-size: 9.5px; letter-spacing: 2.2px; font-weight: 700; margin-bottom: 5px; }
.hero-title { color: #F5F7FA; font-size: 28px; font-weight: 700; letter-spacing: -0.7px; line-height: 1.12; }
.hero-subtitle { color: #9CA7B9; font-size: 12.5px; margin-top: 6px; }

/* KPI CARDS - four equal, perfectly aligned cards */
.kpi-card {
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 106px;
    padding: 16px;
    border: 1px solid #29354A;
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(36,47,73,0.86), rgba(22,30,47,0.96));
    box-shadow: 0 12px 28px rgba(0,0,0,0.12);
    box-sizing: border-box;
}
.kpi-card::after {
    content: "";
    position: absolute;
    width: 88px;
    height: 88px;
    right: -40px;
    bottom: -44px;
    border-radius: 50%;
    background: #D51A29;
    opacity: 0.08;
}
.kpi-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    flex-shrink: 0;
}
.kpi-label { color: #9EA8B8; font-size: 10.5px; margin-bottom: 5px; white-space: nowrap; }
.kpi-value { color: #F5F7FA; font-size: 23px; font-weight: 700; letter-spacing: -0.4px; }
.kpi-note { color: #6F7A8E; font-size: 9.5px; margin-top: auto; line-height: 1.35; }
.kpi-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: rgba(213,26,41,0.14);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* PANELS */
.panel {
    background: linear-gradient(145deg, rgba(36,47,73,0.62), rgba(22,30,47,0.82));
    border: 1px solid #29354A;
    border-radius: 14px;
    padding: 17px;
    margin-bottom: 18px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.10);
    box-sizing: border-box;
    height: 100%;
}
.panel-tall { min-height: 330px; }
.section-heading { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.section-heading > div:last-child { flex: 1 1 auto; min-width: 0; }
.section-icon {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: rgba(213,26,41,0.13);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.section-title { color: #F5F7FA; font-size: 14px; font-weight: 650; }
.section-subtitle { color: #8D98AB; font-size: 10.5px; margin-top: 2px; }
.chart-fit {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 3px;
    height: 245px;
}
.chart-fit img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
}
.chart-fit.donut-fit { justify-content: center; }
.chart-fit.donut-fit img {
    object-fit: contain;
    max-width: 100%;
}

/* TABLES */
.data-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.data-table th {
    text-align: left;
    color: #8D98AB;
    font-size: 9.5px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 7px 9px;
    border-bottom: 1px solid #29354A;
}
.data-table td {
    color: #DDE3EC;
    padding: 8px 9px;
    border-bottom: 1px solid rgba(41,53,74,0.55);
}
.data-table tr:last-child td { border-bottom: none; }
.data-table td.num, .data-table th.num { text-align: right; font-variant-numeric: tabular-nums; }

/* INSIGHT CARDS */
.insight-card {
    border: 1px solid #29354A;
    border-radius: 13px;
    padding: 14px;
    background: linear-gradient(145deg, rgba(56,67,88,0.35), rgba(22,30,47,0.85));
    height: 100%;
    box-sizing: border-box;
}
.insight-icon {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: rgba(255,165,134,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 9px;
}
.insight-title { color: #F5F7FA; font-size: 12px; font-weight: 650; margin-bottom: 5px; }
.insight-text { color: #9CA7B9; font-size: 10.5px; line-height: 1.5; }

/* FOOTER */
.footer {
    margin-top: 24px;
    padding-top: 13px;
    border-top: 1px solid #29354A;
    text-align: center;
    color: #68758A;
    font-size: 10px;
}

/* =====================================================
   RESPONSIVE BEHAVIOR
   - at narrower widths, columns wrap/stack naturally
   ===================================================== */
@media (max-width: 1000px) {
    div[data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 100%;
        min-width: 0;
    }
}
@media (max-width: 760px) {
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
# DERIVED FEATURES (analytics logic unchanged)
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
# SIDEBAR (native Streamlit sidebar): BRAND + NAVIGATION + FILTERS
# =========================================================

with st.sidebar:

    html(f"""
    <div class="brand">
        <div class="brand-mark">{icon("database", 21, "#FFFFFF")}</div>
        <div>
            <div class="brand-name">European Bank</div>
            <div class="brand-sub">Customer Analytics</div>
        </div>
    </div>
    """)

    html("""
    <div class="side-label">Dashboard</div>
    """)

    page = st.radio(
        "Dashboard",
        [
            "Overview",
            "Engagement Analysis",
            "Product Analysis",
            "High-Value Customers",
            "Relationship Strength",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    html(f"""
    <div class="side-label" style="display:flex;align-items:center;gap:7px;color:#DDE2EB;font-size:11px;font-weight:600;">
        {icon("filter", 15, PEACH)}
        <span>Filters</span>
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
# APPLY FILTERS (filtering logic unchanged)
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
# TOP BAR + HERO (shared across pages)
# =========================================================

html(f"""
<div class="topbar">
    <div class="search-box">
        {icon("search", 17, "#7D899D")}
        <span style="margin-left:9px;">Search customers, segments, insights...</span>
    </div>
    <div class="profile">
        <div class="profile-date">2025 Customer Dataset</div>
        <div class="profile-ring">{icon("activity", 16, PEACH)}</div>
        <div class="avatar">EA</div>
        <div style="font-size:11px;color:#AEB7C6;">Analytics</div>
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
            "Customers in current selection",
        ))
    with k2:
        html(kpi_card(
            "trend", "Churn Rate", f"{churn_rate:.2f}%",
            f"{churned_customers:,} customers exited",
        ))
    with k3:
        html(kpi_card(
            "activity", "Active Customers", f"{active_customers:,}",
            f"{inactive_customers:,} inactive customers",
        ))
    with k4:
        html(kpi_card(
            "wallet", "High-Value Disengaged", f"{len(high_value_disengaged):,}",
            f"Balance at or above {high_balance_threshold:,.0f}",
        ))

    left, right = st.columns(2)

    with left:
        stayed = total_customers - churned_customers
        chart_panel(
            "users",
            "Customer Status",
            "Stayed versus churned customers",
            donut_png(
                [stayed, churned_customers],
                ["Stayed", "Churned"],
                f"{total_customers:,}",
                "Customers",
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
            "Churn rate comparison between active and inactive customers",
            bar_chart_png(engagement_churn, figsize=(6.0, 2.8)),
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
            "Churn rate across customer regions",
            bar_chart_png(geo_churn, figsize=(6.0, 2.8)),
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
                "Average Balance",
            ],
            "Value": [
                f"{total_customers:,}",
                f"{churned_customers:,}",
                f"{churn_rate:.2f}%",
                f"{active_customers:,}",
                f"{inactive_customers:,}",
                f"{len(high_value_disengaged):,}",
                f"{avg_balance:,.0f}",
            ],
        })
        table_panel(
            "document",
            "Customer Summary",
            "Key statistics for the current selection",
            html_table(summary),
            panel_class="panel-tall",
        )

    html(f"""
    <div class="section-heading">
        <div class="section-icon">{icon("lightbulb", 20, PEACH)}</div>
        <div>
            <div class="section-title">Key Insights</div>
            <div class="section-subtitle">Important findings from the customer analysis</div>
        </div>
    </div>
    """)

    i1, i2, i3 = st.columns(3)
    with i1:
        html(insight_card(
            "activity",
            "Engagement Matters",
            "Active customers show lower churn than inactive customers, "
            "indicating a strong association between engagement and retention.",
        ))
    with i2:
        html(insight_card(
            "wallet",
            "High-Value Risk",
            f"{len(high_value_disengaged):,} customers have high balances but "
            "are inactive, making them an important retention segment.",
        ))
    with i3:
        html(insight_card(
            "trend",
            "Overall Churn",
            f"{churn_rate:.2f}% of customers in the current selection have "
            "exited, highlighting the need for targeted retention strategies.",
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
        html(kpi_card("activity", "Active Customers", f"{active_count:,}",
                      "Currently engaged members"))
    with e2:
        html(kpi_card("trend", "Active Churn", f"{active_churn:.2f}%",
                      "Churn rate among active customers"))
    with e3:
        html(kpi_card("user", "Inactive Customers", f"{inactive_count:,}",
                      "Currently disengaged members"))
    with e4:
        html(kpi_card("chart", "Inactive Churn", f"{inactive_churn:.2f}%",
                      "Churn rate among inactive customers"))

    left, right = st.columns(2)

    with left:
        distribution = (
            engagement_summary.set_index("Engagement")["Customers"]
            .reindex(["Active", "Inactive"]).fillna(0)
        )
        chart_panel(
            "users",
            "Customer Distribution by Engagement",
            "Number of active versus inactive customers",
            bar_chart_png(distribution, color=PEACH, fmt="{:,.0f}"),
        )

    with right:
        churn_by_engagement = (
            engagement_summary.set_index("Engagement")["Churn_Rate"]
            .reindex(["Active", "Inactive"]).fillna(0)
        )
        chart_panel(
            "chart",
            "Churn Rate by Engagement",
            "Churn comparison between engagement groups",
            bar_chart_png(churn_by_engagement),
        )

    display_engagement = engagement_summary.copy()
    display_engagement["Churn_Rate"] = display_engagement["Churn_Rate"].round(2)
    display_engagement = display_engagement[[
        "Engagement", "Customers", "Churned", "Churn_Rate"
    ]]
    display_engagement.columns = [
        "Engagement", "Customers", "Churned", "Churn Rate (%)"
    ]
    table_panel(
        "document",
        "Engagement Summary",
        "Detailed engagement metrics",
        html_table(
            display_engagement,
            numeric_cols=("Customers", "Churned", "Churn Rate (%)"),
        ),
    )

    st.info(
        f"Inactive customers have a churn rate of {inactive_churn:.2f}%, "
        f"compared with {active_churn:.2f}% for active customers. "
        f"The difference is {inactive_churn - active_churn:.2f} percentage points. "
        "Engagement is a key retention lever for the bank."
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
        html(kpi_card("box", "Most Common Product Count", f"{most_common}",
                      "Modal number of products held"))
    with p2:
        html(kpi_card("chart", "Average Products", f"{avg_products:.2f}",
                      "Mean products per customer"))
    with p3:
        html(kpi_card("wallet", "3+ Product Customers", f"{three_plus:,}",
                      "Small group, unusually high churn"))

    product_chart = product_analysis.set_index("NumOfProducts")["Churn_Rate"]
    chart_panel(
        "box",
        "Churn Rate by Number of Products",
        "Product depth versus customer churn",
        bar_chart_png(product_chart, figsize=(6.8, 3.3)),
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
        "Products", "Engagement", "Customers", "Churned", "Churn Rate (%)"
    ]
    table_panel(
        "activity",
        "Product Count + Engagement",
        "Combined view of product utilization and activity",
        html_table(
            display_pe,
            numeric_cols=("Products", "Customers", "Churned", "Churn Rate (%)"),
        ),
    )

    st.info(
        "Customers with 2 products show substantially lower churn than "
        "customers with 1 product in this dataset. Customers with 3 or more "
        "products form a small but unusually high-churn group and should be "
        "investigated separately. These results indicate association rather "
        "than causation."
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
                      f"{high_balance_threshold:,.0f}",
                      "75th percentile of customer balances"))
    with h2:
        html(kpi_card("user", "High-Value Disengaged",
                      f"{len(high_value):,}",
                      "High-balance customers who are inactive"))
    with h3:
        html(kpi_card("trend", "Their Churn Rate",
                      f"{high_value_churn:.2f}%",
                      "Churn within the disengaged segment"))

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
        "High-Balance Customer Comparison",
        "Active versus inactive high-balance customers",
        html_table(
            comparison,
            numeric_cols=("Customers", "Churn Rate (%)"),
        ),
    )

    chart_panel(
        "chart",
        "Churn Rate: High Balance + Active versus High Balance + Inactive",
        "Engagement matters even among the bank's most valuable customers",
        bar_chart_png(
            comparison.set_index("Group")["Churn Rate (%)"],
            figsize=(7.4, 3.2),
        ),
    )

    html(f"""
    <div class="section-heading">
        <div class="section-icon">{icon("users", 20, PEACH)}</div>
        <div>
            <div class="section-title">At-Risk Customer List</div>
            <div class="section-subtitle">High-balance customers who are currently inactive</div>
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
            height=420,
        )

        csv = high_value[customer_columns].to_csv(index=False)

        st.download_button(
            "Download At-Risk Customer List (CSV)",
            csv,
            "high_value_disengaged_customers.csv",
            "text/csv",
            type="primary",
        )

    else:

        st.success(
            "No high-value disengaged customers match the current filters."
        )

    st.info(
        "High-balance customers should not automatically be considered "
        "loyal. Financial value and customer engagement should be monitored "
        "together."
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
        html(kpi_card("heart", "Strong Relationship Customers",
                      f"{len(strongest):,}",
                      "Active members holding 2 products"))
    with r2:
        html(kpi_card("trend", "Strong Relationship Churn",
                      f"{strongest_churn:.2f}%",
                      "Churn rate within the strong segment"))
    with r3:
        html(kpi_card("chart", "Product-Risk Churn",
                      f"{product_risk_churn:.2f}%",
                      "Customers holding 3 or more products"))

    relationship_chart = (
        relationship_analysis.set_index("RelationshipCategory")["Churn_Rate"]
        .sort_values()
    )
    chart_panel(
        "heart",
        "Churn Rate by Relationship Category",
        "Relationship strength and retention outcomes",
        bar_chart_png(relationship_chart, figsize=(6.8, 3.3)),
    )

    display_rel = relationship_analysis[[
        "RelationshipCategory", "Customers", "Churned",
        "Churn_Rate", "Avg_Balance",
    ]]
    display_rel["Churn_Rate"] = display_rel["Churn_Rate"].round(2)
    display_rel.columns = [
        "Relationship Category", "Customers", "Churned",
        "Churn Rate (%)", "Avg Balance",
    ]
    table_panel(
        "document",
        "Relationship Summary",
        "Customer distribution, churn and average balance",
        html_table(
            display_rel,
            numeric_cols=("Customers", "Churned", "Churn Rate (%)", "Avg Balance"),
        ),
    )

    st.info(
        "Strong relationship customers show substantially lower churn than "
        "weak relationship customers. The Product-Risk category is kept "
        "separate because customers with 3 or more products show an "
        "unusually high churn pattern in this dataset."
    )


# =========================================================
# FOOTER
# =========================================================

html("""
<div class="footer">
    European Bank Customer Analytics &nbsp;&bull;&nbsp;
    Customer Engagement &amp; Product Utilization &nbsp;&bull;&nbsp;
    Financial Analytics Internship
</div>
""")








