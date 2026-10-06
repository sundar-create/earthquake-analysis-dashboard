import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Earthquake Analysis Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🌍 Global Earthquake Analysis Dashboard")
st.write("Five-Year Earthquake Analysis using Python, Pandas, SQL and Streamlit")

# -----------------------------
# MySQL connection
# -----------------------------
password = st.text_input(
    "Enter MySQL password",
    type="password"
)

if password:

    engine = create_engine(
        f"mysql+pymysql://root:{password}@localhost/earthquake_db"
    )

    # Load data
    query = """
    SELECT *
    FROM earthquakes_cleaned
    """

    df = pd.read_sql(query, engine)

    st.success("✅ Connected to MySQL successfully!")
    # -----------------------------
    # -----------------------------
    # Sidebar Filters
    # -----------------------------
    st.sidebar.header("🔎 Filters")

    # Year filter
    years = sorted(df["year"].dropna().unique())

    selected_years = st.sidebar.multiselect(
        "Select Year",
        years,
        default=years
    )

    # Magnitude filter
    min_mag = float(df["mag"].min())
    max_mag = float(df["mag"].max())

    selected_mag = st.sidebar.slider(
        "Magnitude Range",
        min_value=min_mag,
        max_value=max_mag,
        value=(min_mag, max_mag)
    )

    # Depth category filter
    depth_categories = df["depth_category"].dropna().unique()

    selected_depth = st.sidebar.multiselect(
        "Depth Category",
        depth_categories,
        default=list(depth_categories)
    )

    # Apply filters
    filtered_df = df[
        (df["year"].isin(selected_years)) &
        (df["mag"].between(selected_mag[0], selected_mag[1])) &
        (df["depth_category"].isin(selected_depth))
    ]

    st.sidebar.write(
        f"Showing {len(filtered_df):,} earthquakes"
    ) 
        # -----------------------------
        # KPI Cards
        # -----------------------------
    total_earthquakes = len(filtered_df)
    max_magnitude = filtered_df["mag"].max()
    max_depth = filtered_df["depth_km"].max()
    tsunami_count = filtered_df["tsunami"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Earthquakes",
        f"{total_earthquakes:,}"
    )

    col2.metric(
        "Maximum Magnitude",
        f"{max_magnitude:.1f}"
    )

    col3.metric(
        "Maximum Depth (km)",
        f"{max_depth:.1f}"
    )

    col4.metric(
        "Tsunami Events",
        f"{tsunami_count:,}"
    )

    # -----------------------------
    # Yearly Earthquake Count
    # -----------------------------
    st.subheader("📈 Earthquakes by Year")

    yearly = (
        filtered_df.groupby("year")
        .size()
        .reset_index(name="earthquake_count")
    )

    st.line_chart(
        yearly.set_index("year")
    )

    # -----------------------------
    # Monthly Earthquake Count
    # -----------------------------
    st.subheader("📅 Earthquakes by Month")

    monthly = (
        filtered_df.groupby("month")
        .size()
        .reset_index(name="earthquake_count")
    )

    st.bar_chart(
        monthly.set_index("month")
    )

    # -----------------------------
    # Magnitude Distribution
    # -----------------------------
    st.subheader("📊 Magnitude Distribution")

    magnitude_data = (
        filtered_df["mag"]
        .dropna()
        .value_counts()
        .sort_index()
    )

    st.bar_chart(magnitude_data)

    # -----------------------------
    # Strongest Earthquakes
    # -----------------------------
    st.subheader("🔥 Top 10 Strongest Earthquakes")

    strongest = (
        df[
            [
                "id",
                "time",
                "mag",
                "magType",
                "place",
                "depth_km"
            ]
        ]
        .dropna(subset=["mag"])
        .sort_values("mag", ascending=False)
        .head(10)
    )

    st.dataframe(
        strongest,
        use_container_width=True
    )