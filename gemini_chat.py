from google import genai
import os

try:
    # 1. Initialize the Client
    client = genai.Client()
    
    # 2. Create a list to manually track and maintain conversational history
    # The 'contents' list will hold all turns of the conversation (user input and Gemini response)
    conversation_history = []
    
    print("Gemini Chat Client Initialized (Streaming Enabled).")
    print("Model: gemini-2.5-flash (Conversational History Active)")
    print("Enter your prompt (type 'exit' or 'quit' to stop).")

except Exception as e:
    print("Error: Could not initialize Gemini Client or Chat.")
    print("Please check your GEMINI_API_KEY environment variable and network connection.")
    exit()

while True:
    prompt = input('>>> ')

    if prompt.lower() in ['exit', 'quit']:
        print("\nExiting...")
        print("To deactivate your virtual environment, run: deactivate")
        break

    # Add the new user message to the history
    conversation_history.append({"role": "user", "parts": [{"text": prompt}]})

    try:
        print("-" * 30)
        print("Gemini:", end=" ", flush=True) 
        
        # Call the streaming method, passing the full history (contents)
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=conversation_history,
            config={"temperature": 0.5}
        )
        
        full_response = ""
        # Print each chunk of the stream as it arrives
        for chunk in response_stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text
        
        print("\n" + "-" * 30)
        
        # CRITICAL: Add the model's full response to the history for the next turn
        conversation_history.append({"role": "model", "parts": [{"text": full_response}]})
        
    except Exception as e:
        print(f"\nAn error occurred during generation: {e}")