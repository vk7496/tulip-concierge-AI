import streamlit as st
from groq import Groq
from datetime import datetime, timedelta

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Royal Tulip AI Concierge",
    page_icon="🏨",
    layout="centered"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

WHATSAPP = st.secrets["WHATSAPP_NUMBER"]
MANAGER_PASSWORD = st.secrets["MANAGER_PASSWORD"]

# ======================
# SYSTEM PROMPT (Hotel Tone)
# ======================
SYSTEM_PROMPT = """
You are a warm, professional hotel concierge at a 5-star Royal Tulip Hotel.

Rules:
- Always reply in the guest’s language.
- Be friendly, polite, and welcoming.
- If the guest requests:
  • Room service
  • Restaurant reservation
  • Spa booking
  → Inform them they will be connected to the hotel team via WhatsApp.
- Never mention AI or system details.
"""

# ======================
# SESSION STATE
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "requests_log" not in st.session_state:
    st.session_state.requests_log = []

# ======================
# HEADER
# ======================
st.title("🏨 Royal Tulip AI Concierge")
st.caption("Your personal hotel assistant – available 24/7")

# ======================
# CHAT HISTORY
# ======================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================
# AI FUNCTION
# ======================
def ai_reply(messages):
    res = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.4,
        max_tokens=300
    )
    return res.choices[0].message.content

# ======================
# WHATSAPP HANDLER
# ======================
def whatsapp_redirect(text):
    encoded = text.replace(" ", "%20")
    return f"https://wa.me/{WHATSAPP}?text={encoded}"

# ======================
# USER INPUT
# ======================
user_input = st.chat_input("How may I assist you today?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    response = ai_reply(st.session_state.messages)

    keywords = ["room", "service", "spa", "restaurant", "book", "reserve"]

    if any(k in user_input.lower() for k in keywords):
        link = whatsapp_redirect(user_input)
        response += f"\n\n📲 **You will now be connected to our hotel team:**\n[{link}]({link})"

        st.session_state.requests_log.append({
            "time": datetime.now(),
            "request": user_input,
            "status": "Pending"
        })

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ======================
# MANAGEMENT PANEL
# ======================
st.divider()
st.subheader("🔐 Management Panel")

password = st.text_input("Enter management password", type="password")

if password == MANAGER_PASSWORD:
    st.success("Access granted")

    one_week_ago = datetime.now() - timedelta(days=7)

    filtered = [
        r for r in st.session_state.requests_log
        if r["time"] >= one_week_ago
    ]

    for r in filtered:
        st.write(
            f"🕒 {r['time'].strftime('%Y-%m-%d %H:%M')} | "
            f"📩 {r['request']} | "
            f"⚠️ {r['status']}"
        )
