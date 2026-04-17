import streamlit as st
import requests
import json
import time

# --- YAPILANDIRMA ---
# Terminal 1'deki linkinle tam uyumlu!
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai Pro", page_icon="🛡️", layout="wide")

# --- GELİŞMİŞ TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; background-color: #1a1c24; }
    .live-status { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; font-size: 18px; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stButton > button { border-radius: 20px; width: 100%; }
    .sidebar-text { font-size: 14px; color: #aaa; }
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
    
    # Geçmiş mesajları sidebar'da listele
    for msg in st.session_state.messages[-5:]:
        icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f"<p class='sidebar-text'>{icon} {msg['content'][:25]}...</p>", unsafe_allow_html=True)

# --- ANA EKRAN ---
st.title("🛡️ GÜRai Pro")
st.caption(f"Aktif Model: {selected_model} | RTX 3050 Gücüyle")

# Eski Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CEVAP SÜRECİ ---
if prompt := st.chat_input("GÜRai ile konuşmaya başla..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay Zeka Cevabı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Ngrok üzerinden evdeki Ollama'ya bağlanıyoruz
            payload = {
                "model": selected_model, 
                "prompt": prompt,
                "stream": False 
            }
            
            response = requests.post(OLLAMA_URL, json=payload, timeout=90)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "")
                
                # HARF HARF YAZMA EFEKTİ
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01) # Yazma hızı
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata: Sunucu {response.status_code} koduyla cevap verdi.")
        
        except Exception as e:
            st.error("Bağlantı Başarısız! Terminal 1 (Ngrok) açık mı?")
            st.info("Eğer Ngrok'u kapatıp açtıysan link değişmiştir, URL'yi güncellemelisin.")

# Alt Bilgi
st.divider()
st.caption("Geliştirici: Alperen Gürer | Balıkesir / Türkiye")
