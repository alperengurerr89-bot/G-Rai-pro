import streamlit as st
import requests
import json
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
        st.markdown('<p class="live-status">🔴 LIVE AKTİF</p>', unsafe_allow_html=True)
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title("🛡️ GÜRai Pro")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("GÜRai ile konuş..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            payload = {
                "model": selected_model, 
                "prompt": prompt,
                "stream": False 
            }
            
            # --- 403 HATASINI ÇÖZEN KRİTİK KISIM ---
            headers = {
                "ngrok-skip-browser-warning": "69420" # Bu satır Ngrok engelini kaldırır!
            }
            
            response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=90)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "")
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01)
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata Kodu: {response.status_code}. Ngrok terminalini kontrol et!")
        
        except Exception as e:
            st.error("Bağlantı koptu. Terminal 1 açık mı?")

st.caption("Donanım: RTX 3050 | Geliştirici: Alperen Gürer")
