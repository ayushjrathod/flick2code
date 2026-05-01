# flick2code

`flick2code` is a CLI coding agent powered by the Google Gemini API.  
It accepts a prompt, decides which local tools to call, executes them, and returns a final response.

## Features

- Tool-based agent loop with bounded iterations (`MAX_ITERATIONS`)
- Built-in file operations (`get_files_info`, `get_file_content`, `write_file`)
- Python execution support (`run_python_file`)
- Optional verbose token usage output (`--verbose`)

## Requirements

- Python 3.14+
- A Gemini API key

## Setup

1. Install dependencies:
   - `uv sync`
2. Create a `.env` file with:
   - `GOOGLE_API_KEY=your_api_key`
   - `MODEL_ID=gemini-3-flash-preview`

## Usage

Run with a prompt:

`python main.py "list files in this project"`

Run with verbose usage metadata:

`python main.py "read calculator/main.py" --verbose`

## Project Layout

- `main.py` - CLI entrypoint and agent execution loop
- `agent/` - tool declarations, handlers, and system prompt
- `functions/` - concrete function implementations used by the agent
- `config/config.py` - runtime constants (for example `MAX_ITERATIONS`)
- `calculator/` - sample target code used during local testing
