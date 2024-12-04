# 🤖 AI Voice Assistant with Enhanced Features

Welcome to the AI Voice Assistant! This interactive and powerful project offer functionalities like speech recognition, voice synthesis, screen recording, screenshot capturing, music note generation, and much more. 

## 🎬 Demonstration

Turn on sound to hear Human-AI conversation.

https://github.com/user-attachments/assets/0055c03d-6319-4a8c-a24c-8fec9de6907b

---

## 🌟 Features

1. **Speech Recognition & Commands**
   - Recognizes user commands via speech input.
   - Handles tasks like telling the current time, opening websites, answering questions, and more.

2. **Text-to-Speech**
   - Provides auditory responses using **pyttsx3**.

3. **Screen Recording and Screenshot**
   - Capture your screen or take screenshots effortlessly.

4. **Website Navigation**
   - Open websites directly by providing their names.

5. **Music Note Playback**
   - Converts song names into solfa notation and plays the melody.

6. **Conversational Assistant**
   - Built using **LangChain** and **ChatOllama** to answer user queries intelligently.

---

## 🛠️ Technologies Used

- **Streamlit**: For the interactive user interface.
- **SpeechRecognition**: Converts speech into text.
- **pyttsx3**: For voice synthesis.
- **LangChain**: Powers conversational AI capabilities.
- **OpenCV**: Enables screen recording and image manipulation.
- **SoundDevice**: Plays generated sound waves.
- **NumPy**: Used for sound wave generation.
- **Pillow**: Captures screenshots.
- **Selenium**: Automates browser navigation.
- **Mistral LLM**: Provides smart responses for user queries.

---

## 🖥️ Installation Guide

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HoDangCao/Voice-Assistant.git
   cd Voice-Assistant
   ```

2. **Install dependencies**:
   Ensure you have Python 3.9+ and install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Note Frequencies**:
   Place the `note_frequencies.npy` file in the project root.

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

---

## 🎮 Usage

1. Start the application.
2. Interact via speech or text input:
   - Say **"What time is it"** to get the current time.
   - Say **"Take screenshot"** to capture the screen.
   - Say **"Record screen"** to start screen recording.
   - Say **"Stop screen recording"** to stop recording.
   - Say **"Open website [WebsiteName]"** to navigate to a specific website.
   - Say **"Play song [SongName]"** to play a song.
   - Say anything else to ask a question.

3. Check the output directly in the **Streamlit** UI.

---

## 🚀 Key Functions

| Feature                | Functionality                                                    |
|------------------------|-----------------------------------------------------------------|
| **Tell Time**          | Tells the current time using voice synthesis.                   |
| **Screenshot**         | Takes a screenshot and saves it as a PNG file.                  |
| **Screen Recording**   | Records the screen and saves it as an AVI file.                 |
| **Website Navigation** | Opens websites using their official URLs.                       |
| **Play Music**         | Generates and plays songs in solfa notation.                    |
| **Question Answering** | Provides concise answers to user questions.                     |

---

## 📂 Project Structure

```
Voice-Assistant/
├── app.py                # Main application file
├── requirements.txt      # List of dependencies
├── note_frequencies.npy  # Note frequencies for music generation
└── README.md             # Project documentation
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

- Special thanks to the developers of **Streamlit**, **LangChain**, **SoundDevice**, and **Mistral LLM**.
- Inspired by the idea of creating a comprehensive AI assistant.

Enjoy using the **AI Chat Assistant**! 🎉
