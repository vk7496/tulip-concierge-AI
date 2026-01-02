import streamlit as st

# --------------------------------------------------
# Page Configuration (SAFE for Streamlit Cloud)
# --------------------------------------------------
st.set_page_config(
    page_title="AI Hotel Concierge",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; padding-top:20px;">
        <h1>AI Hotel Concierge</h1>
        <p style="color:gray; font-size:16px;">
            Smart assistance for hotel guests – powered by AI
        </p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Language Selector
# --------------------------------------------------
language = st.selectbox(
    "Select Language",
    ["English", "Arabic", "German", "Russian"]
)

# --------------------------------------------------
# Language Dictionary
# --------------------------------------------------
TEXT = {
    "English": {
        "welcome": "Welcome! How can we assist you today?",
        "restaurant": "Restaurant Reservation",
        "spa": "Spa Reservation",
        "transport": "Airport Transfer",
        "whatsapp": "Contact Hotel via WhatsApp",
        "submit": "Submit Request"
    },
    "Arabic": {
        "welcome": "مرحباً! كيف يمكننا مساعدتك اليوم؟",
        "restaurant": "حجز مطعم",
        "spa": "حجز سبا",
        "transport": "حجز نقل من وإلى المطار",
        "whatsapp": "التواصل مع الفندق عبر واتساب",
        "submit": "إرسال الطلب"
    },
    "German": {
        "welcome": "Willkommen! Wie können wir Ihnen helfen?",
        "restaurant": "Restaurantreservierung",
        "spa": "Spa-Reservierung",
        "transport": "Flughafentransfer",
        "whatsapp": "Hotel über WhatsApp kontaktieren",
        "submit": "Anfrage senden"
    },
    "Russian": {
        "welcome": "Добро пожаловать! Чем мы можем помочь?",
        "restaurant": "Бронирование ресторана",
        "spa": "Бронирование спа",
        "transport": "Трансфер из аэропорта",
        "whatsapp": "Связаться с отелем через WhatsApp",
        "submit": "Отправить запрос"
    }
}

t = TEXT[language]

# --------------------------------------------------
# Main Guest Interface
# --------------------------------------------------
st.subheader(t["welcome"])

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(t["restaurant"], use_container_width=True):
        st.success("Restaurant reservation request registered.")

with col2:
    if st.button(t["spa"], use_container_width=True):
        st.success("Spa reservation request registered.")

with col3:
    if st.button(t["transport"], use_container_width=True):
        st.success("Airport transfer request registered.")

# --------------------------------------------------
# WhatsApp Contact
# --------------------------------------------------
st.markdown("---")
st.markdown(
    f"""
    <a href="https://wa.me/96891278434" target="_blank"
       style="
       display:inline-block;
       padding:12px 24px;
       background-color:#25D366;
       color:white;
       border-radius:6px;
       text-decoration:none;
       font-weight:bold;
       ">
       {t["whatsapp"]}
    </a>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray; font-size:13px;">
        Designed by Golden Bird LLC · AI Hospitality Solutions
    </div>
    """,
    unsafe_allow_html=True
)
