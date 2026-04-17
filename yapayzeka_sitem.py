import streamlit as st
import requests
import time
from streamlit_mic_recorder import speech_to_text

# --- YAPILANDIRMA ---
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai Pro", page_icon="🛡️", layout="wide")

# --- SES MOTORU VE TASARIM ---
st.markdown("""
    <script>
    function speak(text) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'tr-TR';
        utterance.rate = 1.1;
        window.speechSynthesis.speak(utterance);
    }
    </script>
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; background-color: #1a1c24; margin-bottom: 10px; }
    .stButton > button { border-radius: 20px; width: 100%; background-color: #ff4b4b; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN MENÜ (ESKİ USUL - 5 KATEGORİ) ---
with st.sidebar:
    st.title("🛡️ GÜRai Panel")
    
    st.subheader("🧠 Zeka Kategorileri")
    selected_model = st.selectbox(
        "Model Değiştir:", 
        ["llama3", "gemma", "mistral", "phi3", "codellama"]
    )
    
    st.divider()
    
    st.subheader("🎙️ Live Modu")
    text_input = speech_to_text(
        language='tr',
        start_prompt="🎤 Sesli Sor",
        stop_prompt="⏹️ Gönder",
        just_once=True,
        key='speech'
    )
    
    st.divider()
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title("🛡️ GÜRai Pro")
st.caption(f"Aktif Zeka: {selected_model.upper()} | Konum: Balıkesir")

# Eski Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş İşleme
prompt = None
if text_input:
    prompt = text_input
elif manual_input := st.chat_input("GÜRai'ye yazın..."):
    prompt = manual_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Karakter ve Hafıza Sistemi
            system_prompt = f"Senin adın GÜRai. Alperen tarafından yapıldın. Sadece Türkçe konuş. Şu anki zekan: {selected_model}."
            
            payload = {
                "model": selected_model, 
                "prompt": f"{system_prompt}\n\nKullanıcı: {prompt}", 
                "stream": False,
                "options": {"temperature": 0.4} # Doğru cevaplar için 0.4 idealdir
            }
            
            headers = {"ngrok-skip-browser-warning": "true", "Content-Type": "application/json"}
            response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=120)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "").strip()
                
                # Yazma Efekti
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
                
                # Sesli Okuma
                st.components.v1.html(f"""
                    <script>window.parent.speak("{full_response.replace('"', "'").replace('\\', '')}");</script>
                """, height=0)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata: {selected_model} henüz hazır değil (404/403).")
        except:
            st.error("Bağlantı koptu!")

st.divider()
st.caption("Geliştirici: Alperen Gürer")
