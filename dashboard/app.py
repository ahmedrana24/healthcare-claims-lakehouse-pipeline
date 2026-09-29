from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Healthcare Claims Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
GOLD_DIR = BASE_DIR / "data" / "gold"


# ============================================================
# GLOBAL STYLE
# ============================================================

st.html(
    """
    <style>

    /* ---------- APP ---------- */

    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1600px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #101827;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }


    /* ---------- HEADERS ---------- */

    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        color: #102a43;
        margin-bottom: 4px;
        letter-spacing: -1px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        color: #64748b;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #102a43;
        margin-top: 25px;
        margin-bottom: 12px;
    }


    /* ---------- KPI ---------- */

    .kpi-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 145px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    }

    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 10px;
    }

    .kpi-value {
        font-size: 30px;
        line-height: 1.15;
        font-weight: 800;
        color: #102a43;
        margin-bottom: 10px;
    }

    .kpi-description {
        font-size: 11px;
        color: #94a3b8;
    }


    /* ---------- INFO ---------- */

    .success-box {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #047857;
        padding: 14px 18px;
        border-radius: 10px;
        font-size: 14px;
        margin: 15px 0 25px 0;
    }

    .info-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    }


    /* ---------- TABLE ---------- */

    .table-title {
        font-size: 19px;
        font-weight: 700;
        color: #102a43;
        margin-top: 25px;
        margin-bottom: 8px;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 35px 0 10px 0;
    }

    </style>
    """
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_parquet(folder_name):
    """
    Finds the first parquet file inside:
    data/gold/<folder_name>
    """
    folder = GOLD_DIR / folder_name

    if not folder.exists():
        return None

    files = list(folder.glob("*.parquet"))

    if not files:
        return None

    return files[0]


@st.cache_data
def load_gold_data(folder_name):
    path = find_parquet(folder_name)

    if path is None:
        return pd.DataFrame()

    return pd.read_parquet(path)


def money(value):
    return f"${value:,.0f}"


def number(value):
    return f"{value:,.0f}"


def percentage(value):
    return f"{value:.2f}%"


def kpi_card(label, value, description):
    """
    IMPORTANT:
    Uses st.html() instead of st.markdown()
    so the HTML is actually rendered.
    """

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                {label}
            </div>

            <div class="kpi-value">
                {value}
            </div>

            <div class="kpi-description">
                {description}
            </div>

        </div>
        """
    )


def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=55, b=45),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#334155",
        ),
        title_font=dict(
            size=17,
            color="#102a43",
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#e2e8f0",
        ),
        yaxis=dict(
            gridcolor="#e5e7eb",
            zeroline=False,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
        ),
    )

    return fig


# ============================================================
# LOAD GOLD DATA
# ============================================================

provider_df = load_gold_data("provider_performance")
denial_df = load_gold_data("claim_denial_analysis")
member_df = load_gold_data("member_utilization")


# ============================================================
# VALIDATION
# ============================================================

missing = []

if provider_df.empty:
    missing.append("provider_performance")

if denial_df.empty:
    missing.append("claim_denial_analysis")

if member_df.empty:
    missing.append("member_utilization")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:800;
            color:white;
            margin-bottom:6px;
        ">
            🏥 Healthcare Claims
        </div>

        <div style="
            color:#94a3b8;
            font-size:12px;
            margin-bottom:25px;
        ">
            Analytics Platform
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            color:#cbd5e1;
            font-size:13px;
            line-height:1.6;
        ">
            Gold-layer executive analytics built on the
            Healthcare Claims Lakehouse.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Data Sources")

    st.write(f"👨‍⚕️ Providers: **{len(provider_df):,}**")
    st.write(f"❌ Denial records: **{len(denial_df):,}**")
    st.write(f"👥 Members: **{len(member_df):,}**")

    st.divider()

    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    st.caption("Healthcare Claims Lakehouse")
    st.caption("Gold Analytics Layer")


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="dashboard-title">
        🏥 Healthcare Claims Analytics
    </div>

    <div class="dashboard-subtitle">
        Executive analytics powered by the Healthcare Claims Lakehouse • Gold Layer
    </div>
    """
)


if missing:

    st.error(
        "The following Gold datasets could not be found: "
        + ", ".join(missing)
    )

    st.stop()


st.html(
    """
    <div class="success-box">
        ✓ Gold provider, denial, and member analytics datasets loaded successfully.
    </div>
    """
)


# ============================================================
# EXECUTIVE METRICS
# ============================================================

total_claims = int(provider_df["total_claims"].sum())

total_billed = float(provider_df["total_billed_amount"].sum())

total_paid = float(provider_df["total_paid_amount"].sum())

denied_claims = int(provider_df["denied_claims"].sum())

avg_denial_rate = float(provider_df["denial_rate"].mean())


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Executive Overview",
        "❌ Denial Analytics",
        "👨‍⚕️ Provider Performance",
        "👥 Member Utilization",
    ]
)


# ============================================================
# TAB 1 — EXECUTIVE OVERVIEW
# ============================================================

with tab1:

    st.html(
        """
        <div class="section-title">
            Executive Claims Overview
        </div>
        """
    )

    cols = st.columns(5)

    with cols[0]:
        kpi_card(
            "Total Claims",
            number(total_claims),
            "Processed claims",
        )

    with cols[1]:
        kpi_card(
            "Total Billed",
            money(total_billed),
            "Billed amount",
        )

    with cols[2]:
        kpi_card(
            "Total Paid",
            money(total_paid),
            "Paid amount",
        )

    with cols[3]:
        kpi_card(
            "Denied Claims",
            number(denied_claims),
            "Claims denied",
        )

    with cols[4]:
        kpi_card(
            "Average Denial Rate",
            percentage(avg_denial_rate),
            "Across providers",
        )


    st.html(
        """
        <div class="section-title">
            Gold Layer Summary
        </div>
        """
    )

    cols = st.columns(3)

    with cols[0]:
        kpi_card(
            "Providers",
            number(len(provider_df)),
            "Provider records",
        )

    with cols[1]:
        if "claim_status" in denial_df.columns:
            statuses = denial_df["claim_status"].nunique()
        else:
            statuses = 0

        kpi_card(
            "Claim Status Categories",
            number(statuses),
            "Distinct statuses",
        )

    with cols[2]:
        kpi_card(
            "Members",
            number(len(member_df)),
            "Member records",
        )


    # --------------------------------------------------------
    # FINANCIAL OVERVIEW
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-title">
            Financial Overview
        </div>
        """
    )

    financial_df = pd.DataFrame(
        {
            "Metric": [
                "Total Billed",
                "Total Paid",
            ],
            "Amount": [
                total_billed,
                total_paid,
            ],
        }
    )

    fig = px.bar(
        financial_df,
        x="Metric",
        y="Amount",
        text="Amount",
        title="Billed vs Paid Amount",
    )

    fig.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
    )

    fig.update_yaxes(tickprefix="$", separatethousands=True)

    st.plotly_chart(
        chart_layout(fig, 430),
        use_container_width=True,
    )


# ============================================================
# TAB 2 — DENIAL ANALYTICS
# ============================================================

with tab2:

    st.html(
        """
        <div class="section-title">
            Denial Analytics
        </div>
        """
    )

    denied_total = int(denial_df["denied_claims"].sum())

    if "financial_impact" in denial_df.columns:
        financial_impact = float(
            denial_df["financial_impact"].sum()
        )
    else:
        financial_impact = 0

    if "denial_rate" in denial_df.columns:
        denial_rate = float(
            denial_df["denial_rate"].mean()
        )
    else:
        denial_rate = 0


    cols = st.columns(3)

    with cols[0]:
        kpi_card(
            "Denied Claims",
            number(denied_total),
            "From Gold denial analytics",
        )

    with cols[1]:
        kpi_card(
            "Financial Impact",
            money(financial_impact),
            "Financial impact of denials",
        )

    with cols[2]:
        kpi_card(
            "Average Denial Rate",
            percentage(denial_rate),
            "Average across records",
        )


    # --------------------------------------------------------
    # CLAIM STATUS
    # --------------------------------------------------------

    if "claim_status" in denial_df.columns:

        status_df = (
            denial_df
            .groupby("claim_status", as_index=False)
            ["denied_claims"]
            .sum()
            .sort_values(
                "denied_claims",
                ascending=False,
            )
        )

        fig = px.bar(
            status_df,
            x="claim_status",
            y="denied_claims",
            text="denied_claims",
            title="Denied Claims by Claim Status",
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            chart_layout(fig, 420),
            use_container_width=True,
        )


    # --------------------------------------------------------
    # FINANCIAL IMPACT
    # --------------------------------------------------------

    if (
        "claim_status" in denial_df.columns
        and "financial_impact" in denial_df.columns
    ):

        impact_df = (
            denial_df
            .groupby("claim_status", as_index=False)
            ["financial_impact"]
            .sum()
            .sort_values(
                "financial_impact",
                ascending=False,
            )
        )

        fig = px.bar(
            impact_df,
            x="claim_status",
            y="financial_impact",
            text="financial_impact",
            title="Financial Impact by Claim Status",
        )

        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
        )

        fig.update_yaxes(
            tickprefix="$",
            separatethousands=True,
        )

        st.plotly_chart(
            chart_layout(fig, 420),
            use_container_width=True,
        )


# ============================================================
# TAB 3 — PROVIDER PERFORMANCE
# ============================================================

with tab3:

    st.html(
        """
        <div class="section-title">
            Provider Performance
        </div>
        """
    )


    # --------------------------------------------------------
    # TOP PROVIDERS BY CLAIM VOLUME
    # --------------------------------------------------------

    top_claims = (
        provider_df
        .sort_values(
            "total_claims",
            ascending=False,
        )
        .head(15)
    )

    fig = px.bar(
        top_claims,
        x="provider_id",
        y="total_claims",
        text="total_claims",
        title="Top 15 Providers by Claim Volume",
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        chart_layout(fig, 400),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # HIGHEST DENIAL RATE
    # --------------------------------------------------------

    top_denial = (
        provider_df
        .sort_values(
            "denial_rate",
            ascending=False,
        )
        .head(15)
    )

    fig = px.bar(
        top_denial,
        x="provider_id",
        y="denial_rate",
        text="denial_rate",
        title="Providers With Highest Denial Rates",
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
    )

    fig.update_yaxes(
        ticksuffix="%"
    )

    st.plotly_chart(
        chart_layout(fig, 400),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # BILLED AMOUNT
    # --------------------------------------------------------

    top_billed = (
        provider_df
        .sort_values(
            "total_billed_amount",
            ascending=False,
        )
        .head(15)
    )

    fig = px.bar(
        top_billed,
        x="provider_id",
        y="total_billed_amount",
        text="total_billed_amount",
        title="Top Providers by Billed Amount",
    )

    fig.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
    )

    fig.update_yaxes(
        tickprefix="$",
        separatethousands=True,
    )

    st.plotly_chart(
        chart_layout(fig, 400),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # PROVIDER TABLE
    # --------------------------------------------------------

    st.html(
        """
        <div class="table-title">
            Provider Detail
        </div>
        """
    )

    display_provider = provider_df.copy()

    for col in [
        "total_billed_amount",
        "total_paid_amount",
    ]:
        if col in display_provider.columns:
            display_provider[col] = display_provider[col].round(2)

    if "denial_rate" in display_provider.columns:
        display_provider["denial_rate"] = (
            display_provider["denial_rate"]
            .round(2)
        )

    st.dataframe(
        display_provider.head(25),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TAB 4 — MEMBER UTILIZATION
# ============================================================

with tab4:

    st.html(
        """
        <div class="section-title">
            Member Utilization
        </div>
        """
    )


    total_members = len(member_df)

    member_claims = int(
        member_df["total_claims"].sum()
    )

    member_billed = float(
        member_df["total_billed_amount"].sum()
    )

    avg_claim_cost = float(
        member_df["average_claim_cost"].mean()
    )


    cols = st.columns(4)

    with cols[0]:
        kpi_card(
            "Members",
            number(total_members),
            "Gold member records",
        )

    with cols[1]:
        kpi_card(
            "Member Claims",
            number(member_claims),
            "Total claims",
        )

    with cols[2]:
        kpi_card(
            "Member Billed",
            money(member_billed),
            "Total billed amount",
        )

    with cols[3]:
        kpi_card(
            "Avg Claim Cost",
            money(avg_claim_cost),
            "Average claim cost",
        )


    # --------------------------------------------------------
    # TOP MEMBERS BY CLAIM VOLUME
    # --------------------------------------------------------

    top_members_claims = (
        member_df
        .sort_values(
            "total_claims",
            ascending=False,
        )
        .head(20)
    )

    fig = px.bar(
        top_members_claims,
        x="member_id",
        y="total_claims",
        text="total_claims",
        title="Top 20 Members by Claim Volume",
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        chart_layout(fig, 400),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # TOP MEMBERS BY AVERAGE COST
    # --------------------------------------------------------

    top_members_cost = (
        member_df
        .sort_values(
            "average_claim_cost",
            ascending=False,
        )
        .head(20)
    )

    fig = px.bar(
        top_members_cost,
        x="member_id",
        y="average_claim_cost",
        text="average_claim_cost",
        title="Top 20 Members by Average Claim Cost",
    )

    fig.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
    )

    fig.update_yaxes(
        tickprefix="$",
        separatethousands=True,
    )

    st.plotly_chart(
        chart_layout(fig, 400),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # MEMBER FINANCIAL PROFILE
    # --------------------------------------------------------

    fig = px.scatter(
        member_df,
        x="total_claims",
        y="total_billed_amount",
        size="total_paid_amount",
        hover_name="member_id",
        title="Member Claims vs Billed Amount",
        labels={
            "total_claims": "Total Claims",
            "total_billed_amount": "Total Billed",
            "total_paid_amount": "Total Paid",
        },
    )

    fig.update_yaxes(
        tickprefix="$",
        separatethousands=True,
    )

    st.plotly_chart(
        chart_layout(fig, 450),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # MEMBER TABLE
    # --------------------------------------------------------

    st.html(
        """
        <div class="table-title">
            Member Detail
        </div>
        """
    )

    display_member = member_df.copy()

    for col in [
        "total_billed_amount",
        "total_paid_amount",
        "average_claim_cost",
    ]:
        if col in display_member.columns:
            display_member[col] = (
                display_member[col]
                .round(2)
            )

    st.dataframe(
        display_member.head(25),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        Healthcare Claims Lakehouse • Gold Analytics Layer
    </div>
    """
)