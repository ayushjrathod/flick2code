from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def get_function_handlers(working_directory):
    return {
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
