import streamlit as st
import requests
import time
from streamlit_mic_recorder import speech_to_text

# --- YAPILANDIRMA ---
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai Pro - Sesli Mod", page_icon="🎙️", layout="wide")

# --- TASARIM VE SES MOTORU (JavaScript) ---
# Bu kısım yapay zekanın cevabını sesli okumasını sağlar
st.markdown("""
    <script>
    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'tr-TR';
        utterance.rate = 1.0;
        window.speechSynthesis.speak(utterance);
    }
    </script>
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; background-color: #1a1c24; }
    .live-status { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; }
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
    
    st.subheader("🎙️ Live Sesli Kontrol")
    # Mikrofon Butonu
    text_input = speech_to_text(
        language='tr',
        start_prompt="🎤 Dinlemeyi Başlat",
        stop_prompt="⏹️ Durdur ve Gönder",
        just_once=False,
        key='speech'
    )
    
    st.divider()
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title("🛡️ GÜRai: Sesli Canlı Mod")
st.caption(f"Donanım: RTX 3050 | Durum: Dinlemede...")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- SESLİ VEYA YAZILI GİRİŞ İŞLEME ---
prompt = None
if text_input: # Eğer sesle konuştuysan
    prompt = text_input
elif manual_input := st.chat_input("Veya buraya yazın..."): # Eğer yazdıysan
    prompt = manual_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            system_instruction = "Adın GÜRai. Alperen Gürer tarafından yapıldın. Sadece Türkçe ve kısa, öz cevaplar ver."
            full_prompt = f"{system_instruction}\n\nKullanıcı: {prompt}"

            payload = {"model": selected_model, "prompt": full_prompt, "stream": False}
            headers = {"ngrok-skip-browser-warning": "true", "Content-Type": "application/json"}
            
            response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=120)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "")
                
                # Yazma Efekti
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
                
                # --- SESLİ CEVAP VERME ---
                # Tarayıcıya JavaScript ile sesli okuma emri gönderiyoruz
                st.components.v1.html(f"""
                    <script>
                    window.parent.speak("{full_response.replace('"', "'")}");
                    </script>
                """, height=0)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Bağlantı Hatası!")
        
        except Exception as e:
            st.error("Bağlantı koptu!")

st.caption("Geliştirici: Alperen Gürer")
