# 💬 Gemini Chat GUI Application

This project has evolved into a complete **Graphical User Interface (GUI)** application built with Python and Tkinter. It provides a full desktop chat client for interacting with Google's Gemini models.

**Features Included:**
* **GUI Interface:** Clean Tkinter window with streaming output.
* **Conversational History:** Remembers past turns within the session.
* **Customization:** Uses command-line arguments to set the model, temperature, and system role.
* **Professional Code:** Structured using OOP (Object-Oriented Programming).

---

## 📋 Prerequisites

* **Python 3.9+**
* An active internet connection
* **A Google Gemini API Key:** Required for all API calls. Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/SayedAliff/gemini-chat-cli.git](https://github.com/SayedAliff/gemini-chat-cli.git)
    cd gemini-chat-cli
    ```
    *(Note: The main application file is now gui_chat.py)*

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install all required dependencies:**
    This installs the Gemini SDK (`google-genai`), `Pillow` (for the logo/GUI), and `argparse`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key (Mandatory):**
    You must set your Gemini API key as an environment variable (`GEMINI_API_KEY`).

    * **macOS/Linux (.zshrc):**
        ```bash
        export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
        ```
        Then, restart your terminal or run `source ~/.zshrc`.
    * **Windows (Command Prompt):**
        ```bash
        setx GEMINI_API_KEY "YOUR_ACTUAL_API_KEY_HERE"
        ```
        Then, restart your terminal.

---

## 🚀 How to Run the GUI Application

Run the main GUI script directly from your activated terminal.

### Default Run (Fast Model):

```bash
python gui_chat.py