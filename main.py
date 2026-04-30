import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_id = os.getenv("MODEL_ID", "gemini-2.5-flash")


def main():
    print("Hello from flick2code!")

    system_prompt = (
        "You are robot"
    )
    
    if len(sys.argv) < 2:
        print("Please provide a model ID as a command-line argument.")
        sys.exit(1)
    prompt = sys.argv[1]
    
    verbose_flag = False
    if (len(sys.argv) > 2 and sys.argv[2] == "--verbose"):
        verbose_flag = True
        
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model=model_id,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    print(response.text)
    messages.append(types.Content(role="model", parts=[types.Part(text=response.text)]))

    if verbose_flag:
        print("prompt token count:", response.usage_metadata.prompt_token_count)
        print("response token count:", response.usage_metadata.candidates_token_count)
        print("thoughts token count:", response.usage_metadata.thoughts_token_count)
        print("total token count:", response.usage_metadata.total_token_count)

        print(messages)

if __name__ == "__main__":
    main()
