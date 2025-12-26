import streamlit as st
from groq import Groq

# تنظیمات صفحه
st.set_page_config(page_title="Groq Test", page_icon="⚡")

# دریافت کلید از Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("لطفاً GROQ_API_KEY را در تنظیمات Streamlit Secrets وارد کنید.")
    st.stop()

st.title("Groq Connection Test 🚀")

# رابط کاربری ساده
if st.button("Test Groq"):
    try:
        with st.spinner('در حال دریافت پاسخ...'):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": "Say hello in Arabic and English"}
                ],
                max_tokens=50
            )
            
            st.success("ارتباط با موفقیت برقرار شد!")
            st.markdown(f"**پاسخ مدل:** {response.choices[0].message.content}")
            
    except Exception as e:
        st.error(f"خطایی رخ داد: {e}")
