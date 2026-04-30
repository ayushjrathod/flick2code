import os

def get_files_info(working_directory, directory="."):
    print(f"Getting files info for directory: {directory} within working directory: {working_directory}")
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

# print(get_files_info("/home/ayra/Documents/code/flick2code"))

""" Example output:
(flick2code) [ayra@archlinux flick2code]$ uv run functions/get_files_info.py 
Getting files info for directory: . within working directory: /home/ayra/Documents/code/flick2code
- main.py: file_size=1278 bytes, is_dir=False
- README.md: file_size=0 bytes, is_dir=False
- pyproject.toml: file_size=213 bytes, is_dir=False
- .python-version: file_size=5 bytes, is_dir=False
- uv.lock: file_size=65913 bytes, is_dir=False
- .git: file_size=4096 bytes, is_dir=True
- functions: file_size=4096 bytes, is_dir=True
- .venv: file_size=4096 bytes, is_dir=True
- .gitignore: file_size=114 bytes, is_dir=False
- .env: file_size=207 bytes, is_dir=False
- calculator: file_size=4096 bytes, is_dir=True
"""
