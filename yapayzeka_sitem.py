import streamlit as st
import requests
import json
import time

# --- YAPILANDIRMA ---
# Ngrok linkin (Link değişirse burayı güncellemeyi unutma!)
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev -> http://localhost:11434/api/generate"

st.set_page_config(page_title="GÜRai Pro - Live", page_icon="🛡️", layout="wide")

# --- GELİŞMİŞ TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; background-color: #1a1c24; }
    .live-status { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; font-size: 18px; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stButton > button { border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SOHBET HAFIZASI KURULUMU ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN MENÜ (MODLAR VE GEÇMİŞ) ---
with st.sidebar:
    st.title("🛡️ GÜRai Panel")
    
    # 1. AI MODU SEÇİMİ
    st.subheader("🛠️ AI Modu")
    selected_model = st.selectbox("Model Seç:", ["Llama 3 (Varsayılan)", "Gemma 2", "Mistral"])
    
    st.divider()

    # 2. LIVE MODU
    st.subheader("🎙️ Live Modu")
    live_on = st.toggle("GÜRai Live'ı Etkinleştir")
    if live_on:
        st.markdown('<p class="live-status">🔴 LIVE AKTİF - DİNLİYOR...</p>', unsafe_allow_html=True)
        st.caption("Live modunda cevaplar gerçek zamanlı olarak akıtılır.")
    
    st.divider()

    # 3. SOHBET KAYDI (HISTORY)
    st.subheader("📜 Sohbet Geçmişi")
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    if len(st.session_state.messages) > 0:
        for i, msg in enumerate(st.session_state.messages[-3:]): # Son 3 mesajı önizleme yap
            label = "Siz" if msg["role"] == "user" else "GÜRai"
            st.caption(f"**{label}:** {msg['content'][:30]}...")

# --- ANA EKRAN ---
st.title("🛡️ GÜRai Pro")
st.write(f"Şu an aktif model: `{selected_model}`")

# Mesajları Ekranda Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CEVAP SÜRECİ ---
if prompt := st.chat_input("GÜRai ile konuşmaya başla..."):
    # Kullanıcı mesajını göster ve kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay Zeka Cevabı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            payload = {
                "model": "llama3", # Bilgisayarında yüklü olan model adı
                "prompt": prompt,
                "stream": False 
            }
            
            # Ngrok üzerinden evdeki PC'ye bağlantı
            response = requests.post(OLLAMA_URL, json=payload, timeout=90)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "")
                
                # YAZMA EFEKTİ (Harf harf akıtma)
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01) # Akış hızını ayarlar
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Terminal cevap vermedi. Ngrok tünelini kontrol et!")
        
        except Exception as e:
            st.error("Bağlantı Başarısız! Bilgisayarın açık mı?")
