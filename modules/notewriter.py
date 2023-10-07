import os
import json
from utils.clearterminal import clear_terminal
from utils import colors



task_JSON = os.path.join(colors.notes_file, "tasks.json")
TRACKER_DB = os.path.join(colors.notes_file, 'trackerprime.json')
FTRACKER_DB = os.path.join(colors.notes_file, 'freetracker.json')
XTRACKER_DB = os.path.join(colors.notes_file, 'exercisetracker.json')
NOTES_JSON = os.path.join(colors.notes_file, 'notewriter.json')

def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\mainnote.md"
        editor = 'notepad'
    else:
        notes_file = os.path.join(colors.notes_file,"mainnote.md")
        editor = 'nvim'
    os.system(f"{editor} {notes_file}")


# Function to load JSON data from a file or return an empty list if the file doesn't exist
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []

# Function to save JSON data to a file
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# Function to add a note to a specific item
def add_note(data, item_name, note):
    for item in data:
        if isinstance(item, dict) and item.get("name") == item_name:
            item["note"] = note
            return True

    # If the item doesn't exist, create a new item
    new_item = {"name": item_name, "note": note}
    data.append(new_item)
    return True

# Function to remove a note from a specific item
def remove_note():
    notes_data = load_data(NOTES_JSON)
    items_with_notes = list_items_with_notes(notes_data)

    if not items_with_notes:
        print("No items with notes found.")
        return

    print("\n\nItems with notes:")
    for index, item in enumerate(items_with_notes, start=1):
        item_name = item.get('name', 'Unknown')
        print(f"{index}. {colors.YELLOW}{item_name}{colors.RESET}")

    try:
        choice = int(input("\nEnter the index of the item to remove the note (0 to cancel): "))
        if 1 <= choice <= len(items_with_notes):
            selected_item = items_with_notes[choice - 1]
            item_name = selected_item.get('name', 'Unknown')
            for item in notes_data:
                if isinstance(item, dict) and item.get("name") == item_name:
                    if "note" in item:
                        del item["note"]
                        save_notes_data(notes_data)  # Save the updated notes data
                        print(f"Note removed successfully for {colors.YELLOW}{item_name}{colors.RESET}.")
                        return
            print(f"Item '{colors.YELLOW}{item_name}{colors.RESET}' not found in notes_data.")
        elif choice == 0:
            return
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function to list items with notes
def list_items_with_notes(data):
    items_with_notes = []
    for item in data:
        if isinstance(item, dict) and "note" in item:
            items_with_notes.append(item)
    return items_with_notes

# Function to display a note with indexes
def show_note():
    notes_data = load_data(NOTES_JSON)
    items_with_notes = list_items_with_notes(notes_data)

    if not items_with_notes:
        print("No items with notes found.")
        return

    print("\n\nItems with notes:")
    for index, item in enumerate(items_with_notes, start=1):
        item_name = item.get('name', 'Unknown')
        print(f"{index}. {colors.YELLOW}{item_name}{colors.RESET}")

    try:
        choice = int(input("\nEnter the index of the item to show the note (0 to cancel): "))
        if 1 <= choice <= len(items_with_notes):
            item = items_with_notes[choice - 1]
            item_name = item.get('name', 'Unknown')
            note = item.get('note', 'No note found')
            clear_terminal()
            print(f"\n\n{colors.space*5}{colors.BLUE}Note for {colors.RESET}{colors.CYAN}{item_name}\n{colors.space*5}{colors.line*15}\n{colors.RESET}{colors.space*5}{note}")
            input(f"\n\n{colors.YELLOW}{colors.space*5}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == 0:
            return
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def list_options(options):
    notes_data = load_data(NOTES_JSON)
    items_with_notes = list_items_with_notes(notes_data)

    for index, (option_name, _) in enumerate(options, start=1):
        has_note_indicator = " [has note]" if option_name in [item.get("name") for item in items_with_notes] else ""
        print(f"{index}. {colors.GREEN}{option_name}{colors.RESET}{has_note_indicator}")

def add_notes():
    notes_data = load_data(NOTES_JSON)

    print("\n\nSelect an option to add a note:")
    list_options(options)
    try:
        option_choice = int(input("\nEnter a number (q to exit): "))
        clear_terminal()
        print("\n\n")
        if 1 <= option_choice <= len(options):
            option_name, option_path = options[option_choice - 1]
            option_data = load_data(option_path)

            # Display the list of items in the selected option
            print("available notes:")
            list_options([(item.get("name", "Unknown"), item) for item in option_data])

            item_choice = int(input("\n\nSelect an item to add a note (q to cancel): "))
            if 1 <= item_choice <= len(option_data):
                item = option_data[item_choice - 1]
                if isinstance(item, dict):
                    item_name = item.get("name", "")
                    print(f"Adding a note for item: {colors.GREEN}{item_name}{colors.RESET}")
                    note = input("Enter your note: ")
                    if add_note(notes_data, item_name, note):
                        save_notes_data(notes_data)
                        clear_terminal()
                        print(f"Note added successfully for {colors.GREEN}{item_name}{colors.RESET}.")
                    else:
                        print(f"Item '{colors.GREEN}{item_name}{colors.RESET}' not found in notes_data.")
                else:
                    print("Invalid item choice.")
            else:
                print("Invalid item choice.")
    except ValueError:
        clear_terminal()

# Function to save the notes data to the JSON file
def save_notes_data(data):
    save_data(NOTES_JSON, data)

# Function to load reminders
def load_reminders():
    load_data(REMINDER_FILE)
    print("Reminders loaded successfully.")

# Define options
options = [
    ("Tasks", task_JSON),
    ("Trackers", TRACKER_DB),
    ("Free Trackers", FTRACKER_DB),
    ("Exercise Trackers", XTRACKER_DB)
]

# Main program
def main():
    clear_terminal()
    while True:
        print(f"\n\n{colors.YELLOW}||Notes for tracker and tasks||\n{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add a Note{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove a Note{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show a Note{colors.RESET}")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Main note{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter your choice: ")

        if choice == 'a':
            clear_terminal()
            add_notes()
        elif choice == 'r':
            clear_terminal()
            remove_note()
        elif choice == 's':
            clear_terminal()
            show_note()
        elif choice == "n":
            clear_terminal()
            edit_notes()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == "__main__":
    main()
