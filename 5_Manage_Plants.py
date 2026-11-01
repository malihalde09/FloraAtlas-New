import streamlit as st
from database import get_all_plants, delete_plant, add_plant, get_total_plants

st.set_page_config(
    page_title="FloraAtlas",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp { background-color: #c7d7b8; }
    .stButton > button {
        background-color: #445932 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
        font-size: 1rem !important;
        border: none !important;
        width: 100% !important;
    }
    .stButton > button:hover { background-color: #354526 !important; }
    .stTextInput input {
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
        border: 2px solid #445932 !important;
        padding: 10px !important;
    }
    .stTextInput label { color: black !important; }
    .stTextArea textarea {
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
        border: 2px solid #445932 !important;
        padding: 10px !important;
    }
    .stSelectbox > div > div {
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
        border: 2px solid #445932 !important;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: black !important;
    }
    .stSuccess { color: black !important; }
    .stWarning { color: black !important; }
    .stInfo { color: black !important; }
    .stError { color: black !important; }
    </style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown('<h1 style="color: #445932; text-align: center; font-size: 4rem;">🌿 FloraAtlas</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #000000; font-size: 1.2rem;">Campus Plant Information System</p>', unsafe_allow_html=True)

# ===== LOGIN =====
if not st.session_state.get('logged_in', False):
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown('<h3 style="text-align: center; color: #000000;">🔐 Login</h3>', unsafe_allow_html=True)
            username = st.text_input("👤 Username", placeholder="Enter any username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter any password")
            if st.form_submit_button("🔐 Login", use_container_width=True):
                if username and password:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("⚠️ Please enter both username and password")
        st.caption("🆕 Anyone can login - No restrictions!")

# ===== AFTER LOGIN =====
else:
    st.markdown("---")
    st.markdown(f'<p style="text-align: center; color: #000000; font-size: 1.2rem;">👋 Welcome, <b>{st.session_state["username"]}</b>!</p>', unsafe_allow_html=True)

    # ===== MAIN BUTTONS =====
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📱 QR Scanner", key="qr_main", use_container_width=True):
            st.switch_page("1_QR_Scanner.py")
    with col2:
        if st.button("📍 Location Tracker", key="location_main", use_container_width=True):
            st.switch_page("2_Location_Tracker.py")

    st.markdown("---")

    # ===== ADMIN DASHBOARD =====
    if st.button("📊 Admin Dashboard", key="admin_dashboard_btn", use_container_width=True):
        st.session_state['show_dashboard'] = True
        st.rerun()

    if st.session_state.get('show_dashboard', False):
        st.markdown("---")
        st.markdown('<h2 style="color: #445932;">📊 Admin Dashboard</h2>', unsafe_allow_html=True)

        # Stats
        total = get_total_plants()
        st.markdown(f'<p style="color: black;">🌱 Total Plants: <b>{total}</b></p>', unsafe_allow_html=True)

        st.markdown("---")

        # ===== VIEW PLANTS =====
        st.markdown('<h3 style="color: #445932;">📋 Manage Plants</h3>', unsafe_allow_html=True)

        plants = get_all_plants()
        if plants:
            for plant in plants:
                with st.container():
                    cols = st.columns([2, 2, 1.5, 1])
                    with cols[0]:
                        st.markdown(f"**🌿 {plant[1]}**")
                    with cols[1]:
                        st.markdown(f"*{plant[2]}*")
                    with cols[2]:
                        st.markdown(f"📂 {plant[6]}")
                    with cols[3]:
                        if st.button("🗑️ Delete", key=f"del_{plant[0]}"):
                            success, msg = delete_plant(plant[0])
                            if success:
                                st.success(f"✅ {msg}")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
                st.markdown("---")
        else:
            st.info("No plants found. Add your first plant!")

        # ===== ADD PLANT =====
        st.markdown('<h3 style="color: #445932;">➕ Add New Plant</h3>', unsafe_allow_html=True)

        with st.expander("Click to add new plant", expanded=False):
            with st.form("add_plant_form"):
                col1, col2 = st.columns(2)
                with col1:
                    plant_id = st.text_input("Plant ID *", placeholder="P001")
                    plant_name = st.text_input("Plant Name *", placeholder="Neem Tree")
                    scientific_name = st.text_input("Scientific Name", placeholder="Azadirachta indica")
                    category = st.selectbox("Category", ["Tree", "Herb", "Flower", "Succulent", "Other"])
                with col2:
                    qr_code_id = st.text_input("QR Code ID", placeholder="QR001")
                    latitude = st.text_input("Latitude", placeholder="28.6139")
                    longitude = st.text_input("Longitude", placeholder="77.2090")
                    description = st.text_area("Description")

                if st.form_submit_button("✅ Add Plant"):
                    if plant_id and plant_name:
                        data = {
                            'plant_id': plant_id,
                            'plant_name': plant_name,
                            'scientific_name': scientific_name,
                            'kingdom': '',
                            'family': '',
                            'species': '',
                            'category': category,
                            'description': description,
                            'medicinal_uses': '',
                            'environmental_benefits': '',
                            'image_path': '',
                            'qr_code_id': qr_code_id,
                            'latitude': float(latitude) if latitude else None,
                            'longitude': float(longitude) if longitude else None
                        }
                        success, msg = add_plant(data)
                        if success:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    else:
                        st.error("⚠️ Plant ID and Name are required!")

        # ===== HIDE DASHBOARD =====
        if st.button("🔒 Hide Dashboard", key="hide_dash_btn", use_container_width=True):
            st.session_state['show_dashboard'] = False
            st.rerun()

    # ===== LOGOUT =====
    st.markdown("---")
    if st.button("🚪 Logout", key="logout_btn_main", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['show_dashboard'] = False
        st.rerun()

# ===== FOOTER =====
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 15px 0; color: #000000; border-top: 1px solid rgba(0,0,0,0.1);">
    <p>© 2026 FloraAtlas</p>
</div>
""", unsafe_allow_html=True)