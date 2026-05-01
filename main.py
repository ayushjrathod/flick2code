import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from agent.available_functions import get_available_functions
from agent.function_handlers import get_function_handlers
from agent.prompt import SYSTEM_PROMPT
from config.config import MAX_ITERATIONS

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_id = os.getenv("MODEL_ID", "gemini-2.5-flash")


def main():
    print("Hello from flick2code! \n")
    working_directory = os.getcwd()
    # working_directory = "/home/ayra/Documents/code/flick2code/calculator"
    
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)
    prompt = sys.argv[1]
    
    verbose_flag = False
    if (len(sys.argv) > 2 and sys.argv[2] == "--verbose"):
        verbose_flag = True
        
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    available_functions = get_available_functions()
    function_handlers = get_function_handlers(working_directory)
    max_iterations = MAX_ITERATIONS
    completed_with_final_response = False
    last_usage_metadata = None
    iteration_count = 0
    while not completed_with_final_response and iteration_count < max_iterations:
        iteration_count += 1
        response = client.models.generate_content(
            model=model_id,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[available_functions]
            )
        )
        last_usage_metadata = getattr(response, "usage_metadata", None)

        if response.function_calls:
            if response.candidates and response.candidates[0].content:
                messages.append(response.candidates[0].content)
            else:
                messages.append(types.Content(
                    role="model",
                    parts=[types.Part(function_call=function_call) for function_call in response.function_calls]
                ))
            for function_call in response.function_calls:
                print("function call", function_call)
                handler = function_handlers.get(function_call.name)
                if not handler:
                    print(f"Unknown function: {function_call.name}")
                    continue
                try:
                    result = handler(function_call.args or {})
                except Exception as e:
                    result = f"Error executing {function_call.name}: {e}"
                messages.append(types.Content(
                    role="user", # role: "tool" is not supported by google sdk, using "user" role for function responses
                    parts=[types.Part(
                        function_response=types.FunctionResponse(
                            name=function_call.name,
                            id=function_call.id,
                            response={"output": result},
                        )
                    )]
                ))

        if not response.function_calls:
            print("Response:") 
            print(response.text)
            messages.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
            completed_with_final_response = True

    if not completed_with_final_response:
        print(f"No final response generated after {max_iterations} iterations.")
        print("Last response:")
        print(response.text)

    if verbose_flag:
        print("\n--- usage metadata (last response) ---")
        if last_usage_metadata:
            print("prompt token count:", last_usage_metadata.prompt_token_count)
            print("response token count:", last_usage_metadata.candidates_token_count)
            print("thoughts token count:", last_usage_metadata.thoughts_token_count)
            print("total token count:", last_usage_metadata.total_token_count)
        else:
            print("usage metadata is unavailable for this response.")

if __name__ == "__main__":
    main()
