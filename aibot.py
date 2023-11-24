import streamlit as st
import pyttsx3
import speech_recognition as sr
from streamlit_chat import message
from bardapi import Bard
from bardapi import BardCookies

cookie_dict = {
    "__Secure-1PSID": "",
    "__Secure-1PSIDTS": "",
    # Any cookie values you want to pass to the session object.
}

bard = BardCookies(cookie_dict=cookie_dict)

st.title("IVR-AI-BOT")

# Can Add CSS changes for Better UI
changes = '''
<style>
[data-testid="stAppViewContainer"] {
    background-color: rgba(255, 255, 255, 0.05);
    background-size: fit;
}
.st-bx {
    background-color: rgba(255, 255, 255, 0.05);
}

html {
    background: transparent;
}

div.esravye2 > iframe {
    background-color: transparent;
}
</style>
'''

st.markdown(changes, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text-to-Speech (TTS) Function
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Speech-to-Text (STT) Function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.text("Say something...")
        audio = recognizer.listen(source,timeout=3)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "There was an error with the speech recognition service."

def generate_response(prompt):
    response = bard.get_answer(prompt)['content']
    return response

# Toggle for Voice 
voice_interaction = st.checkbox("Enable Voice Interaction")

if voice_interaction:
    # Voice  Section
    if st.button("Start Recording"):
        st.text("Recording... Speak now!")
        user_audio_input = speech_to_text()
        st.text(f"User (Speech): {user_audio_input}")

        response = generate_response(user_audio_input)
        st.session_state.messages.append({"role": "user", "content": f"User (Speech): {user_audio_input}"})
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("user"):
            st.markdown(f"User (Speech): {user_audio_input}")

        with st.chat_message("assistant"):
            st.markdown(response)
        
        text_to_speech(response)
else:
    # Default Text Input Section
    if prompt := st.text_input("Type your message:", key="input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            text_to_speech(response)


