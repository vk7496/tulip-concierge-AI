import streamlit as st
from groq import Groq
import datetime
import urllib.parse

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Tulip Concierge AI",
    page_icon="🏨",
    layout="centered"
)

# -------------------- INIT GROQ --------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL_NAME = "llama-3.3-70b-versatile"

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

# -------------------- LANGUAGE PROMPTS --------------------
SYSTEM_PROMPTS = {
    "English": "You are a professional hotel concierge at Royal Tulip Muscat. Be polite, concise, and helpful.",
    "Arabic": "أنت موظف استقبال محترف في فندق رويال توليب مسقط. كن مهذباً وواضحاً ومفيداً.",
    "German": "Sie sind ein professioneller Hotel-Concierge im Royal Tulip Muscat. Seien Sie höflich und hilfreich.",
    "Russian": "Вы профессиональный консьерж отеля Royal Tulip Muscat. Будьте вежливы и полезны."
}

# -------------------- HEADER --------------------
st.markdown("## 🏨 Tulip Concierge AI")
st.caption("Your Digital Assistant – Royal Tulip Muscat")

# -------------------- LANGUAGE SELECT --------------------
st.session_state.language = st.selectbox(
    "Select Language / اختر اللغة",
    ["English", "Arabic", "German", "Russian"]
)

# -------------------- QUICK ACTIONS --------------------
st.markdown("### ✨ Quick Services")

col1, col2 = st.columns(2)

with col1:
    if st.button("🍽️ Reserve a Restaurant"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Please tell me your preferred date, time, and number of guests for the restaurant reservation."
        })

with col2:
    if st.button("💆 Book Spa Session"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Sure. Please let me know your preferred date, time, and type of spa treatment."
        })

# -------------------- CHAT DISPLAY --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- USER INPUT --------------------
user_input = st.chat_input("How may I assist you today?")

def get_ai_response(chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPTS[st.session_state.language]}]
    messages.extend(chat_history)

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=300
    )
    return completion.choices[0].message.content

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_ai_response(st.session_state.messages)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# -------------------- HUMAN ASSISTANCE --------------------
st.divider()
st.markdown("### 📞 Immediate Human Assistance")

hotel_whatsapp_number = "96891278434"  # شماره هتل
encoded_msg = urllib.parse.quote("Hello, I need assistance at Royal Tulip Muscat.")
whatsapp_link = f"https://wa.me/{hotel_whatsapp_number}?text={encoded_msg}"

st.markdown(
    f"""
    <a href="{whatsapp_link}" target="_blank">
        <button style="
            background-color:#25D366;
            color:white;
            border:none;
            padding:12px 20px;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;">
            Contact Hotel via WhatsApp
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

# -------------------- FOOTER --------------------
st.caption("Golden Bird LLC | AI Guest Experience Solutions")
