import streamlit as st
import pandas as pd
import requests

# -----------------------------------------------------------------
# 1. Role-Based Access Control (RBAC) Setup
# -----------------------------------------------------------------
st.sidebar.title("System Login")
user_role = st.sidebar.selectbox("Select User Role", ["Viewer", "Operator", "Admin"])

# Mock Database / State
if 'withdrawals' not in st.session_state:
    st.session_state.withdrawals = pd.DataFrame({
        'ID': [1, 2],
        'User': ['Mg Mg', 'Aye Aye'],
        'Amount': [50000, 120000],
        'Status': ['Pending', 'Approved']
    })

# -----------------------------------------------------------------
# 2. Telegram Notification Function
# -----------------------------------------------------------------
def send_telegram_alert(message):
    """Telegram Bot မှတဆင့် အသိပေးချက်ပို့ရန် Function"""
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    CHAT_ID = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        return False

# -----------------------------------------------------------------
# 3. Main Dashboard Interface
# -----------------------------------------------------------------
st.title("🚀 Enterprise Operations Dashboard")
st.markdown(f"Current Logged-in Role: **{user_role}**")

# Display Table
st.subheader("Withdrawal Requests Management")
st.dataframe(st.session_state.withdrawals, use_container_width=True)

# -----------------------------------------------------------------
# 4. Role-Based Action Controls
# -----------------------------------------------------------------
if user_role in ["Operator", "Admin"]:
    st.divider()
    st.subheader("Quick Action: Update Status")
    
    selected_id = st.selectbox("Select Request ID to Update", st.session_state.withdrawals['ID'])
    new_status = st.selectbox("New Status", ["Pending", "Approved", "Rejected"])
    
    if st.button("Update Status & Notify"):
        # Status ပြောင်းလဲခြင်း
        st.session_state.withdrawals.loc[
            st.session_state.withdrawals['ID'] == selected_id, 'Status'
        ] = new_status
        
        # Telegram သို့ အသိပေးချက်ပို့ခြင်း
        msg_text = f"⚠️ *Status Updated!*\nRequest ID: {selected_id}\nNew Status: {new_status}\nUpdated by: {user_role}"
        success = send_telegram_alert(msg_text)
        
        st.success(f"Request ID {selected_id} status updated to {new_status} successfully!")
        if success:
            st.info("Telegram notification sent to management team.")
else:
    st.info("ℹ️ Viewer mode: You have read-only access to the dashboard. Contact an Admin for modification permissions.")

# Admin သီးသန့် အထူးလုပ်ဆောင်ချက်များ
if user_role == "Admin":
    st.divider()
    st.subheader("🔒 Admin Control Panel")
    if st.button("Export Full Audit Logs"):
        st.download_button("Download CSV", st.session_state.withdrawals.to_csv(index=False), "audit_logs.csv", "text/csv")
