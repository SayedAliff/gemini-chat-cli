🤖 Terminal Guru Chat GUI Application
This project is a sophisticated, fully object-oriented (OOP) chat client that utilizes the CustomTkinter library for a modern, dark-themed Graphical User Interface (GUI). It features the Terminal Guru persona and advanced multimedia capabilities.

✨ Key Features
Modern GUI: Clean, dark-themed interface built with CustomTkinter for superior aesthetics and stability.

Image Generation: Directly request and view generated images within the chat window, with a dedicated Download button.

Streaming & Context: Supports live response streaming and maintains full conversation history.

Customization: Fully configurable via command-line arguments (Model, Temperature, System Role).

Professional Code: Structured using OOP in Python.

📋 Prerequisites
Python 3.9+

An active internet connection

A Google Gemini API Key (Required for all API calls). Get one from Google AI Studio.

The requirements.txt file (included in the repository).

🛠️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/SayedAliff/gemini-chat-cli.git
cd gemini-chat-cli
Create and activate a virtual environment:

Bash
python3 -m venv venv
source venv/bin/activate
Install all required dependencies: This command installs google-genai, customtkinter, Pillow, and requests.

Bash
pip install -r requirements.txt
Set up your API Key (Mandatory): The application reads the GEMINI_API_KEY environment variable.

macOS/Linux (.zshrc):

Bash
export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
Then, restart your terminal or run source ~/.zshrc.

Windows (Command Prompt):

Bash
setx GEMINI_API_KEY "YOUR_ACTUAL_API_KEY_HERE"
Then, restart your terminal.

🚀 How to Run the Application
Run the main GUI script directly from your activated terminal.

Default Run (Fast Model, Terminal Guru Persona):

Bash
python gui_chat.py
Advanced Run (Customizing Model and Creativity):

Use flags to override the default settings:

Flag	Example	Description
-m / --model	-m pro	Uses the advanced gemini-2.5-pro model.
-t / --temperature	-t 0.9	Sets creativity higher (0.0 to 1.0).
-s / --system	-s 'Answer like a formal professor.'	Gives the AI a specific, customized role.
Image Generation Test: Ask for an image: Generate a photorealistic image of a futuristic skyline.