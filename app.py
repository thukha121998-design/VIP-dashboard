import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(
    page_title="Enterprise Operations Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar: Role & Secure Password Authentication ---
st.sidebar.title("🔐 System Login")
selected_role = st.sidebar.selectbox("Select User Role", ["Viewer", "Operator", "Admin"])

# Password Security Logic
user_role = "Viewer"  # Default is Viewer
if selected_role in ["Operator", "Admin"]:
    password_input = st.sidebar.text_input(f"Enter Password for {selected_role}", type="password")
    # ဒီနေရာမှာ Admin Password ကို သတ်မှတ်ထားပါတယ် (ဥပမာ - admin123)
    admin_password = st.secrets.get("ADMIN_PASSWORD", "admin123")
    
    if password_input == admin_password:
        user_role = selected_role
        st.sidebar.success(f"Logged in as {selected_role} ✅")
    else:
        if password_input:
            st.sidebar.error("❌ Incorrect Password! Defaulted to Viewer mode.")
        user_role = "Viewer"
else:
    user_role = "Viewer"

st.sidebar.markdown("---")
st.sidebar.subheader("📡 Telegram Integration")
tg_status = st.sidebar.checkbox("Enable Telegram Alerts", value=False)

# --- Main Dashboard Header ---
st.title("🚀 Enterprise Operations Dashboard")
st.markdown(f"**Current Verified Role:** `{user_role}` | **Dashboard URL:** `https://vip-dashboard-vt4mapqymzfkktvlybby3n.streamlit.app/`")

# --- Mock / Database State Management ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"ID": 1, "User": "Mg Mg", "Amount": 50000, "Status": "Pending", "Currency": "EGP"},
        {"ID": 2, "User": "Aye Aye", "Amount": 120000, "Status": "Approved", "Currency": "EGP"}
    ])

# --- Core Features: Withdrawal Requests Management ---
st.subheader("💳 Withdrawal Requests Management")

editable = True if user_role in ["Operator", "Admin"] else False

if editable:
    st.success(f"🔓 {user_role} Mode Active: You have full modification permissions.")
    edited_df = st.data_editor(st.session_state.data, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Save Changes & Notify via Telegram"):
        st.session_state.data = edited_df
        st.success("Changes saved successfully!")
        st.rerun()
else:
    st.dataframe(st.session_state.data, use_container_width=True)
    st.info("🔒 Viewer Mode: Read-only access. Enter the correct Admin/Operator password in the sidebar to gain edit permissions.")

# --- Analytics ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Total Requests", len(st.session_state.data))
col2.metric("Total Volume (EGP)", f"{st.session_state.data['Amount'].sum():,}")
col3.metric("System Status", "Online 🟢")
