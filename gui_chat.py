import argparse
import os
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from google import genai
from PIL import Image, ImageTk 
from datetime import date 

# --- CONFIGURATION CONSTANTS ---
MODEL_FLASH = 'gemini-2.5-flash'
MODEL_PRO = 'gemini-2.5-pro'
FONT_SIZE = 14 
LOGO_FILENAME = "gemini_logo.png" 
LOG_FILE_NAME = "chat_history.json" 
COPYRIGHT_TEXT = f"Gemini Chat CLI | © {date.today().year} Sayed Aliff" 

class GeminiChat:
    
    def __init__(self, master):
        self.master = master
        master.title("Gemini Chat GUI")
        
        # --- INITIALIZATION LOGIC ---
        self.args = self._get_args()
        
        if not os.getenv("GEMINI_API_KEY"):
            messagebox.showerror("Setup Error", "GEMINI_API_KEY environment variable not found.")
            master.destroy()
            return

        self.model_name = self.args.model if self.args.model.lower() not in ['flash', 'pro'] else (MODEL_FLASH if self.args.model.lower() == 'flash' else MODEL_PRO)
        self.config = {"temperature": self.args.temperature}
        
        if self.args.system:
            self.config["system_instruction"] = self.args.system
            
        self.history_file = self.args.file if self.args.file else LOG_FILE_NAME
        self.history = self._load_history()
        
        try:
            self.client = genai.Client()
        except Exception:
            messagebox.showerror("API Error", "Could not initialize Gemini Client. Check network/key validity.")
            master.destroy()
            return
            
        # --- GUI SETUP ---
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)

        # 1. Logo Display Area (Row 0)
        self.logo_label = tk.Label(master)
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="n") 
        
        # 2. Output/Display Area (Scrolled Text) - Row 1
        self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', font=('Arial', FONT_SIZE)) 
        self.chat_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 3. Input Field (Row 2)
        self.input_field = tk.Entry(master, font=('Arial', FONT_SIZE)) 
        self.input_field.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_field.bind("<Return>", lambda event: self.send_message_thread())
        
        # 4. Send Button (Row 2)
        self.send_button = tk.Button(master, text="Send", command=self.send_message_thread, font=('Arial', 12))
        self.send_button.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky="e")
        
        # 5. Footer/Copyright Label (Row 3)
        self.footer_label = tk.Label(master, text=COPYRIGHT_TEXT, font=('Arial', 8), fg='gray')
        self.footer_label.grid(row=3, column=0, columnspan=2, pady=(0, 5), sticky="s") 
        
        self._load_logo()
        self.print_initial_info()


    # --- CORE METHODS ---

    def _get_args(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-m', '--model', type=str, default=MODEL_FLASH)
        parser.add_argument('-t', '--temperature', type=float, default=0.5)
        parser.add_argument('-s', '--system', type=str, default=None)
        parser.add_argument('-f', '--file', type=str, default=None)
        
        try:
            return parser.parse_known_args()[0]
        except SystemExit:
            return parser.parse_args([])

    def _load_history(self):
        if self.history_file and os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded {len(data)} previous messages from {self.history_file}")
                    return data
            except json.JSONDecodeError:
                return []
        return []

    def _save_history(self):
        if self.history_file:
            try:
                with open(self.history_file, 'w') as f:
                    if self.history:
                        json.dump(self.history, f, indent=4)
                        print(f"History saved to {self.history_file}")
            except Exception as e:
                print(f"Error saving history: {e}")

    def _load_logo(self):
        try:
            logo_path = LOGO_FILENAME
            img = Image.open(logo_path)
            img_display = img.resize((64, 64), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(img_display) 
            self.logo_label.config(image=self.logo_photo)
            self.master.iconphoto(True, self.logo_photo)
            
        except Exception as e:
            print(f"DEBUG: Logo display failed: {e}") 
            pass 

    def print_initial_info(self):
        info = f"--- Gemini Chat GUI Initialized ---\n"
        info += f"Model: {self.model_name}\n"
        info += f"Temperature: {self.args.temperature}\n"
        if self.args.system:
            info += f"System Role: {self.args.system[:50]}...\n"
        info += f"--------------------------------------\n"
        if self.history:
             info += "Loaded previous session. Continue chatting...\n"
        else:
             info += "Start chatting below...\n"
        
        self.append_to_chat("System", info)

    def append_to_chat(self, role, text):
        self.chat_display.config(state='normal')
        
        tag = role.lower()
        if role == "System": tag = "system_info"

        self.chat_display.insert(tk.END, f"{role}: ", (tag,))
        self.chat_display.insert(tk.END, text + "\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send_message_thread(self):
        prompt = self.input_field.get()
        if not prompt.strip(): return

        self.input_field.delete(0, tk.END)
        self.send_button.config(state=tk.DISABLED)
        self.append_to_chat("User", prompt)
        
        thread = Thread(target=self.process_api_call, args=(prompt,))
        thread.start()


    def process_api_call(self, prompt):
        
        self.history.append({"role": "user", "parts": [{"text": prompt}]})

        try:
            self.master.after(0, self._prepare_stream)

            response_stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=self.history,
                config=self.config
            )
            
            full_response = ""
            for chunk in response_stream:
                if chunk.text:
                    self.master.after(0, self._stream_update, chunk.text)
                    full_response += chunk.text
            
            self.master.after(0, self._finalize_response, full_response)

        except Exception as e:
            error_msg = f"API Error: {e}"
            self.master.after(0, self.append_to_chat, "Error", error_msg)
            self.master.after(0, lambda: self.send_button.config(state=tk.NORMAL))


    def _prepare_stream(self):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Gemini: ", ('model',))
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
    def _stream_update(self, text):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, text)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def _finalize_response(self, full_response):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "\n\n")
        self.chat_display.config(state='disabled')
        
        self.history.append({"role": "model", "parts": [{"text": full_response}]})
        
        self.send_button.config(state=tk.NORMAL)
        self.input_field.focus_set()


def main():
    root = tk.Tk()
    app = GeminiChat(root)
    
    # Configure colors/tags
    app.chat_display.tag_config('user', foreground='#0000FF')
    app.chat_display.tag_config('model', foreground='#008000')
    app.chat_display.tag_config('system_info', foreground='#808080', font=('Arial', FONT_SIZE-2, 'italic'))
    app.chat_display.tag_config('error', foreground='red', font=('Arial', FONT_SIZE, 'bold'))
    
    # Set window close event to save history
    def on_closing():
        app._save_history()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()