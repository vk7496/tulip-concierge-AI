import streamlit as st
from groq import Groq

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Tulip Concierge AI",
    page_icon="🌷",
    layout="centered"
)

# -----------------------------
# Load Groq Client
# -----------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("GROQ_API_KEY در Streamlit Secrets تنظیم نشده است.")
    st.stop()

# -----------------------------
# UI Header
# -----------------------------
st.title("🌷 Tulip Concierge AI")
st.caption("AI-powered luxury concierge service")

# -----------------------------
# Language Selection
# -----------------------------
language_map = {
    "English": "Respond in English.",
    "Arabic": "أجب باللغة العربية.",
    "German": "Antworte auf Deutsch.",
    "Russian": "Отвечай на русском языке."
}

selected_language = st.selectbox(
    "Select Language",
    list(language_map.keys())
)

language_instruction = language_map[selected_language]

# -----------------------------
# Service Selection
# -----------------------------
service = st.selectbox(
    "Select Service",
    [
        "General Concierge",
        "Table Reservation",
        "Spa Booking"
    ]
)

# -----------------------------
# User Input
# -----------------------------
user_input = st.text_area(
    "Your request",
    placeholder="Example: Book a romantic dinner for two tonight at 8 PM"
)

# -----------------------------
# Prompt Builder
# -----------------------------
def build_prompt(service, user_input, language_instruction):
    base_context = f"""
You are a professional luxury hotel concierge.
Be polite, clear, and helpful.
{language_instruction}
"""

    if service == "Table Reservation":
        task = """
Handle a restaurant table reservation.
Ask politely for missing details like date, time, number of guests.
Confirm the reservation clearly.
"""
    elif service == "Spa Booking":
        task = """
Handle a spa booking request.
Ask for preferred treatment, date, and time if missing.
Confirm the booking professionally.
"""
    else:
        task = """
Provide concierge assistance for hotels, tourism, dining, or services.
"""

    return f"{base_context}\n{task}\nUser request:\n{user_input}"

# -----------------------------
# Generate Response
# -----------------------------
if st.button("Submit Request"):
    if not user_input.strip():
        st.warning("Please enter your request.")
    else:
        with st.spinner("Processing your request..."):
            try:
                prompt = build_prompt(
                    service,
                    user_input,
                    language_instruction
                )

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6,
                    max_tokens=300
                )

                st.success("Response generated successfully")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Error communicating with Groq API: {e}")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Designed by Golden Bird LLC | Tulip Concierge AI")
