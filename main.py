import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_id = os.getenv("MODEL_ID", "gemini-2.5-flash")


def main():
    print("Hello from flick2code!")
    working_directory = os.getcwd()

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Write file contents
    - Run Python files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    function_handlers = {
        "get_files_info": lambda args: get_files_info(
            working_directory, args.get("directory", ".")
        ),
        "get_file_content": lambda args: get_file_content(
            working_directory, args["file_path"]
        ),
        "write_file": lambda args: write_file(
            working_directory, args["file_path"], args["content"]
        ),
        "run_python_file": lambda args: run_python_file(
            working_directory, args["file_path"], args.get("args")
        ),
    }

    response = client.models.generate_content(
        model=model_id,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )
    if verbose_flag:
        print("prompt token count:", response.usage_metadata.prompt_token_count)
        print("response token count:", response.usage_metadata.candidates_token_count)
        print("thoughts token count:", response.usage_metadata.thoughts_token_count)
        print("total token count:", response.usage_metadata.total_token_count)

    if not response.function_calls:
        print("Response:") 
        print(response.text)
        messages.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
    else:        
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
            print("function result:")
            print(result)

if __name__ == "__main__":
    main()
