import streamlit as st
import requests
import json

# --- YAPILANDIRMA (Senin Aktif Ngrok Linkin) ---
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai - Türkiye'nin En İyisi", page_icon="🛡️")

# --- STİLLER (Hatalı kısım düzeltildi) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border-radius: 10px; }
    .stButton > button { background-color: #ff4b4b; color: white; border-radius: 20px; width: 100%; }
    /* Sohbet balonlarını renklendirelim */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ GÜRai: Yapay Zeka")
st.subheader("Türkiye'nin En İyi 2. Yapay Zekası Yayında!")

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Ekranda Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ ---
if prompt := st.chat_input("GÜRai'ye bir şey sor..."):
    # Kullanıcı mesajını ekrana bas ve hafızaya al
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- YAPAY ZEKA CEVABI ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Senin bilgisayarındaki Ollama'ya istek gönderiyoruz
            payload = {
                "model": "llama3", 
                "prompt": prompt,
                "stream": False
            }
            
            # Ngrok tüneli üzerinden evdeki PC'ye bağlanıyoruz
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                full_response = result.get("response", "Cevap alınamadı.")
                message_placeholder.markdown(full_response)
                
                # Asistan cevabını hafızaya al
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata: Sunucu cevap vermedi (Kod: {response.status_code})")
        
        except Exception as e:
            st.error(f"Bağlantı Hatası: Bilgisayarındaki terminalin (Ngrok) açık olduğundan emin ol!")
            st.info("Eğer Ngrok'u kapatıp açtıysan link değişmiş olabilir, kodu güncellemen gerekir.")

# Yan Menü Bilgileri
st.sidebar.title("🤖 Sistem Bilgisi")
st.sidebar.success("Tünel Durumu: Aktif")
st.sidebar.info("Donanım: NVIDIA RTX 3050 (32GB RAM)")
st.sidebar.write("---")
st.sidebar.write("Geliştirici: **Alperen Gürer**")
