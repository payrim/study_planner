import os
import json
import pyperclip
from utils.clearterminal import clear_terminal
from utils import colors

# List to store prompts as dictionaries with 'name' and 'text'
prompts = []
PROMPT_DB = os.path.join(colors.notes_file, 'gptprompt.json')

# Function to load prompts from the JSON file
def load_prompts():
    if os.path.exists(PROMPT_DB):
        with open(PROMPT_DB, 'r') as file:
            global prompts
            prompts = json.load(file)

# Function to save prompts to the JSON file
def save_prompts():
    with open(PROMPT_DB, 'w') as file:
        json.dump(prompts, file)

# Function to add a prompt
def add_prompt():
    prompt_text = input("\nEnter a new prompt text: ")
    prompt_name = input("Enter a name for the prompt: ")
    prompt_dict = {'name': prompt_name, 'text': prompt_text}
    prompts.append(prompt_dict)  # Add the new prompt to the list
    save_prompts()
    clear_terminal()
    print("Prompt added successfully!")

# Function to list prompts
def list_prompts():
    if not prompts:
        clear_terminal()
        print("No prompts available.")
    else:
        clear_terminal()
        print(f"\n{colors.YELLOW}List of Prompts\n{colors.line*14}\n")
        num_columns = 3
        max_name_length = max(len(prompt_dict['name']) for prompt_dict in prompts)

        for i, prompt_dict in enumerate(prompts, start=1):
            column = (i - 1) % num_columns
            padding = " " * (max_name_length - len(prompt_dict['name']) + 1)
            print(f"{colors.CYAN} {i}) {colors.BLUE}{prompt_dict['name']}{padding}", end="\n" if column == num_columns - 1 else "\t")



# Function to remove a prompt
def remove_prompt():
    list_prompts()
    try:
        if prompts:
            index = int(input("\nEnter the index of the prompt to remove: "))
            if 1 <= index <= len(prompts):
                deleted_prompt = prompts.pop(index - 1)  # Adjust index to 0-based
                save_prompts()
                clear_terminal()
                print(f"Removed prompt: {deleted_prompt['name']}")
            else:
                clear_terminal()
                print("Invalid index. No prompt removed.")
        else:
            clear_terminal()
            print("No prompts available to remove.")
    except ValueError:
        clear_terminal()
        print("Invalid input. No prompt removed.")

# Function to copy a selected prompt to the clipboard
def copy_to_clipboard():
    list_prompts()
    try:
        index = int(input("\nEnter the index of the prompt to copy: "))
        if 1 <= index <= len(prompts):
            selected_prompt = prompts[index - 1]['text']  # Adjust index to 0-based and get the text
            pyperclip.copy(selected_prompt)
            clear_terminal()
            print(f"{colors.YELLOW}Prompt copied to clipboard.{colors.RESET}")
        else:
            clear_terminal()
            print("Invalid index. No prompt copied.")
    except ValueError:
        clear_terminal()
        print("Invalid input. No prompt copied.")

# Main program loop
def main():
    load_prompts()
    while True:
        print(f"\n\n{colors.YELLOW}||GPT PROMPTS||{colors.RESET}\n")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add a prompt{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove a prompt{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Copy a prompt to clipboard{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}List prompts{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == 'a':
            add_prompt()
        elif choice == 'l':
            list_prompts()
        elif choice == 'r':
            remove_prompt()
        elif choice == 'c':
            copy_to_clipboard()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()
