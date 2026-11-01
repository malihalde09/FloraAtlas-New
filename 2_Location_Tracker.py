import streamlit as st
import folium
from streamlit_folium import st_folium
from database import get_all_plants, get_plant_by_id

st.set_page_config(
    page_title="Location Tracker",
    page_icon="📍",
    layout="wide"
)

# =========================================================
# FIXED CAMPUS LOCATION
# =========================================================

CAMPUS_LATITUDE = 18.325111
CAMPUS_LONGITUDE = 72.960389

# =========================================================
# PAGE STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F5DC;
}

h1, h2, h3, p, div, label {
    color: #000000;
}

.stButton > button {
    background-color: #228B51 !important;
    color: white !important;
    border-radius: 25px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #3A9D60 !important;
}

.plant-row {
    padding: 20px 5px;
    border-bottom: 1px solid #d5ddc8;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.title("📍 Location Tracker")

st.caption("🔍 Search any plant and view its location on map")


# =========================================================
# SEARCH
# =========================================================

search_term = st.text_input(
    "🌿 Enter plant name:",
    placeholder="e.g., Neem"
)

col1, col2 = st.columns(2)

with col1:
    search_clicked = st.button(
        "🔍 Search",
        use_container_width=True
    )

with col2:
    show_all_clicked = st.button(
        "📋 Show All",
        use_container_width=True
    )


# =========================================================
# GET PLANTS
# =========================================================

if "plants_to_show" not in st.session_state:
    st.session_state["plants_to_show"] = []

if "selected_plant" not in st.session_state:
    st.session_state["selected_plant"] = None


if search_clicked:

    if search_term.strip():

        all_plants = get_all_plants()

        plants_to_show = []

        for plant in all_plants:

            plant_name = str(plant[1])

            if search_term.lower() in plant_name.lower():
                plants_to_show.append(plant)

        st.session_state["plants_to_show"] = plants_to_show

        if not plants_to_show:
            st.warning("❌ No plants found with that name.")

    else:
        st.warning("⚠️ Please enter a plant name.")


elif show_all_clicked:

    st.session_state["plants_to_show"] = get_all_plants()

    if not st.session_state["plants_to_show"]:
        st.info("No plants in database yet.")


plants_to_show = st.session_state["plants_to_show"]


# =========================================================
# MAP
# =========================================================

if st.session_state["selected_plant"] is not None:

    plant_id = st.session_state["selected_plant"]

    plant = get_plant_by_id(plant_id)

    if plant:

        plant_name = plant[1]
        scientific_name = plant[2]

        st.markdown("---")

        st.subheader(f"📍 Location: {plant_name}")

        st.write(
            f"**Scientific Name:** *{scientific_name}*"
        )

        st.write(
            f"**Campus Latitude:** {CAMPUS_LATITUDE}"
        )

        st.write(
            f"**Campus Longitude:** {CAMPUS_LONGITUDE}"
        )

        # -------------------------------------------------
        # CREATE MAP
        # -------------------------------------------------

        map_object = folium.Map(
            location=[
                CAMPUS_LATITUDE,
                CAMPUS_LONGITUDE
            ],
            zoom_start=17,
            tiles="OpenStreetMap"
        )

        # -------------------------------------------------
        # MARKER
        # -------------------------------------------------

        folium.Marker(
            [
                CAMPUS_LATITUDE,
                CAMPUS_LONGITUDE
            ],
            tooltip=plant_name,
            popup=f"""
            <b>{plant_name}</b><br>
            {scientific_name}<br><br>
            📍 Campus Location
            """,
            icon=folium.Icon(
                color="green",
                icon="leaf"
            )
        ).add_to(map_object)

        # -------------------------------------------------
        # DISPLAY MAP
        # -------------------------------------------------

        st_folium(
            map_object,
            width=900,
            height=500,
            returned_objects=[]
        )

        st.markdown(
            f"""
            📍 **Google Maps:**
            [Open Campus Location](https://www.google.com/maps?q={CAMPUS_LATITUDE},{CAMPUS_LONGITUDE})
            """
        )

        st.markdown("---")


# =========================================================
# PLANT LIST
# =========================================================

if plants_to_show:

    st.success(
        f"✅ Found {len(plants_to_show)} plant(s)"
    )

    for plant in plants_to_show:

        plant_id = plant[0]
        plant_name = plant[1]
        scientific_name = plant[2]
        category = plant[6]

        st.markdown(
            '<div class="plant-row">',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(
            [2, 3, 2, 1]
        )

        with col1:

            st.markdown(
                f"🌿 **{plant_name}**"
            )

        with col2:

            st.markdown(
                f"*{scientific_name}*"
            )

        with col3:

            st.write(
                f"📁 {category}"
            )

        with col4:

            # IMPORTANT:
            # EVERY PLANT GETS MAP BUTTON
            # DATABASE LOCATION IS NOT CHECKED

            if st.button(
                "📍 Map",
                key=f"map_{plant_id}",
                use_container_width=True
            ):

                st.session_state["selected_plant"] = plant_id

                st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# BACK TO HOME
# =========================================================

st.markdown("")

if st.button("← Back to Home"):

    st.switch_page("app.py")