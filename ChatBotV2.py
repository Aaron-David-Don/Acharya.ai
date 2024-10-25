import streamlit as st
from openai import OpenAI
import os
import requests
import time

st.set_page_config(
    page_title="Acharya.Ai",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

def generate_audio(text, filename="output15.mp3"):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/sY2peC9GbHX8NCy5enOe"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "enter ur api key"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    
    return os.path.abspath(filename)

def main():
    st.sidebar.title("MENU")
    api_key = "enter ur api key"
    st.sidebar.image("Picture1.png", use_column_width=True)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    st.title("Acharya.Ai")

    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("संस्कृतसम्बद्धं किमपि मां पृच्छतु (Ask me anything related to Sanskrit)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

            audio_file_path = generate_audio(response)
            ##st.write(f"Audio saved at: {audio_file_path}")
            time.sleep(10)
            audio_file = open("output15.mp3", "rb") 
            audio_bytes = audio_file.read() 
            st.audio(audio_bytes, format="audio/mp3")

if __name__ == "__main__":
    main()
