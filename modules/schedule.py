import datetime
from utils.clearterminal import clear_terminal
from utils import colors
import os

# Get the current day of the week (0=Monday, 1=Tuesday, ..., 6=Sunday)
current_day = datetime.datetime.now().weekday()

# Define a dictionary to map day numbers to day names
day_names = {
    0: 'MON',
    1: 'TUE',
    2: 'WED',
    3: 'THUR',
    4: 'FRI',
    5: 'SAT',
    6: 'SUN'
}


SCH_TXT = os.path.join(colors.notes_file, 'plan.txt')

def showschedule():
    print("\n\n")
    # Read the "plan.txt" file
    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    # Initialize a flag to indicate whether to print schedules
    print_schedule = False

    # Iterate through the lines in the file
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace

        # Check if the line matches the current day
        if line.startswith('#') and day_names[current_day] in line:
            print_schedule = True
            print(f"{colors.CYAN}{line}{colors.RESET}")  # Print the day header in colors.CYAN
        elif print_schedule and line:  # Only print non-empty lines for the current day
            print(f"{colors.BLUE}{line}{colors.RESET}")  # Print non-empty lines in colors.BLUE
        elif print_schedule and not line:  # Stop printing when an empty line is encountered
            break
    input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")

def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\plan.txt"
        editor = 'notepad'
    else:
        notes_file = os.path.expanduser("./plan.txt")
        editor = 'nvim'
    os.system(f"{editor} {notes_file}")

def showschedule_by_time():
    # Get the output of the showschedule() function
    schedule_output = get_schedule_output()

    # Get the current time in HH:MM format
    current_time = datetime.datetime.now().strftime('%H:%M')

    # Initialize a flag to indicate whether to print the schedule for the current day
    print_current_day = False

    # Iterate through the lines in the schedule output
    for line in schedule_output.split('\n'):
        line = line.strip()  # Remove leading/trailing whitespace

        # Check if the line is a day header
        if line.startswith(f"{colors.CYAN}#") and day_names[current_day] in line:
            print_current_day = True
            print(f"\n\n\n{colors.CYAN}{line}{colors.RESET}")  # Print the day header in colors.CYAN
        elif print_current_day and line:  # Only print non-empty lines for the current day
            start_time, end_time, activity = line.split(' - ')
            # Check if the current time is within the time range
            if start_time <= current_time <= end_time:
                print(f"{colors.BLUE}{line}{colors.RESET}")  # Print the current activity in colors.BLUE

    if not print_current_day:
        print(f"{colors.YELLOW}No scheduled activities for today at the current time.{colors.RESET}")

    input(f"\n\n{colors.space*3}{colors.YELLOW}Press any key to continue...{colors.RESET}")

def get_schedule_output():
    # This function returns the output of showschedule() without printing it to the console
    output = []
    # Read the "plan.txt" file
    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    # Initialize a flag to indicate whether to print schedules
    print_schedule = False

    # Iterate through the lines in the file
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace

        # Check if the line matches the current day
        if line.startswith('#') and day_names[current_day] in line:
            print_schedule = True
            output.append(f"{colors.CYAN}{line}{colors.RESET}")  # Store the day header in colors.CYAN
        elif print_schedule and line:  # Only add non-empty lines for the current day
            output.append(f"{colors.BLUE}{line}{colors.RESET}")  # Store non-empty lines in colors.BLUE
        elif print_schedule and not line:  # Stop adding when an empty line is encountered
            break

    return '\n'.join(output)


def main():
    while True:
        print(f"\n{colors.YELLOW}||Schedule Program||{colors.RESET}\n")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}change Schedules{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show Schedules{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Show Schedule by Current Time{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}quit{colors.RESET}")
        choice = input("\nEnter choice: ")
        if choice == "s":
            clear_terminal()
            showschedule()
            clear_terminal()
        elif choice == "n":
            clear_terminal()
            edit_notes()
            clear_terminal()
        elif choice == "t":  # Added handling for the new option
            clear_terminal()
            showschedule_by_time()
            clear_terminal()
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()