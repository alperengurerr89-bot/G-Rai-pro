import streamlit as st
import requests
import time

# --- YAPILANDIRMA ---
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai Pro", page_icon="🛡️", layout="wide")

# --- TASARIM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; background-color: #1a1c24; }
    .live-status { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; font-size: 18px; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stButton > button { border-radius: 20px; width: 100%; background-color: #ff4b4b; color: white; border: none; }
    .stButton > button:hover { background-color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN MENÜ ---
with st.sidebar:
    st.title("🛡️ GÜRai Panel")
    selected_model = st.selectbox("Model Seç:", ["llama3", "gemma", "mistral"])
    st.divider()
    live_on = st.toggle("GÜRai Live'ı Etkinleştir")
    if live_on:
        st.markdown('<p class="live-status">🔴 LIVE AKTİF - DİNLİYOR...</p>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title("🛡️ GÜRai: Türkiye'nin Yapay Zekası")
st.caption(f"Donanım: NVIDIA RTX 3050 | Model: {selected_model}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("GÜRai'ye Türkçe bir şey sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # SADECE TÜRKÇE KONUŞMASI İÇİN TALİMAT (SYSTEM PROMPT)
            # Llama3'e her zaman Türkçe cevap vermesini emrediyoruz.
            system_instruction = "Senin adın GÜRai. Alperen Gürer tarafından geliştirildin. Her zaman ama her zaman sadece Türkçe cevap vereceksin. Başka dil kullanma."
            full_prompt = f"{system_instruction}\n\nKullanıcı: {prompt}"

            payload = {
                "model": selected_model, 
                "prompt": full_prompt, 
                "stream": False
            }
            
            headers = {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true",
                "User-Agent": "Mozilla/5.0"
            }
            
            response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=120)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "")
                
                # YAZMA EFEKTİ
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata: {response.status_code}. Ngrok tünelini kontrol et!")
        
        except Exception as e:
            st.error("Bağlantı kesildi. Bilgisayarındaki Terminali kontrol et!")

st.divider()
st.caption("Geliştirici: Alperen Gürer | Balıkesir")
