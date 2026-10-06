import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Earthquake Analysis Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Earthquake Analysis Dashboard")
st.write("5-Year Global Earthquake Analysis")

# MySQL password
password = st.text_input(
    "Enter MySQL password",
    type="password"
)

if password:

    engine = create_engine(
        f"mysql+pymysql://root:{password}@localhost/earthquake_db"
    )

    query = """
    SELECT *
    FROM earthquakes_cleaned
    """

    df = pd.read_sql(query, engine)

    st.success("Connected to MySQL successfully!")

    # Dataset summary
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Earthquakes", f"{len(df):,}")
    col2.metric("Maximum Magnitude", df["mag"].max())
    col3.metric("Maximum Depth (km)", round(df["depth_km"].max(), 2))

    st.subheader("Earthquake Data")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )