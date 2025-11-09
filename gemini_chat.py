import argparse
from google import genai
import os

# Define constants
MODEL_FLASH = 'gemini-2.5-flash'
MODEL_PRO = 'gemini-2.5-pro'

class GeminiChat:
    """
    A customizable command-line chat application built with OOP principles.
    Manages client initialization, history, and user interaction.
    """

    def __init__(self):
        """Initializes the chat client and configuration based on command-line arguments."""
        
        # Parse command line arguments
        self.args = self._get_args()
        
        # Normalize model name
        if self.args.model.lower() == 'flash':
            self.model_name = MODEL_FLASH
        elif self.args.model.lower() == 'pro':
            self.model_name = MODEL_PRO
        else:
            self.model_name = self.args.model
            
        # Initialize configuration and history
        self.config = {"temperature": self.args.temperature}
        
        # Initialize history with system instruction if provided
        self.history = []
        if self.args.system:
            self.config["system_instruction"] = self.args.system
        
        try:
            # Initialize the client (Encapsulation)
            self.client = genai.Client()
            self._print_initial_info()
            
        except Exception as e:
            print("Error: Could not initialize Gemini Client.")
            print("Please check your GEMINI_API_KEY environment variable and network connection.")
            exit()

    def _get_args(self):
        """Private method to set up and parse command-line arguments using argparse."""
        parser = argparse.ArgumentParser(
            description="A customizable command-line chat interface for the Gemini API."
        )
        parser.add_argument(
            '-m', '--model',
            type=str,
            default=MODEL_FLASH,
            choices=[MODEL_FLASH, MODEL_PRO, 'flash', 'pro'],
            help=f"Specify the Gemini model to use. Default: {MODEL_FLASH}"
        )
        parser.add_argument(
            '-t', '--temperature',
            type=float,
            default=0.5,
            help="Set the creativity/randomness of the response (0.0 to 1.0). Default is 0.5."
        )
        parser.add_argument(
            '-s', '--system',
            type=str,
            default=None,
            help="Set a system instruction to define the model's personality or role."
        )
        return parser.parse_args()

    def _print_initial_info(self):
        """Prints initial application setup details."""
        print("\n--- Gemini Chat CLI Initialized (OOP) ---")
        print(f"Model: {self.model_name}")
        print(f"Temperature: {self.args.temperature}")
        if self.args.system:
            print(f"System Role: {self.args.system[:50]}...")
        print("---")
        print("Enter your prompt (type 'exit' or 'quit' to stop).")

    def start_chat(self):
        """Main loop to handle user input and stream responses."""
        while True:
            prompt = input('>>> ')

            if prompt.lower() in ['exit', 'quit']:
                print("\nExiting...")
                print("To deactivate your virtual environment, run: deactivate")
                break

            # Add the new user message to the history
            self.history.append({"role": "user", "parts": [{"text": prompt}]})

            try:
                print("-" * 30)
                print("Gemini:", end=" ", flush=True) 
                
                # Call the streaming method with full history and configuration
                response_stream = self.client.models.generate_content_stream(
                    model=self.model_name,
                    contents=self.history,
                    config=self.config
                )
                
                full_response = ""
                # Stream and capture the full response
                for chunk in response_stream:
                    if chunk.text:
                        print(chunk.text, end="", flush=True)
                        full_response += chunk.text
                
                print("\n" + "-" * 30)
                
                # Add the model's full response to the history
                self.history.append({"role": "model", "parts": [{"text": full_response}]})
                
            except Exception as e:
                print(f"\nAn error occurred during generation: {e}")
                print("If using 'pro', ensure you have access to that model.")

if __name__ == "__main__":
    # Create an instance of the class and start the chat
    chat_app = GeminiChat()
    chat_app.start_chat()