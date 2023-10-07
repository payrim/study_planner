from utils.clearterminal import clear_terminal
from utils import colors
import os
import json

# File paths
FOCUS_FILE = os.path.join(colors.notes_file, 'focuses.json')

# Define the list to store focuses
focuses = []

# Function to load focuses from the JSON file
def load_focuses():
    global focuses
    if os.path.exists(FOCUS_FILE):
        with open(FOCUS_FILE, "r") as f:
            focuses = json.load(f)

# Function to save focuses to the JSON file
def save_focuses():
    with open(FOCUS_FILE, "w") as f:
        json.dump(focuses, f, indent=4)

# Function to add a focus
def add_focus():
    clear_terminal()
    name = input(f"\n{colors.YELLOW}Enter the name of the focus: {colors.RESET}")
    focus = {
        'name': name,
        'status': 'inactive'
    }
    focuses.append(focus)
    clear_terminal()
    print(f"Focus '{name}' added successfully.")
    save_focuses()  # Save focuses after adding

# Function to select a focus
def select_focus():
    if not focuses:
        clear_terminal()
        print("No focuses available. Please add a focus first.")
        return
    clear_terminal()
    print(f"\n\n{colors.YELLOW}Available Focuses\n{colors.line*9}{colors.RESET}")
    for i, focus in enumerate(focuses):
        if focus['status'] == 'active':
            x_mark = 'x'
        elif focus['status'] == 'inactive':
            x_mark = ' '
        print(f"{i + 1}. {focus['name']} [{x_mark}]")

    choice = input(f"\n{colors.WWITE}Enter the index of the focus to select: {colors.RESET}")
    try:
        index = int(choice) - 1
        if 0 <= index < len(focuses):
            for i, focus in enumerate(focuses):
                focus['status'] = 'active' if i == index else 'inactive'
            clear_terminal()
            print(f"{colors.BLUE}Focus '{focuses[index]['name']}' is now active.{colors.RESET}")
            save_focuses()  # Save focuses after selecting
        else:
            clear_terminal()
            print("Invalid index. Please select a valid index.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")

# Function to show the selected focus
def show_focus():
    load_focuses()
    load_styles()
    active_focus = next((focus for focus in focuses if focus['status'] == 'active'), None)
    selected_style = next((style for style in styles if style['status'] == 'active'), None)

    focus_message = (
        f"{colors.space*7}{colors.WWITE}Focus: {colors.CYAN}[{active_focus['name']}]{colors.RESET}"
        if active_focus else
        f"{colors.RED}{colors.space*7}No focus is currently active. Please select one.{colors.RESET}"
    )

    style_message = (
        f"{colors.WWITE}Style: {colors.WPURPLE}[{selected_style['name']}]{colors.RESET}"
        if selected_style else
        f"{colors.RED}{colors.space * 7}No style is currently selected. Please select one.{colors.RESET}"
    )

    print(focus_message+" - "+style_message)

def remove_focus():
    clear_terminal()
    if not focuses:
        print("No focuses available to remove.")
        return
    
    print(f"\n\n{colors.YELLOW}Available Focuses to Remove\n{colors.line*9}{colors.RESET}")
    for i, focus in enumerate(focuses):
        print(f"{i + 1}. {focus['name']} ({focus['status']})")

    choice = input(f"\n{colors.WWITE}Enter the index of the focus to remove: {colors.RESET}")
    try:
        index = int(choice) - 1
        if 0 <= index < len(focuses):
            removed_focus = focuses.pop(index)
            clear_terminal()
            print(f"{colors.BLUE}Focus '{removed_focus['name']}' removed successfully.{colors.RESET}")
            save_focuses()  # Save focuses after removing
        else:
            clear_terminal()
            print("Invalid index. Please select a valid index.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")

def reset_focus():
    for focus in focuses:
        focus['status'] = 'inactive'
    clear_terminal()
    print(f"All focuses are now inactive.")
    save_focuses() 


STYLES_FILE = os.path.join(colors.notes_file, 'styles.json')
styles = []

def load_styles():
    global styles
    if os.path.exists(STYLES_FILE):
        with open(STYLES_FILE, "r") as f:
            styles = json.load(f)

def save_styles():
    with open(STYLES_FILE, "w") as f:
        json.dump(styles, f, indent=4)

def add_style():
    clear_terminal()
    name = input(f"\n{colors.YELLOW}Enter the name of the style: {colors.RESET}")
    style = {
        'name': name,
        'status': 'inactive', 
    }
    styles.append(style)
    clear_terminal()
    print(f"Style '{name}' added successfully.")
    save_styles() 

def select_style():
    load_styles()
    if not styles:
        clear_terminal()
        print("No styles available. Please add a style first.")
        return
    clear_terminal()
    print(f"\n\n{colors.YELLOW}Available Styles\n{colors.line*9}{colors.RESET}")
    for i, style in enumerate(styles):
        status = style['status']
        x_mark = 'x' if status == 'active' else ' '
        print(f"{i + 1}. {style['name']} [{x_mark}]")

    choice = input(f"\n{colors.WWITE}Enter the index of the style to select: {colors.RESET}")
    try:
        index = int(choice) - 1
        if 0 <= index < len(styles):
            selected_style = styles[index]
            for style in styles:
                style['status'] = 'inactive'
            selected_style['status'] = 'active'
            clear_terminal()
            print(f"{colors.BLUE}Style '{selected_style['name']}' is now active.{colors.RESET}")
            save_styles() 
        else:
            clear_terminal()
            print("Invalid index. Please select a valid index.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")

def remove_style():
    clear_terminal()
    if not styles:
        print("No styles available to remove.")
        return
    
    print(f"\n\n{colors.YELLOW}Available Styles to Remove\n{colors.line*9}{colors.RESET}")
    for i, style in enumerate(styles):
        print(f"{i + 1}. {style['name']} ({style['status']})")

    choice = input(f"\n{colors.WWITE}Enter the index of the style to remove: {colors.RESET}")
    try:
        index = int(choice) - 1
        if 0 <= index < len(styles):
            removed_style = styles.pop(index)
            clear_terminal()
            print(f"{colors.BLUE}Style '{removed_style['name']}' removed successfully.{colors.RESET}")
            save_styles()  # Save styles after removing
        else:
            clear_terminal()
            print("Invalid index. Please select a valid index.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")


# Main program loop
def main():
    load_focuses()
    load_styles()
    while True:
        print(f"\n\n{colors.YELLOW}||Focus Manager||{colors.RESET}\n")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add a Focus{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Select a Focus{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show Focus{colors.RESET}")
        print(f"{colors.CYAN}e.{colors.RESET} {colors.YELLOW}Reset Focus{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove Focus{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}quit{colors.RESET}")

        choice = input("\nEnter your choice(double for styles): ").lower()
        
        if choice == 'a':
            add_focus()
            save_focuses()
        elif choice == 'aa':
            add_style()
            save_styles()
        elif choice == 't':
            select_focus()
            select_style()
            save_styles()
            save_focuses()
        elif choice == 'e':
            reset_focus()
        elif choice == 's':
            clear_terminal()
            print("\n\n")
            show_focus()
        elif choice == 'r':
            remove_focus()
            save_focuses()
        elif choice == 'rr':
            remove_style()
            save_styles()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == "__main__":
    main()
