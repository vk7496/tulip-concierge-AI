import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="AI Hotel Intelligence Demo",
    layout="wide"
)

st.title("AI Hotel & Restaurant Intelligence (Demo)")
st.caption("Simulated internal data – No external files required")

# -------------------------
# Simulated Hotel / Restaurant Data
# -------------------------
np.random.seed(42)

data = {
    "Hotel_Name": [
        "Muscat Pearl Hotel", "Golden Dunes Resort", "Oman Vista Hotel",
        "Desert Rose Inn", "Qatar Bay Hotel", "Doha Grand Stay",
        "Arabian Nights Resort", "Sea Breeze Hotel"
    ],
    "City": [
        "Muscat", "Muscat", "Muscat",
        "Nizwa", "Doha", "Doha",
        "Salalah", "Salalah"
    ],
    "Restaurant_Name": [
        "Pearl Restaurant", "Dunes Grill", "Vista Lounge",
        "Rose Kitchen", "Bay Seafood", "Grand Steakhouse",
        "Arabian Taste", "Sea Breeze Cafe"
    ],
    "Google_Rating": np.round(np.random.uniform(3.5, 4.8, 8), 1),
    "Monthly_Bookings": np.random.randint(200, 1200, 8),
    "Avg_Room_Price_USD": np.random.randint(80, 320, 8),
    "Customer_Complaints": np.random.randint(5, 80, 8)
}

df = pd.DataFrame(data)

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

selected_city = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

min_rating = st.sidebar.slider(
    "Minimum Google Rating",
    min_value=3.0,
    max_value=5.0,
    value=3.5,
    step=0.1
)

filtered_df = df[
    (df["City"].isin(selected_city)) &
    (df["Google_Rating"] >= min_rating)
]

# -------------------------
# KPIs
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Rating",
    f"{filtered_df['Google_Rating'].mean():.2f}"
)

col2.metric(
    "Total Monthly Bookings",
    int(filtered_df["Monthly_Bookings"].sum())
)

col3.metric(
    "Avg Room Price (USD)",
    f"{filtered_df['Avg_Room_Price_USD'].mean():.0f}"
)

col4.metric(
    "Total Complaints",
    int(filtered_df["Customer_Complaints"].sum())
)

st.divider()

# -------------------------
# Data Table
# -------------------------
st.subheader("Hotel & Restaurant Data")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------
# Simple AI Insight Logic
# -------------------------
st.subheader("AI-Generated Insights")

def generate_insight(row):
    if row["Google_Rating"] < 4.0 and row["Customer_Complaints"] > 40:
        return "High risk: Improve service quality & staff training."
    elif row["Google_Rating"] >= 4.5 and row["Monthly_Bookings"] > 800:
        return "Top performer: Consider premium pricing strategy."
    elif row["Avg_Room_Price_USD"] > 250 and row["Google_Rating"] < 4.2:
        return "Overpriced: Price-value mismatch detected."
    else:
        return "Stable performance: Monitor trends."

filtered_df["AI_Insight"] = filtered_df.apply(generate_insight, axis=1)

st.dataframe(
    filtered_df[[
        "Hotel_Name", "City", "Google_Rating",
        "Monthly_Bookings", "Avg_Room_Price_USD",
        "AI_Insight"
    ]],
    use_container_width=True
)

# -------------------------
# Explanation Section
# -------------------------
with st.expander("How this demo helps hotels"):
    st.markdown("""
    **This demo simulates how AI can help hotels and restaurants:**
    - Identify underperforming branches
    - Detect pricing issues
    - Highlight top-performing properties
    - Support management decisions without external data dependency
    
    In real deployment, this system can be connected to:
    - Google Maps & Reviews
    - Booking engines
    - PMS systems
    - Customer feedback platforms
    """)

st.success("Demo ready for presentation to hotels or investors.")
