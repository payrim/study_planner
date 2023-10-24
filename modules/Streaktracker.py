import json
import os
from datetime import datetime, timedelta
from utils.clearterminal import clear_terminal
from utils import colors


STREAKS_FILE = os.path.join(colors.notes_file, 'streaks.json')

# Initialize the list of streaks
streaks = []

# Load streak data from file (if available)
def load_streaks():
    global streaks  
    if os.path.exists(STREAKS_FILE):
        with open(STREAKS_FILE, "r") as f:
            streaks = json.load(f)

# Function to save streak data to a file
def save_streaks():
    global streaks  
    with open(STREAKS_FILE, "w") as f:
        json.dump(streaks, f, indent=4)

# Function to display all streaks
def show_streaks():
    load_streaks()
    if not streaks:
        print("\n\nNo streaks to display.")
    else:
        current_date = datetime.now().date()
        print(f"\n\n{colors.space*7}{colors.CYAN}Daily Challenges\n{colors.space*7}{colors.line2*50}{colors.RESET}")
        for i, streak in enumerate(streaks, start=1):
            if streak['count'] == streak['target']:
                print(f"{colors.space*7} {colors.GREEN} {i}. {colors.YELLOW}{streak['name']} {colors.GREEN}({streak['count']}/{streak['target']}){colors.BLUE} reset in {streak['reset_in']} days {colors.RESET}")
            else:
                last_checked_date = datetime.strptime(streak['last_checked'], "%Y-%m-%d").date()
                reset_duration = timedelta(days=streak['reset_in'])
                days_left = (last_checked_date + reset_duration - current_date).days
                print(f"{colors.space*7} {colors.GREEN} {i}. {colors.YELLOW}{streak['name']} ({colors.BLUE}{streak['count']}{colors.YELLOW}/{streak['target']}){colors.BLUE} reset in {streak['reset_in']} days{colors.RED} ({days_left} left){colors.RESET}")

# Function to add a new streak
def add_streak():
    load_streaks()
    clear_terminal()
    name = input("\nEnter streak name: ")
    target = int(input("Enter the target count for the streak: "))
    reset_in = int(input("Enter the reset duration (in days): "))
    new_streak = {
        'name': name,
        'count': 0,
        'target': target,
        'reset_in': reset_in,
        'last_checked': str(datetime.now().date())
    }
    streaks.append(new_streak)
    save_streaks()
    clear_terminal()
    print(f"{name} streak added successfully.")

# Function to remove a streak
def remove_streak():
    clear_terminal()
    show_streaks()
    choice = input("\nEnter the number of the streak to remove: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(streaks):
            removed_streak = streaks.pop(choice - 1)
            save_streaks()
            clear_terminal()
            print(f"{removed_streak['name']} streak removed.")
        else:
            clear_terminal()
            print("Invalid streak number.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")

# Function to manually reset a streak
def reset_streak():
    clear_terminal()
    show_streaks()
    choice = input("\nEnter the number of the streak to manually reset: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(streaks):
            streak = streaks[choice - 1]
            streak['count'] = 0
            streak['last_checked'] = str(datetime.now().date())
            save_streaks()
            clear_terminal()
            print(f"{streak['name']} streak manually reset.")
        else:
            clear_terminal()
            print("Invalid streak number.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")

def auto_reset_streaks():
    load_streaks()
    current_date = datetime.now().date()
    for streak in streaks:
        if 'last_checked' in streak:  # Check if 'last_checked' key exists
            last_checked_date = datetime.strptime(streak['last_checked'], "%Y-%m-%d").date()
            reset_duration = timedelta(days=streak['reset_in'])
            if current_date - last_checked_date >= reset_duration:
                streak['count'] = 0
                streak['last_checked'] = str(current_date)
    save_streaks()

def check_streak():
    clear_terminal()
    show_streaks()
    choice = input("\nEnter the number of the streak to check: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(streaks):
            streak = streaks[choice - 1]
            last_checked_date = datetime.strptime(streak['last_checked'], "%Y-%m-%d").date()
            current_date = datetime.now().date()
            reset_duration = timedelta(days=streak['reset_in'])
            if current_date - last_checked_date >=reset_duration:
                streak['count'] = 1
                streak['last_checked'] = str(current_date)
                save_streaks()
                print(f"{streak['name']} streak checked ({streak['count']}/{streak['target']}).")
            else:
                if streak['count'] < streak['target']:
                    streak['count'] += 1
                    save_streaks()
                    clear_terminal()
                    print(f"{streak['name']} streak checked ({streak['count']}/{streak['target']}).")
                else:
                    clear_terminal()
                    print(f"\n{colors.BLUE}streak {streak['name']} has already reached the target.{colors.RESET}")
        else:
            clear_terminal()
            print("Invalid streak number.")
    except ValueError:
        clear_terminal()
        print("Invalid input. Enter a number.")

def flush_streaks():
    load_streaks()
    global streaks  # Access the global streaks list
    clear_terminal()
    choice = input("Are You sure?(y/n)")
    if choice.lower == "y":
        streaks = []  # Clear all streaks
        save_streaks()  # Save the empty list to the streak data file
        print("Streak database flushed.")
    else:
        clear_terminal()

# Main program loop
def main():
    auto_reset_streaks()
    clear_terminal()
    while True:
        print(f"\n{colors.YELLOW}||treak Tracker||\n{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET}{colors.YELLOW} Show Streaks{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET}{colors.YELLOW} Add Streak{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET}{colors.YELLOW} Remove Streak{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET}{colors.YELLOW} Check Streak{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET}{colors.YELLOW} Manually reset Streaks{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET}{colors.YELLOW} flush streak database{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET}{colors.YELLOW} Quit{colors.RESET}")
        choice = input("\nEnter your choice: ")

        if choice == 's':
            clear_terminal()
            show_streaks()
            input(f"{colors.WWITE}\nPress any key to continue...")
            clear_terminal()
        elif choice == 'a':
            add_streak()
        elif choice == 'r':
            remove_streak()
        elif choice == 'm':
            reset_streak()
        elif choice == 'c':
            check_streak()
        elif choice == 'f':
            flush_streaks()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()
