import os
from utils import colors

if not os.path.exists(colors.notes_file):
    try:
        # Create the directory
        os.makedirs(colors.notes_file)
        print(f"Directory '{colors.notes_file}' created successfully.")
    except OSError as e:
        print(f"Error: {e}")
else:
    print(f"Directory '{colors.notes_file}' already exists.")

os.chdir(colors.notes_file)