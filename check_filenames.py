import os
import re
import sys


def is_snake_case(name):
    return re.match(r'^[a-z0-9_]+$', name) is not None


def check_filenames(directory):
    errors = []
    for root, dirs, files in os.walk(directory):
        # Exclude directories
        if any(d in root for d in ['migrations', '.tox', '__pycache__', '.git', '.venv']):
            continue

        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                name, ext = os.path.splitext(file)
                if not is_snake_case(name):
                    errors.append(os.path.join(root, file))

    return errors


if __name__ == '__main__':
    search_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    error_files = check_filenames(search_dir)

    if error_files:
        for error_file in error_files:
            print(f"Error: Filename '{error_file}' is not in snake_case")
        sys.exit(1)
    else:
        print('All filenames are in snake_case')
        sys.exit(0)
