import streamlit as st
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="Political Intelligence Dashboard",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv("news.csv")
df.columns = df.columns.str.strip()

# -------------------------------
# TITLE
# -------------------------------

st.title("Political Intelligence Dashboard")
st.caption(
    "Developed by Neha Singh | Political Intelligence Dashboard | 2026"
)

if st.button("🔄 Fetch Latest News"):
    import os

    os.system("python news_fetcher.py")

    st.success("Latest news fetched successfully!")

    st.rerun()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------

search_term = st.sidebar.text_input(
    "Search Headlines"
)

constituency = st.sidebar.selectbox(
    "Select Constituency",
    ["All"] + sorted(df["Constituency"].dropna().unique().tolist())
)

leader = st.sidebar.selectbox(
    "Select Leader",
    ["All"] + sorted(df["Leader"].dropna().unique().tolist())
)

party = st.sidebar.selectbox(
    "Select Party",
    ["All"] + sorted(df["Party"].dropna().unique().tolist())
)

topic = st.sidebar.selectbox(
    "Select Topic",
    ["All"] + sorted(df["Topic"].dropna().unique().tolist())
)

source = st.sidebar.selectbox(
    "Select Source",
    ["All"] + sorted(df["Source"].dropna().unique().tolist())
)

# -------------------------------
# APPLY FILTERS
# -------------------------------

filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[
        filtered_df["Headline"].str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

if constituency != "All":
    filtered_df = filtered_df[
        filtered_df["Constituency"] == constituency
    ]

if leader != "All":
    filtered_df = filtered_df[
        filtered_df["Leader"] == leader
    ]

if party != "All":
    filtered_df = filtered_df[
        filtered_df["Party"] == party
    ]

if topic != "All":
    filtered_df = filtered_df[
        filtered_df["Topic"] == topic
    ]

if source != "All":
    filtered_df = filtered_df[
        filtered_df["Source"] == source
    ]

# -------------------------------
# METRICS
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total News",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Topics Covered",
        filtered_df["Topic"].nunique()
    )

with col3:
    st.metric(
        "Sources Tracked",
        filtered_df["Source"].nunique()
    )

with col4:
    st.metric(
        "Articles Fetched",
        len(filtered_df)
    )

# -------------------------------
# NEWS TABLE
# -------------------------------

st.subheader("Recent News")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -------------------------------
# CHARTS
# -------------------------------

colA, colB = st.columns(2)

with colA:

    st.subheader("Issue Distribution")

    issue_counts = filtered_df["Topic"].value_counts()

    st.bar_chart(issue_counts)

with colB:

    st.subheader("Source Distribution")

    source_counts = filtered_df["Source"].value_counts()

    st.bar_chart(source_counts)

# -------------------------------
# LEADER COVERAGE
# -------------------------------

st.subheader("Leader Coverage")

leader_counts = filtered_df["Leader"].value_counts()

st.bar_chart(leader_counts)

# -------------------------------
# CONSTITUENCY SUMMARY
# -------------------------------

st.subheader("Constituency Summary")

summary = (
    filtered_df.groupby("Constituency")
    .size()
    .reset_index(name="News Count")
)

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")
st.caption(
    "Political Intelligence Dashboard Prototype | Developed by Neha Singh © 2026"
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Developed by Neha Singh"
)