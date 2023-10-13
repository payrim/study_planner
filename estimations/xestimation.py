import copy
import datetime
import json
import math
import os
import re
from utils.clearterminal import clear_terminal
from utils import colors


    
BOOKP_DB = os.path.join(colors.notes_file, 'bookprime.json')
XTODAY_JSON = os.path.join(colors.notes_file, 'todaysdate3x.json')
XTRACKER_DB = os.path.join(colors.notes_file, 'exercisetracker.json')
XUNACTIVE_DB = os.path.join(colors.notes_file, 'unactivetrackersx.json')
XDONE_DB = os.path.join(colors.notes_file, 'done_ex.json')
pomofile = os.path.join(colors.pomo_file, 'taskexercises.txt')


def save_todays_date():
    # Get today's date in the format 'dd-mm-yyyy'
    today_date = datetime.date.today().strftime("%d-%m-%Y")

    # Save today's date to a JSON file
    with open(XTODAY_JSON, 'w') as f:
        json.dump(today_date, f)

def load_todays_date():
    try:
        with open(XTODAY_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or there's an issue with JSON decoding, return None
        save_todays_date()
        return None

def update_trackers_and_remove_days():
    # Check if the date saved in the file is different from today's date
    saved_date = load_todays_date()
    if saved_date is not None and saved_date != datetime.date.today().strftime("%d-%m-%Y"):
        # Calculate the difference in days
        saved_date_obj = datetime.datetime.strptime(saved_date, "%d-%m-%Y").date()
        today_date_obj = datetime.date.today()
        days_difference = (today_date_obj - saved_date_obj).days

        if days_difference > 0:
            for tracker in trackers:
                # Check if "days_left" is an integer, treat it as number of days to subtract
                if isinstance(tracker["days_left"], int):
                    days_left = tracker["days_left"] - days_difference
                    tracker["days_left"] = days_left
                else:
                    # If "days_left" is a date, subtract the days_difference from it
                    target_date = datetime.datetime.strptime(tracker["days_left"], "%d-%m-%Y").date()
                    new_date = target_date - datetime.timedelta(days=days_difference)
                    tracker["days_left"] = new_date.strftime("%d-%m-%Y")
        save_todays_date()
        save_trackers()


def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\trackernote.md"
        editor = 'notepad'
    else:
        notes_file = os.path.join(colors.notes_file,"trackernote.md")
        editor = 'nvim'
    os.system(f"{editor} {notes_file}")

# Initialize an empty list to hold the trackers
trackers = []
tasks = [] 


# Load the trackers data from a JSON file
def load_trackers():
    global trackers
    try:
        with open(XTRACKER_DB, 'r') as f:
            trackers = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist yet, create an empty one
        save_trackers()

# Save the trackers data to a JSON file
def save_trackers():
    with open(XTRACKER_DB, 'w') as f:
        json.dump(trackers, f)

# Remove a tracker from the list
def remove_tracker():
    print_trackers()
    index = int(input("\n\nEnter index of tracker to remove: "))
    try:
        del trackers[index]
        clear_terminal()
        print("tracker removed successfully.")
    except IndexError:
        print("Invalid index.")

# Load the tasks data from a JSON file
def load_tasks():
    global tasks
    try:
        with open(XDONE_DB, 'r') as f:
            tasks = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist yet, create an empty one
        save_tasks()

# Save the tasks data to a JSON file
def save_tasks():
    with open(XDONE_DB, 'w') as f:
        json.dump(tasks, f)

# Add a new tracker to the list
def add_tracker():
    name = input("\n\nEnter tracker name: ")
    amount = int(input("Enter number of amount: "))
    desc = str(input("Enter description for amount: "))
    dayutil = []
    for tracker in trackers:
         days = tracker["days_left"]
         dayutil.append(days)
    dayutil.sort(key=lambda x: x)
    print("current occupied days are:",dayutil)
    target = int(input("Enter how many days: "))
    tracker = {
        "name": name,
        "amount": amount,
        "amount_desc": desc,
        "days_left": target
    } 
    trackers.append(tracker)
    save_trackers()  # Save the updated list of trackers to the JSON file
    clear_terminal()
    print("tracker added successfully.")

# Display a list of all the trackers
def print_trackers():
    total_trackers = sum(tracker['amount'] for tracker in trackers)
    if total_trackers == 0:
        clear_terminal()
        print(f"{colors.RED}No trackers found.{colors.RESET}")
        return

    header = f"{colors.CYAN}Index{colors.RESET}\t{colors.CYAN}Name{colors.RESET}\t\t\t{colors.CYAN}Amount{colors.RESET}\t{colors.CYAN}Done{colors.RESET}\t{colors.CYAN}Desc{colors.RESET}\t\t\t{colors.CYAN}Progress{colors.RESET}\t{colors.CYAN}Days Left{colors.RESET}"
    print(f"\n{header}")
    total_trackers_read = sum(task['amount'] for task in tasks if task['tracker'] in [tracker['name'] for tracker in trackers])
    progress_bar_length = 20
    progress_bar_fill = '█'

    sorted_trackers = sorted(trackers, key=lambda x: x.get('days_left', float('inf')))

    for i, tracker in enumerate(sorted_trackers):
        trackers_read = sum(task['amount'] for task in tasks if task['tracker'] == tracker['name'])
        progress = int(trackers_read * 100 / tracker['amount']) if tracker['amount'] != 0 else 0

        # Use string formatting with fixed width for each column
        print(f"{colors.BLUE}{trackers.index(tracker)}{colors.RESET}\t{colors.YELLOW}{tracker['name']:20}{colors.RESET}\t{colors.GREEN}{tracker['amount']}{colors.RESET}\t{colors.YELLOW}{trackers_read}{colors.RESET}\t{tracker['amount_desc']}\t\t{colors.GREEN}{progress}%{colors.RESET}\t\t{colors.YELLOW}{tracker.get('days_left', 'N/A')}{colors.RESET}")

    progress_bar_fill_count = int(total_trackers_read / total_trackers * progress_bar_length)
    progress_bar = f"[{progress_bar_fill * progress_bar_fill_count}{' ' * (progress_bar_length - progress_bar_fill_count)}]"
    print(f"\n{colors.BLUE}Progress: {progress_bar} {int(total_trackers_read / total_trackers * 100)}%{colors.RESET}")
    print(f"{colors.YELLOW}[{total_trackers} total]{colors.RESET}")



def tracker_greedy():
    if len(trackers) >0:
        sorted_trackers = []
        shared_indices = []
        merged_trackers = [[0,0]]

        for tracker in trackers:
            amount = tracker.get("amount", 0)
            read = sum(task['amount'] for task in tasks if task['tracker'] == tracker['name'])
            time_left = tracker.get("days_left", 0)
            sorted_trackers.append(copy.deepcopy([amount-read, time_left]))

        sorted_trackers.sort(key=lambda x: x[1])

        newt = copy.deepcopy(sorted_trackers)

        for i in range(1, len(sorted_trackers)):
            if sorted_trackers[i][1] == sorted_trackers[i - 1][1]:
                shared_indices.append(i)
                shared_indices.append(i - 1)

        for i in range(len(sorted_trackers)):
            if i not in shared_indices:
                merged_trackers.append(sorted_trackers[i])
                
        #print("sorted:",sorted_trackers)

        merged_trackers.sort(key=lambda x: x[1])

        # Calculate the sum of amount for each group of trackers sharing the same days left
        for i in range(0, len(shared_indices), 2):
            index1 = shared_indices[i]
            index2 = shared_indices[i + 1]
            merged_amount = sorted_trackers[index1][0] + sorted_trackers[index2][0]
            shared_day = sorted_trackers[index1][1]
            merged_trackers.append([merged_amount, shared_day])

        merged_trackers.sort(key=lambda x: x[1])
        #print("merged:",merged_trackers)

        # Loop over the trackers and merge if needed
        i = 1
        day_list = []
        if len(merged_trackers)>2:
            while i < len(merged_trackers) - 1:
                #print("merged:",merged_trackers,len(merged_trackers))
                average1 = merged_trackers[i][0] / (merged_trackers[i][1] -  merged_trackers[i-1][1])
                average2 = merged_trackers[i + 1][0] / (merged_trackers[i + 1][1] - merged_trackers[i][1])
                #print("average1",average1,"average2",average2)
                if average2 > average1:
                    day_list.clear()
                    # Merge the current tracker and the next one
                    merged_amount = merged_trackers[i][0] + merged_trackers[i + 1][0]
                    new_time_left = merged_trackers[i + 1][1]
                    merged_trackers[i][0] = merged_amount
                    merged_trackers[i][1] = new_time_left
                    #print("merged:",merged_trackers,len(merged_trackers))

                    # Remove the next tracker from the merged_trackers list
                    merged_trackers.pop(i + 1)
                    i = 0
                else:
                    day_list.append(average1)
                    #print("I DID IT")
                    # Move on to the next tracker
                    new_time_left = merged_trackers[i + 1][1] - merged_trackers[i][1]
                    i += 1
                    #print("merged_sec:",merged_trackers,len(merged_trackers))

            # New part to add and loop over sorted_trackers
            day_list.append(average2)
            # print(day_list)
            # print(merged_trackers)
            # print(sorted_trackers)
            # print(newt)
            result_list = []
            j = 0
            
            mergeplier = day_list[0] * newt[0][1]
            while j < len(newt):
                lastmerge = mergeplier
                mergeplier = mergeplier - newt[j][0]
                result_list.append(copy.deepcopy(newt[j][0]))
                if mergeplier > 0:
                    j+=1
                elif mergeplier <= 0:
                    result_list.pop()
                    last_element = lastmerge
                    result_list.append(last_element)
                    break
            
            trackername = []
            time_left_list = []

            for i in range(len(result_list)):
                time_left = result_list[i]
                time_left_formatted = "{:.1f}".format(time_left)
                time_left_list.append(time_left_formatted)  # Add the formatted value to the time_left_list
                #print("trackers in next:",time_left_list)

            for tracker in trackers:
                name = tracker.get("name", 0)
                days_left = tracker.get("days_left", 0)
                trackername.append([name, days_left ])  # Append the name and time_left to the trackername list as a tuple

            trackername.sort(key=lambda x: x[1])
            
            # for element, time_left in zip(trackername, time_left_list):
            #     print(f"{element[0]}: {time_left}")

            print(f"\n\n{colors.space*5}{colors.YELLOW}Exercises in next {newt[0][1]} days:{colors.RESET}")
            #print(newt)
            m=1
            
            for element in trackername:
                name = element[0]
                if m <= len(time_left_list):
                    tracker_amount = float(time_left_list[trackername.index(element)]) # Get the corresponding time_left from time_left_list
                    for tracker in trackers:
                        if tracker["name"] == name:
                            tracker_desc = tracker["amount_desc"]
                            break

                    if tracker_amount == 0:
                        continue
                    else:
                        print(f"{colors.space*5}➕ {colors.CYAN}{name}:{colors.RESET}{colors.BLUE} {tracker_amount}{colors.RESET}{colors.GREEN} -- {tracker_desc}{colors.RESET}({(tracker_amount/newt[0][1]):.2f} per day can do)")
                    m+=1
                else:
                    break
            print(f"{colors.space*5}{colors.YELLOW}tracker per day: {day_list[0]:.2f}{colors.RESET}")
        else:
            print("ERROR: Merge conflict type [EXERCISE]")
    else:
        print("no trackers found.")

# Add a new tracker to the list
def add_task():
    print_trackers()
    while True:
        try:
            index = int(input("\n\nEnter index of tracker to add task: "))
            tracker = trackers[index]
            break
        except (ValueError, IndexError):
            print("Invalid index. Please try again.")

    print("Selected tracker:", tracker["name"])
    name = str(input("Enter the name for this task: "))
    amount = int(input("Enter number of amount: "))
    time_spent = int(input("Enter the time you spent studying (in minutes): "))
    date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%d-%m-%Y")
    if time_spent != "":
        task = {
            "name": name,
            "tracker": tracker["name"],
            "date": date,
            "time_spent": time_spent,
            "amount": amount
        }
    else:
        pass

    tasks.append(task)
    save_tasks() 
    clear_terminal()
    print("task added successfully.")


def remove_task():
    unique_dates = sorted(set(task['date'] for task in tasks), key=lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'), reverse=True)

    if not unique_dates:
        clear_terminal()
        print("No tasks found.")
        return

    print("\nUnique Dates with Tasks (Newest first):\n")
    for i, date in enumerate(unique_dates):
        print(f"{i}\t{date}")

    try:
        date_index = int(input("\nEnter index of the date you want to remove tasks from: "))
        selected_date = unique_dates[date_index]

        tasks_to_remove = [task for task in tasks if task['date'] == selected_date]

        if not tasks_to_remove:
            clear_terminal()
            print(f"No tasks found for the selected date: {selected_date}")
            return

        print("\nTasks for the selected date:\n")
        print("Index\tTracker\t\tName\t\tAmount\t\tTime Spent")
        for i, task in enumerate(tasks_to_remove):
            print(f"{i}\t{task['tracker']}\t\t{task['name']}\t\t{task['amount']}\t\t{task['time_spent']}")

        task_index = int(input("\nEnter index of the task you want to remove: "))
        del tasks[tasks.index(tasks_to_remove[task_index])]
        clear_terminal()
        print("Task removed successfully.")
    except (ValueError, IndexError):
        clear_terminal()
        print("Invalid input or index.")

    save_tasks()  # Save the updated list of tasks to the JSON file
    clear_terminal()

# Display a list of all unique dates in the tasks and allow the user to select one to view tasks for that date
def show_tasks():
    unique_dates = sorted(set(task['date'] for task in tasks), key=lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'), reverse=True)

    if not unique_dates:
        clear_terminal()
        print("No tasks found.")
        return

    print("\nUnique Dates with Tasks (Newest first):\n")
    for i, date in enumerate(unique_dates):
        print(f"{i:<5}{date}")

    try:
        date_index = int(input("\nEnter index of the date you want to view tasks for: "))
        selected_date = unique_dates[date_index]

        tasks_for_selected_date = [task for task in tasks if task['date'] == selected_date]

        if not tasks_for_selected_date:
            clear_terminal()
            print(f"No tasks found for the selected date: {selected_date}")
            return

        print("\nTasks for the selected date:\n")
        print("Index  Tracker                 Name                     Tracker                 Amount  Time Spent")
        for i, task in enumerate(tasks_for_selected_date):
            print(f"{i:<6}{task['tracker']:<25}{task['name']:<25}{task['tracker']:<25}{task['amount']:<8}{task['time_spent']}")

    except (ValueError, IndexError):
        clear_terminal()
        print("Invalid input or index.")

    input("\nPress any key to continue...")
    clear_terminal()

def modify_tracker():
    print_trackers()
    index = int(input("\n\nEnter index of tracker to modify: "))
    try:
        tracker = trackers[index]
        print("Selected tracker:", tracker["name"])
        print("Current number of amount:", tracker["amount"])
        name = input("change name?(y/"")")
        if name == "y":
            name = input("enter name: ")
            tracker["name"]=name
        amount = input("Enter number of amount to add or remove(r/""/n): ")
        if amount == "r":
            amount = input(": ")
            tracker["amount"] = int(amount)
        elif amount != "":
            tracker["amount"] += int(amount)
        else:
            pass
        print("Current number of days:", tracker["days_left"])
        days = input("Enter number of days to add or remove(r/""/n): ")
        if days == "r":
            days = input(": ")
            tracker["days_left"] = int(days)
        elif days != "":
            tracker["days_left"] += int(days)
        else:
            pass
        clear_terminal()
        print("tracker modified successfully.")
    except IndexError:
        print("Invalid index.")


# Clear the list of trackers
def flush_trackers():
    confirm = input("Are you sure you want to delete all trackers? (y/n) ")
    if confirm.lower() == "y":
        global trackers
        trackers = []
        print("trackers flushed successfully. remember to save!")
        clear_terminal()
        print("\nAll trackers removed successfully.")
    else:
        clear_terminal()
        print("cancelled.\n")

# Clear the list of tasks
def flush_tasks():
    confirm = input("Are you sure you want to delete all tasks? (y/n) ")
    if confirm.lower() == "y":
        global tasks
        tasks = []
        print("tasks flushed successfully. remember to save!")
        clear_terminal()
        print("\nAll tasks removed successfully.")
    else:
        clear_terminal()
        print("cancelled.\n")

# Show trackers divided into a time interval t
def show_trackers_by_length_interval():
    total_amount_read = sum(task["amount"] for task in tasks)
    total_amount_left = 0
    time_saved = 0
    total_time_spent = sum(task["time_spent"] for task in tasks)  # Calculate total amount time spent for all trackers

    print(f"\n\n{'='*80}\n{' '*15}TASKS BY INTERVAL\n{'='*80}\n")
    print(f"time studied for all tasks: {(total_time_spent)/60:.2f} hour(s)")
    time_spent_saved = 0
    print("\n\n")
    print(f"{'Name':<30} {'Amount worked':<15} {'Amount left':<15} {'time spent':<20} {'Left estimation':<20}")
    print("-" * 120)
    for tracker in trackers:
        amount = tracker.get("amount", 0)
        time_spent = 0
        amount_worked = 0 
        amount_left = 0
        time_estimated = 0

        # Calculate total amount and time spent in tasks for this tracker
        for task in tasks:
            if task["tracker"] == tracker["name"]:
                time_spent += task["time_spent"]
                amount_worked += task["amount"]

        amount_left = amount - amount_worked

        if amount_worked == 0:
            average_time_spent_per_amount = 0  # Avoid division by zero
        else:
            average_time_spent_per_amount = time_spent / amount_worked

        if amount_left > 0:
            time_estimated = average_time_spent_per_amount * amount_left / 60


        if amount == 0:
            amount = 1
        time_spent_estimated = time_spent / 60
        time_spent_saved += time_spent_estimated

        # estimation
        
        time_saved += time_estimated

        # Calculate the amount left by subtracting the amount_worked from the tracker's amount
        amount_left = amount - amount_worked
        total_amount_left += amount_left


        # Calculate the amount left by deducting the time_spent from the amount
        #amount_left = tracker["amount"] - amount_worked

        print(f"{tracker['name']:<30} {amount_worked:<15} {amount_left:<15} {time_spent_estimated:.2f} hours {' ' * 10} {time_estimated:.2f} hours  ")
    print("-" * 120)
    print(f"{'TOTAL':<30} {total_amount_read:<15} {total_amount_left:<15} {time_spent_saved:.2f} hours {' ' * 10} {time_saved:.2f} hours")
    print("-" * 120)
    input("\n\nPress any key to continue...")
    clear_terminal()

def view_statistics():
    clear_terminal()
    total_time = 0
    tracker_time = {}

    # Iterate over each task in tasks
    for task in tasks:
        tracker = task["tracker"]
        time_spent = int(task["time_spent"])

        # Update total time spent studying
        total_time += time_spent

        # Update tracker time dictionary
        if tracker in tracker_time:
            tracker_time[tracker] += time_spent
        else:
            tracker_time[tracker] = time_spent

    # Calculate average time spent studying per task
    num_tasks = len(tasks)
    avg_time = total_time / num_tasks if num_tasks > 0 else 0

    # Print statistics
    print(f"\n\nTotal time spent studying: {total_time} minutes / {total_time/60:.2f} hours")
    print(f"Average time spent studying per task: {avg_time:.2f} minutes / {avg_time/60:.2f} hours")
    if tracker_time:
        print("\n\n----------------------")
        print("Top 5 studied trackers:")
        print("----------------------")
        sorted_tracker = sorted(tracker_time, key=tracker_time.get, reverse=True)
        for i, tracker in enumerate(sorted_tracker[:5]):
            if tracker_time[tracker] < 60:
                print(f"{i + 1}. {tracker}: {tracker_time[tracker]} minutes")
            else:
                print(f"{i + 1}. {tracker}: {tracker_time[tracker]/60} hours")
    input("\n\npress any key to continue...")
    clear_terminal()

def fire():
    load_trackers()
    a= input(str("add one day or remove? (a/r): "))
    for tracker in trackers:
        if a ==  "a":
            tracker["days_left"] += 1
        elif a == "r":
            tracker["days_left"] -= 1
        else:
            print("invalid")
    save_trackers()
    clear_terminal()
    print("done!")


def add_missing_books():
    # Load data from bookprime.json and exercisetracker.json
    with open(BOOKP_DB, 'r') as book_file:
        books = json.load(book_file)
    with open(XTRACKER_DB, 'r') as tracker_file:
        trackers = json.load(tracker_file)

    # Find missing books
    missing_books = []
    for book in books:
        book_name = book["name"]
        matching_trackers = [tracker for tracker in trackers if tracker["name"] == book_name]
        if not matching_trackers and book["exercises"] > 0:
            missing_books.append(book)

    # Display missing books and prompt user to add
    if missing_books:
        print("The following books are missing from trackers:")
        for i, book in enumerate(missing_books):
            print(f"{i}. {book['name']} - Exercises: {book['exercises']}")

        choice = input("\nEnter the index of the exercise you want to add (or 'q' to quit): ")
        if choice.lower() != 'q':
            try:
                dayutt = []
                for tracker in trackers:
                    days = tracker["days_left"]
                    dayutt.append(days)
                dayutt.sort(key=lambda x: x)
                print("current occupied days are:",dayutt)
                daysz = int(input("Enter Days Left: "))
                index = int(choice)
                if 0 <= index < len(missing_books):
                    book = missing_books[index]
                    new_tracker = {
                        "name": book["name"],
                        "amount": book["exercises"],  # You mentioned mapping "chapters" to "amount"
                        "amount_desc": input("Enter Description for Amount: "),
                        "days_left": daysz
                    }
                    trackers.append(new_tracker)
                    print(f"Added '{book['name']}' to trackers.")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input.")
            
            # Save updated trackers to exercisetracker.json
            with open(XTRACKER_DB, 'w') as tracker_file:
                json.dump(trackers, tracker_file, indent=4)
    else:
        print("No missing books found.")

def toggle_tracker_status():
    clear_terminal()

    print("Toggle Tracker Status:")
    print("h. Hibernate a Tracker")
    print("a. Activate a Tracker")
    choice = input("Enter your choice (h/a): ")

    if choice == "h":
        # Hibernate a Tracker
        clear_terminal()
        print_trackers()
        index = int(input("\nEnter index of tracker to hibernate: "))

        if 0 <= index < len(trackers):
            # Get the selected tracker
            selected_tracker = trackers[index]

            # Load the unactivetrackersx.json file
            unactive_trackersx = []
            try:
                with open(XUNACTIVE_DB, 'r') as f:
                    unactive_trackersx = json.load(f)
            except FileNotFoundError:
                pass

            # Add the selected tracker to unactive_trackersx
            unactive_trackersx.append(selected_tracker)

            # Save unactive_trackersx to unactivetrackersx.json
            with open(XUNACTIVE_DB, 'w') as f:
                json.dump(unactive_trackersx, f, indent=4)

            # Remove the selected tracker from trackers
            del trackers[index]
            clear_terminal()
            print("Tracker hibernated successfully.")
        else:
            print("Invalid index.")

    elif choice == "a":
        # Activate a Tracker
        clear_terminal()

        # Load the unactivetrackersx.json file
        unactive_trackersx = []
        try:
            with open(XUNACTIVE_DB, 'r') as f:
                unactive_trackersx = json.load(f)
        except FileNotFoundError:
            clear_terminal()
            print("No trackers to activate.")
            return
        if len(unactive_trackersx) == 0:
            clear_terminal()
            print("No trackers to activate.")
            return

        print("Unactivated Trackers:")
        for i, tracker in enumerate(unactive_trackersx):
            print(f"{i}. {tracker['name']}")

        index = int(input("\nEnter index of tracker to activate: "))
        if 0 <= index < len(unactive_trackersx):
            # Get the selected tracker from unactive_trackersx
            selected_tracker = unactive_trackersx[index]

            # Add the selected tracker back to trackers
            trackers.append(selected_tracker)

            # Remove the selected tracker from unactive_trackersx
            unactive_trackersx.pop(index)

            # Save unactive_trackersx to unactivetrackersx.json
            with open(XUNACTIVE_DB, 'w') as f:
                json.dump(unactive_trackersx, f, indent=4)

            clear_terminal()
            print("Tracker activated successfully.")
        else:
            clear_terminal()
            print("Invalid index.")

    else:
        clear_terminal()
        print("Invalid choice.")

    save_trackers()



def load_tasks_from_file(file_path):
    tasks_from_file = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip the header line
                parts = line.strip().split(',')
                if len(parts) == 5:
                    task_name = parts[1].strip('"')
                    duration = int(parts[2])
                    tasks_from_file.append((task_name, duration))
    except FileNotFoundError:
        print("Tracker main file not found.")
    return tasks_from_file

def show_available_tasks(tasks_list):
    print("\nAvailable Tasks:")
    for index, (task_name, duration) in enumerate(tasks_list):
        print(f"{index}. {task_name} \t\t {math.floor(duration/60)} minutes")

def add_task_from_file():
    merge_duplicate_tasks()
    tasks_from_file = load_tasks_from_file(pomofile)
    
    if not tasks_from_file:
        #print("No tasks found in the file.")
        return
    print("\n\nNew Exercises found! wanna add them?")
    show_available_tasks(tasks_from_file)

    try:
        choice = int(input("\nEnter the index of the task you want to save: "))
        if 0 <= choice < len(tasks_from_file):
            selected_task = tasks_from_file[choice]
            print(f"\nSelected task: {selected_task[0]} \t\t {selected_task[1]} minutes")

            print_trackers()
            while True:
                try:
                    index = int(input("\n\nEnter index of tracker to add task: "))
                    tracker = trackers[index]
                    break
                except (ValueError, IndexError):
                    print("Invalid index. Please try again.")

            print("Selected tracker:", tracker["name"])
            name = input("Enter Name for the Task:")
            amount = int(input("Enter number of amount: "))
            time_spent = math.floor(selected_task[1]/60)
            date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%d-%m-%Y")

            task = {
                "name": name,
                "tracker": tracker["name"],
                "date": date,
                "time_spent": time_spent,
                "amount": amount
            }
            tasks.append(task)
            save_tasks()
            clear_terminal()
            print("Task added successfully.")

            # Remove the selected line from the file
            with open(pomofile, 'r') as file:
                lines = file.readlines()
            with open(pomofile, 'w') as file:
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 5 and parts[1].strip('"') != selected_task[0]:
                        file.write(line)

    except (ValueError, IndexError):
        print("Invalid input or index.")


def add_studying_tasks_from_file():
    # Load the existing trackers to check if a task is already added
    with open(XTRACKER_DB, 'r') as tracker_file:
        existing_trackers = json.load(tracker_file)

    # Load tasks from tasks.json
    try:
        with open('tasks.json', 'r') as tasks_file:
            tasks = json.load(tasks_file)
    except FileNotFoundError:
        print("tasks.json not found.")
        return

    # Filter tasks with status "Studying right now" and not already added as trackers
    studying_tasks = []
    for task in tasks:
        if task.get("status") == "Studying right now":
            task_name = task.get("name")
            if not any(tracker["name"] == task_name for tracker in existing_trackers):
                studying_tasks.append(task)

    # List available studying tasks
    if not studying_tasks:
        print("No tasks with status 'Studying right now' to add as trackers.")
        return

    print("\nAvailable Tasks to Add as Trackers:")
    for index, task in enumerate(studying_tasks):
        print(f"{index}. {colors.CYAN}{task['name']}- Deadline: {task['deadline']}){colors.RESET}")

    try:
        choice = int(input("\n\nEnter the index of the task you want to add as a tracker (or q to cancel): "))

        if choice == 'q':
            return

        if 0 <= choice < len(studying_tasks):
            selected_task = studying_tasks[choice]

            # Calculate the deadline by subtracting the saved date from today's date
            saved_date = datetime.datetime.strptime(selected_task["deadline"], "%d-%m-%Y")
            days_left = (saved_date - datetime.datetime.now()).days+1

            # Ask for a description
            description = input("Enter a description for this tracker: ")
            amount = int(input("Enter amount for the tracker: "))

            # Create a new tracker based on the selected task
            new_tracker = {
                "name": selected_task["name"],
                "amount": amount,  # You may want to set this to an appropriate value
                "amount_desc": description,
                "days_left": days_left
            }

            # Add the new tracker to the existing trackers
            existing_trackers.append(new_tracker)

            # Save the updated trackers to exercisetracker.json
            with open(XTRACKER_DB, 'w') as tracker_file:
                json.dump(existing_trackers, tracker_file, indent=4)

            clear_terminal()
            print(f"Added '{new_tracker['name']}' as a tracker with {days_left} days left and description: '{description}'.")

        else:
            clear_terminal()
            print("Invalid index.")

    except (ValueError, IndexError):
        clear_terminal()
        print("Invalid input or index.")

def merge_duplicate_tasks():
    try:
        # Read tasks from taskmain.txt and create a dictionary to store merged tasks
        merged_tasks = {}
        with open(pomofile, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip the header line
                parts = line.strip().split(',')
                if len(parts) == 5:
                    task_name = parts[1].strip('"')
                    duration = int(parts[2])
                    if task_name in merged_tasks:
                        # If task with the same name exists, merge run times
                        merged_tasks[task_name] += duration
                    else:
                        # If task is not in the dictionary, add it with its run time
                        merged_tasks[task_name] = duration
        
        # Write merged tasks back to taskmain.txt
        with open(pomofile, 'w') as file:
            file.write("Index,Task,Duration,Start Time,End Time\n")
            for index, (task_name, duration) in enumerate(merged_tasks.items()):
                file.write(f"{index},{task_name},{duration},,\n")
        
        print("Duplicate tasks merged and saved successfully.")
    except FileNotFoundError:
        print("taskmain.txt file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Load the trackers data from the file at program start
load_trackers()
load_tasks()
clear_terminal()
update_trackers_and_remove_days()
add_task_from_file()
add_studying_tasks_from_file()

# Main menu loop
def main():
    while True:
        load_trackers()
        load_tasks()
        print(f"\n{colors.YELLOW}||Exercise Tracker||{colors.RESET}\n\n{colors.GREEN}Menu:{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add tracker{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}add a task{colors.RESET}")
        print(f"{colors.CYAN}i.{colors.RESET} {colors.YELLOW}import from Books{colors.RESET}")
        print(f"{colors.CYAN}k.{colors.RESET} {colors.YELLOW}import from Tasks{colors.RESET}")
        print(f"{colors.CYAN}g.{colors.RESET} {colors.YELLOW}greedy algorithm{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show trackers{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET} {colors.YELLOW}Show Length interval{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Show Statistics{colors.RESET}")
        print(f"{colors.CYAN}ss.{colors.RESET} {colors.YELLOW}show tasks{colors.RESET}")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Edit notes{colors.RESET}")
        print(f"{colors.CYAN}ft.{colors.RESET} {colors.YELLOW}Flush trackers{colors.RESET}")
        print(f"{colors.CYAN}fs.{colors.RESET} {colors.YELLOW}Flush tasks{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET} {colors.YELLOW}Modify tracker{colors.RESET}")
        print(f"{colors.CYAN}h.{colors.RESET} {colors.YELLOW}Hibernate Tracker{colors.RESET}")
        print(f"{colors.CYAN}rt.{colors.RESET} {colors.YELLOW}Remove tracker{colors.RESET}")
        print(f"{colors.CYAN}rs.{colors.RESET} {colors.YELLOW}Remove tasks{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}(experimental){colors.RESET}")
        print(f"{colors.CYAN}v.{colors.RESET} {colors.YELLOW}save{colors.RESET}")
        print(f"{colors.CYAN}o.{colors.RESET} {colors.YELLOW}load{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter choice: ")

        if choice == "a":
            clear_terminal()
            add_tracker()
            save_trackers()
        elif choice == "t":
            clear_terminal()
            add_task()
            save_tasks()
        elif choice == "g":
            clear_terminal()
            tracker_greedy()
            input("\n\npress any key to continue...")
            clear_terminal()
        elif choice == "h":
            clear_terminal()
            toggle_tracker_status()
            save_tasks()
        elif choice == "ss":
            clear_terminal()
            show_tasks()
            save_tasks()
            save_trackers()
        elif choice == "k":
            clear_terminal()
            add_studying_tasks_from_file()
        elif choice == "i":
            clear_terminal()
            add_missing_books()
            save_tasks()
            load_tasks()
        elif choice == "l":
            clear_terminal()
            view_statistics()
        elif choice == "rt":
            clear_terminal()
            remove_tracker()
            save_trackers()
        elif choice == "rs":
            clear_terminal()
            remove_task()
            save_tasks()
        elif choice == "m":
            clear_terminal()
            modify_tracker()
            save_trackers()
        elif choice == "s":
            clear_terminal()
            print_trackers()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == "ft":
            clear_terminal()
            flush_trackers()
        elif choice == "fs":
            clear_terminal()
            flush_tasks()
        elif choice == "d":
            clear_terminal()
            show_trackers_by_length_interval()
        elif choice == "v":
            clear_terminal()
            save_trackers()
            save_tasks()
            save_todays_date()
            clear_terminal()
        elif choice == "n":
            clear_terminal()
            edit_notes()
        elif choice == "f":
            clear_terminal()
            fire()
        elif choice == "q":
            clear_terminal()
            break
        elif choice == "o":
            load_trackers()
            load_tasks()
        else:
            clear_terminal()

if __name__ == '__main__':
    main()