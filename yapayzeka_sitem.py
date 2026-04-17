import streamlit as st
import requests
import json
import os
import pyttsx3
import base64
from PIL import Image
import io
from datetime import datetime

# --- GÜRai PROFESYONEL YAPILANDIRMA ---
st.set_page_config(page_title="GÜRai PRO | Yerel Sistem", page_icon="🛡️", layout="wide")

# Klasör Kontrolü (Sohbet Kayıtları İçin)
HISTORY_DIR = "gurai_history"
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

# Ses Motoru Fonksiyonu
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# Görsel İşleme Fonksiyonu
def process_image(image_file):
    img = Image.open(image_file)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- SOL PANEL: ARŞİV, SIRALAMA VE MODLAR ---
with st.sidebar:
    st.title("🛡️ GÜRai Kontrol")
    
    # 1. MOD SEÇİCİ
    st.subheader("🤖 Sistem Modu")
    selected_model = st.selectbox("Model Seçin:", ["llama3", "llava"], help="llava: Resim görme modu")
    
    # 2. SES AYARI
    st.subheader("🔊 Sesli Yanıt")
    voice_on = st.checkbox("GÜRai Konuşsun", value=False)
    
    st.divider()
    
    # 3. SOHBET ARŞİVİ VE SIRALAMA
    st.subheader("📂 Geçmiş Sohbetler")
    history_files = os.listdir(HISTORY_DIR)
    history_files.sort(reverse=True) # En yeni sohbet en üstte (Sıralama Özelliği)
    
    selected_chat_file = st.selectbox("Arşivi Yükle:", ["Yeni Oturum"] + history_files)
    
    if st.button("🔴 Tüm Geçmişi Temizle"):
        for f in history_files:
            os.remove(os.path.join(HISTORY_DIR, f))
        st.rerun()

# --- SOHBET YÜKLEME / BAŞLATMA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if selected_chat_file != "Yeni Oturum":
    with open(os.path.join(HISTORY_DIR, selected_chat_file), "r", encoding="utf-8") as f:
        st.session_state.messages = json.load(f)
elif selected_chat_file == "Yeni Oturum" and st.session_state.get('last_loaded') != "Yeni Oturum":
    st.session_state.messages = []
    st.session_state.last_loaded = "Yeni Oturum"

# --- ANA EKRAN ---
st.title("🛡️ GÜRai Üst Düzey YZ")
st.caption(f"Aktif Mod: {selected_model} | Sızdırmazlık Katmanı Aktif")

# Mesajları Ekranda Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Görsel Yükleme (Sadece llava modunda aktif olur)
uploaded_file = None
if selected_model == "llava":
    uploaded_file = st.file_uploader("Bir görsel yükleyin...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Analiz edilecek görsel", width=250)

# --- SORGÜ VE YANIT DÖNGÜSÜ ---
if prompt := st.chat_input("GÜRai'ye talimat iletin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("GÜRai düşünülüyor..."):
                payload = {
                    "model": selected_model,
                    "prompt": f"Sen GÜRai'sin. Türkiye'nin en iyi yerel yapay zekasısın. Ciddi cevap ver: {prompt}",
                    "stream": False
                }
                
                if uploaded_file and selected_model == "llava":
                    payload["images"] = [process_image(uploaded_file)]

                response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
                cevap = response.json()["response"]
                
                st.markdown(cevap)
                st.session_state.messages.append({"role": "assistant", "content": cevap})
                
                # Otomatik Kayıt (Arşivleme)
                chat_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                save_path = os.path.join(HISTORY_DIR, f"chat_{chat_id}.json")
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)
                
                if voice_on:
                    speak(cevap)
                    
        except Exception as e:
            st.error(f"Sistem Hatası: {e}. Ollama'nın çalıştığından emin olun.")

st.divider()
st.caption("GÜRai PRO | RTX 3050 & Ollama Yerel Gücüyle")