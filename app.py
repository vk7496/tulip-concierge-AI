import streamlit as st

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="AI Hotel Concierge",
    page_icon="🏨",
    layout="wide"
)

# ---------------------------
# Header
# ---------------------------
st.markdown(
    """
    <h1 style='text-align:center;'>🏨 AI Hotel Concierge</h1>
    <p style='text-align:center; color:gray;'>
    Smart assistance for hotel guests – powered by AI
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Language Selector
# ---------------------------
language = st.selectbox(
    "🌍 Select Language",
    ["English", "Arabic"]
)

# ---------------------------
# Welcome Message
# ---------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

welcome_text = {
    "English": "Welcome! I am your AI hotel concierge. How can I assist you today?",
    "Arabic": "مرحبًا! أنا المساعد الذكي الخاص بالفندق. كيف يمكنني مساعدتك اليوم؟"
}

st.success(welcome_text[language])

# ---------------------------
# Service Cards
# ---------------------------
st.subheader("✨ Guest Services")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("🏨 Hotel Info\n\nCheck-in, WiFi, services")

with col2:
    st.info("🍽 Restaurants\n\nBest dining options")

with col3:
    st.info("🧖 Spa & Wellness\n\nRelaxation & treatments")

with col4:
    st.info("🗺 Attractions\n\nPlaces to visit nearby")

# ---------------------------
# Chat Section
# ---------------------------
st.subheader("💬 Concierge Chat")

user_input = st.text_input("Type your request here")

if st.button("Send"):
    if user_input.strip():
        st.session_state.chat.append(("Guest", user_input))
        st.session_state.chat.append(
            ("Concierge", "Thank you for your request. A concierge agent will assist you shortly.")
        )

# Display chat
for role, msg in st.session_state.chat:
    if role == "Guest":
        st.markdown(f"**🧑 Guest:** {msg}")
    else:
        st.markdown(f"**🤖 Concierge:** {msg}")

# ---------------------------
# Contact Hotel
# ---------------------------
st.markdown("---")
st.subheader("📞 Contact Hotel")

st.markdown(
    """
    <a href="https://wa.me/96891278434" target="_blank">
    📲 Contact via WhatsApp
    </a>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Footer
# ---------------------------
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:gray; font-size:12px;'>
    Designed by Golden Bird LLC – AI Hospitality Solutions
    </p>
    """,
    unsafe_allow_html=True
)
