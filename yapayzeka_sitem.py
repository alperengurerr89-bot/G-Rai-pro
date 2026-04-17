import streamlit as st
import requests
import json
import time

# --- YAPILANDIRMA ---
# Senin aktif linkin
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai Pro", page_icon="🛡️", layout="wide")

# --- TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; background-color: #1a1c24; }
    .live-status { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; font-size: 18px; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stButton > button { border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN MENÜ ---
with st.sidebar:
    st.title("🛡️ GÜRai Panel")
    
    st.subheader("🛠️ AI Modu")
    selected_model = st.selectbox("Model Seç:", ["llama3", "gemma", "mistral"])
    
    st.divider()

    st.subheader("🎙️ Live Modu")
    live_on = st.toggle("GÜRai Live'ı Etkinleştir")
    if live_on:
        st.markdown('<p class="live-status">🔴 LIVE AKTİF - DİNLİYOR...</p>', unsafe_allow_html=True)
    
    st.divider()

    st.subheader("📜 Geçmiş")
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title("🛡️ GÜRai Pro")
st.caption(f"Donanım: RTX 3050 | Aktif Model: {selected_model}")

# Eski Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CEVAP SÜRECİ ---
if prompt := st.chat_input("GÜRai ile konuşmaya başla..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # --- 403 HATASINI ÇÖZEN KRİTİK AYARLAR ---
            payload = {
                "model": selected_model, 
                "prompt": prompt,
                "stream": False 
            }
            
            # Ngrok'un uyarı sayfasını atlamak için bu başlıklar (headers) şart!
            headers = {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true",
                "User-Agent": "GURai-App"
            }
            
            response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=90)
            
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
                st.error(f"Hata: Sunucu {response.status_code} koduyla kapıyı kapattı. Terminaldeki linki kontrol et!")
        
        except Exception as e:
            st.error("Bağlantı koptu! Ngrok (Terminal 1) kapalı olabilir.")

st.divider()
st.caption("Geliştirici: Alperen Gürer")
