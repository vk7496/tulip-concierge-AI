import streamlit as st
from groq import Groq
import re

# ======================
# Page Config
# ======================
st.set_page_config(
    page_title="Royal Tulip AI Concierge",
    page_icon="🏨",
    layout="centered"
)

# ======================
# Groq Client
# ======================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MODEL_NAME = "llama-3.3-70b-versatile"

# ======================
# System Prompt
# ======================
SYSTEM_PROMPT = """
You are a professional AI Concierge for a 5-star Royal Tulip Hotel.

Rules:
- Always reply in the SAME language as the guest.
- Be polite, short, and hotel-professional.
- If guest asks for location, ALWAYS provide a Google Maps link.
- You can help with:
  - Restaurant reservation
  - Spa reservation
  - Hotel facilities
  - Complaints and feedback
- Never say you are an AI model.
"""

# ======================
# Session State
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ======================
# Title
# ======================
st.title("🏨 Royal Tulip AI Concierge")
st.caption("Available 24/7 • Multilingual Assistant")

# ======================
# Show Chat History
# ======================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================
# Helper: Google Maps
# ======================
def add_google_maps_if_needed(text):
    keywords = ["location", "address", "map", "where", "لوکیشن", "موقعیت"]
    if any(k in text.lower() for k in keywords):
        return text + "\n\n📍 **Google Maps:** https://www.google.com/maps"
    return text

# ======================
# AI Response
# ======================
def get_ai_response(messages):
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.4,
        max_tokens=350
    )
    return completion.choices[0].message.content

# ======================
# Chat Input
# ======================
user_input = st.chat_input("How can I assist you today?")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI Response
    with st.chat_message("assistant"):
        with st.spinner("Please wait..."):
            ai_reply = get_ai_response(st.session_state.messages)
            ai_reply = add_google_maps_if_needed(ai_reply)
            st.markdown(ai_reply)

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

# ======================
# Quick Actions
# ======================
st.divider()
st.subheader("Quick Services")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🍽️ Book Restaurant"):
        st.session_state.messages.append(
            {"role": "user", "content": "I want to book a table at the restaurant."}
        )
        st.rerun()

with col2:
    if st.button("💆 Book Spa"):
        st.session_state.messages.append(
            {"role": "user", "content": "I want to book a spa session."}
        )
        st.rerun()

with col3:
    st.link_button(
        "📲 WhatsApp Hotel",
        "https://wa.me/96891278434"
    )
