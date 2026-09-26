
import folium
from streamlit_folium import st_folium
import streamlit as st
from predictor import predict

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Haven | Property Estimator",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #F5F7FA;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .hero {
        background: linear-gradient(120deg, #122C2A, #1D4941);
        padding: 36px 40px;
        border-radius: 22px;
        color: white;
        margin-bottom: 28px;
    }

    .brand {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #A8D5C5;
        text-transform: uppercase;
    }

    .hero h1 {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(28px, 4vw, 42px);
        font-weight: 800;
        line-height: 1.15;
        color: white;
        margin: 16px 0 12px 0;
    }

    .hero p {
        color: #D5E7E1;
        font-size: 16px;
        max-width: 600px;
        line-height: 1.7;
    }

    .section-label {
        font-size: 13px;
        color: #648078;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .panel {
        background: white;
        border: 1px solid #E4EAE8;
        border-radius: 18px;
        padding: 26px;
        margin-bottom: 20px;
    }

    .panel h3 {
        font-family: 'Manrope', sans-serif;
        color: #183B35;
        font-size: 21px;
        margin-top: 0;
    }

    .result-card {
        background: linear-gradient(135deg, #183B35, #24594D);
        border-radius: 20px;
        padding: 30px;
        color: white;
        margin-top: 24px;
    }

    .result-label {
        font-size: 13px;
        color: #B9D9CE;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-weight: 700;
    }

    .result-value {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(32px, 5vw, 48px);
        color: white;
        font-weight: 800;
        margin: 12px 0;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }

    .result-note {
        color: #D5E7E1;
        font-size: 14px;
        line-height: 1.6;
    }

    .stButton > button {
        background: #1E5146;
        color: white;
        border: none;
        border-radius: 10px;
        height: 52px;
        font-size: 16px;
        font-weight: 700;
        width: 100%;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background: #2B6B5B;
        color: white;
        border: none;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 9px;
        border-color: #DCE5E1;
    }

    .footer {
        text-align: center;
        color: #83918C;
        font-size: 12px;
        margin-top: 36px;
        line-height: 1.8;
    }

    @media (max-width: 640px) {
        .hero {
            padding: 26px 22px;
        }

        .panel {
            padding: 20px;
        }

        .result-card {
            padding: 24px;
        }
    }
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="brand">⌂ HAVEN &nbsp; / &nbsp; PROPERTY INTELLIGENCE</div>
    <h1>Find the value of<br>your next property.</h1>
    <p>
        Get a data-driven estimate using housing and neighborhood
        characteristics. Enter the property details below to get started.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- INTERACTIVE CALIFORNIA MAP ----------------

st.markdown(
    '<div class="section-label">01 / Choose a location</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="panel">
    <h3>Explore California</h3>
    <p style="color:#71817B; font-size:14px;">
        Click anywhere on the map to select a neighborhood location.
        You can also adjust the coordinates manually below.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize location state
if "latitude" not in st.session_state:
    st.session_state.latitude = 34.0

if "longitude" not in st.session_state:
    st.session_state.longitude = -120.0

# Create map centered on California
california_map = folium.Map(
    location=[36.7783, -119.4179],
    zoom_start=6,
    tiles="OpenStreetMap"
)

# Add a marker for the currently selected location
folium.Marker(
    location=[
        st.session_state.latitude,
        st.session_state.longitude
    ],
    tooltip="Selected location",
    popup="Your selected neighborhood",
    icon=folium.Icon(color="green", icon="home")
).add_to(california_map)

# Display map and capture clicks
map_result = st_folium(
    california_map,
    width=None,
    height=450,
    returned_objects=["last_clicked"],
    key="california_map"
)

# Update coordinates when the user clicks the map
if map_result and map_result.get("last_clicked"):
    clicked = map_result["last_clicked"]

    new_lat = clicked["lat"]
    new_lon = clicked["lng"]

    if (
        new_lat != st.session_state.latitude
        or new_lon != st.session_state.longitude
    ):
        st.session_state.latitude = new_lat
        st.session_state.longitude = new_lon
        st.rerun()

st.caption(
    f"Selected coordinates: "
    f"{st.session_state.latitude:.4f}, "
    f"{st.session_state.longitude:.4f}"
)

# ---------------- INPUT FORM ----------------
st.markdown('<div class="section-label">01 / Property details</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="panel">
    <h3>Tell us about the neighborhood</h3>
    <p style="color:#71817B; font-size:14px;">
        Use the available neighborhood statistics to generate an estimate.
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("property_form"):
    st.markdown("#### Neighborhood & location")

    col1, col2 = st.columns(2)

    with col1:
        med_income = st.number_input(
            "Median income (in $10,000s)",
            min_value=0.0,
            max_value=20.0,
            value=3.5,
            step=0.1,
            help="Median household income in the area, measured in tens of thousands of dollars."
        )

        
        latitude = st.number_input(
            "Latitude",
            min_value=32.0,
            max_value=42.0,
            step=0.01,
            format="%.4f",
            key="latitude",
            help="Automatically populated by the map; you can edit it."
        )

    with col2:
        house_age = st.number_input(
            "Median house age (years)",
            min_value=1.0,
            max_value=52.0,
            value=20.0,
            step=1.0
        )

        
        longitude = st.number_input(
            "Longitude",
            min_value=-125.0,
            max_value=-114.0,
            step=0.01,
            format="%.4f",
            key="longitude",
            help="Automatically populated by the map; you can edit it."
        )

    st.divider()
    st.markdown("#### Housing characteristics")

    col3, col4 = st.columns(2)

    with col3:
        avg_rooms = st.number_input(
            "Average rooms per household",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.1
        )

        population = st.number_input(
            "Neighborhood population",
            min_value=1.0,
            max_value=50000.0,
            value=1000.0,
            step=100.0
        )

    with col4:
        avg_bedrooms = st.number_input(
            "Average bedrooms per household",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1
        )

        avg_occupancy = st.number_input(
            "Average occupants per household",
            min_value=0.5,
            max_value=20.0,
            value=3.0,
            step=0.1
        )

    st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button(
        "Estimate property value  →",
        use_container_width=True
    )


# ---------------- PREDICTION ----------------
if submitted:
    input_features = [
        med_income,
        house_age,
        avg_rooms,
        avg_bedrooms,
        population,
        avg_occupancy,
        latitude,
        longitude,
    ]

    try:
        prediction = predict(input_features)
        estimated_value = prediction * 100000

        st.markdown("""
        <div class="section-label">02 / Your estimate</div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Estimated median property value</div>
            <div class="result-value">${estimated_value:,.0f}</div>
            <div class="result-note">
                Model-based estimate for the neighborhood represented
                by the details you entered.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.success("Estimate generated successfully.")

        with st.expander("View your submitted details"):
            st.write({
                "Median income ($10,000s)": med_income,
                "Median house age (years)": house_age,
                "Average rooms": avg_rooms,
                "Average bedrooms": avg_bedrooms,
                "Population": population,
                "Average occupancy": avg_occupancy,
                "Latitude": latitude,
                "Longitude": longitude,
            })

    except Exception as e:
        st.error(f"Unable to generate prediction: {e}")


# ---------------- DISCLAIMER & FOOTER ----------------
st.markdown("""
<div class="footer">
    <b>HAVEN · Smart Property Estimator</b><br>
    Built with machine learning and the California Housing dataset.<br><br>
    This tool estimates neighborhood-level median house values.
    It is not an individual property appraisal, a verified market quote,
    or financial advice. Actual property prices may differ significantly.
</div>
""", unsafe_allow_html=True)