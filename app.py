import streamlit as st
from groq import Groq
import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Tulip Concierge AI",
    page_icon="🌷",
    layout="centered"
)

# ---------------------------
# GROQ CLIENT
# ---------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL_NAME = "llama3-70b-8192"

# ---------------------------
# UTIL FUNCTIONS
# ---------------------------
def reshape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def get_ai_response(messages):
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_tokens=300
    )
    return completion.choices[0].message.content

# ---------------------------
# PROMPTS
# ---------------------------
SYSTEM_PROMPT_EN = """
You are a professional hotel concierge for Royal Tulip Muscat.
You are polite, concise, and hospitality-focused.
Answer clearly and professionally.
If a request requires human assistance, politely refer the guest to the front desk.
"""

SYSTEM_PROMPT_AR = """
أنت موظف استقبال محترف في فندق رويال توليب مسقط.
أسلوبك مهذب، واضح، ورسمي.
قدم المساعدة المتعلقة بخدمات الفندق فقط.
إذا احتاج الطلب إلى تدخل بشري، قم بتوجيه الضيف إلى مكتب الاستقبال بلطف.
"""

# ---------------------------
# SESSION STATE
# ---------------------------
if "language" not in st.session_state:
    st.session_state.language = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# HEADER
# ---------------------------
st.markdown(
    "<h2 style='text-align:center;'>🌷 Tulip Concierge AI</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Smart Digital Concierge for Royal Tulip Muscat</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------------------
# LANGUAGE SELECTION
# ---------------------------
if st.session_state.language is None:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.language = "EN"
            st.session_state.messages = [
                {"role": "system", "content": SYSTEM_PROMPT_EN}
            ]

    with col2:
        if st.button("🇴🇲 العربية", use_container_width=True):
            st.session_state.language = "AR"
            st.session_state.messages = [
                {"role": "system", "content": SYSTEM_PROMPT_AR}
            ]

    st.stop()

# ---------------------------
# QUICK QUESTIONS
# ---------------------------
st.subheader("Quick Questions" if st.session_state.language == "EN" else reshape_arabic("أسئلة سريعة"))

quick_questions_en = [
    "What time is breakfast?",
    "Do you provide airport transfer?",
    "Can I request late checkout?",
    "What attractions are nearby?"
]

quick_questions_ar = [
    "ما هو وقت الإفطار؟",
    "هل يوجد خدمة توصيل من المطار؟",
    "هل يمكن طلب تسجيل خروج متأخر؟",
    "ما هي الأماكن القريبة من الفندق؟"
]

questions = quick_questions_en if st.session_state.language == "EN" else quick_questions_ar

cols = st.columns(2)
for i, q in enumerate(questions):
    if cols[i % 2].button(q, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": q})

# ---------------------------
# CHAT HISTORY
# ---------------------------
st.divider()

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        content = msg["content"]
        if st.session_state.language == "AR":
            content = reshape_arabic(content)
        st.chat_message("assistant").write(content)

# ---------------------------
# CHAT INPUT
# ---------------------------
user_input = st.chat_input(
    "Type your message here..."
    if st.session_state.language == "EN"
    else "اكتب رسالتك هنا..."
)

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking..."):
        ai_reply = get_ai_response(st.session_state.messages)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    st.rerun()

# ---------------------------
# MANAGEMENT INSIGHT (DEMO)
# ---------------------------
st.divider()
st.subheader("Management Insight (Demo)")

demo_data = {
    "Metric": [
        "Most Asked Topic",
        "Peak Request Time",
        "Primary Language"
    ],
    "Value": [
        "Breakfast & Services",
        "08:00 – 10:00",
        "Arabic / English"
    ]
}

df = pd.DataFrame(demo_data)
st.table(df)

# ---------------------------
# FOOTER
# ---------------------------
st.divider()
st.markdown(
    "<p style='text-align:center; font-size:12px;'>"
    "Designed & Developed by <b>Golden Bird LLC</b><br>"
    "AI Solutions for Hospitality in Oman"
    "</p>",
    unsafe_allow_html=True
)
