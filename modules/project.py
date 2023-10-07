import json
import math
import os
from datetime import datetime, timedelta
from utils.clearterminal import clear_terminal
from utils import colors


studies = []

PROJECT_DB = os.path.join(colors.notes_file, "projecttracker.json")
DAYT_DB = os.path.join(colors.notes_file, "taskdays.json")
TDATE_JSON = os.path.join(colors.notes_file, "todaysdate.json")

def save_data():
    with open(PROJECT_DB, "w") as f:
        json.dump(studies, f)
    #print("\nData saved successfully!\n")

def load_data():
    global studies
    try:
        with open(PROJECT_DB, "r") as f:
            studies = json.load(f)
    except FileNotFoundError:
        studies = []
        save_data()
        print("No saved data found. A new data file has been created.")


def update_project_indexes():
    global studies
    num_studies = len(studies)
    if num_studies == 0:
        pass
    else:
        for i in range(num_studies):
            studies[i]['index'] = i+1


def add_project():
    name = input("\n\nEnter project name: ")
    desc = input("Enter project description: ")
    multiplier = float(input("Enter project multiplier: "))
    index = len(studies) + 1
    studies.append({"index": index, "name": name, "desc": desc, "days": 0, "multiplier": multiplier, "selected": 0, "done": 0})
    print("Study added successfully!")

def remove_project():
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        print("\n\nList of studies:")
        for project in studies:
            print(f"{project['index']}. {project['name']}")
        index = int(input("Enter project index to remove: "))
        for project in studies:
            if project["index"] == index:
                studies.remove(project)
                print(f"{project['name']} removed successfully.")
                return
        print(f"Study with index {index} not found.")

def reset_project_index():
    if len(studies) == 0:
        pass
    else:
        n = len(studies)
        for i in range(n):
            studies[i]["index"] = i + 1

def list_studies():
    if len(studies) == 0:
        print("No studies added yet.")
    else:
        total_days = sum([project['days'] for project in studies])  # Calculate the sum of all days
        total_multiplier = sum([project['multiplier'] for project in studies])  # Calculate the sum of all days
        print(f"\n{'Index':<6}{'Name':<39}{'Days':<20}{'Multiplier':<20}{'Done':<10}{'selected':<10}")
        print("----------------------------------------------------------------------------------------------------------")
        for project in studies:
            print(f"{project['index']:<6}{project['name']:<39}{project['days']:<20.2f}{str(project['multiplier']):<20}{project['done']:<12}{project['selected']:<13}")
        print("----------------------------------------------------------------------------------------------------------")
    print(f"{'':<45}{total_days:<20.2f}{total_multiplier:<20.2f}")
    input("\npress any key to continue......")
    clear_terminal()


def save_task_days():
    task_days= input("enter task days: ")
    with open(DAYT_DB, "w") as f:
        json.dump(task_days, f)
    print("\nTask days saved successfully!\n")

def change_project_multiplier():
    global studies
    print("\n\nList of studies:")
    for project in studies:
        print(f"{project['index']}. {project['name']}: {project['multiplier']}")
    index = int(input("Enter project index to modify: "))
    multiplier = float(input("Enter new multiplier for project: "))
    studies[index - 1]['multiplier'] = multiplier
    save_data()
    clear_terminal()
    print(f"Multiplier for project '{studies[index - 1]['name']}' updated to {multiplier}")


def load_task_days():
    global task_days
    try:
        with open(DAYT_DB, "r") as f:
            task_days = json.load(f)
        #print("Task days loaded successfully!")
    except FileNotFoundError:
        print("No saved task days found.")
    except json.JSONDecodeError:
        print("Invalid JSON format in saved task days file.")

task_days = 0
load_task_days()

def assign_days_to_studies():
    global studies
    num_studies = len(studies)
    if num_studies == 0:
        print("No studies added yet.")
    else:
        total_multiplier = sum([project['multiplier'] for project in studies if project['done'] != 1])
        if total_multiplier == 0:
            print("No multipliers set yet. Please set multipliers before assigning days.")
            return
        undone_studies = [project for project in studies if project['done'] != 1]
        days_per_project = round(int(task_days) / total_multiplier, 2)
        for project in undone_studies:
            project_days = days_per_project * project['multiplier']
            project['days'] = round(project_days, 2)
        print(f"Assigned {days_per_project} days to each project except those already marked as done.")


def flush_studies():
    confirm = input("Are you sure you want to delete all studies? (y/n) ")
    if confirm.lower() == "y":
        global studies
        studies = []
        clear_terminal()
        print("\nAll studies removed successfully. remember to save")
    else:
        clear_terminal()
        print("cancelled.\n")

def adjust_project_days():
    if len(studies) < 2:
        print("At least two studies are required to perform this operation.")
        return

    # List all studies
    print("\nList of studies:")
    for i, project in enumerate(studies):
        print(f"{i+1}. {project['name']}\t - days: {project['days']}")

    # Ask for first project to add days to
    while True:
        first_choice = input("Enter the number of the project you want to add days to: ")
        if not first_choice.isdigit() or int(first_choice) < 1 or int(first_choice) > len(studies):
            print("Invalid choice. Please enter a valid project number.")
        else:
            first_choice = int(first_choice)
            break

    # Ask for second project to remove days from
    while True:
        second_choice = input("Enter the number of the project you want to remove days from: ")
        if not second_choice.isdigit() or int(second_choice) < 1 or int(second_choice) > len(studies) or second_choice == first_choice:
            print("Invalid choice. Please enter a valid project number that is different from the first choice.")
        else:
            second_choice = int(second_choice)
            break

    # Ask for the number of days to transfer
    while True:
        days = input("Enter the number of days to transfer: ")
        if not days.isdigit():
            print("Invalid input. Please enter a positive integer.")
        else:
            days = int(days)
            break

    # Update the days of the two studies
    studies[first_choice-1]["days"] += days
    studies[second_choice-1]["days"] -= days

    print(f"{days} days were transferred from {studies[second_choice-1]['name']} to {studies[first_choice-1]['name']}.")

def mark_selected():
    print("\nList of studies:")
    for i, project in enumerate(studies):
        print(f"{i+1}. {project['name']}")
    
    selected = input("\nEnter the number of the project you want to mark as selected: ")
    selected_index = int(selected) - 1
    
    if selected_index < 0 or selected_index >= len(studies):
        print("Invalid selection.")
        return
    
    for project in studies:
        project['selected'] = 0
    studies[selected_index]['selected'] = 1
    clear_terminal()
    save_data()
    print(f"{studies[selected_index]['name']} marked as selected.")

def save_today_date():
    today_date = (datetime.now() - timedelta(days=0)).strftime("%d-%m-%Y")
    with open(TDATE_JSON, "w") as f:
        json.dump(today_date, f)
    #print("Today's date saved successfully!")

def check_date():
    if not os.path.isfile(TDATE_JSON):
        with open(TDATE_JSON, "w") as f:
            json.dump(datetime.now().strftime("%d-%m-%Y"), f)

    with open(TDATE_JSON, "r") as f:
        saved_date = json.load(f)
    today_date = datetime.now().strftime("%d-%m-%Y")

    if saved_date != today_date:
        saved_date_obj = datetime.strptime(saved_date, "%d-%m-%Y")
        today_date_obj = datetime.strptime(today_date, "%d-%m-%Y")
        days_diff = (today_date_obj - saved_date_obj).days
        with open(TDATE_JSON, "w") as f:
            json.dump(today_date, f)
        for project in studies:
            if project["selected"] == 1:
                project["days"] -= days_diff
        save_data()
        print(f"{days_diff} day(s) have been removed from the selected Study.")
    else:
        #print("Today's date is already saved.")
        pass


def mark_subject_done():
    if len(studies) == 0:
        print("No Study added yet.")
        return
    
    print("Select a Study to mark as done:")
    
    try:
        print("\n\nList of studies:")
        for project in studies:
            print(f"{project['index']}. {project['name']}")
        index = int(input("Enter project index to set as done: "))
        clear_terminal()
        subject = next((subject for subject in studies if subject["index"] == index), None)
        if subject:
            subject["done"] = 1
            print(f"{subject['name']} marked as done.")
            print("Congrats!!! 🎉🎉🎉🎉")
            save_data()
        else:
            print(f"Study with index {index} not found.")
    except ValueError:
        print("Invalid input. Please enter a valid index.")

def display_project_chart():
    global studies

    # Find the selected project
    selected_project = None
    for project in studies:
        if project.get('selected') == 1:
            selected_project = project
            break

    if selected_project is None:
        print("No project is selected.")
        return

    # Display the chart
    print("+" + "-" * 78 + "+")
    print("|{:<78}|".format("{}".format(selected_project.get('name', '')).center(77)))
    print("|{:<78}|".format("{:.2f} Days left".format(selected_project.get('days', 0)).center(77)))
    print("|{:<78}|".format(datetime.today().strftime("%d-%m-%Y").center(77)))
    print("+" + "-" * 78 + "+")
    print("|{:<78}|".format("Study Description".center(77)))
    desc = selected_project.get('desc', '')
    desc_lines = [desc[i:i+75].ljust(75) for i in range(0, len(desc), 75)]
    for line in desc_lines:
        print("|{:<78}|".format(line))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("|{:<78}|".format("".center(77)))
    print("+" + "-" * 78 + "+")
    print("\n")

def main():
    clear_terminal()
    load_data()
    load_task_days()
    check_date()
    save_today_date()
    while True:
        update_project_indexes()
        print(f"\n{colors.YELLOW}||Project Automation||\n{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add project{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show current project{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}List studies{colors.RESET}")
        print(f"{colors.CYAN}o.{colors.RESET} {colors.YELLOW}Set deadline date and colors.RESET studies{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET} {colors.YELLOW}Adjust a project{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET} {colors.YELLOW}Mark a project as on-going{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Change a project's multiplier{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Mark a project as done{colors.RESET}")
        print(f"{colors.CYAN}v.{colors.RESET} {colors.YELLOW}Save data{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove project{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Flush studies{colors.RESET}")
        print(f"{colors.CYAN}b.{colors.RESET} {colors.YELLOW}Load data{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter choice: ")
        if choice == "a":
            clear_terminal()
            add_project()
            reset_project_index()
            save_data()
        elif choice == "r":
            clear_terminal()
            remove_project()
            reset_project_index()
            save_data()
            clear_terminal()
        elif choice == "o":
            clear_terminal()
            save_task_days()
            load_task_days()
            assign_days_to_studies()
            save_data()
        elif choice == "f":
            clear_terminal()
            flush_studies()
        elif choice == "v":
            clear_terminal()
            save_data()
        elif choice == "s":
            clear_terminal()
            display_project_chart()
        elif choice == "l":
            clear_terminal()
            list_studies()
        elif choice == "t":
            clear_terminal()
            change_project_multiplier()
        elif choice == "c":
            clear_terminal()
            mark_subject_done()
        elif choice == "d":
            clear_terminal()
            adjust_project_days()
            save_data()
        elif choice == "b":
            clear_terminal()
            load_data()
        elif choice == "m":
            clear_terminal()
            mark_selected()
            save_data()
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")
            clear_terminal()


if __name__ == '__main__':
    main()