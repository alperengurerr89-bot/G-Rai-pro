import streamlit as st
import google.generativeai as genai

# API anahtarını buraya hatasız yapıştır
genai.configure(api_key="AIza...") 

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ GÜRai - Yapay Zeka")

soru = st.text_input("GÜRai'ye merhaba de:")

# Sadece soru yazılmışsa çalıştır
if soru:
    try:
        response = model.generate_content(soru)
        st.write(response.text)
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
