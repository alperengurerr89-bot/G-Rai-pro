import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIza...") # Buraya anahtarını yaz
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ GÜRai - Yapay Zeka Asistanı")
soru = st.text_input("GÜRai'ye bir şey sor:")

if soru:
    response = model.generate_content(soru)
    st.write(response.text)
