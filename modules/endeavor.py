import json
import os
from datetime import datetime, timedelta
from utils.clearterminal import clear_terminal
from utils import colors

data = []

ENDV_DB = os.path.join(colors.notes_file, 'endeavors.json')
TODAYDATE_JSON = os.path.join(colors.notes_file,  'todaysdate2.json')


def load_data():
    global data
    try:
        with open(ENDV_DB) as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data


def save_data(data):
    with open(ENDV_DB, 'w') as f:
        json.dump(data, f, indent=4)

def show_endeavors():
    clear_terminal()
    data = load_data()
    tags = set(endeavor['tag'] for endeavor in data)
    print("\n\n")
    for tag in sorted(tags):
        print(f"{colors.YELLOW}#{tag}{colors.RESET}")  # Print the tag in colors.GREEN
        endeavors = sorted(filter(lambda e: e['tag'] == tag, data), key=lambda e: e['priority'], reverse=True)  # Sort by priority (highest to lowest)

        total_priority = sum(endeavor['priority'] for endeavor in endeavors)
        total_ticks = sum(endeavor['done'] * endeavor['priority'] for endeavor in endeavors)
        progress_bar_length = 20
        progress_bar_fill = '█'
        progress_bar_fill_count = int((total_ticks / total_priority) * progress_bar_length)

        for i, endeavor in enumerate(endeavors):
            done = '[x]' if endeavor['done'] else '[ ]'
            print(f" {str(endeavor['index']).rjust(2)}) {done.ljust(3)} {colors.YELLOW}{endeavor['name']}{colors.RESET}")  # Print endeavor names in colors.BLUE

        progress_bar = f"{colors.YELLOW}[{progress_bar_fill * progress_bar_fill_count}{' ' * (progress_bar_length - progress_bar_fill_count)}]{colors.RESET}"  # Print the progress bar in colors.YELLOW
        print(f"{colors.CYAN}Progress: {progress_bar} {int((total_ticks / total_priority) * 100)}%{colors.RESET}\n\n")  # Print progress information in colors.CYAN

    input(f"{colors.YELLOW}Press any key to continue...{colors.RESET}")
    clear_terminal()

def showsmall():
    clear_terminal()
    print()
    data = load_data()
    tags = set(endeavor['tag'] for endeavor in data)

    for tag in sorted(tags):
        print(f"{colors.BLUE}#{tag}{colors.RESET}")  # Print the tag in colors.GREEN
        endeavors = sorted(filter(lambda e: e['tag'] == tag, data), key=lambda e: e['priority'], reverse=True)  # Sort by priority (highest to lowest)

        for i, endeavor in enumerate(endeavors):
            done = '[ ]'
            if endeavor['done'] == False:
                print(f"({endeavor['index']}) {done} {colors.YELLOW}{endeavor['name']}{colors.RESET}")  # Print endeavor names in colors.BLUE


def add_endeavor():
    clear_terminal()
    data = load_data()
    tag = input("Tag of endeavor: ")
    name = input("Name of endeavor: ")
    importance = int(input("Enter Priority number: "))
    index = len(data)
    data.append({'index': index, 'name': name, 'tag': tag, 'priority':importance, 'done': False})
    save_data(data)
    print(f"{colors.GREEN}Endeavor added successfully.{colors.RESET}")  # Print success message in colors.GREEN
    clear_terminal()

def remove_endeavor():
    clear_terminal()
    showsmall()
    data = load_data()
    index = int(input("\nIndex of endeavor to remove: "))
    data = [endeavor for endeavor in data if endeavor['index'] != index]
    for i, endeavor in enumerate(data):
        endeavor['index'] = i
    save_data(data)
    clear_terminal()
    print(f"{colors.GREEN}Endeavor removed successfully.{colors.RESET}\n")  # Print success message in colors.GREEN

def toggle_done():
    clear_terminal()
    showsmall()
    data = load_data()
    index = int(input("\nIndex of endeavor to toggle: "))
    for endeavor in data:
        if endeavor['index'] == index:
            endeavor['done'] = not endeavor['done']
            save_data(data)
            clear_terminal()
            print(f"{colors.GREEN}Endeavor toggled successfully.{colors.RESET}\n")  # Print success message in colors.GREEN
            return
    clear_terminal()
    print(f"{colors.RED}Endeavor not found.{colors.RESET}\n")  # Print error message in red


def check_date():
    data = load_data()
    if not os.path.isfile(TODAYDATE_JSON):
        with open(TODAYDATE_JSON, "w") as f:
            json.dump(datetime.now().strftime("%d-%m-%Y"), f)

    with open(TODAYDATE_JSON, "r") as f:
        saved_date = json.load(f)
    today_date = datetime.now().strftime("%d-%m-%Y")
    if saved_date != today_date:
        for endeavor in data:
            endeavor["done"] = False
        save_data(data)
        print("All endeavors have been marked as undone due to a new day.\n")
    else:
        pass

def save_today_date():
    today_date = datetime.now().strftime("%d-%m-%Y")
    with open(TODAYDATE_JSON, "w") as f:
        json.dump(today_date, f)

def show_by_priority():
    clear_terminal()
    data = load_data()
    priorities = set(endeavor['priority'] for endeavor in data)  # Get unique priorities from the data

    if not priorities:
        print("\nNo endeavors available.")
        input(f"{colors.YELLOW}Press any key to continue...{colors.RESET}")
        clear_terminal()
        return

    print(f"\n{colors.YELLOW}Available Priorities: {', '.join(map(str, sorted(priorities, reverse=True)))}{colors.RESET}")
    selected_priority = int(input(f"\nEnter the priority to show endeavors for: "))

    filtered_endeavors = [endeavor for endeavor in data if endeavor['priority'] == selected_priority]
    if not filtered_endeavors:
        print(f"No endeavors found for priority {selected_priority}.")
    else:
        clear_terminal()
        print(f"\n\n{colors.GREEN}Endeavors with Priority {selected_priority}:{colors.RESET}\n")
        for i, endeavor in enumerate(filtered_endeavors):
            if endeavor['done'] == False:
                done = '[ ]'
                print(f"({endeavor['index']}) {done} {colors.WPURPLE}{endeavor['name']}{colors.RESET}")

    input(f"\n\n{colors.YELLOW}Press any key to continue...{colors.RESET}")
    clear_terminal()

def print_menu():
    print(f"\n{colors.YELLOW}||Daily Challenges||{colors.RESET}\n")
    print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add endeavor{colors.RESET}")
    print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Toggle endeavor as done{colors.RESET}")
    print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show endeavors{colors.RESET}")
    print(f"{colors.CYAN}p.{colors.RESET} {colors.YELLOW}Show by Priority{colors.RESET}")
    print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove endeavor{colors.RESET}")
    print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")



def main():
    clear_terminal()
    while True:
        print_menu()
        choice = input("\nEnter choice: ")
        if choice == 's':
            show_endeavors()
        elif choice == 'a':
            add_endeavor()
        elif choice == 'r':
            remove_endeavor()
        elif choice == 't':
            toggle_done()
        elif choice == 'q':
            clear_terminal()
            break
        elif choice =='p':
            show_by_priority()
        else:
            clear_terminal()

if __name__ == '__main__':
    main()