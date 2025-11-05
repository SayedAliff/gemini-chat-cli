from google import genai
import os

try:
    client = genai.Client()
    print("Gemini Client initialized successfully.")
    print("Enter your prompt (type 'exit' or 'quit' to stop).")
except Exception as e:
    print("Error: Could not initialize Gemini Client.")
    print("Please check if your GEMINI_API_KEY environment variable is set correctly.")
    exit()

while True:
    prompt = input('>>> ')

    if prompt.lower() in ['exit', 'quit']:
        print("Exiting...")
        break

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={"temperature": 0.5}
        )
        print("-" * 30)
        print(response.text)
        print("-" * 30)

    except Exception as e:
        print(f"An error occurred during generation: {e}")
