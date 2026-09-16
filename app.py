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

# Custom Styling (Tailwind/Modern CSS integration)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- Telegram Bot Notification Function ---
def send_telegram_notification(message):
    """
    Telegram Bot ကို အသုံးပြု၍ အလိုအလျောက် Status မက်ဆေ့ခ်ျ ပို့ပေးသော လုပ်ဆောင်ချက်
    (Bot Token နှင့် Chat ID တို့ကို Streamlit secrets သို့မဟုတ် ဤနေရာတွင် ထည့်သွင်းနိုင်သည်)
    """
    bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
    chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")
    
    if bot_token != "YOUR_BOT_TOKEN" and chat_id != "YOUR_CHAT_ID":
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            st.error(f"Telegram notification failed: {e}")

# --- Sidebar: Role & System Configuration ---
st.sidebar.title("🔐 System Login")
user_role = st.sidebar.selectbox("Select User Role", ["Viewer", "Operator", "Admin"])

st.sidebar.markdown("---")
st.sidebar.subheader("📡 Telegram Integration")
tg_status = st.sidebar.checkbox("Enable Telegram Alerts", value=False)

# --- Main Dashboard Header ---
st.title("🚀 Enterprise Operations Dashboard")
st.markdown(f"**Current Logged-in Role:** `{user_role}` | **Dashboard URL:** `https://vip-dashboard-vt4mapqymzfkktvlybby3n.streamlit.app/`")

# --- Mock / Database State Management (Supabase Ready) ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"ID": 1, "User": "Mg Mg", "Amount": 50000, "Status": "Pending", "Currency": "EGP"},
        {"ID": 2, "User": "Aye Aye", "Amount": 120000, "Status": "Approved", "Currency": "EGP"}
    ])

# --- Core Features: Withdrawal Requests Management ---
st.subheader("💳 Withdrawal Requests Management")

# Display Table
editable = True if user_role in ["Operator", "Admin"] else False

if editable:
    st.info("💡 Operator/Admin mode: You can update statuses directly below.")
    edited_df = st.data_editor(st.session_state.data, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Save Changes & Notify via Telegram"):
        st.session_state.data = edited_df
        st.success("Changes saved successfully!")
        if tg_status:
            send_telegram_notification("🔔 *Enterprise Alert*: Withdrawal request statuses have been updated by an operator.")
        st.rerun()
else:
    st.dataframe(st.session_state.data, use_container_width=True)
    st.warning("🔒 Viewer mode: You have read-only access to the dashboard. Contact an Admin for modification permissions.")

# --- Analytics & Extras ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Total Requests", len(st.session_state.data))
col2.metric("Total Volume (EGP)", f"{st.session_state.data['Amount'].sum():,}")
col3.metric("System Status", "Online 🟢")
