import datetime
import json
import os
from modules import endeavor
from colorama import Back, Fore, Style, init
from utils.clearterminal import clear_terminal
from utils import colors


# Initialize colorama
init(autoreset=True)
# Constants for rating colors
COLORS = {
    'red: Terrible': Fore.RED,
    'colors.YELLOW: Okay': Fore.YELLOW,
    'colors.CYAN: Good': Fore.CYAN,
    'pure colors.GREEN: perfect': Fore.GREEN,
}

# Database file path
DB_FILE = os.path.join(colors.notes_file, 'activity_data.json')
ENDV_FILE = os.path.join(colors.notes_file, 'endeavors.json')

# Initialize the activity database or load existing data
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r') as file:
        activity_data = json.load(file)
else:
    activity_data = {}

# Function to display the activity for the current month in a grid format
def show_activity():
    today = datetime.date.today()
    current_month = today.strftime('%B %Y')
    print(f"Activity for {current_month}\n")

    # Determine the number of days in the current month
    num_days = 31 if today.month in [1, 3, 5, 7, 8, 10, 12] else 30

    # Initialize the grid
    grid = [['' for _ in range(7)] for _ in range(5)]
    day_counter = 1

    for row in range(5):
        for col in range(7):
            if day_counter > num_days:
                break

            date_str = f'{today.year}-{today.month:02d}-{day_counter:02d}'
            activity_color = activity_data.get(date_str, ' ')

            # Use color to represent activity rating
            colored_activity = COLORS.get(activity_color, '')
            grid[row][col] = f'{day_counter:2d} [{colored_activity}■{Fore.RESET}]'

            day_counter += 1

    # Fill any remaining cells in the last row with empty strings
    for col in range(day_counter % 7, 7):
        grid[4][col] = ' ' * 5

    # Print the grid
    for row in grid:
        print(' '.join(row))
    
    print("\n")
    for index, (color, rating) in enumerate(COLORS.items()):
        print(f"{color} ({rating})")

# Function to add today's activity with a color rating
def add_activity():
    clear_terminal()
    today = datetime.date.today()
    date_str = today.strftime('%Y-%m-%d')

    print(f"Adding activity for {date_str}:")
    print("\n\nSelect a color rating:")

    # Print color options with indices
    for index, (color, rating) in enumerate(COLORS.items()):
        print(f"{index + 1}: {color} ({rating})")

    try:
        index_input = int(input("\nEnter the index of the color rating: "))
        if 1 <= index_input <= len(COLORS):
            selected_color = list(COLORS.keys())[index_input - 1]
            activity_data[date_str] = selected_color
            print(f"Activity added for {date_str}: {COLORS[selected_color]}")
        else:
            print("Invalid index. Activity not added.")
    except ValueError:
        print("Invalid input. Activity not added.")


# Function to flush the database
def flush_database():
    INPUT = input("Are you Sure(y/n)? ")
    if INPUT.lower() == "y":
        activity_data.clear()
        clear_terminal()
        print("Database flushed.")
    else:
        clear_terminal()
        print("Canceled.")

# Function to save activity data to a JSON file
def save_data():
    with open(DB_FILE, 'w') as file:
        json.dump(activity_data, file)

# Function to load activity data from a JSON file
def load_data():
    global activity_data
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            activity_data = json.load(file)
    else:
        print("No existing activity data to load.")

def show_specific_month_activity(year, month):
    clear_terminal()
    month_str = datetime.date(year, month, 1).strftime('%B %Y')
    print(f"Activity for {month_str}\n")

    # Determine the number of days in the specified month
    num_days = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30

    # Initialize the grid
    grid = [['' for _ in range(7)] for _ in range(5)]
    day_counter = 1

    for row in range(5):
        for col in range(7):
            if day_counter > num_days:
                break

            date_str = f'{year}-{month:02d}-{day_counter:02d}'
            activity_color = activity_data.get(date_str, ' ')

            # Use color to represent activity rating
            colored_activity = COLORS.get(activity_color, '')
            grid[row][col] = f'{day_counter:2d} [{colored_activity}■{Fore.RESET}]'

            day_counter += 1

    # Fill any remaining cells in the last row with empty strings
    for col in range(day_counter % 7, 7):
        grid[4][col] = ' ' * 5

    # Print the grid
    for row in grid:
        print(' '.join(row))

    input("\n\npress enter to continue...")

def list_months():
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year

    print("Select a month to view activity:")
    months = []

    for i in range(12):
        year = current_year
        month = current_month - i
        if month <= 0:
            month += 12
            year -= 1
        months.append((year, month))

    for index, (year, month) in enumerate(months):
        month_str = datetime.date(year, month, 1).strftime('%B %Y')
        print(f"{index + 1}: {month_str}")

    return months

def remove_activity():
    clear_terminal()
    today = datetime.date.today()
    date_str = today.strftime('%Y-%m-%d')

    if date_str in activity_data:
        del activity_data[date_str]
        clear_terminal()
        print(f"Activity removed for {date_str}")
    else:
        clear_terminal()
        print("No activity found for today.")

def calculate_activity_rating():
    try:
        color_rating = 'red: Terrible'
        # Read the "endeavors.json" file
        with open(ENDV_FILE, 'r') as file:
            tasks = json.load(file)
        
        total_tasks = len(tasks)
        total_priority = sum(task['priority'] for task in tasks)  # Sum of priorities of all tasks
        completed_priority = sum(task['priority'] for task in tasks if task['done'])  # Sum of priorities of completed tasks

        if total_priority == 0:
            completion_percentage = 0
        else:
            completion_percentage = (completed_priority / total_priority) * 100

        if completion_percentage == 0:
            color_rating = "haven't started"
            color = '\033[97m'  # white
        elif completion_percentage <= 27:
            color_rating = 'You gotta push a lot more <3'
            color = colors.WPURPLE #'\033[91m'  # Red
        elif completion_percentage <= 73:
            color_rating = 'Good Job, Keep working!'
            color = '\033[93m'  # colors.YELLOW
        elif completion_percentage <= 99:
            color_rating = 'Nice work, almost finished!'
            color = '\033[96m'  # colors.CYAN
        else:
            color_rating = 'perfect'
            color = '\033[92m'  # colors.GREEN

        # Print the activity rating
        print(f"{colors.space*7}{colors.CYAN}Today's activity rating:{colors.RESET} {color}{color_rating}{colors.RESET}")

        # Create a simple progress bar
        progress = f"[{'#' * int(completion_percentage / 10)}{' ' * (10 - int(completion_percentage / 10))}]"
        print(f"{colors.space*7}{colors.CYAN}Progress:{colors.RESET} {progress} ({completion_percentage:.2f}%)")

    except FileNotFoundError:
        print(f"{colors.space*7}{colors.RED}The ENDV_FILE file was not found.{colors.RESET}")
    except json.JSONDecodeError:
        print("Error reading JSON data from ENDV_FILE. Please check the file format.")


def calculate_and_save_activity_rating():
    try:
        color_rating = 'red: Terrible'
        # Read the "endeavors.json" file
        with open(ENDV_FILE, 'r') as file:
            tasks = json.load(file)
        
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task['done'])

        if total_tasks == 0:
            completion_percentage = 0
        else:
            completion_percentage = (completed_tasks / total_tasks) * 100

        if completion_percentage == 0:
            color_rating = 'red: Terrible'
        elif completion_percentage <= 32:
            color_rating = 'red: Terrible'
        elif completion_percentage <= 65:
            color_rating = 'colors.YELLOW: Okay'
        elif completion_percentage <= 99:
            color_rating = 'colors.CYAN: Good'
        else:
            color_rating = 'pure colors.GREEN: perfect'

        # Load existing activity data or initialize an empty dictionary
        activity_data = {}
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as activity_file:
                activity_data = json.load(activity_file)

        # Get the current date in YYYY-MM-DD format
        today_date = datetime.date.today().strftime('%Y-%m-%d')

        # Assign the calculated activity rating to today's date
        activity_data[today_date] = color_rating

        # Save the updated activity data to the "activity_data.json" file
        with open(DB_FILE, 'w') as activity_file:
            json.dump(activity_data, activity_file)

        print(f"Today's activity rating: {color_rating}")

    except FileNotFoundError:
        print(f"{colors.space*7}{colors.RED}The ENDV_FILE file was not found.{colors.RESET}")
    except json.JSONDecodeError:
        print("Error reading JSON data from ENDV_FILE. Please check the file format.")

def check_work_finished():
    global work_finished
    # Load existing activity data or initialize an empty dictionary
    activity_data = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as activity_file:
            activity_data = json.load(activity_file)

    # Get the current date in YYYY-MM-DD format
    today_date = datetime.date.today().strftime('%Y-%m-%d')

    # Check if today's activity rating is set
    if today_date in activity_data:
        work_finished = True
        print(f"{colors.YELLOW}{colors.space*7}Work finished, congrats!{colors.RESET}")
    else:
        work_finished = False
        calculate_activity_rating()

def check_and_update_yesterday_activity():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    # Check if yesterday's date exists in the activity data
    if yesterday_str not in activity_data:
        last_colored_date = None

        # Find the last colored date in the activity data
        for date, color in sorted(activity_data.items(), reverse=True):
            if color != '':
                last_colored_date = date
                break

        # Calculate color_rating based on completion_percentage
        try:
            color_rating = 'red: Terrible'
            with open(ENDV_FILE, 'r') as file:
                tasks = json.load(file)
            
            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if task['done'])

            if total_tasks != 0:
                completion_percentage = (completed_tasks / total_tasks) * 100
                if completion_percentage == 0:
                    color_rating = 'red: Terrible'
                elif completion_percentage <= 32:
                    color_rating = 'red: Terrible'
                elif completion_percentage <= 65:
                    color_rating = 'colors.YELLOW: Okay'
                elif completion_percentage <= 99:
                    color_rating = 'colors.CYAN: Good'
                else:
                    color_rating = 'pure colors.GREEN: perfect'
            else:
                color_rating = 'red: Terrible'
        except FileNotFoundError:
            print(f"{colors.space*7}{colors.RED}The ENDV_FILE file was not found, Please make sure to save routines.{colors.RESET}") 

        # If there's a last colored date, set yesterday's color to the same color
        if last_colored_date:
            activity_data[yesterday_str] = color_rating

            # Set the days until the last colored date to red
            last_colored_date = datetime.datetime.strptime(last_colored_date, '%Y-%m-%d').date()
            current_date = yesterday
            while current_date >= last_colored_date:
                date_str = current_date.strftime('%Y-%m-%d')
                if date_str != yesterday_str:
                    activity_data[date_str] = 'red: Terrible'  # Set the color to red for empty days
                current_date -= datetime.timedelta(days=1)
        else:
            # If there's no last colored date, set yesterday to red
            activity_data[yesterday_str] = color_rating

        # Save the updated activity data to the "activity_data.json" file
        with open(DB_FILE, 'w') as file:
            json.dump(activity_data, file)


# Function to calculate color statistics for a given month
def calculate_color_statistics(year, month):
    month_str = datetime.date(year, month, 1).strftime('%B %Y')
    total_days = 0
    color_counts = {color: 0 for color in COLORS}

    for day in range(1, 32):
        date_str = f'{year}-{month:02d}-{day:02d}'
        if date_str in activity_data:
            color = activity_data[date_str]
            color_counts[color] += 1
            total_days += 1

    return month_str, color_counts, total_days

# Function to display color statistics for a given month
def show_color_statistics():
    clear_terminal()
    months = list_months()
    
    try:
        month_choice = int(input("\n\nEnter the index of the month (1 for this month, 2 for previous month, etc.): "))-1
        if 0 <= month_choice < len(months):
            year, month = months[month_choice]
            month_str, color_counts, total_days = calculate_color_statistics(year, month)
            
            print(f"\nStatistics for {month_str}:\n")
            for color, count in color_counts.items():
                percentage = (count / total_days) * 100 if total_days > 0 else 0
                print(f"{COLORS[color]}{color}: {count} days ({percentage:.2f}%)")
            
            input("\nPress enter to continue...")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input.")

check_and_update_yesterday_activity()
load_data()
# check the dates
endeavor.check_date()
endeavor.save_today_date()

# Main program loop
def main():
    clear_terminal()
    while True:
        print(f"\n\n\n{colors.space*7}{colors.YELLOW}||Activity Tracker||{colors.RESET}\n")
        print(f"{colors.space*7}{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show Activity{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add Today's Activity{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}u.{colors.RESET} {colors.YELLOW}Show today's progress{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Add today based on endeavors{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove Today's Activity{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Show Color Statistics{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}l.{colors.RESET} {colors.YELLOW}List Months{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Flush Database{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}v.{colors.RESET} {colors.YELLOW}Save Data to JSON{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}o.{colors.RESET} {colors.YELLOW}Load Data from JSON{colors.RESET}")
        print(f"{colors.space*7}{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        print()
        #check_work_finished()
        choice = input("\n"+colors.space*7+"Enter your choice: ").strip()

        if choice == 's':
            clear_terminal()
            show_activity()
            input("\npress enter to continue...")
            clear_terminal()
        elif choice == 'a':
            clear_terminal()
            add_activity()
            save_data()
            clear_terminal()
        elif choice == 'r':
            remove_activity()
            save_data()
        elif choice == 'f':
            flush_database()
        elif choice == 'v':
            save_data()
        elif choice == 'o':
            load_data()
        elif choice == 'c':
            clear_terminal()
            show_color_statistics()
            clear_terminal()
        elif choice == 'u':
            clear_terminal()
            print("\n")
            calculate_activity_rating()
            print("\n")
        elif choice == 't':
            clear_terminal()
            calculate_and_save_activity_rating()
            load_data()
        elif choice =='l':
            clear_terminal()
            months = list_months()
            try:
                month_choice = int(input("\n\nEnter the index of the month: "))
                if 1 <= month_choice <= len(months):
                    year, month = months[month_choice - 1]
                    show_specific_month_activity(year, month)
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input.")
            clear_terminal()
        elif choice == 'q':
            print("Goodbye!")
            clear_terminal()
            break
        else:
            clear_terminal()
   
if __name__ == '__main__':
    main()