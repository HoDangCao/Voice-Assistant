import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_ollama import ChatOllama
from threading import Thread
import cv2
from PIL import ImageGrab
import time
from datetime import datetime
from selenium import webdriver
import numpy as np
import sounddevice as sd
import re
import ast
from streamlit.runtime.scriptrunner import add_script_run_ctx

prompt4Web = """Your mission is to give the original online URL of websites. Only give the URL. For example:
Query: Youtube
You: https://www.youtube.com/

Query: Messenger
You: https://www.messenger.com/

Query: ChatGPT
You: https://chatgpt.com/

Query: Google Translate
You: https://translate.google.com/

Query: Gmail
You: https://mail.google.com/

Query: Zalo
You: https://chat.zalo.me/

Query: {webName}
You: 
"""

prompt4Song = """Your mission is to ONLY give the music notes in solfa notation and the duration of each note of the given song name. 
If there are multiple songs or multiple version, you just pick the longest one.
You must follow exactly the format as [('note name', duration), ('note name', duration)].
You must ONLY respond to nothing but the music notes and the duration of each note.
For example:
Song name: happy birthday
You: [('G4', 0.5), ('G4', 0.5), ('A4', 0.75), ('G4', 0.5), ('C5', 0.5), ('B4', 0.75),
    ('G4', 0.5), ('G4', 0.5), ('A4', 0.75), ('G4', 0.5), ('D5', 0.5), ('C5', 0.75),
    ('G4', 0.5), ('G4', 0.5), ('E5', 0.75), ('C5', 0.5), ('B4', 0.5), ('A4', 0.75),
    ('F5', 0.5), ('F5', 0.5), ('E5', 0.75), ('C5', 0.5), ('D5', 0.75), ('C5', 1)]

Song name: Baby Shark
You: [('G4', 0.5), ('G4', 0.5), ('G4', 0.5), ('G4', 0.5),
      ('E4', 0.5), ('E4', 0.5), ('E4', 0.5), ('E4', 0.5),
      ('G4', 0.5), ('G4', 0.5), ('G4', 0.5), ('G4', 0.5),
      ('G4', 0.5), ('G4', 0.5), ('G4', 0.5), ('G4', 0.5),
      ('E4', 0.5), ('E4', 0.5), ('E4', 0.5), ('E4', 0.5),
      ('C4', 0.5), ('C4', 0.5), ('C4', 0.5), ('C4', 0.5)]

Song name: Little Fingers
You: [('C4', 0.5), ('D4', 0.5), ('E4', 0.5), ('F4', 0.5), ('G4', 0.5),
      ('G4', 0.5), ('G4', 1),
      ('C4', 0.5), ('D4', 0.5), ('E4', 0.5), ('F4', 0.5), ('G4', 0.5),
      ('G4', 0.5), ('G4', 1),
      ('G4', 0.5), ('A4', 0.5), ('A4', 0.5), ('G4', 0.5),
      ('F4', 0.5), ('F4', 0.5), ('F4', 1),
      ('C4', 0.5), ('D4', 0.5), ('E4', 0.5), ('F4', 0.5), ('G4', 0.5),
      ('G4', 0.5), ('G4', 1)]

Song name: {songName}
You: 
"""
note_frequencies = np.load('note_frequencies.npy', allow_pickle=True).item()
SAMPLE_RATE = 44100

if 'recognizer' not in st.session_state:
    st.session_state['recognizer'] = sr.Recognizer()
if 'llm' not in st.session_state:
    st.session_state['llm'] = ChatOllama(model='mistral', quantization='1bit')
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'out' not in st.session_state:
    st.session_state.out = None

if st.session_state.is_recording:
    st.info('Recording screen..')

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Error in speech synthesis: {e}")

### Tell time
def tell_time():
    message = f"It's {datetime.now().strftime('%H:%M')} now."
    Thread(target=speak, args=(message,), daemon=True).start()
    with st.chat_message('assistant'):
        st.write(message)

### Take screenshot
def take_screenshot():
    screenshot = ImageGrab.grab()
    st.image(screenshot, 'The screenshot')
    timeStamp = time.time_ns()
    screenshot.save(f"screenshot_{timeStamp}.png")
    Thread(target=speak, args=("Screenshot saved",), daemon=True).start()
    with st.chat_message('assistant'):
        st.write(f"Screenshot saved as 'screenshot_{timeStamp}.png'")

### Record screen
def stop_recording():
    """Stops the recording."""
    if not st.session_state.is_recording:
        response = "No recording is in progress!"
        Thread(target=speak, args=(response,), daemon=True).start()
        with st.chat_message('assistant'):
            st.write(response)
        return

    st.session_state.is_recording = False
    time.sleep(1)

    if st.session_state.out:
        st.session_state.out.release()
        st.session_state.out = None
        cv2.destroyAllWindows()

    response = "Screen recording stopped. The screen record saved!"
    Thread(target=speak, args=(response,), daemon=True).start()
    with st.chat_message('assistant'):
        st.write(response)

def start_record(screen_size, output_file, fps=12):
    fourcc = cv2.VideoWriter_fourcc(*"XVID")  # Codec for AVI format
    out = cv2.VideoWriter(output_file, fourcc, fps, screen_size)
    st.session_state.out = out

    while st.session_state.is_recording:
        screenshot = ImageGrab.grab()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

def record_screen():
    if st.session_state.is_recording:
        response = "Recording is already in progress!"
        Thread(target=speak, args=(response,), daemon=True).start()
        with st.chat_message('assistant'):
            st.write(response)
        return
    
    st.session_state.is_recording = True

    screen_size = (ImageGrab.grab().size[0], ImageGrab.grab().size[1])
    output_file = f"screen_recording_{time.time_ns()}.avi"

    thread = Thread(target=start_record, args=(screen_size, output_file), daemon=True)
    add_script_run_ctx(thread)
    thread.start()

    response = "Screen recording started."
    Thread(target=speak, args=(response,), daemon=True).start() 
    with st.chat_message('assistant'):
        st.write(response)

### Answer the question
def respond_question(text):
    response = st.session_state.llm.invoke('Answer the following question concisely: '+ text).content.strip()
    with st.chat_message('assistant'):
        st.write(f"{response}")
    Thread(target=speak, args=(response,), daemon=True).start()

### Open website
def start_browse(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

def open_website(webName):
    url = st.session_state.llm.invoke(prompt4Web.format(webName = webName)).content.strip()
    with st.chat_message('assistant'):
        st.write(f"Opening {url}")
    Thread(target=speak, args=(f"Opening {webName}",), daemon=True).start()
    Thread(target=start_browse, args=(url,), daemon=True).start()

### Play song
def create_note(note_name, duration): # Duration in seconds
    num_sample = int(SAMPLE_RATE * duration)
    amplitude = np.linspace(1, 0, num_sample, endpoint=False)
    frequency = note_frequencies[note_name]
    t = np.linspace(0, duration, num_sample, endpoint=False)
    return np.float32(amplitude * np.sin(2 * np.pi * frequency * t))  # 440 Hz sine wave, # Convert to 16-bit PCM format

def create_song(notes):
    song = np.array([])
    for note in notes:
        song = np.concatenate([song, create_note(note[0], note[1])])
        song = np.concatenate([song, np.zeros(int(SAMPLE_RATE * 0.1))])
    return np.float32(song)

def play_song(songName):
    response = st.session_state.llm.invoke(prompt4Song.format(songName=songName)).content.strip()
    pattern = r"\[\('.*?',\s*[\d.]+\)(?:,\s*\('.*?',\s*[\d.]+\))*\]"
    notes = list(ast.literal_eval(re.findall(pattern, response)[0]))
    with st.chat_message('assistant'):
        st.write(f"Playing {songName}: {notes}")
    
    if not notes:
        st.error("No valid notes found in the response.")
        return
    try:
        song = create_song(notes)
        Thread(target=sd.play, args=(song, SAMPLE_RATE,), daemon=True).start()
    except KeyError as e:
        st.error(f"Note {e} is not in the note frequencies list.")

### UI Layout
st.title("🤖 Chat Assistant")

raw_audio = st.audio_input('Click the microphone to start speaking')

with st.chat_message('assistant'):
    st.write("Listening... Speak now!")

if raw_audio: 
    with sr.AudioFile(raw_audio) as source:
        audio = st.session_state.recognizer.record(source)
        st.session_state.recognizer.adjust_for_ambient_noise(source)
        try:
            # Recognize speech using Google's Web Speech API
            text = st.session_state.recognizer.recognize_google(audio)
            with st.chat_message("user"):
                st.write(f"{text}")

            text = text.lower()
            if text == "what time is it":
                tell_time()
            elif text == 'take screenshot':
                take_screenshot()
            elif text == 'record screen':
                record_screen()
            elif text == 'stop screen recording':
                stop_recording()
            elif text.startswith('open website '):
                webName = text.split(' ', 1)[1]
                open_website(webName)
            elif text.startswith('play song '):
                songName = text.split(' ', 1)[1]
                play_song(songName)
            else:
                respond_question(text)

        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
