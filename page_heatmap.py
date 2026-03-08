import streamlit as st
import pandas as pd

# Path to the school-level Excel
EXCEL_PATH = "district_school_dropout_data.xlsx"

def show():
    st.title("🗺 District-Level Dropout Risk Heatmap ")

    # Load school-level data
    df_schools = pd.read_excel(EXCEL_PATH)

    # Aggregate average Risk_Score per district
    df_district = df_schools.groupby("District", as_index=False)["Risk_Score"].mean()

    # Add mock lat/lon for districts (for map visualization)
    district_coords = {
        "Chennai": (13.0827, 80.2707),
        "Coimbatore": (11.0168, 76.9558),
        "Madurai": (9.9252, 78.1198),
        "Salem": (11.6643, 78.1460),
        "Trichy": (10.7905, 78.7047),
        "Tirunelveli": (8.7139, 77.7567),
        "Erode": (11.3410, 77.7172),
        "Vellore": (12.9165, 79.1325)
    }

    # Map lat/lon to df
    df_district["Latitude"] = df_district["District"].apply(lambda x: district_coords[x][0])
    df_district["Longitude"] = df_district["District"].apply(lambda x: district_coords[x][1])

    # Identify high-risk schools (Risk_Score >= 0.5)
    high_risk_schools = df_schools[df_schools["Risk_Score"] >= 0.5]
    high_risk_per_district = high_risk_schools.groupby("District")["School"].apply(lambda x: ", ".join(x)).reset_index()
    high_risk_per_district.rename(columns={"School": "High_Risk_Schools"}, inplace=True)

    # Merge with district dataframe
    df_district = df_district.merge(high_risk_per_district, on="District", how="left")
    df_district["High_Risk_Schools"].fillna("-", inplace=True)

    st.subheader("Tamil Nadu District Risk Map")

    # Streamlit map expects columns 'lat' and 'lon'
    st.map(
        df_district.rename(columns={"Latitude":"lat", "Longitude":"lon"})
    )

    st.subheader("District Risk Data (Average of Schools)")

    # Display table without Latitude and Longitude
    df_table = df_district[["District", "Risk_Score", "High_Risk_Schools"]]
    st.dataframe(df_table, use_container_width=True)

    if st.button("⬅ Back"):
        st.session_state.page = "main"
        st.rerun()