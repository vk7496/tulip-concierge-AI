import streamlit as st
from groq import Groq

st.set_page_config(page_title="Groq Test")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Groq Connection Test")

if st.button("Test Groq"):
    response = client.chat.completions.create(
        model="Llama-3.3-70b",
        messages=[
            {"role": "user", "content": "Say hello in Arabic and English"}
        ],
        max_tokens=50
    )
    st.success(response.choices[0].message.content)
