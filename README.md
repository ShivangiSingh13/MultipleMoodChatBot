🎭 MoodBot AI — Multi-Personality Chatbot Dashboard


One bot. Seven attitudes. Zero chill.



MoodBot AI is a full-stack AI chatbot dashboard built with Mistral AI, LangChain, and Streamlit. Unlike a regular chatbot, MoodBot lets you switch between 7 completely different personalities — each with its own visual theme, font, color palette, and conversational style. From savage roasts to romantic poetry, the bot adapts its entire look and feel to match its attitude.


✨ Live Demo


Deploy your own → Streamlit Cloud (see deployment section below)




🤖 Personalities

PersonalityVibeTone😈 Savage RoasterBrutally honest. Zero mercy.Dark humor, witty insults🤣 Funny BuddyLife's too short to be serious.Puns, wordplay, chaos🧘 Zen MasterStill waters. Deep wisdom.Calm metaphors, koans🤖 Glitchy AIERR_0R: personality.exe crashed.C0rrupt3d, broken but helpful🎭 Drama QueenEvery message is a performance.Shakespearean overreaction🧊 Cold RealistFacts. No fluff. Zero empathy.Clinically honest, direct💝 Hopeless RomanticEvery word, a love letter.Poetic, tender, lyrical

Each personality has a fully unique UI — different background color, accent color, font family, chat bubble style, and welcome message.


🚀 Features


🎭 7 AI Personalities — each with custom system prompts and dynamic theming
📊 Live Sentiment Meter — tracks the emotional mood of your conversation in real time
🔊 Text-to-Speech — every bot reply can be read aloud using gTTS
🌐 8 Language Support — reply in Hindi, Spanish, French, German, Japanese, Arabic, or Portuguese
🧠 User Memory — enter your name once; the bot remembers and uses it naturally
📁 File Upload (PDF / TXT) — upload a document and ask the bot questions about it
🗂️ Save & Load Chats — save named sessions and reload them anytime
📤 Export to JSON — download your full conversation history
🗑️ Clear Chat — reset any personality's conversation independently



🛠️ Tech Stack

TechnologyPurposeMistral AILLM backbone (mistral-small-2603)LangChainMessage chaining & conversation memoryStreamlitInteractive web dashboard UIgTTSText-to-speech audio generationTextBlobSentiment analysisPyPDF2PDF text extractionpython-dotenvSecure API key management


📁 Project Structure

MoodBot/
├── streamlit.py          # Main app — all personalities, UI, and logic
├── .env                  # Your API keys (never commit this!)
├── .streamlit/
│   └── config.toml       # Streamlit config (disables file watcher warnings)
├── requirements.txt      # All dependencies
└── README.md


⚙️ Setup & Installation

1. Clone the repository

bashgit clone https://github.com/yourusername/moodbot-ai.git
cd moodbot-ai

2. Create a virtual environment

bashpython -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate

3. Install dependencies

bashpip install -r requirements.txt

4. Add your API key

Create a .env file in the root folder:

MISTRAL_API_KEY=your_mistral_api_key_here

Get your free API key at 👉 console.mistral.ai

5. Run the app

bashstreamlit run streamlit.py --server.fileWatcherType none

Open your browser at http://localhost:8501 🎉


📦 requirements.txt

streamlit
langchain
langchain-mistralai
langchain-core
python-dotenv
gtts
textblob
PyPDF2

Install all at once:

bashpip install streamlit langchain langchain-mistralai langchain-core python-dotenv gtts textblob PyPDF2

After installing TextBlob, download its language data:

bashpython -m textblob.download_corpora


🌐 Deploy on Streamlit Cloud (Free)


Push your project to a GitHub repository
Go to 👉 share.streamlit.io
Click New app → select your repo → set main file as streamlit.py
Go to App Settings → Secrets and add:


tomlMISTRAL_API_KEY = "your_mistral_api_key_here"


Click Deploy — your app is live with a public URL! 🚀



🖼️ Screenshots


(Add screenshots of different personality themes here)



😈 Savage Roaster🧘 Zen Master💝 Hopeless Romantic(screenshot)(screenshot)(screenshot)


🔧 Configuration

To suppress torchvision warnings from the Streamlit file watcher, create .streamlit/config.toml:

toml[server]
fileWatcherType = "none"


🗺️ Roadmap


 Login system with per-user saved chats
 Streaming responses (word-by-word output)
 Custom personality creator (build your own!)
 Chat analytics dashboard
 Mobile-optimized layout
 Voice input (speech-to-text)



🤝 Contributing

Pull requests are welcome! If you have a new personality idea or feature suggestion, open an issue and let's discuss.


Fork the repo
Create your branch: git checkout -b feature/cool-personality
Commit your changes: git commit -m "Add cool personality"
Push and open a Pull Request



📄 License

This project is licensed under the MIT License — see LICENSE for details.
