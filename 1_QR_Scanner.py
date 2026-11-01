import streamlit as st
import cv2
import numpy as np
from PIL import Image
import ollama
import re
import pytesseract

st.set_page_config(page_title="QR Scanner - FloraAtlas", page_icon="📱", layout="wide")

if not st.session_state.get('logged_in', False):
    st.switch_page("app.py")

st.markdown("""
    <style>
    .stApp { background-color: #c7d7b8; }

    /* ===== GREEN DABBA AB WHITE ===== */
    div[data-testid="stAlert"][data-baseweb="notification"],
    .stSuccess {
        border: 2px solid #155724 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    div[data-testid="stAlertContentSuccess"],
    div[data-testid="stAlertContentSuccess"] *,
    .stSuccess, .stSuccess *,
    .stSuccess p, .stSuccess div, .stSuccess span, .stSuccess strong,
    .stSuccess h1, .stSuccess h2, .stSuccess h3,
    .stSuccess [data-testid="stMarkdownContainer"],
    .stSuccess [data-testid="stMarkdownContainer"] * {
        color: #000000 !important;                 /* ← TEXT BLACK */
        fill: #000000 !important;
    }

    /* BAAKI SAB TEXT BLACK */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown div, .stMarkdown span, .stMarkdown strong {
        color: #000000 !important;
    }

    /* INFO BOX – BLACK */
    .stInfo {
        background-color: #d1ecf1 !important;
        border: 2px solid #0c5460 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    .stInfo, .stInfo p, .stInfo div, .stInfo span, .stInfo strong {
        color: #000000 !important;
    }

    /* TEXT WALA DABBA – WHITE */
    .stTextArea textarea {
        color: #ffffff !important;
        background-color: #2d2d2d !important;
        border-radius: 8px !important;
        border: 2px solid #445932 !important;
        font-size: 16px !important;
    }
    .stTextArea label {
        color: #ffffff !important;
    }

    /* BUTTONS – GREEN BACKGROUND, BLACK TEXT */
    .stButton > button {
        background-color: #445932 !important;
        color: #000000 !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100% !important;
    }
    .stButton > button:hover { background-color: #354526 !important; }

    /* TEXT INPUT */
    .stTextInput input {
        color: black !important;
        background-color: white !important;
        border-radius: 8px !important;
        border: 2px solid #445932 !important;
        padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📱 QR Scanner")
st.caption("🔍 Scan QR code or upload plant card")

tab1, tab2 = st.tabs(["📷 Upload Photo", "⌨️ Enter QR ID"])

PLANT_NAMES = ["Neem", "Tulsi", "Aloe Vera", "Rose", "Mango", "Lavender", "Sunflower",
               "Shankarsivari", "Tagar", "Jaswand", "Supari", "Lakshman Phal", "Gulmohar",
               "Kaju", "Madhumalati", "Nandaruk"]

def decode_qr_image(image):
    try:
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        qr = cv2.QRCodeDetector()
        data, _, _ = qr.detectAndDecode(img_array)
        return data if data else None
    except:
        return None

def extract_plant_name_from_text(text):
    if not text:
        return None
    lines = text.split('\n')
    for line in lines:
        for plant in PLANT_NAMES:
            if plant.lower() in line.lower():
                return plant
    return None

def read_plant_name_from_image(image):
    try:
        if isinstance(image, Image.Image):
            img = np.array(image)
        else:
            img = image
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(thresh)
        plant_name = extract_plant_name_from_text(text)
        return plant_name, text
    except Exception as e:
        return None, str(e)

def get_ai_info(plant_name):
    try:
        resp = ollama.chat(
            model='tinyllama',
            options={'num_predict': 500},
            messages=[{'role': 'user', 'content': f"Tell me about {plant_name} plant briefly."}]
        )
        return resp['message']['content']
    except:
        return "⚠️ AI service not available."

def display_plant_info(plant_name):
    st.success(f"🌿 **{plant_name}**")
    with st.spinner("🤖 Getting AI information..."):
        ai_info = get_ai_info(plant_name)
        st.write("### 🌿 Information")
        st.write(ai_info)

def process_qr(qr_data, image=None):
    if not qr_data and not image:
        st.warning("⚠️ No data found.")
        return

    if qr_data:
        st.success("✅ QR Code Detected Successfully!")  # ← WHITE BOX, BLACK TEXT
        st.info(f"📱 **QR Data:** {qr_data}")
        st.write("---")

    plant_name = None

    if image:
        with st.spinner("🔍 Reading plant name from image..."):
            plant_name, text = read_plant_name_from_image(image)

    if plant_name:
        display_plant_info(plant_name)
        return

    st.warning("⚠️ Could not detect plant name from image automatically.")
    st.write("💡 **Please type the plant name manually:**")

    manual_plant = st.text_input("🌱 Plant Name:", placeholder="e.g., Neem, Tulsi, Rose")

    if st.button("🔍 Get Information", key="manual_info"):
        if manual_plant:
            display_plant_info(manual_plant)
        else:
            st.warning("⚠️ Please enter a plant name.")

with tab1:
    uploaded = st.file_uploader("Choose QR code or plant card image", type=['jpg','png','jpeg'])
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        with st.spinner("🔍 Processing..."):
            qr_data = decode_qr_image(image)
            process_qr(qr_data, image)

with tab2:
    st.write("### ⌨️ Enter QR Code Data")
    qr_input = st.text_input("QR Data:", placeholder="e.g., QR012 or https://me-qr.com/...")
    if st.button("🔍 Search"):
        if qr_input:
            process_qr(qr_input, None)
        else:
            st.warning("Please enter QR data.")

st.write("---")
if st.button("← Back to Home"):
    st.switch_page("app.py")