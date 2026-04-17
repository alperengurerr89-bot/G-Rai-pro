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
    .stChatMessage { border-radius: 15px; border: 1px solid #333; background-color: #1a1c24; }
    .stButton > button { border-radius: 20px; width: 100%; background-color: #ff4b4b; color: white; }
    .model-info { color: #00ffcc; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN MENÜ (5 MODLU PANEL) ---
with st.sidebar:
    st.title("🛡️ GÜRai Panel")
    
    # 5 Farklı Model Seçeneği
    selected_model = st.selectbox(
        "Zeka Modeli Seç:", 
        ["llama3", "gemma", "mistral", "phi3", "codellama"]
    )
    
    # Model Açıklamaları
    model_desc = {
        "llama3": "En dengeli ve akıllı genel sohbet robotu.",
        "gemma": "Google destekli, mantık ve bilgi deposu.",
        "mistral": "Hızlı, çevik ve yaratıcı cevaplar.",
        "phi3": "Microsoft'un minik dev devrimcisi, en hızlısı.",
        "codellama": "Unity, Python ve yazılım konusunda uzman."
    }
    st.markdown(f"<p class='model-info'>{model_desc[selected_model]}</p>", unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("🎙️ Sesli Sohbet")
    text_input = speech_to_text(
        language='tr',
        start_prompt="🎤 Dinlemeyi Başlat",
        stop_prompt="⏹️ Gönder",
        just_once=True,
        key='speech'
    )
    
    st.divider()
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title(f"🛡️ GÜRai: {selected_model.upper()} Modu")
st.caption("RTX 3050 & 32GB RAM Gücüyle Yayında")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş Kontrolü
prompt = None
if text_input:
    prompt = text_input
elif manual_input := st.chat_input("GÜRai'ye bir şey sor..."):
    prompt = manual_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Karakter ve Hafıza Ayarı
            system_context = (
                f"Senin adın GÜRai. Alperen Gürer tarafından geliştirildin. "
                f"Şu an {selected_model} zekasını kullanıyorsun. Sadece Türkçe konuş."
            )
            
            payload = {
                "model": selected_model, 
                "prompt": f"{system_context}\n\nKullanıcı: {prompt}", 
                "stream": False,
                "options": {"temperature": 0.5}
            }
            
            headers = {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true"
            }
            
            response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=150)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "").strip()
                
                # Yazma Efekti
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
                
                # Sesli Okutma (JavaScript)
                st.components.v1.html(f"""
                    <script>window.parent.speak("{full_response.replace('"', "'").replace('\\', '')}");</script>
                """, height=0)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata {response.status_code}: '{selected_model}' yüklü olmayabilir.")
        except:
            st.error("Bağlantı kesildi! Terminali kontrol et.")

st.divider()
st.caption("Geliştirici: Alperen Gürer | Balıkesir")
