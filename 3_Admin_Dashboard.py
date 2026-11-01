import streamlit as st
from database import get_total_plants, get_all_categories

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

# Agar login nahi hai toh wapas bhejo
if not st.session_state.get('logged_in', False):
    st.warning("⚠️ Please login first.")
    st.switch_page("pages/2_Admin_Login.py")

st.markdown("""
    <style>
    .stApp { background-color: #c7d7b8; }
    .dashboard-title { color: #445932; font-size: 2.5rem; }
    .stat-card {
        background-color: rgba(255,255,255,0.85);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stat-number { color: #445932; font-size: 2.5rem; font-weight: bold; }
    .stButton > button {
        background-color: #445932 !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100% !important;
    }
    .stButton > button:hover { background-color: #354526 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="dashboard-title">📊 Admin Dashboard</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="color: black;">👋 Welcome, {st.session_state.get("username", "Admin")}!</p>', unsafe_allow_html=True)

# Stats
total_plants = get_total_plants()
total_categories = len(get_all_categories())

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_plants}</div>
        <div class="stat-label">🌱 Total Plants</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_categories}</div>
        <div class="stat-label">📋 Categories</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">👤</div>
        <div class="stat-label">Visitors</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">📱</div>
        <div class="stat-label">QR Codes</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("➕ Add Plant", use_container_width=True):
        st.switch_page("pages/4_Manage_Plants.py")

with col2:
    if st.button("📋 Manage Plants", use_container_width=True):
        st.switch_page("pages/4_Manage_Plants.py")

with col3:
    if st.button("🔍 Search Plants", use_container_width=True):
        st.switch_page("pages/5_Search_Plant.py")

with col4:
    if st.button("📱 QR Scanner", use_container_width=True):
        st.switch_page("pages/7_QR_Scanner.py")

st.markdown("---")

# Logout
if st.button("🚪 Logout", use_container_width=True):
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.rerun()

# Back to Home
st.write("---")
if st.button("🏠 Back to Home", use_container_width=True):
    st.switch_page("app.py")