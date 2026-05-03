import streamlit as st
import google.generativeai as genai

# API Anahtarın
genai.configure(api_key="AIzaSyCGWNPpkXbkyN5DY9NaqoNV07C6iqSYRUc")

# GÜRai'nin Beyni
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ GÜRai - Yapay Zeka")

soru = st.text_input("GÜRai'ye bir şey sor:")

if soru:
    try:
        # Yanıt oluşturma
        response = model.generate_content(soru)
        st.write(response.text)
    except Exception as e:
        # Hata varsa burada açıkça yazar
        st.error(f"Gelen Hata: {e}")
        st.info("Eğer 404 alıyorsan terminale 'pip install -U google-generativeai' yazmayı unutma!")
