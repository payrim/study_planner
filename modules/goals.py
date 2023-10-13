import datetime as dt
import json
import os
from utils.clearterminal import clear_terminal
from utils import colors


goals_DB = os.path.join(colors.notes_file, 'goals2.json')
date_JSON = os.path.join(colors.notes_file, 'daygoals.json')
subgoals_DB = os.path.join(colors.notes_file, 'subgoals.json')
subgoals = []

# Load goals from JSON file
def load_goals():
    try:
        with open(goals_DB, 'r') as file:
            goals = json.load(file)
        return goals
    except FileNotFoundError:
        return {}

# Load subgoals from JSON file
def load_subgoals():
    try:
        with open(subgoals_DB, 'r') as file:
            subgoals = json.load(file)
        return subgoals
    except FileNotFoundError:
        return []

def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\goalnotes.md"
        editor = 'notepad'
    else:
        notes_file = os.path.join(colors.notes_file,"goalnotes.md")
        editor = 'nvim'
    os.system(f"{editor} {notes_file}")


# Print all goals with indices
def print_goals_with_indices(goals):
    subgoals = load_subgoals()
    goals_with_subgoals = [(goal_name, goal_status, len([subgoal for subgoal in subgoals if subgoal.get("related_goal") == goal_name])) for goal_name, goal_status in goals.items()]
    
    # Sort the goals by the number of subgoals in descending order
    sorted_goals = sorted(goals_with_subgoals, key=lambda x: x[2], reverse=True)
    sorted_goal_names = [goal[0] for goal in sorted_goals]
    
    print(f"\n\n{colors.YELLOW}Current Goals (sorted by number of subgoals):{colors.RESET}")
    
    for index, (goal_name, goal_status, num_subgoals) in enumerate(sorted_goals):
        goal_color = colors.GREEN if goal_status[0] == 'active' else colors.YELLOW
        status_color = colors.CYAN if goal_status[0] == 'active' else colors.YELLOW
        num_subgoals_color = colors.BLUE
        
        formatted_goal_status = f"{goal_color}{goal_name}{colors.RESET}{status_color} - {goal_status[1]} days{colors.RESET}"
        if num_subgoals == 1:
            formatted_num_subgoals = f", {num_subgoals_color}({num_subgoals} subgoal){colors.RESET}"
        elif num_subgoals > 1:
            formatted_num_subgoals = f", {num_subgoals_color}({num_subgoals} subgoals){colors.RESET}"
        else:
            formatted_num_subgoals = ""
        
        original_index = list(goals.keys()).index(sorted_goal_names[index])
        print(f"{original_index + 1}. {formatted_goal_status}{formatted_num_subgoals}")


# Save goals to JSON file
def save_goals(goals):
    with open(goals_DB, 'w') as file:
        json.dump(goals, file, indent=4)

# Load or create daygoals.json and return today's date
def load_or_create_daygoals():
    try:
        with open(date_JSON, 'r') as file:
            saved_date = file.read().strip()
            return dt.datetime.strptime(saved_date, "%Y,%m,%d").date()
    except FileNotFoundError:
        today = dt.date.today()
        with open(date_JSON, 'w') as file:
            file.write(today.strftime("%Y,%m,%d"))
        return today

# Calculate the difference between today's date and the saved date
def calculate_date_difference(saved_date):
    today = dt.date.today()
    print
    return (today-saved_date).days

# Print active goals with indices sorted by days left until expiration
def print_active_goals(goals, date_difference):
    active_goals = [(goal_name, (goal_status, days_left)) for goal_name, (goal_status, days_left) in goals.items() if goal_status == "active"]
    sorted_goals = sorted(active_goals, key=lambda x: x[1][1])
    print(" "*7+"Active Goals:")
    for goal_name, (goal_status, days_left) in sorted_goals:
        print(f"{colors.space*7}⭐ {goal_name} - {days_left} days left until expiration")


# Toggle goal status (select/deselect)
def toggle_goal_status(goals, goal_index):
    goal_names = list(goals.keys())
    if 0 <= goal_index < len(goal_names):
        goal_name = goal_names[goal_index]
        goals[goal_name][0] = "active" if goals[goal_name][0] == "inactive" else "inactive"
        save_goals(goals)
        new_status = "active" if goals[goal_name][0] == "active" else "inactive"
        clear_terminal()
        print(f"Goal '{goal_name}' is now {new_status}.")
    else:
        clear_terminal()
        print("Invalid goal index.")

# Remove a goal
def remove_goal(goals, goal_index):
    goal_names = list(goals.keys())
    if 0 <= goal_index < len(goal_names):
        goal_name = goal_names[goal_index]
        del goals[goal_name]
        save_goals(goals)
        clear_terminal()
        print(f"Goal '{goal_name}' removed.")
    else:
        clear_terminal()
        print("Invalid goal index.")

# Add a new goal with expiration date
def add_goal(goals, goal_name, expiration_days):
    today = dt.date.today()
    expiration_date = today + dt.timedelta(days=expiration_days)
    goals[goal_name] = ["active", (expiration_date - today).days]
    save_goals(goals)
    print(f"Goal '{goal_name}' added with {expiration_days} days to complete.")

def remove_days_from_active_goals(goals, date_difference):
    for goal_name, (goal_status, days_left) in goals.items():
        if goal_status == "active":
            new_days_left = max(days_left - date_difference, 0)
            goals[goal_name] = [goal_status, new_days_left]
    today = dt.date.today()
    with open(date_JSON, 'w') as file:
        file.write(today.strftime("%Y,%m,%d"))
    save_goals(goals)

def add_subgoal(subgoals, goal_name, subgoal_name, index=None):
    load_subgoals()
    subgoals = load_subgoals()
    goal_exists = True

    if index is None:
        subgoal_index = len(subgoals)
    else:
        subgoal_index = max(0, min(index, len(subgoals)))

    subgoal = {"related_goal": goal_name, "subgoal_name": subgoal_name, "status": "unchecked"}
    subgoals.insert(subgoal_index, subgoal)

    # Update the indices for all subgoals of the same goal
    for i in range(subgoal_index + 1, len(subgoals)):
        if subgoals[i]["related_goal"] == goal_name:
            subgoals[i]["index"] = i

    save_subgoals(subgoals)
    clear_terminal()
    print(f"Subgoal '{subgoal_name}' added to '{goal_name}' at index {subgoal_index}.")

def check_subgoal(subgoals, goal_name, subgoal_index):
    for subgoal in subgoals:
        if subgoal["related_goal"] == goal_name:
            subgoal["status"] = "checked"
            save_subgoals(subgoals)
            print(f"Subgoal '{subgoal['subgoal_name']}' checked for '{goal_name}'.")
            return
    print(f"Invalid subgoal index or subgoal not related to '{goal_name}'.")

def show_first_unchecked_subgoal(subgoals):
    unchecked_subgoals = {}
    for subgoal in subgoals:
        goal_name = subgoal["related_goal"]
        status = subgoal["status"]
        subgoal_name = subgoal["subgoal_name"]
        
        if status == "unchecked":
            if goal_name not in unchecked_subgoals:
                unchecked_subgoals[goal_name] = subgoal_name
    
    if not unchecked_subgoals:
        print("No unchecked subgoals for any goal.")
        return
    
    print(f"\n\n\n{colors.YELLOW}{colors.space*7}First unchecked subgoals for each goal:{colors.RESET}\n")
    for goal_name, subgoal_name in unchecked_subgoals.items():
        print(f"{colors.CYAN}{colors.space*7}🌠- {goal_name}:{colors.RESET}{colors.YELLOW} {subgoal_name}{colors.RESET}")

def modify_subgoal_index(subgoals, goal_name, subgoal_index, new_index):
    if 0 <= subgoal_index < len(subgoals):
        subgoal = subgoals.pop(subgoal_index)
        new_index = max(0, min(new_index, len(subgoals)))
        subgoals.insert(new_index, subgoal)
        save_subgoals(subgoals)
        clear_terminal()
        print(f"Subgoal '{subgoal['subgoal_name']}' moved to index {new_index} for '{goal_name}'.")

def save_subgoals(subgoals):
    with open(subgoals_DB, 'w') as file:
        json.dump(subgoals, file, indent=4)

def remove_subgoal(subgoals, goal_name, subgoal_index):
    removed_subgoal = None
    for index, subgoal in enumerate(subgoals):
        if subgoal["related_goal"] == goal_name and index == subgoal_index:
            removed_subgoal = subgoals.pop(index)
            save_subgoals(subgoals)
            clear_terminal()
            print(f"Subgoal '{removed_subgoal['subgoal_name']}' removed from '{goal_name}'.")
            return

    clear_terminal()
    print(f"Invalid subgoal index or subgoal not related to '{goal_name}'.")

def print_subgoals(subgoals, goal_name):
    clear_terminal()
    print(f"\n\n{colors.YELLOW}Subgoals for '{goal_name}':{colors.RESET}")
    for index, subgoal in enumerate(subgoals):
        if subgoal["related_goal"] == goal_name:
            status = subgoal["status"]
            subgoal_name = subgoal["subgoal_name"]
            status_color = colors.GREEN if status == "checked" else colors.CYAN
            print(f"{index}. [{status_color}{status}{colors.RESET}] {subgoal_name}")


# Main function
def main():
    clear_terminal()
    goals = load_goals()
    saved_date = load_or_create_daygoals()
    date_difference = calculate_date_difference(saved_date)
    remove_days_from_active_goals(goals, date_difference)
    
    while True:
        subgoals = load_subgoals()
        print(f"\n\n{colors.YELLOW}||Goal Management Menu||{colors.RESET}\n")
        print(f"{colors.CYAN}sg.{colors.RESET} {colors.YELLOW}Show Current Goals{colors.RESET}")
        print(f"{colors.CYAN}ss.{colors.RESET} {colors.YELLOW}Show Subgoals{colors.RESET}")
        print(f"{colors.CYAN}ag.{colors.RESET} {colors.YELLOW}Add Goal{colors.RESET}")
        print(f"{colors.CYAN}as.{colors.RESET} {colors.YELLOW}Add Subgoal{colors.RESET}")
        print(f"{colors.CYAN}rg.{colors.RESET} {colors.YELLOW}Remove Goal{colors.RESET}")
        print(f"{colors.CYAN}rs.{colors.RESET} {colors.YELLOW}Remove Subgoal{colors.RESET}")
        print(f"{colors.CYAN}mg.{colors.RESET} {colors.YELLOW}Modify Goal Status{colors.RESET}")
        print(f"{colors.CYAN}ms.{colors.RESET} {colors.YELLOW}Modify Subgoal Status{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Modify Subgoal's Index{colors.RESET}")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Edit Notes{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter your choice: ")
        if choice == "sg":
            clear_terminal()
            print("\n\n")
            print_active_goals(goals, date_difference)
        elif choice == "ag":
            goal_name = input("\nEnter the new goal: ")
            expiration_days = int(input("Enter how many days this task takes: "))
            add_goal(goals, goal_name, expiration_days)
            clear_terminal()
        elif choice == "rg":
            clear_terminal()
            print_goals_with_indices(goals)
            goal_index = int(input("\nEnter the index of the goal to remove: ")) - 1
            remove_goal(goals, goal_index)
        elif choice == "mg":
            clear_terminal()
            print_goals_with_indices(goals)
            goal_index = int(input("\nEnter the index of the goal to toggle: ")) - 1
            toggle_goal_status(goals, goal_index)
        elif choice == "n":
            clear_terminal()
            edit_notes()
        elif choice == "as":
            clear_terminal()
            print_goals_with_indices(goals)
            goal_index = int(input("\nEnter the index of the goal to add a subgoal to: ")) - 1  # Adjust the index
            if 0 <= goal_index < len(goals):
                goal_name = list(goals.keys())[goal_index]
                print(goal_name)
                subgoal_name = input("Enter the subgoal name: ")
                add_subgoal(subgoals, goal_name, subgoal_name)
            else:
                clear_terminal()
                print("Invalid goal index.")
        elif choice == "rs":
            clear_terminal()
            print_goals_with_indices(goals)
            goal_index = int(input("\nEnter the index of the goal to remove a subgoal from: ")) - 1
            if 0 <= goal_index < len(goals):
                goal_name = list(goals.keys())[goal_index]
                print_subgoals(subgoals, goal_name)
                subgoal_index = int(input("\nEnter the index of the subgoal to remove: "))
                remove_subgoal(subgoals, goal_name, subgoal_index)
            else:
                clear_terminal()
                print("Invalid goal index.")
        elif choice == "ms":
            clear_terminal()
            print_goals_with_indices(goals)
            goal_index = int(input("Enter the index of the goal to check a subgoal for: ")) - 1
            if 0 <= goal_index < len(goals):
                goal_name = list(goals.keys())[goal_index]
                print_subgoals(subgoals, goal_name)
                subgoal_index = int(input("\nEnter the index of the subgoal to check: "))
                check_subgoal(subgoals, goal_name, subgoal_index)
                save_subgoals(subgoals)
            else:
                clear_terminal()
                print("Invalid goal index.")
        elif choice == "ss":
            clear_terminal()
            show_first_unchecked_subgoal(subgoals)
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "c":
            clear_terminal()
            print_goals_with_indices(goals)
            goal_index = int(input("\nEnter the index of the goal to modify a subgoal's index: ")) - 1
            if 0 <= goal_index < len(goals):
                goal_name = list(goals.keys())[goal_index]
                print_subgoals(subgoals, goal_name)
                subgoal_index = int(input("\nEnter the index of the subgoal to modify: "))
                new_index = int(input("Enter the new index: "))
                modify_subgoal_index(subgoals, goal_name, subgoal_index, new_index)
                save_subgoals(subgoals)         
            else:
                clear_terminal()
                print("Invalid goal index.")
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == "__main__":
    main()
