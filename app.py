import streamlit as st
from groq import Groq

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Tulip Concierge AI",
    page_icon="🌷",
    layout="centered"
)

# -----------------------------
# Groq Client
# -----------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("GROQ_API_KEY is missing in Streamlit Secrets.")
    st.stop()

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Header
# -----------------------------
st.title("🌷 Tulip Concierge AI")
st.caption("AI Concierge designed to resolve real guest pain points")

# -----------------------------
# Language Selection
# -----------------------------
language_map = {
    "English": "Respond in English.",
    "Arabic": "أجب باللغة العربية وبأسلوب فندقي راقٍ.",
    "German": "Antworte höflich auf Deutsch.",
    "Russian": "Отвечай вежливо на русском языке."
}

selected_language = st.selectbox(
    "Preferred Language",
    list(language_map.keys())
)

language_instruction = language_map[selected_language]

# -----------------------------
# Display Chat History
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Pain Point Classifier
# -----------------------------
def classify_issue(text: str):
    text = text.lower()

    if any(k in text for k in ["check", "check-in", "reception", "arrival"]):
        return "Check-in & Reception delays"
    if any(k in text for k in ["water", "shower", "drain", "air", "ac", "room"]):
        return "Room maintenance issue"
    if any(k in text for k in ["food", "breakfast", "restaurant", "menu"]):
        return "Restaurant & food experience"
    if any(k in text for k in ["spa", "pool", "steam", "sauna"]):
        return "Spa / wellness service"
    if any(k in text for k in ["call", "phone", "reach", "contact"]):
        return "Difficulty contacting staff"

    return "General concierge request"

# -----------------------------
# Prompt Builder
# -----------------------------
def build_prompt(conversation, issue_type):
    history = "\n".join(
        [f"{m['role'].capitalize()}: {m['content']}" for m in conversation]
    )

    return f"""
You are a luxury hotel AI concierge for Royal Tulip.
Your goal is to resolve guest dissatisfaction professionally.

Detected issue category:
{issue_type}

Guidelines:
- Be calm, polite, and solution-oriented
- If issue needs staff intervention, clearly offer it
- Ask only ONE follow-up question if needed
- Never blame the guest or hotel

{language_instruction}

Conversation:
{history}
"""

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("How may I assist you today?")

if user_input:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    issue_type = classify_issue(user_input)

    with st.spinner("Resolving your request..."):
        try:
            prompt = build_prompt(
                st.session_state.messages,
                issue_type
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=350
            )

            assistant_reply = response.choices[0].message.content

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_reply}
            )

            with st.chat_message("assistant"):
                st.markdown(assistant_reply)

            # Action Suggest Note
            if issue_type != "General concierge request":
                st.info(
                    "If you wish, I can forward this request directly to hotel staff for immediate assistance."
                )

        except Exception as e:
            st.error(f"Groq API Error: {e}")

# -----------------------------
# WhatsApp Escalation
# -----------------------------
st.divider()
st.markdown("### 📲 Immediate Human Assistance")

whatsapp_number = "96891278434"  # replace with hotel number
whatsapp_text = "Hello, I need assistance regarding my stay at Royal Tulip."

whatsapp_url = (
    f"https://wa.me/{whatsapp_number}"
    f"?text={whatsapp_text.replace(' ', '%20')}"
)

st.link_button("Contact Hotel via WhatsApp", whatsapp_url)

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Golden Bird LLC | AI Guest Experience Solutions")
