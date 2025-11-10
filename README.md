# Gemini Chat CLI (Terminal Guru)

A polished, object-oriented Python chat client with a sleek dark GUI built using **CustomTkinter**. Includes integrated image generation, streaming responses, conversation history, and CLI configuration. Perfect as a template to publish on GitHub.

---

## ✨ Key Features

* **Modern Dark GUI** — Built with CustomTkinter for a clean, stable, desktop look.
* **Terminal Guru Persona** — A friendly, configurable system role that shapes assistant behavior.
* **Image Generation** — Request generated images directly in the chat and download them with a single click.
* **Streaming & Context** — Live response streaming and full conversation history are preserved.
* **Configurable** — Command-line flags to set model, temperature, and system role.
* **OOP Design** — Clear, modular object-oriented Python code for maintainability and reuse.

---

## 🧩 Prerequisites

* Python **3.9+**
* Active internet connection
* A **Google Gemini API Key** (from Google AI Studio)
* `requirements.txt` included in the repo

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/SayedAliff/gemini-chat-cli.git
cd gemini-chat-cli

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Set the GEMINI API key

macOS / Linux (e.g. `~/.zshrc`):

```bash
export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
# then: source ~/.zshrc
```

Windows (Command Prompt):

```cmd
setx GEMINI_API_KEY "YOUR_ACTUAL_API_KEY_HERE"
# then restart terminal
```

---

## 🚀 Running the App

Run the GUI directly from your activated environment:

```bash
# default run (fast model + Terminal Guru persona)
python gui_chat.py
```

### Advanced (custom model / temperature / system role)

```bash
python gui_chat.py --model pro --temperature 0.7 --system "Answer like a formal professor."
```

**Flags**

* `-m`, `--model` — model name (e.g. `fast`, `pro`, `gemini-2.5-pro`)
* `-t`, `--temperature` — creativity / randomness (0.0 — 1.0)
* `-s`, `--system` — system role prompt (string)

---

## 🖼 Image Generation

Ask the assistant to generate an image (e.g. `Generate a photorealistic image of a futuristic skyline`) and view it inline. A **Download** button saves the image locally.

---

## 🧭 Project Structure (example)

```
gemini-chat-cli/
├─ gui_chat.py            # entrypoint (CustomTkinter GUI)
├─ core/                  # OOP modules (client, model, image manager, ui components)
├─ assets/                # icons, default images
├─ requirements.txt
└─ README.md
```

---

## ✅ Notes & Tips

* Ensure `GEMINI_API_KEY` is set before launching the app.
* Use a virtualenv to avoid dependency conflicts.
* For production or packaging, consider PyInstaller or creating a macOS app bundle.

---

## 🙌 Contributing

Contributions, issues, and feature requests are welcome. Please open an issue or create a PR with a clear description of changes.

---

## 📝 License

This project is available under the MIT License. See `LICENSE` for details.

---

## 📌 TODO / Future Improvements

* Add unit tests and CI pipeline
* Export/import conversation history
* Theme switch (light/dark)
* Optional local caching for images and tokens

---

If you want, I can also:

* generate a `setup.py` / `pyproject.toml` template,
* create a simple `gui_chat.py` scaffold with OOP classes, or
* prepare a `LICENSE` file (MIT) and a short CONTRIBUTING.md.

Tell me which of those you'd like and I'll add them as files ready for GitHub.
