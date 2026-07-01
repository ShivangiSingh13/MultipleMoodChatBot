# 🎭 MoodBot AI — Multi-Personality Chatbot Dashboard

> *One bot. Seven attitudes. Zero chill.*

MoodBot AI is a full-stack AI chatbot dashboard built with **Mistral AI**, **LangChain**, and **Streamlit**. Unlike a regular chatbot, MoodBot lets you switch between 7 completely different personalities — each with its own visual theme, font, color palette, and conversational style. From savage roasts to romantic poetry, the bot adapts its entire look and feel to match its attitude.

---

## ✨ Live Demo

> Deploy your own → [Streamlit Cloud](https://share.streamlit.io) *(see deployment section below)*

---

## 🤖 Personalities

| Personality | Vibe | Tone |
|---|---|---|
| 😈 Savage Roaster | Brutally honest. Zero mercy. | Dark humor, witty insults |
| 🤣 Funny Buddy | Life's too short to be serious. | Puns, wordplay, chaos |
| 🧘 Zen Master | Still waters. Deep wisdom. | Calm metaphors, koans |
| 🤖 Glitchy AI | ERR_0R: personality.exe crashed. | C0rrupt3d, broken but helpful |
| 🎭 Drama Queen | Every message is a performance. | Shakespearean overreaction |
| 🧊 Cold Realist | Facts. No fluff. Zero empathy. | Clinically honest, direct |
| 💝 Hopeless Romantic | Every word, a love letter. | Poetic, tender, lyrical |

Each personality has a **fully unique UI** — different background color, accent color, font family, chat bubble style, and welcome message.

---

## 🚀 Features

- 🎭 **7 AI Personalities** — each with custom system prompts and dynamic theming
- 📊 **Live Sentiment Meter** — tracks the emotional mood of your conversation in real time
- 🔊 **Text-to-Speech** — every bot reply can be read aloud using gTTS
- 🌐 **8 Language Support** — reply in Hindi, Spanish, French, German, Japanese, Arabic, or Portuguese
- 🧠 **User Memory** — enter your name once; the bot remembers and uses it naturally
- 📁 **File Upload (PDF / TXT)** — upload a document and ask the bot questions about it
- 🗂️ **Save & Load Chats** — save named sessions and reload them anytime
- 📤 **Export to JSON** — download your full conversation history
- 🗑️ **Clear Chat** — reset any personality's conversation independently

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Mistral AI](https://mistral.ai) | LLM backbone (`mistral-small-2603`) |
| [LangChain](https://langchain.com) | Message chaining & conversation memory |
| [Streamlit](https://streamlit.io) | Interactive web dashboard UI |
| [gTTS](https://pypi.org/project/gTTS/) | Text-to-speech audio generation |
| [TextBlob](https://textblob.readthedocs.io) | Sentiment analysis |
| [PyPDF2](https://pypi.org/project/PyPDF2/) | PDF text extraction |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Secure API key management |

---

## 📁 Project Structure

```
MoodBot/
├── streamlit.py          # Main app — all personalities, UI, and logic
├── .env                  # Your API keys (never commit this!)
├── .streamlit/
│   └── config.toml       # Streamlit config (disables file watcher warnings)
├── requirements.txt      # All dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/moodbot-ai.git
cd moodbot-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the root folder:

```
MISTRAL_API_KEY=your_mistral_api_key_here
```

Get your free API key at 👉 [console.mistral.ai](https://console.mistral.ai/api-keys)

### 5. Run the app

```bash
streamlit run streamlit.py --server.fileWatcherType none
```

Open your browser at `http://localhost:8501` 🎉

---

## 📦 requirements.txt

```
streamlit
langchain
langchain-mistralai
langchain-core
python-dotenv
gtts
textblob
PyPDF2
```

Install all at once:

```bash
pip install streamlit langchain langchain-mistralai langchain-core python-dotenv gtts textblob PyPDF2
```

After installing TextBlob, download its language data:

```bash
python -m textblob.download_corpora
```

---

## 🌐 Deploy on Streamlit Cloud (Free)

1. Push your project to a **GitHub repository**
2. Go to 👉 [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set main file as `streamlit.py`
4. Go to **App Settings → Secrets** and add:

```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```

5. Click **Deploy** — your app is live with a public URL! 🚀

---

## 🖼️ Screenshots

> *(Add screenshots of different personality themes here)*

| 😈 Savage Roaster | 🧘 Zen Master | 💝 Hopeless Romantic |
|---|---|---|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## 🔧 Configuration

To suppress `torchvision` warnings from the Streamlit file watcher, create `.streamlit/config.toml`:

```toml
[server]
fileWatcherType = "none"
```

---

## 🗺️ Roadmap

- [ ] Login system with per-user saved chats
- [ ] Streaming responses (word-by-word output)
- [ ] Custom personality creator (build your own!)
- [ ] Chat analytics dashboard
- [ ] Mobile-optimized layout
- [ ] Voice input (speech-to-text)

---

## 🤝 Contributing

Pull requests are welcome! If you have a new personality idea or feature suggestion, open an issue and let's discuss.

1. Fork the repo
2. Create your branch: `git checkout -b feature/cool-personality`
3. Commit your changes: `git commit -m "Add cool personality"`
4. Push and open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author

**Shivangi**
- LinkedIn: [your-linkedin-url]
- GitHub: [your-github-url]

---

> *Built with curiosity, caffeine, and the occasional roast from the Savage Roaster. 😈*
