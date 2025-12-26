import streamlit as st
from groq import Groq

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Tulip Concierge AI",
    page_icon="🌷",
    layout="centered"
)

MODEL_NAME = "llama3-70b-8192"

SYSTEM_PROMPT = """
You are Tulip Concierge AI for Royal Tulip Muscat hotel.
You assist hotel guests professionally and politely.
You speak Arabic and English fluently.
You only provide hotel-related information, services, and assistance.
Tone: Luxury, helpful, concise.
"""

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_response(messages):
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.4,
        max_tokens=350
    )
    return completion.choices[0].message.content


# ---------------- UI ----------------
st.title("🌷 Tulip Concierge AI")
st.caption("Royal Tulip Muscat – Smart Hotel Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.chat_input("Ask about hotel services / اسأل عن خدمات الفندق")

if user_prompt:
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_reply = get_ai_response(st.session_state.messages)
            st.markdown(ai_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Designed & Developed by Golden Bird LLC | AI Hotel Solutions")
