import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from database import get_plant_by_qr, get_plant_by_id, search_plants, get_all_plants
import ollama
from urllib.parse import urlparse, parse_qs, unquote


st.set_page_config(
    page_title="QR Scanner - FloraAtlas",
    page_icon="📱",
    layout="wide"
)


# ==================== CHECK LOGIN ====================

if not st.session_state.get('logged_in', False):
    st.switch_page("app.py")


# ==================== PAGE STYLE ====================

st.markdown("""
    <style>
    .stApp {
        background-color: #c7d7b8;
    }

    .stButton > button {
        background-color: #445932 !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background-color: #354526 !important;
    }

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3 {
        color: black !important;
    }

    .stSuccess {
        color: black !important;
    }

    .stWarning {
        color: black !important;
    }

    .stInfo {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)


st.title("📱 QR Scanner")


# ==================== TABS ====================

tab1, tab2, tab3, tab4 = st.tabs([
    "📷 Camera Scan",
    "📤 Upload Photo",
    "⌨️ Enter QR ID",
    "🔍 Search Plant"
])


# ============================================================
# QR DECODE - IMPROVED OPENCV
# ============================================================

def decode_qr_image(image):
    """
    Improved QR decoder.

    Handles:
    - PIL RGB images
    - OpenCV images
    - original image
    - resized image
    - grayscale
    - adaptive threshold
    - enhanced contrast
    - rotated/processed versions
    """

    try:

        # ----------------------------------------------------
        # STEP 1: Convert image correctly to OpenCV BGR
        # ----------------------------------------------------

        if isinstance(image, Image.Image):

            # PIL image is RGB
            pil_image = image.convert("RGB")

            # RGB -> OpenCV BGR
            img_array = np.array(pil_image)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        else:

            img_bgr = image.copy()

            # If image has alpha channel
            if len(img_bgr.shape) == 3 and img_bgr.shape[2] == 4:
                img_bgr = cv2.cvtColor(
                    img_bgr,
                    cv2.COLOR_BGRA2BGR
                )


        # ----------------------------------------------------
        # STEP 2: Make image larger
        # ----------------------------------------------------

        height, width = img_bgr.shape[:2]

        if width < 1000:

            scale = 2

            img_bgr = cv2.resize(
                img_bgr,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_CUBIC
            )


        # ----------------------------------------------------
        # STEP 3: Create QR detector
        # ----------------------------------------------------

        detector = cv2.QRCodeDetector()


        # ----------------------------------------------------
        # METHOD 1: Original image
        # ----------------------------------------------------

        try:

            data, points, _ = detector.detectAndDecode(img_bgr)

            if data:
                return data.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # METHOD 2: Grayscale
        # ----------------------------------------------------

        try:

            gray = cv2.cvtColor(
                img_bgr,
                cv2.COLOR_BGR2GRAY
            )

            detector = cv2.QRCodeDetector()

            data, points, _ = detector.detectAndDecode(gray)

            if data:
                return data.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # METHOD 3: Increased contrast
        # ----------------------------------------------------

        try:

            gray = cv2.cvtColor(
                img_bgr,
                cv2.COLOR_BGR2GRAY
            )

            enhanced = cv2.equalizeHist(gray)

            detector = cv2.QRCodeDetector()

            data, points, _ = detector.detectAndDecode(
                enhanced
            )

            if data:
                return data.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # METHOD 4: Adaptive threshold
        # ----------------------------------------------------

        try:

            gray = cv2.cvtColor(
                img_bgr,
                cv2.COLOR_BGR2GRAY
            )

            threshold = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )

            detector = cv2.QRCodeDetector()

            data, points, _ = detector.detectAndDecode(
                threshold
            )

            if data:
                return data.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # METHOD 5: OTSU threshold
        # ----------------------------------------------------

        try:

            gray = cv2.cvtColor(
                img_bgr,
                cv2.COLOR_BGR2GRAY
            )

            _, threshold = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            detector = cv2.QRCodeDetector()

            data, points, _ = detector.detectAndDecode(
                threshold
            )

            if data:
                return data.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # METHOD 6: Sharpen image
        # ----------------------------------------------------

        try:

            gray = cv2.cvtColor(
                img_bgr,
                cv2.COLOR_BGR2GRAY
            )

            sharpen_kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ])

            sharpened = cv2.filter2D(
                gray,
                -1,
                sharpen_kernel
            )

            detector = cv2.QRCodeDetector()

            data, points, _ = detector.detectAndDecode(
                sharpened
            )

            if data:
                return data.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # METHOD 7: PIL contrast enhancement
        # ----------------------------------------------------

        try:

            pil_img = Image.fromarray(
                cv2.cvtColor(
                    img_bgr,
                    cv2.COLOR_BGR2RGB
                )
            )

            enhancer = ImageEnhance.Contrast(
                pil_img
            )

            enhanced = enhancer.enhance(2.5)

            enhanced_np = np.array(
                enhanced
            )

            enhanced_bgr = cv2.cvtColor(
                enhanced_np,
                cv2.COLOR_RGB2BGR
            )

            detector = cv2.QRCodeDetector()

            data, points, _ = detector.detectAndDecode(
                enhanced_bgr
            )

            if data:
                return data.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # METHOD 8: Detect multiple QR codes
        # ----------------------------------------------------

        try:

            detector = cv2.QRCodeDetector()

            ok, decoded_info, points, _ = (
                detector.detectAndDecodeMulti(
                    img_bgr
                )
            )

            if ok and decoded_info:

                for item in decoded_info:

                    if item:
                        return item.strip()

        except Exception:
            pass


        # ----------------------------------------------------
        # Nothing detected
        # ----------------------------------------------------

        return None


    except Exception:

        return None


# ============================================================
# AI FUNCTION
# ============================================================

def get_ai_info(plant_name):

    try:

        response = ollama.chat(
            model='tinyllama',
            options={
                'num_predict': 512
            },
            messages=[
                {
                    'role': 'user',
                    'content':
                    f"Tell me about {plant_name}. "
                    "Give short, useful information "
                    "about benefits and uses."
                }
            ]
        )

        return response['message']['content']

    except Exception:

        return (
            "AI information is not available "
            "at the moment. Please try again later."
        )


# ============================================================
# EXTRACT NAME FROM URL
# ============================================================

def extract_plant_name_from_url(url):

    try:

        parsed = urlparse(url)

        params = parse_qs(
            parsed.query
        )

        if "LatinName" in params:

            return unquote(
                params["LatinName"][0]
            )

        elif "name" in params:

            return unquote(
                params["name"][0]
            )

        elif "q" in params:

            return unquote(
                params["q"][0]
            )

        else:

            path = parsed.path

            if path:

                parts = path.split('/')

                if parts:

                    last = parts[-1]

                    if last:

                        return unquote(
                            last
                            .replace('.html', '')
                            .replace('.php', '')
                        )

        return url

    except Exception:

        return url


# ============================================================
# DISPLAY PLANT INFO
# ============================================================

def display_plant_info(plant):

    st.success(
        f"🌿 Plant: {plant[1]}"
    )

    st.write(
        f"**Scientific Name:** {plant[2]}"
    )

    st.write(
        f"**Category:** {plant[6]}"
    )

    st.write(
        f"**📱 QR Code ID:** {plant[11]}"
    )


    with st.spinner(
        "🤖 Getting AI information..."
    ):

        ai_info = get_ai_info(
            plant[1]
        )

        st.write("---")

        st.write(
            "### 🤖 AI Information"
        )

        st.write(
            ai_info
        )


    if plant[12] and plant[13]:

        st.write("---")

        if st.button(
            "📍 View Location on Map",
            key="view_location_btn"
        ):

            st.session_state[
                'selected_plant'
            ] = plant[0]

            st.switch_page(
                "pages/2_Location_Tracker.py"
            )

    else:

        st.info(
            "📍 No location data available for this plant."
        )


# ============================================================
# DISPLAY UNKNOWN QR INFO
# ============================================================

def display_unknown_qr_info(qr_data):

    search_text = qr_data

    if qr_data.startswith("http"):

        search_text = (
            extract_plant_name_from_url(
                qr_data
            )
        )


    st.warning(
        "⚠️ QR Code is not registered "
        "in the campus database."
    )

    st.write(
        f"**QR Data:** {qr_data}"
    )

    st.write("---")

    st.write(
        f"### 🤖 General Information about: "
        f"{search_text}"
    )


    with st.spinner(
        "🤖 Getting information from AI..."
    ):

        ai_info = get_ai_info(
            search_text
        )

        st.write(
            ai_info
        )


# ============================================================
# TAB 1: CAMERA SCAN
# ============================================================

with tab1:

    st.write(
        "### 📷 Scan QR Code with Camera"
    )

    st.info(
        "💡 QR code ko camera ke saamne "
        "clear aur seedha rakhein."
    )


    camera_image = st.camera_input(
        "📸 Take a photo of the QR code"
    )


    if camera_image:

        try:

            image = Image.open(
                camera_image
            ).convert("RGB")


            st.image(
                image,
                caption="Captured QR Image",
                use_container_width=True
            )


            with st.spinner(
                "🔍 Scanning QR code..."
            ):

                qr_data = decode_qr_image(
                    image
                )


            if qr_data:

                st.success(
                    "✅ QR Code Detected!"
                )

                # IMPORTANT:
                # QR se jo value mili hai
                # wahi directly database mein search hogi.

                plant = get_plant_by_qr(
                    qr_data
                )


                if plant:

                    display_plant_info(
                        plant
                    )

                else:

                    display_unknown_qr_info(
                        qr_data
                    )


            else:

                st.error(
                    "❌ QR Code detect nahi hua."
                )

                st.info(
                    "💡 QR code ko frame ke beech mein "
                    "rakhein, light achhi rakhein aur "
                    "photo thodi close se lein."
                )


        except Exception as e:

            st.error(
                f"⚠️ Error: {e}"
            )


# ============================================================
# TAB 2: UPLOAD
# ============================================================

with tab2:

    st.write(
        "### 📤 Upload QR Code Photo"
    )

    st.info(
        "💡 Upload a clear image of the QR code"
    )


    uploaded_file = st.file_uploader(
        "Choose QR code image",
        type=[
            'jpg',
            'jpeg',
            'png',
            'bmp',
            'webp'
        ],
        key="qr_uploader"
    )


    if uploaded_file:

        try:

            image = Image.open(
                uploaded_file
            ).convert("RGB")


            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )


            with st.spinner(
                "🔍 Scanning QR code..."
            ):

                qr_data = decode_qr_image(
                    image
                )


            if qr_data:

                st.success(
                    "✅ QR Code Detected!"
                )

                plant = get_plant_by_qr(
                    qr_data
                )


                if plant:

                    display_plant_info(
                        plant
                    )

                else:

                    display_unknown_qr_info(
                        qr_data
                    )


            else:

                st.warning(
                    "⚠️ No QR code detected "
                    "in this image."
                )


        except Exception as e:

            st.error(
                f"⚠️ Error: {e}"
            )


# ============================================================
# TAB 3: MANUAL
# ============================================================

with tab3:

    st.write(
        "### ⌨️ Enter QR Code ID"
    )

    st.caption(
        "💡 This method always works - "
        "just type the QR code ID"
    )


    qr_id = st.text_input(
        "QR Code ID:",
        placeholder="e.g., QR001",
        key="qr_manual_input"
    )


    if st.button(
        "🔍 Search",
        key="search_qr_btn"
    ):

        if qr_id:

            plant = get_plant_by_qr(
                qr_id
            )


            if plant:

                display_plant_info(
                    plant
                )

            else:

                st.error(
                    "❌ No plant found with this QR ID."
                )

                st.info(
                    "💡 Available QR Codes: "
                    "QR001, QR002, QR003, QR004, "
                    "QR005, QR006, QR007, QR008"
                )

        else:

            st.warning(
                "⚠️ Please enter a QR ID."
            )


# ============================================================
# TAB 4: SEARCH
# ============================================================

with tab4:

    st.write(
        "### 🔍 Search Plant by Name"
    )


    search_term = st.text_input(
        "Enter plant name:",
        placeholder="e.g., Neem",
        key="plant_search_input"
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🔍 Search",
            key="search_plant_btn"
        ):

            if search_term:

                results = search_plants(
                    search_term
                )


                if results:

                    st.success(
                        f"✅ Found {len(results)} plant(s):"
                    )


                    for plant in results:

                        st.markdown(
                            f"""
                            <div style="
                                background: white;
                                border-radius: 10px;
                                padding: 12px 18px;
                                margin: 8px 0;
                                border: 2px solid #445932;
                            ">
                                <div>
                                    <strong>
                                        🌿 {plant[1]}
                                    </strong>
                                </div>

                                <div>
                                    <i>{plant[2]}</i>
                                </div>

                                <div>
                                    📂 {plant[6]}
                                </div>

                                <div>
                                    📱 QR Code:
                                    {plant[11] if plant[11] else 'N/A'}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.warning(
                        "❌ No plants found."
                    )

            else:

                st.warning(
                    "⚠️ Please enter a plant name."
                )


    with col2:

        if st.button(
            "📋 Show All Plants",
            key="show_all_plants_btn"
        ):

            all_plants = get_all_plants()


            if all_plants:

                st.success(
                    f"✅ Showing all "
                    f"{len(all_plants)} plants:"
                )


                for plant in all_plants:

                    st.markdown(
                        f"""
                        <div style="
                            background: white;
                            border-radius: 10px;
                            padding: 12px 18px;
                            margin: 8px 0;
                            border: 2px solid #445932;
                        ">
                            <div>
                                <strong>
                                    🌿 {plant[1]}
                                </strong>
                            </div>

                            <div>
                                <i>{plant[2]}</i>
                            </div>

                            <div>
                                📂 {plant[6]}
                            </div>

                            <div>
                                📱 QR Code:
                                {plant[11] if plant[11] else 'N/A'}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# ============================================================
# QR CODE LIST
# ============================================================

st.write("---")

st.write(
    "### 📋 Available QR Codes:"
)


all_plants = get_all_plants()


if all_plants:

    st.write(
        "| QR Code | Plant Name | Scientific Name |"
    )

    st.write(
        "|---------|------------|-----------------|"
    )


    for plant in all_plants:

        qr = (
            plant[11]
            if plant[11]
            else "N/A"
        )

        st.write(
            f"| {qr} | {plant[1]} | {plant[2]} |"
        )

else:

    st.info(
        "No plants in database. "
        "Please add some plants first!"
    )


# ============================================================
# BACK BUTTON
# ============================================================

st.write("---")


if st.button(
    "← Back to Home",
    key="back_home_btn"
):

    st.switch_page(
        "app.py"
    )