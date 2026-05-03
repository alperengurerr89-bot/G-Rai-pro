import streamlit as st
import google.generativeai as genai

# API Anahtarı
genai.configure(api_key="AIzaSyCGWNPpkXbkyN5DY9NaqoNV07C6iqSYRUc") 

# MODEL İSMİNİ BÖYLE DENE (Flash-latest her zaman çalışır)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("🛡️ GÜRai - Yapay Zeka")

soru = st.text_input("GÜRai'ye bir şey sor:")

if soru:
    try:
        response = model.generate_content(soru)
        st.write(response.text)
    except Exception as e:
        # Eğer hala hata verirse model ismini 'gemini-pro' olarak değiştirmeyi dene
        st.error(f"Hala bir sorun var: {e}")
