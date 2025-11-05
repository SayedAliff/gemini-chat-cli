💬 Gemini Chat CLI

This is a command-line interface (CLI) for chatting with Google's Gemini models directly from your terminal. The project is in active development. Stay tuned for future features!
📋 Prerequisites

Before you begin, ensure you have the following:
Python 3.9+
An active internet connection
A Google Gemini API Key: You can get one from Google AI Studio.
🛠️ Installation & Setup (macOS & Windows)

Follow these steps exactly as run in your terminal:
Clone the repository:
git clone [https://github.com/YOUR_USERNAME/gemini-chat-cli.git](https://github.com/YOUR_USERNAME/gemini-chat-cli.git)

(Replace YOUR_USERNAME with your GitHub username)
Navigate to the project directory:
cd gemini-chat-cli

Create the virtual environment:
python3 -m venv venv

(On some Windows systems, you might need to use python instead of python3)
Activate the virtual environment:
macOS/Linux:source venv/bin/activate

Windows (Command Prompt):.\venv\Scripts\activate

(Your terminal prompt should now start with (venv))
Install the Google GenAI SDK:
pip install google-genai

(Note: If you get a timeout error, use pip install --timeout 600 google-genai)
Set up your API Key: You must set your Gemini API key as an environment variable.
macOS/Linux: Add the following line to your ~/.zshrc or ~/.bashrc file:
export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"

Then, restart your terminal or run source ~/.zshrc.
Windows (Command Prompt): Run the following command to permanently set the key:
setx GEMINI_API_KEY "YOUR_ACTUAL_API_KEY_HERE"

After running this, you must close and reopen your terminal for the change to take effect.
🚀 How to Use

Once your environment is activated ((venv)) and the API key is set, simply run the script:
python gemini_chat.py
