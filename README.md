# Jarvis Voice Assistant 🎙️🤖

A lightweight Python voice assistant powered by **Groq's fast, free-tier AI**, capable of web navigation, music playback, news updates, and natural conversational responses.

## 🚀 Features
- **Wake-Word Detection:** Listens continuously for the trigger word **"Jarvis"**.
- **AI-Powered Responses:** Utilizes Groq's high-speed API for natural language understanding and conversation.
- **Web Navigation:** Dynamically opens websites and search targets (e.g., *"Open YouTube"*).
- **Music Playback:** Plays your favorite tracks using a custom local music library.
- **Live News Updates:** Fetches and reads top global headlines using the NewsAPI.
- **Voice Synthesis:** Clean speech output via `gTTS` (Google Text-to-Speech) and `pygame`.
- **Easy Shutdown:** Safely terminate the program anytime by saying **"Jarvis bye"**.

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/jarvis-voice-assistant.git](https://github.com/YOUR_USERNAME/jarvis-voice-assistant.git)
   cd jarvis-voice-assistant

   pip install -r requirements.txt

   from openai import OpenAI

client = OpenAI(
    base_url="[https://api.groq.com/openai/v1](https://api.groq.com/openai/v1)",
    api_key="YOUR_GROQ_API_KEY"
)

🎯 Detailed Usage Guide
1. Starting the Assistant
Run the main script from your terminal:

Bash
python main.py
Jarvis will initialize, announce his readiness, and start listening for the wake word.

2. The Interaction Workflow
Say the Wake Word: Speak clearly into your microphone: "Jarvis".

Listen for Confirmation: Jarvis will acknowledge you by saying "Ya" and enter active listening mode.

Give Your Command: State what you want Jarvis to do.

3. Example Voice Commands
General AI Conversation / Questions:

"What is quantum computing?"

"Tell me a joke"

Web Navigation:

"Open YouTube"

"Open Wikipedia dot org"

Music Playback:

"Play [song name from your music library]"

Live News:

"Tell me the news"

Closing / Exiting:

"Jarvis bye" or "Jarvis stop"

🛠️ Project Structure
main.py: Core application script handling speech recognition, wake-word detection, and command dispatching.

client.py: Configuration file for the Groq API client connection.

musicLibrary.py: Dictionary mapping song names to their respective links.

.gitignore: Secures sensitive files (client.py, venv/, temp.mp3) from public view.
