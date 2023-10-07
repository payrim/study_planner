import json
from datetime import datetime
import os
from utils.clearterminal import clear_terminal
from utils import colors


EXD_DB = os.path.join(colors.notes_file, "exercise_data.json")

# Check if EXD_DB file exists
if not os.path.exists(EXD_DB):
    source_file = "exercise_data.json"  # Assuming exercise_data.json is in the project directory

    try:
        with open(source_file, 'rb') as src, open(EXD_DB, 'wb') as dst:
            while True:
                chunk = src.read(1024)
                if not chunk:
                    break
                dst.write(chunk)
        print(f"Copied {source_file} to {EXD_DB}")
    except Exception as e:
        print(f"Error copying {source_file} to {EXD_DB}: {e}")

def save_data(data):
    with open(EXD_DB, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    try:
        with open(EXD_DB, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def show_exercise(exercise_dict, day):
    if day in exercise_dict:
        
        print(f"\n\n{colors.YELLOW}{colors.space*5}||  {day} exercises ||\n{colors.RESET}")
        exercises = exercise_dict[day].split("\n")
        m=0
        for exercise in exercises:
             # Print in different colors
            if m % 2 == 0:
                color = colors.CYAN
            elif m % 2 == 1:
                color = colors.GREEN
            else:
                color = colors.CYAN
            if m==0:
                print(color+colors.space*5+exercise+colors.RESET)
            else:
                print(color+colors.space*5+MUSC+exercise+colors.RESET)
            m+=1
        print()
    else:
        print("No exercise scheduled, free stuff then!")

def main():
    exercise_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    exercise_data = load_data()
    
    today_index = (datetime.today().weekday() + 2) % 7
    today = exercise_days[today_index]

    while True:
        print(f"\n{colors.YELLOW}||Exercise Program Tracker Menu||{colors.RESET}:")
        print(f"{colors.CYAN}m.{colors.RESET} {colors.YELLOW}Modify a date{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show today's exercise{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter your choice: ")

        if choice == "m":
            for index, day in enumerate(exercise_days, start=1):
                print(f"{index}. {day.capitalize()}")
            selected_index = int(input("Enter the index of the day you want to modify: ")) - 1
            if selected_index in range(len(exercise_days)):
                selected_day = exercise_days[selected_index]
                new_exercise = input(f"Enter the exercise for {selected_day.capitalize()}: ")
                exercise_data[selected_day] = new_exercise
                save_data(exercise_data)
                print(f"Exercise for {selected_day.capitalize()} has been modified.")
            else:
                print("Invalid index.")

        elif choice == "s":
            clear_terminal()
            show_exercise(exercise_data, today)
        elif choice =="q":
            clear_terminal()
            break

        else:
            clear_terminal()
            print("Invalid choice. Please enter 'm' or 's'.")

if __name__ == "__main__":
    main()
