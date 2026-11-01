import streamlit as st
from database import admin_login

st.set_page_config(
    page_title="Admin Login",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #c7d7b8; }
    .stButton > button {
        background-color: #445932 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 40px !important;
        font-size: 1.1rem !important;
        border: none !important;
        width: 100% !important;
    }
    .stButton > button:hover { background-color: #354526 !important; }
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #445932 !important;
        padding: 10px !important;
        color: black !important;
        background-color: white !important;
    }
    .stTextInput label { color: black !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color: #445932; text-align: center;">🔐 Admin Login</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #000000;">Please enter your credentials</p>', unsafe_allow_html=True)

# Agar already login hai toh dashboard pe bhejo
if st.session_state.get('logged_in', False):
    st.switch_page("pages/3_Admin_Dashboard.py")

with st.form("login_form"):
    username = st.text_input("👤 Username", placeholder="Enter your username")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
    submitted = st.form_submit_button("🔐 Login")
    
    if submitted:
        if not username or not password:
            st.error("⚠️ Please enter both username and password.")
        else:
            if admin_login(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

if st.button("← Back to Home", use_container_width=True):
    st.switch_page("app.py")