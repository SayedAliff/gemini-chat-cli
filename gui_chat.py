import argparse
import os
import json
import tkinter as tk # BASE Tkinter for ScrolledText, constants
from tkinter import scrolledtext, messagebox, filedialog
from threading import Thread
from google import genai
from PIL import Image, ImageTk 
from datetime import date 
import requests 
import io 
import customtkinter as ctk # CustomTkinter (Main GUI Library)

# --- CONFIGURATION CONSTANTS ---
MODEL_FLASH = 'gemini-2.5-flash'
MODEL_PRO = 'gemini-2.5-pro'
FONT_SIZE = 14 
LOGO_FILENAME = "gemini_logo.png" 
LOG_FILE_NAME = "chat_history.json" 
COPYRIGHT_TEXT = f"Gemini Chat GUI | © {date.today().year} Sayed Aliff" 
MODEL_ROLE_NAME = "Terminal Guru" # FINAL ROLE NAME

class GeminiChat:
    
    def __init__(self, master):
        self.master = master
        master.title("Gemini Chat GUI - CustomTkinter")
        
        # --- STATE VARIABLES ---
        self.generated_image_data = None 
        self.tk_image = None
        
        # --- INITIALIZATION LOGIC ---
        self.args = self._get_args() 
        
        if not os.getenv("GEMINI_API_KEY"):
            messagebox.showerror("Setup Error", "GEMINI_API_KEY environment variable not found. Please set your API key.")
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
        self.logo_label = ctk.CTkLabel(master, text="") 
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="n") 
        
        # 2. Output/Display Area (Scrolled Text) - Row 1 (Text view)
        # FIX APPLIED HERE: Setting background (bg) to a reliable dark gray color (#242424)
        self.chat_display = scrolledtext.ScrolledText(
            master, 
            wrap=tk.WORD, 
            state='disabled', 
            font=('Arial', FONT_SIZE), 
            bg='#242424', 
            fg='#DCE4EE' 
        )
        self.chat_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 3. Image Display Area (NEW FRAME) - Row 1 (Image view, initially hidden)
        self.image_frame = ctk.CTkFrame(master, border_width=2) 
        self.image_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.image_frame.grid_remove() 
        
        self.image_label = ctk.CTkLabel(self.image_frame, text="") 
        self.image_label.pack(side=tk.TOP, padx=5, pady=5)
        
        self.download_button = ctk.CTkButton( 
            self.image_frame, 
            text="ছবিটি ডাউনলোড করুন", 
            command=self.download_image, 
            font=('Arial', 12)
        )
        self.download_button.pack(side=tk.BOTTOM, pady=10)
        
        # 4. Input Field (Row 2)
        self.input_field = ctk.CTkEntry(master, font=('Arial', FONT_SIZE)) 
        self.input_field.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_field.bind("<Return>", lambda event: self.send_message_thread())
        
        # 5. Send Button (Row 2)
        self.send_button = ctk.CTkButton(master, text="Send", command=self.send_message_thread, font=('Arial', 12)) 
        self.send_button.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky="e")
        
        # 6. Footer/Copyright Label (Row 3)
        self.footer_label = ctk.CTkLabel(master, text=COPYRIGHT_TEXT, font=('Arial', 8), text_color='gray') 
        self.footer_label.grid(row=3, column=0, columnspan=2, pady=(0, 5), sticky="s") 
        
        self._set_window_icon()
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

    def _set_window_icon(self):
        try:
            icon_image = Image.open(LOGO_FILENAME)
            photo = ImageTk.PhotoImage(icon_image)
            self.master.iconphoto(False, photo)
        except Exception:
            pass

    def _load_logo(self):
        try:
            logo_path = LOGO_FILENAME
            img = Image.open(logo_path)
            self.logo_photo = ctk.CTkImage(light_image=img, dark_image=img, size=(64, 64))
            self.logo_label.configure(image=self.logo_photo, text="")
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

    def append_to_chat(self, role, text, is_image_request=False):
        self.chat_display.config(state='normal')
        
        tag = role.lower()
        if role == "System": tag = "system_info"
        if is_image_request: tag = "image_info"
        
        display_role = MODEL_ROLE_NAME if role == "Gemini" else role

        self.chat_display.insert(tk.END, f"{display_role}: ", (tag,))
        self.chat_display.insert(tk.END, text + "\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        if not is_image_request:
            self.image_frame.grid_remove()
            self.chat_display.grid() 


    def send_message_thread(self):
        prompt = self.input_field.get()
        if not prompt.strip(): return

        self.input_field.delete(0, tk.END)
        self.send_button.configure(state=tk.DISABLED) 
        self.append_to_chat("User", prompt)
        
        thread = Thread(target=self.process_api_call, args=(prompt,))
        thread.start()

    # --- IMAGE HANDLING LOGIC (Final Calibration) ---

    def _display_image_from_url(self, url, prompt_text):
        """Downloads the image from URL and displays it in the dedicated frame (called from background thread)."""
        
        def download_and_display_task():
            """Function to run safely in a dedicated thread."""
            try:
                response = requests.get(url, timeout=60) 
                response.raise_for_status() 
                
                image_data = io.BytesIO(response.content)
                img = Image.open(image_data)
                self.generated_image_data = img 
                
                width, height = img.size
                if width > 500:
                    new_width = 500
                    new_height = int(new_width * height / width)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_width, new_height))
                self.tk_image = ctk_image
                
                self.master.after(0, self._show_image_on_gui, prompt_text)

            except requests.exceptions.RequestException as e:
                print(f"DEBUG ERROR: Failed to download image (Network): {e}") 
                self.master.after(0, self.append_to_chat, "Error", f"ছবি ডাউনলোড করা যায়নি। নেটওয়ার্ক চেক করুন। Error: {e}")
                self.master.after(0, self.chat_display.grid) 
            except Exception as e:
                print(f"DEBUG ERROR: Error displaying image (PIL/TK): {e}")
                self.master.after(0, self.append_to_chat, "Error", f"ছবি প্রদর্শনে ত্রুটি। ফাইল ফরম্যাট/সাইজ সমস্যা। Error: {e}")
                self.master.after(0, self.chat_display.grid) 
            finally:
                 self.master.after(0, lambda: self.send_button.configure(state=tk.NORMAL))

        Thread(target=download_and_display_task).start()

    def _show_image_on_gui(self, prompt_text):
        """Helper function to perform actual GUI update on the main thread."""
        try:
            self.chat_display.grid_remove() 
            self.image_label.configure(image=self.tk_image, text="") 
            self.image_frame.grid()       
            
            self.append_to_chat("Gemini", f"Image generated: {prompt_text}", is_image_request=True)
            self.send_button.configure(state=tk.NORMAL)
            self.input_field.focus_set()
        except Exception as e:
            print(f"DEBUG ERROR: Error in _show_image_on_gui: {e}")
            self.append_to_chat("Error", f"GUI আপডেট করতে সমস্যা হয়েছে: {e}")
            self.chat_display.grid() 
            self.send_button.configure(state=tk.NORMAL)


    def download_image(self):
        if self.generated_image_data:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile="generated_image.png"
            )
            if file_path:
                try:
                    self.generated_image_data.save(file_path)
                    messagebox.showinfo("Success", f"Image successfully saved to:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("Warning", "No image currently available to download.")


    def process_api_call(self, prompt):
        
        self.history.append({"role": "user", "parts": [{"text": prompt}]})

        try:
            self.master.after(0, self._prepare_stream)
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.history,
                config=self.config
            )
            
            if response.function_calls and response.function_calls[0].name == 'image_generation:generate_images':
                
                prompt_text = response.function_calls[0].args['prompts'][0]

                image_result = self.client.models.generate_images(
                    model='imagen-3.0-generate-002', 
                    prompt=prompt_text,
                    config={'number_of_images': 1}
                )

                if image_result.generated_images:
                    image_url = image_result.generated_images[0].uri
                    self._display_image_from_url(image_url, prompt_text)
                    self.history.append({"role": "model", "parts": [{"text": f"Generated image for: {prompt_text}"}]})
                else:
                    self.master.after(0, self.append_to_chat, "Gemini", "Sorry, I couldn't generate an image for that prompt.")
                
                return 

            # Handle Standard Text Response (Streaming)
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
            self.master.after(0, lambda: self.send_button.configure(state=tk.NORMAL))


    # --- STREAMING/GUI METHODS ---

    def _prepare_stream(self):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{MODEL_ROLE_NAME}: ", ('model',))
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
        
        self.send_button.configure(state=tk.NORMAL)
        self.input_field.focus_set()


def main():
    # Set dark mode and use CTk root window
    ctk.set_appearance_mode("Dark") 
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk() # Use CTk for the root window
    app = GeminiChat(root)
    
    # Configure colors/tags
    app.chat_display.tag_config('user', foreground='#6495ED')
    app.chat_display.tag_config('model', foreground='#3CB371')
    app.chat_display.tag_config('system_info', foreground='#A9A9A9', font=('Arial', FONT_SIZE-2, 'italic'))
    app.chat_display.tag_config('error', foreground='#DC143C', font=('Arial', FONT_SIZE, 'bold'))
    app.chat_display.tag_config('image_info', foreground='#9400D3', font=('Arial', FONT_SIZE, 'bold')) 
    
    def on_closing():
        app._save_history()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()