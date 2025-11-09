# 💬 Gemini Chat CLI

This is a command-line interface (CLI) for chatting with Google's Gemini models directly from your terminal. **The application now supports conversational history and streaming output.** The project is in active development. Stay tuned for future features!

---

## 📋 Prerequisites

Before you begin, ensure you have the following:

* **Python 3.9+**
* An active internet connection
* **A Google Gemini API Key:** You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
* **The requirements.txt file** (included in the repository)

---

## 🛠️ Installation & Setup (macOS & Windows)

Follow these steps exactly as run in your terminal:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/gemini-chat-cli.git](https://github.com/YOUR_USERNAME/gemini-chat-cli.git)
    ```
    *(Replace `YOUR_USERNAME` with your GitHub username)*

2.  **Navigate to the project directory:**
    ```bash
    cd gemini-chat-cli
    ```

3.  **Create the virtual environment:**
    ```bash
    python3 -m venv venv
    ```

4.  **Activate the virtual environment:**

    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    *(Your terminal prompt should now start with `(venv)`)*

5.  **Install the required dependencies:**
    This command reads the `requirements.txt` file to install the Google GenAI SDK.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If you get a timeout error, use `pip install --timeout 600 -r requirements.txt`)*

6.  **Set up your API Key:**
    You must set your Gemini API key as an environment variable.

    * **macOS/Linux:**
        Add the following line to your `~/.zshrc` or `~/.bashrc` file:
        ```bash
        export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
        ```
        Then, restart your terminal or run `source ~/.zshrc`.

    * **Windows (Command Prompt):**
        Run the following command to **permanently** set the key:
        ```bash
        setx GEMINI_API_KEY "YOUR_ACTUAL_API_KEY_HERE"
        ```
        After running this, you **must close and reopen your terminal** for the change to take effect.

---

## 🚀 How to Use

Once your environment is activated (`(venv)`) and the API key is set, simply run the script. The model will **stream its response** and **remember your previous questions** in the same session.

```bash
python gemini_chat.py
