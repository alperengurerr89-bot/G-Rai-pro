import streamlit as st
import requests
import time
from streamlit_mic_recorder import speech_to_text

# --- YAPILANDIRMA ---
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai Pro", page_icon="🛡️", layout="wide")

# --- SES VE TASARIM ---
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
    .stButton > button { border-radius: 20px; width: 100%; background-color: #ff4b4b; color: white; border: none; }
    .model-card { padding: 10px; border: 1px solid #444; border-radius: 10px; background-color: #262730; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ANA EKRAN KATEGORİ SEÇİMİ ---
st.title("🛡️ GÜRai: Yapay Zeka Merkezi")

with st.container():
    st.markdown('<div class="model-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        # Modelleri artık buradan direkt seçebilirsin
        selected_model = st.selectbox(
            "🧠 Zeka Kategorisi Seç:", 
            ["llama3", "gemma", "mistral", "phi3", "codellama"],
            index=0
        )
    with col2:
        model_info = {
            "llama3": "🛡️ **Genel Sohbet:** En akıllı ve dengeli mod.",
            "gemma": "💡 **Mantık & Bilgi:** Google'ın derin bilgi havuzu.",
            "mistral": "⚡ **Hızlı Cevap:** Seri ve yaratıcı konuşma.",
            "phi3": "🚀 **Ultra Hafif:** Microsoft'un en hızlı zekası.",
            "codellama": "💻 **Yazılım Uzmanı:** Unity ve Python kod desteği."
        }
        st.info(model_info[selected_model])
    st.markdown('</div>', unsafe_allow_html=True)

# --- YAN MENÜ (SADECE SES VE TEMİZLİK) ---
with st.sidebar:
    st.header("🎙️ Kontrol Paneli")
    text_input = speech_to_text(language='tr', start_prompt="🎤 Sesli Sor", stop_prompt="⏹️ Gönder", just_once=True, key='speech')
    st.divider()
    if st.button("🗑️ Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- SOHBET AKIŞI ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = None
if text_input:
    prompt = text_input
elif manual_input := st.chat_input("GÜRai'ye mesaj gönder..."):
    prompt = manual_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Sistem komutu: Her zaman Türkçe ve seçilen modele göre karakter analizi
            payload = {
                "model": selected_model, 
                "prompt": f"Senin adın GÜRai. Alperen tarafından yapıldın. Sadece Türkçe konuş.\nKullanıcı: {prompt}", 
                "stream": False,
                "options": {"temperature": 0.5}
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
                
                # Sesli okutma
                st.components.v1.html(f"""<script>window.parent.speak("{full_response.replace('"', "'").replace('\\', '')}");</script>""", height=0)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata: {selected_model} aktif değil. Terminalde 'ollama pull {selected_model}' yapmalısın.")
        except:
            st.error("Terminal bağlantısı koptu!")

st.caption(f"Aktif Zeka: {selected_model.upper()} | Alperen Gürer")
