import json
from utils.clearterminal import clear_terminal
import os
from utils import colors

ACTIVE = os.path.join(colors.notes_file,  'activet.json')

def set_active_task():
    task = input("\n\nEnter the active task: ")
    data = {"active_task": task}
    with open(ACTIVE, "w") as file:
        json.dump(data, file)
    clear_terminal()
    print(f"Active task '{task}' has been saved.")

def view_active_task():
    try:
        with open(ACTIVE, "r") as file:
            data = json.load(file)
            active_task = data.get("active_task")
            if active_task:
                print(f"{colors.space*7}{colors.WPURPLE}Active task: {active_task}")
            else:
                print(f"{colors.space*7}{colors.WRED}[A? -> e]")
    except FileNotFoundError:
        print(f"{colors.space*7}{colors.WRED}[A? -> e]")

def main():
    while True:
        print("\nMenu:")
        print("s. Set Active Task")
        print("v. View Active Task")
        print("q. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "s":
            clear_terminal()
            set_active_task()
        elif choice == "v":
            clear_terminal()
            view_active_task()
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()