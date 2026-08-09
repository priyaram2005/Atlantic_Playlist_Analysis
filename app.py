import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------
# PAGE CONFIG
# ------------------------------------

st.set_page_config(
    page_title="Atlantic Playlist Analytics",
    page_icon="🎵",
    layout="wide"
)

# ------------------------------------
# CUSTOM CSS
# ------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f5f7fb;
}

/* Main text color */
html, body, [class*="css"] {
    color: #1f2937;
}

/* Headers */
h1 {
    color: #0E4C92;
    font-weight: 700;
}

h2, h3 {
    color: #184E9E;
}

/* Paragraph text */
p {
    color: #222222;
}
            
/* ===========================
   KPI Card
=========================== */

div[data-testid="metric-container"]{
    background: white !important;
    border:1px solid #dcdcdc;
    border-radius:12px;
    padding:18px;
    box-shadow:0 3px 10px rgba(0,0,0,.08);
}

/* Label */
div[data-testid="metric-container"] label{
    color:#555 !important;
    font-weight:600 !important;
}

/* Every text inside metric */
div[data-testid="metric-container"] *{
    color:#000 !important;
}

/* Metric value */
div[data-testid="stMetricValue"]{
    color:#000 !important;
    font-size:34px !important;
    font-weight:700 !important;
}

/* Delta (if present) */
div[data-testid="stMetricDelta"]{
    color:#16a34a !important;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:18px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
}

/* Tabs */
button[data-baseweb="tab"]{
    color:#184E9E !important;
    font-weight:600;
}

button[data-baseweb="tab"][aria-selected="true"]{
    color:#FF4B4B !important;
}
            
/* Download Button */
div.stDownloadButton > button {
    background-color: rgb(202, 241, 180) !important;
    border: 1px solid rgba(7, 6, 6, 0.2) !important;
    color: black !important;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
    transition: 0.3s;
}

div.stDownloadButton > button:hover {
    background-color: rgb(180, 230, 150) !important;
    border: 1px solid rgba(7, 6, 6, 0.4) !important;
    color: black !important;
}

/* Dataframes */
[data-testid="stDataFrame"]{
    background:white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#20222B;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------
# LOAD DATA
# ------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/playlist_feature_engineered.csv")

    df["date"]=pd.to_datetime(df["date"])

    return df

df=load_data()

# ------------------------------------
# SIDEBAR
# ------------------------------------

st.sidebar.title("🎵 Dashboard Filters")

date_range=st.sidebar.date_input(
    "Date Range",
    [df.date.min(),df.date.max()]
)

artist_filter=st.sidebar.multiselect(
    "Artist",
    sorted(df.artist.unique())
)

song_filter=st.sidebar.multiselect(
    "Song",
    sorted(df.song.unique())
)

album_filter=st.sidebar.multiselect(
    "Album Type",
    df.album_type.unique(),
    default=df.album_type.unique()
)

rank_filter=st.sidebar.slider(
    "Rank Range",
    1,
    50,
    (1,50)
)

# ------------------------------------
# FILTER DATA
# ------------------------------------

filtered=df.copy()

filtered=filtered[
    (filtered.position>=rank_filter[0])&
    (filtered.position<=rank_filter[1])
]

filtered=filtered[
    filtered.album_type.isin(album_filter)
]

if artist_filter:
    filtered=filtered[
        filtered.artist.isin(artist_filter)
    ]

if song_filter:
    filtered=filtered[
        filtered.song.isin(song_filter)
    ]

if len(date_range)==2:

    filtered=filtered[
        (filtered.date>=pd.to_datetime(date_range[0]))&
        (filtered.date<=pd.to_datetime(date_range[1]))
    ]

# ------------------------------------
# TITLE
# ------------------------------------

st.title("🎵 United States Top 50 Playlist Performance Dashboard")

st.write(
"""
Analyze playlist rankings,
artist performance,
song popularity,
and streaming trends.
"""
)

# ------------------------------------
# KPI CARDS
# ------------------------------------

c1,c2,c3,c4=st.columns(4)

c1.metric(
    "Songs",
    filtered.song.nunique()
)

c2.metric(
    "Artists",
    filtered.artist.nunique()
)

c3.metric(
    "Average Popularity",
    round(filtered.popularity.mean(),2)
)

c4.metric(
    "Average Rank",
    round(filtered.position.mean(),2)
)

st.divider()

# ------------------------------------
# TABS
# ------------------------------------

overview,songs,artists,insights=st.tabs(
[
"📊 Overview",
"🎵 Song Analysis",
"👑 Artist Analysis",
"📈 Business Insights"
]
)

# ==========================================================
# OVERVIEW
# ==========================================================

with overview:

    st.subheader("Playlist Rank Distribution")

    fig=px.histogram(
        filtered,
        x="position",
        nbins=50,
        color_discrete_sequence=["royalblue"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Popularity vs Rank")

    fig=px.scatter(
        filtered,
        x="popularity",
        y="position",
        color="album_type",
        hover_data=["song","artist"]
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Daily Playlist Popularity")

    daily=filtered.groupby("date").agg(
        avg_popularity=("popularity","mean")
    ).reset_index()

    fig=px.line(
        daily,
        x="date",
        y="avg_popularity",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# SONG ANALYSIS
# ==========================================================

with songs:

    st.subheader("🎵 Song Ranking Trend")

    selected_song = st.selectbox(
        "Select Song",
        sorted(filtered["song"].unique())
    )

    song_df = filtered[
        filtered["song"] == selected_song
    ]

    fig = px.line(
        song_df,
        x="date",
        y="position",
        markers=True,
        title=f"{selected_song} Rank Trend"
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🏆 Longest Charting Songs")

    longest = (
        filtered[
            ["song", "artist", "days_on_chart"]
        ]
        .drop_duplicates()
        .sort_values(
            "days_on_chart",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        longest,
        x="days_on_chart",
        y="song",
        color="artist",
        orientation="h",
        text="days_on_chart"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        longest,
        use_container_width=True
    )

    st.divider()

    st.subheader("🔥 Highest Popularity Songs")

    top_pop = (
        filtered.groupby(
            ["song", "artist"]
        )["popularity"]
        .mean()
        .reset_index()
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_pop,
        x="popularity",
        y="song",
        color="artist",
        orientation="h",
        text="popularity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        top_pop,
        use_container_width=True
    )

    st.divider()

    st.subheader("📊 Rank Volatility")

    volatility = (
        filtered[
            ["song", "artist", "rank_volatility"]
        ]
        .drop_duplicates()
        .sort_values(
            "rank_volatility",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        volatility,
        x="rank_volatility",
        y="song",
        color="artist",
        orientation="h",
        text="rank_volatility"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        volatility,
        use_container_width=True
    )

    st.divider()

    st.subheader("⏱ Duration vs Popularity")

    fig = px.scatter(
        filtered,
        x="duration_minutes",
        y="popularity",
        color="album_type",
        hover_data=["song", "artist"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# ARTIST ANALYSIS
# ==========================================================

with artists:

    st.subheader("👑 Top Artists")

    artist_df = (
        filtered.groupby("artist")
        .size()
        .reset_index(name="Appearances")
        .sort_values(
            "Appearances",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        artist_df,
        x="Appearances",
        y="artist",
        orientation="h",
        text="Appearances",
        color="Appearances"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        artist_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("💿 Album Type Analysis")

    album = (
        filtered.groupby("album_type")
        .agg(
            Average_Popularity=("popularity", "mean"),
            Average_Rank=("position", "mean")
        )
        .reset_index()
    )

    fig = px.bar(
        album,
        x="album_type",
        y="Average_Popularity",
        color="album_type",
        text="Average_Popularity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        album,
        use_container_width=True
    )

    st.divider()

    st.subheader("🔞 Explicit vs Non Explicit")

    explicit = (
        filtered.groupby("is_explicit")
        .agg(
            Average_Popularity=("popularity", "mean"),
            Average_Rank=("position", "mean")
        )
        .reset_index()
    )

    fig = px.bar(
        explicit,
        x="is_explicit",
        y="Average_Popularity",
        color="is_explicit",
        text="Average_Popularity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        explicit,
        use_container_width=True
    )

    st.divider()

    st.subheader("🎼 Song Duration Distribution")

    fig = px.histogram(
        filtered,
        x="duration_minutes",
        nbins=30,
        color_discrete_sequence=["royalblue"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

with insights:

    st.markdown("### 📊 Overall Dataset Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Playlist Records", len(filtered))
        st.metric("Unique Songs", filtered["song"].nunique())
        st.metric("Unique Artists", filtered["artist"].nunique())

    with col2:
        st.metric("Average Popularity", round(filtered["popularity"].mean(), 2))
        st.metric("Average Rank", round(filtered["position"].mean(), 2))
        st.metric("Average Duration (min)", round(filtered["duration_minutes"].mean(), 2))

    st.divider()

    st.subheader("📌 Correlation Heatmap")

    numeric_cols = [
        "position",
        "popularity",
        "duration_minutes",
        "days_on_chart",
        "average_rank",
        "best_rank",
        "rank_volatility",
        "artist_dominance"
    ]

    corr = filtered[numeric_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🏅 Top 10 Songs by Average Popularity")

    top10 = (
        filtered.groupby(["song", "artist"])["popularity"]
        .mean()
        .reset_index()
        .sort_values("popularity", ascending=False)
        .head(10)
    )

    st.dataframe(top10, use_container_width=True)

    st.divider()

    st.subheader("🎤 Top 10 Artists by Playlist Appearances")

    top_artist = (
        filtered.groupby("artist")
        .size()
        .reset_index(name="Appearances")
        .sort_values("Appearances", ascending=False)
        .head(10)
    )

    st.dataframe(top_artist, use_container_width=True)

    st.divider()

    st.subheader("📋 Executive Insights")

    st.success(f"""
✅ **{filtered['song'].nunique()} unique songs** from **{filtered['artist'].nunique()} artists** were analyzed.

✅ Average popularity score: **{filtered['popularity'].mean():.2f}**

✅ Average playlist rank: **{filtered['position'].mean():.2f}**

✅ Average song duration: **{filtered['duration_minutes'].mean():.2f} minutes**

These insights help identify long-performing songs, dominant artists, chart stability, and factors influencing playlist performance.
""")

    st.info("""
### Recommendations

• Promote songs with consistently high popularity and low average rank.

• Focus marketing efforts on artists with high playlist dominance.

• Monitor highly volatile songs to understand audience engagement.

• Evaluate album type and explicit content when planning future releases.

• Use playlist longevity as an indicator for long-term promotional strategies.
""")

st.divider()

# ==========================================================
# DOWNLOAD DATASET
# ==========================================================

st.subheader("📥 Download Filtered Dataset")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_playlist_analysis.csv",
    mime="text/csv"
)

st.divider()
