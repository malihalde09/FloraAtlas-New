import asyncio
import sys

# Windows Python 3.14 Event Loop Error Fix
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
from database import (get_all_plants, search_plants, get_plant_by_id,
                      delete_plant, add_plant, get_total_plants, update_plant,
                      get_plant_by_qr)
import cv2
import numpy as np
from PIL import Image
import os
import pytesseract
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="FloraAtlas", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# =====================================================================
# CSS (Sundar Formatting)
# =====================================================================
st.markdown("""
    <style>
    .stApp { background-color: #c7d7b8; }
    .stButton > button { background-color: #445932 !important; color: white !important; border-radius: 50px !important; padding: 12px 30px !important; font-size: 1rem !important; border: none !important; width: 100% !important; }
    .stButton > button:hover { background-color: #354526 !important; }
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div { background-color: white !important; color: black !important; border-radius: 8px !important; border: 2px solid #445932 !important; padding: 10px !important; }
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: black !important; }
    
    .ai-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 6px solid #445932;
        margin-top: 15px;
        color: #000000 !important;
    }
    .ai-card p { margin-bottom: 8px; line-height: 1.6; }
    .ai-card b { color: #000000 !important; font-size: 1.05rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color: #445932; text-align: center; font-size: 4rem;">🌿 FloraAtlas</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #000000; font-size: 1.2rem;">Campus Plant Information System</p>', unsafe_allow_html=True)

# =====================================================================
# SMART BACKUP FUNCTION
# =====================================================================
def get_gemini_info(plant_name):
    clean_name = str(plant_name).lower()
    
    if "ficus" in clean_name or "nandaruk" in clean_name:
        return """
        <b>Scientific Name:</b> Ficus benjamina L.<br><br>
        <b>Family:</b> Moraceae<br><br>
        <b>Description:</b> Ficus benjamina, commonly known as weeping fig, is a species of flowering plant in the family Moraceae. It is native to Asia and Australia.<br><br>
        <b>Medicinal Uses:</b> <br>
        • The latex from the plant is used in traditional medicine to treat skin diseases.<br>
        • Root extracts are used to treat fever and stomach disorders.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Excellent air purifier, removing toxins like formaldehyde from the environment.<br>
        • Provides dense shade and acts as a habitat for various bird species.
        """
    elif "hibiscus" in clean_name or "jaswand" in clean_name:
        return """
        <b>Scientific Name:</b> Hibiscus rosa-sinensis<br><br>
        <b>Family:</b> Malvaceae<br><br>
        <b>Description:</b> A tropical evergreen shrub renowned for its large, showy, trumpet-shaped blossoms and glossy foliage. It blooms year-round in frost-free climates.<br><br>
        <b>Medicinal Uses:</b> <br>
        • Infusions made from the flowers are used in traditional medicine to help lower blood pressure.<br>
        • Leaf and petal extracts are commonly applied to nourish the scalp and promote hair growth.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Serves as an excellent nectar source for pollinators such as hummingbirds, bees, and butterflies.<br>
        • Acts as an effective windbreak and helps prevent soil erosion when used in hedges.
        """
    elif "neem" in clean_name or "azadirachta" in clean_name:
        return """
        <b>Scientific Name:</b> Azadirachta indica<br><br>
        <b>Family:</b> Meliaceae<br><br>
        <b>Description:</b> Neem is a fast-growing tree that can reach a height of 15–20 metres. It is evergreen but in severe drought it may shed most of its leaves.<br><br>
        <b>Medicinal Uses:</b> <br>
        • Neem leaves are used to treat skin diseases, acne, and fungal infections.<br>
        • Neem oil is widely used in traditional medicine for its antibacterial properties.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Highly effective in improving soil fertility and restoring degraded ecosystems.<br>
        • Acts as a natural pesticide, protecting nearby plants from insects.
        """
    elif "delonix" in clean_name or "gulmohar" in clean_name:
        return """
        <b>Scientific Name:</b> Delonix regia<br><br>
        <b>Family:</b> Fabaceae<br><br>
        <b>Description:</b> Delonix regia, commonly known as the flame tree or Gulmohar, is a species of flowering plant in the bean family. It is noted for its fern-like leaves and flamboyant display of orange-red flowers.<br><br>
        <b>Medicinal Uses:</b> <br>
        • The seeds and bark are used in traditional medicine to treat constipation and inflammation.<br>
        • The leaves have anti-diabetic and anti-inflammatory properties.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Provides excellent shade and is widely planted in tropical regions for its ornamental value.<br>
        • Helps in soil stabilization and acts as a nitrogen-fixing plant.
        """
    elif "anacardium" in clean_name or "kaju" in clean_name:
        return """
        <b>Scientific Name:</b> Anacardium occidentale<br><br>
        <b>Family:</b> Anacardiaceae<br><br>
        <b>Description:</b> Anacardium occidentale, commonly known as the cashew tree, is a tropical evergreen tree that produces the cashew seed and the cashew apple.<br><br>
        <b>Medicinal Uses:</b> <br>
        • Cashew apple is rich in vitamin C and is used to treat scurvy and stomach issues.<br>
        • The bark and leaves have anti-inflammatory and antimicrobial properties.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Helps in soil conservation and prevents erosion in coastal areas.<br>
        • Provides shade and acts as a windbreak for other crops.
        """
    elif "shankarsivari" in clean_name or "gmelina" in clean_name:
        return """
        <b>Scientific Name:</b> Gmelina arborea<br><br>
        <b>Family:</b> Lamiaceae<br><br>
        <b>Description:</b> Gmelina arborea, commonly known as Gamhar or Shankarsivari, is a fast-growing deciduous tree. It is known for its high-quality timber and medicinal properties.<br><br>
        <b>Medicinal Uses:</b> <br>
        • The root and bark are used in Ayurveda to treat fever, diarrhea, and skin diseases.<br>
        • It has anti-inflammatory and antioxidant properties.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Used for reforestation and soil conservation due to its fast growth.<br>
        • Provides good quality timber and fuelwood.
        """
    elif "madhumalati" in clean_name or "quisqualis" in clean_name:
        return """
        <b>Scientific Name:</b> Quisqualis indica L.<br><br>
        <b>Family:</b> Combretaceae<br><br>
        <b>Description:</b> Quisqualis indica, commonly known as Madhumalati or Rangoon Creeper, is a vigorous, woody climber. It is famous for its fragrant flowers that change color from white to pink to red as they mature.<br><br>
        <b>Medicinal Uses:</b> <br>
        • The seeds are used in traditional medicine as an anthelmintic (to treat intestinal worms).<br>
        • It is also used to treat diarrhea and fever in some traditional systems.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Excellent ornamental plant used for covering walls, fences, and pergolas.<br>
        • Attracts pollinators like butterflies and bees.
        """
    else:
        return f"""
        <b>Scientific Name:</b> {plant_name}<br><br>
        <b>Family:</b> N/A<br><br>
        <b>Description:</b> A plant species found in the campus botanical garden. It has distinct green foliage and contributes to the local ecosystem.<br><br>
        <b>Medicinal Uses:</b> <br>
        • Traditionally used in local herbal remedies for various minor ailments.<br><br>
        <b>Environmental Benefits:</b> <br>
        • Provides oxygen and supports local biodiversity.<br>
        • Helps in maintaining ecological balance.
        """

# =====================================================================
# FORCE COMMON NAME LOGIC
# =====================================================================
def get_common_name(name):
    name_lower = str(name).lower()
    if "delonix" in name_lower or "gulmohar" in name_lower:
        return "Gulmohar"
    elif "ficus" in name_lower or "nandaruk" in name_lower:
        return "Nandaruk"
    elif "hibiscus" in name_lower or "jaswand" in name_lower:
        return "Jaswand"
    elif "neem" in name_lower or "azadirachta" in name_lower:
        return "Neem"
    elif "anacardium" in name_lower or "kaju" in name_lower:
        return "Kaju"
    elif "shankarsivari" in name_lower or "gmelina" in name_lower:
        return "Shankarsivari"
    elif "madhumalati" in name_lower or "quisqualis" in name_lower:
        return "Madhumalati"
    return name

# =====================================================================
# MAP/INFO LINK LOGIC
# =====================================================================
def get_plant_link(plant_name, original_qr_data):
    if original_qr_data and original_qr_data.strip().startswith(("http://", "https://")):
        return original_qr_data.strip()
        
    name_lower = str(plant_name).lower()
    if "delonix" in name_lower or "gulmohar" in name_lower:
        return "https://en.wikipedia.org/wiki/Delonix_regia"
    elif "ficus" in name_lower or "nandaruk" in name_lower:
        return "https://en.wikipedia.org/wiki/Ficus_benjamina"
    elif "hibiscus" in name_lower or "jaswand" in name_lower:
        return "https://en.wikipedia.org/wiki/Hibiscus_rosa-sinensis"
    elif "neem" in name_lower or "azadirachta" in name_lower:
        return "https://en.wikipedia.org/wiki/Azadirachta_indica"
    elif "anacardium" in name_lower or "kaju" in name_lower:
        return "https://en.wikipedia.org/wiki/Cashew"
    elif "shankarsivari" in name_lower or "gmelina" in name_lower:
        return "https://en.wikipedia.org/wiki/Gmelina_arborea"
    elif "madhumalati" in name_lower or "quisqualis" in name_lower:
        return "https://en.wikipedia.org/wiki/Combretum_indicum"
    else:
        return f"https://www.google.com/search?q={plant_name}+plant"

# =====================================================================
# OCR — image se text padhna
# =====================================================================
def extract_text_from_image(image):
    try:
        img = np.array(image)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except Exception:
        return ""

# =====================================================================
# CORE QR PROCESSING FUNCTION
# =====================================================================
def process_image(image):
    img_array = np.array(image)
    
    try:
        qr_detector = cv2.wechat_qrcode_WeChatQRCode()
        res, points = qr_detector.detectAndDecode(img_array)
        data = res[0] if res else ""
    except Exception:
        qr_detector = cv2.QRCodeDetector()
        data, points, _ = qr_detector.detectAndDecode(img_array)

    plant_name_for_ai = None

    if data:
        st.markdown('<div style="background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-bottom: 10px;">✅ QR Code Scanned Successfully</div>', unsafe_allow_html=True)

    detected_text = extract_text_from_image(image)
    
    if detected_text and len(detected_text.strip()) > 2:
        if "madhumalati" in detected_text.lower() or "quisqualis" in detected_text.lower():
            plant_name_for_ai = "Madhumalati"
        elif "shankarsivari" in detected_text.lower() or "gmelina" in detected_text.lower():
            plant_name_for_ai = "Shankarsivari"
        elif "gulmohar" in detected_text.lower() or "delonix" in detected_text.lower():
            plant_name_for_ai = "Gulmohar"
        elif "ficus" in detected_text.lower() or "nandaruk" in detected_text.lower():
            plant_name_for_ai = "Nandaruk"
        elif "hibiscus" in detected_text.lower() or "jaswand" in detected_text.lower():
            plant_name_for_ai = "Jaswand"
        elif "kaju" in detected_text.lower() or "anacardium" in detected_text.lower():
            plant_name_for_ai = "Kaju"
        elif "neem" in detected_text.lower() or "azadirachta" in detected_text.lower():
            plant_name_for_ai = "Neem"
        else:
            plant_name_for_ai = detected_text

    if not plant_name_for_ai and data:
        plant_found_in_db = get_plant_by_qr(data)
        if plant_found_in_db:
            plant_name_for_ai = plant_found_in_db[1]
        else:
            plant_name_for_ai = data.strip()

    if plant_name_for_ai:
        common_name = get_common_name(plant_name_for_ai)
        final_link = get_plant_link(plant_name_for_ai, data)
        
        st.markdown(f'<div style="background-color: #d1e7dd; color: black; padding: 10px; border-radius: 5px; margin-top: 10px; font-size: 18px;"><b>🌿 Plant Name Found:</b> {common_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color: black; margin-top: 5px; font-size: 16px;">📍 <b>QR Link:</b> <a href="{final_link}" target="_blank">{final_link}</a></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<h3 style="color: black;">🌿 Plant Information</h3>', unsafe_allow_html=True)
        with st.spinner("Fetching plant information..."):
            ai_info = get_gemini_info(plant_name_for_ai)
            st.markdown(f'<div class="ai-card">{ai_info}</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Is image me koi plant ki information nahi mili.")

# =====================================================================
# APP NAVIGATION
# =====================================================================
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
        st.caption("🆕 Anyone can login - No restrictions!")
else:
    st.markdown("---")
    st.markdown(f'<p style="text-align: center; color: #000000; font-size: 1.2rem;">👋 Welcome, <b>{st.session_state["username"]}</b>!</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📱 QR Scanner", key="qr_main", use_container_width=True):
            st.session_state.update({'show_qr': True, 'show_location': False, 'show_dashboard': False})
            st.rerun()
    with col2:
        if st.button("📍 Location Tracker", key="location_main", use_container_width=True):
            st.session_state.update({'show_qr': False, 'show_location': True, 'show_dashboard': False})
            st.rerun()

    st.markdown("---")

    if st.session_state.get("username") == "admin":
        if st.button("📊 Admin Dashboard", key="admin_dashboard_btn", use_container_width=True):
            st.session_state.update({'show_qr': False, 'show_location': False, 'show_dashboard': True})
            st.rerun()

    # --- QR SCANNER PAGE ---
    if st.session_state.get('show_qr', False):
        st.markdown("---")
        st.markdown('<h2 style="color: #445932;">📱 QR Scanner</h2>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📷 Camera", "📤 Upload"])

        with tab1:
            camera_image = st.camera_input("Point camera at QR code")
            if camera_image:
                process_image(Image.open(camera_image))

        with tab2:
            uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                process_image(Image.open(uploaded_file))

        if st.button("🔙 Back", key="back_qr"):
            st.session_state['show_qr'] = False
            st.rerun()

    # --- LOCATION TRACKER PAGE ---
    if st.session_state.get('show_location', False):
        st.markdown("---")
        st.markdown('<h2 style="color: #445932;">📍 Location Tracker</h2>', unsafe_allow_html=True)
        search_term = st.text_input("🌿 Enter plant name:", placeholder="e.g., Neem", key="loc_search_input")
        col1, col2 = st.columns(2)
        with col1:
            search_clicked = st.button("🔍 Search", key="loc_search", use_container_width=True)
        with col2:
            show_all_clicked = st.button("📋 Show All", key="loc_show_all", use_container_width=True)

        if search_clicked:
            st.session_state['selected_plant'] = None 
            if search_term:
                plants_list = []
                for plant in get_all_plants():
                    if search_term.lower() in plant[1].lower():
                        plants_list.append(plant)
                st.session_state['plants_to_show'] = plants_list
            else:
                st.session_state['plants_to_show'] = []
                
        elif show_all_clicked:
            st.session_state['selected_plant'] = None
            st.session_state['plants_to_show'] = get_all_plants()

        if 'plants_to_show' in st.session_state and st.session_state['plants_to_show']:
            # Yahan Found wala text black bold kiya hai
            st.markdown(f'<div style="background-color: #d1e7dd; color: black; padding: 10px; border-radius: 5px; font-size: 16px;"><b>✅ Found {len(st.session_state["plants_to_show"])} plant(s):</b></div>', unsafe_allow_html=True)
            
            for plant in st.session_state['plants_to_show']:
                with st.container():
                    c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])
                    with c1: st.write(f"🌿 **{plant[1]}**")
                    with c2: st.write(f"*{plant[2]}*")
                    with c3: st.write(f"📂 {plant[6]}")
                    with c4:
                        if plant[12] and plant[13] and plant[12] != 0.0:
                            if st.button("📍 Loc", key=f"loc_map_{plant[0]}"):
                                st.session_state['selected_plant'] = plant[0]
                                st.rerun()
                        else:
                            st.write("❌ No location")
                    st.markdown("---")

        if st.session_state.get('selected_plant'):
            plant = get_plant_by_id(st.session_state['selected_plant'])
            if plant and plant[12] and plant[13]:
                # Yahan Location wala text black bold kiya hai
                st.markdown(f'<div style="background-color: #d1e7dd; color: black; padding: 10px; border-radius: 5px; font-size: 18px;"><b>Location of {plant[1]}:</b> Lat: {plant[12]}, Lon: {plant[13]}</div>', unsafe_allow_html=True)
                st.markdown(f"📍 [Open in Google Maps](https://www.google.com/maps?q={plant[12]},{plant[13]})")

        if st.button("🔙 Back", key="back_location"):
            st.session_state.update({'show_location': False, 'selected_plant': None, 'plants_to_show': []})
            st.rerun()

    # --- ADMIN DASHBOARD PAGE ---
    if st.session_state.get('show_dashboard', False) and st.session_state.get("username") == "admin":
        st.markdown("---")
        st.markdown('<h2 style="color: #445932;">📊 Admin Dashboard</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: black;">🌱 Total Plants: <b>{get_total_plants()}</b></p>', unsafe_allow_html=True)
        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("➕ Add Plant", key="add_plant_btn", use_container_width=True):
                st.session_state.update({'show_add': True, 'show_manage': False, 'show_search': False})
                st.rerun()
        with c2:
            if st.button("📋 Manage Plants", key="manage_plants_btn", use_container_width=True):
                st.session_state.update({'show_manage': True, 'show_add': False, 'show_search': False})
                st.rerun()
        with c3:
            if st.button("🔍 Search", key="search_plants_btn", use_container_width=True):
                st.session_state.update({'show_search': True, 'show_add': False, 'show_manage': False})
                st.rerun()
        with c4:
            if st.button("📱 QR Scanner", key="qr_scanner_dash_btn", use_container_width=True):
                st.session_state.update({'show_qr': True, 'show_dashboard': False})
                st.rerun()
        st.markdown("---")

        if st.session_state.get('show_add', False):
            st.markdown('<h3 style="color: #445932;">➕ Add New Plant</h3>', unsafe_allow_html=True)
            with st.form("add_plant_form"):
                c1, c2 = st.columns(2)
                with c1:
                    p_id = st.text_input("Plant ID *", placeholder="P001")
                    p_name = st.text_input("Plant Name *", placeholder="Neem Tree")
                    s_name = st.text_input("Scientific Name", placeholder="Azadirachta indica")
                    cat = st.selectbox("Category", ["Tree", "Herb", "Flower", "Succulent", "Other"])
                with c2:
                    qr_id = st.text_input("QR Code ID", placeholder="QR001")
                    lat = st.text_input("Latitude", placeholder="18.3252")
                    lon = st.text_input("Longitude", placeholder="72.9604")
                    desc = st.text_area("Description")
                if st.form_submit_button("✅ Add Plant"):
                    if p_id and p_name:
                        data = {'plant_id': p_id, 'plant_name': p_name, 'scientific_name': s_name,
                                'kingdom': '', 'family': '', 'species': '', 'category': cat,
                                'description': desc, 'medicinal_uses': '', 'environmental_benefits': '',
                                'image_path': '', 'qr_code_id': qr_id,
                                'latitude': float(lat) if lat else None,
                                'longitude': float(lon) if lon else None}
                        success, msg = add_plant(data)
                        if success:
                            st.success(f"✅ {msg}")
                            st.session_state['show_add'] = False
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    else:
                        st.error("⚠️ Plant ID and Name are required!")

        if st.session_state.get('show_manage', False):
            st.markdown('<h3 style="color: #445932;">📋 Manage Plants</h3>', unsafe_allow_html=True)
            plants = get_all_plants()
            if plants:
                for plant in plants:
                    c1, c2, c3, c4, c5 = st.columns([2, 2, 1.5, 0.7, 0.7])
                    with c1: st.markdown(f"**🌿 {plant[1]}**")
                    with c2: st.markdown(f"*{plant[2]}*")
                    with c3: st.markdown(f"📂 {plant[6]}")
                    with c4:
                        if st.button("✏️", key=f"edit_{plant[0]}"):
                            st.session_state.update({'edit_plant': plant[0], 'show_edit': True, 'show_manage': False})
                            st.rerun()
                    with c5:
                        if st.button("🗑️", key=f"del_{plant[0]}"):
                            success, msg = delete_plant(plant[0])
                            if success:
                                st.success(f"✅ {msg}")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
                    st.markdown("---")
            else:
                st.info("No plants found.")

        if st.session_state.get('show_edit', False):
            plant = get_plant_by_id(st.session_state.get('edit_plant'))
            if plant:
                st.markdown(f'<h3 style="color: #445932;">✏️ Edit: {plant[1]}</h3>', unsafe_allow_html=True)
                with st.form("edit_plant_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        p_name = st.text_input("Plant Name", value=plant[1])
                        s_name = st.text_input("Scientific Name", value=plant[2] if plant[2] else "")
                        cat = st.selectbox("Category", ["Tree", "Herb", "Flower", "Succulent", "Other"], index=0)
                    with c2:
                        qr_id = st.text_input("QR Code ID", value=plant[11] if plant[11] else "")
                        lat = st.text_input("Latitude", value=str(plant[12]) if plant[12] else "")
                        lon = st.text_input("Longitude", value=str(plant[13]) if plant[13] else "")
                        desc = st.text_area("Description", value=plant[7] if plant[7] else "")
                    if st.form_submit_button("💾 Save Changes"):
                        data = {'plant_name': p_name, 'scientific_name': s_name, 'kingdom': '',
                                'family': '', 'species': '', 'category': cat, 'description': desc,
                                'medicinal_uses': '', 'environmental_benefits': '', 'image_path': '',
                                'qr_code_id': qr_id, 'latitude': float(lat) if lat else None,
                                'longitude': float(lon) if lon else None}
                        success, msg = update_plant(st.session_state['edit_plant'], data)
                        if success:
                            st.success(f"✅ {msg}")
                            st.session_state.update({'show_edit': False, 'show_manage': True})
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                if st.button("❌ Cancel", key="cancel_edit"):
                    st.session_state.update({'show_edit': False, 'show_manage': True})
                    st.rerun()

        if st.session_state.get('show_search', False):
            st.markdown('<h3 style="color: #445932;">🔍 Search Plants</h3>', unsafe_allow_html=True)
            term = st.text_input("Enter plant name:", placeholder="e.g., Neem", key="search_input")
            if st.button("🔍 Search", key="search_btn"):
                if term:
                    results = search_plants(term)
                    if results:
                        for plant in results:
                            st.markdown(f"<div style='background: white; border-radius: 10px; padding: 15px; margin: 10px 0; border: 2px solid #445932;'><strong>🌿 {plant[1]}</strong><br><i>{plant[2]}</i><br>📂 {plant[6]}</div>", unsafe_allow_html=True)
                    else:
                        st.warning("No plants found.")
                else:
                    st.warning("Please enter a plant name.")

        if st.button("🔒 Hide Dashboard", key="hide_dash_btn", use_container_width=True):
            st.session_state.update({'show_dashboard': False, 'show_add': False, 'show_manage': False, 'show_search': False, 'show_edit': False})
            st.rerun()

    st.markdown("---")
    if st.button("🚪 Logout", key="logout_btn_main", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown("<div style='text-align: center; margin-top: 2rem; padding: 15px 0; color: #000000; border-top: 1px solid rgba(0,0,0,0.1);'><p>© 2026 FloraAtlas</p></div>", unsafe_allow_html=True)