import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from utils.clearterminal import clear_terminal
from utils import colors
from estimations import estimation
import json, random, os, re

current_day = datetime.now().weekday()
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
JOB_TXT = os.path.join(colors.notes_file, 'jobtodo.txt')
JobDB = os.path.join(colors.notes_file, 'jobdo.json')
TIMEJC = os.path.join(colors.notes_file, 'timejc.json')
EBDB = os.path.join(colors.notes_file, 'endeavors.json')


def remove_color_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def edit_notes():
    filechoose = int(input(f"\n{colors.YELLOW}||list||\n\n{colors.YELLOW}1.schedule\n{colors.YELLOW}2.job\n\n{colors.WWITE}select the one you want to edit: "))
    if os.name == 'nt':
        if filechoose == 1:
            notes_file = "C:\\Program Files\\Planner\\plan.txt"
        else:
            notes_file = "C:\\Program Files\\Planner\\jobtodo.txt"
        editor = 'notepad'
    else:
        if filechoose == 1:
            notes_file = os.path.expanduser("./plan.txt")
        else:
            notes_file = os.path.expanduser("./jobtodo.txt")
        editor = 'nvim'
    os.system(f"{editor} {notes_file}")


def show_schedule_by_time(print_output):
    schedule_lines = get_schedule_output(lastl=False).strip().split('\n')
    schedule_output = '\n'.join(schedule_lines[1:])
    current_time = datetime.now().strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    activities_found = False  
    for line in schedule_output.split('\n'):
        line = remove_color_codes(line.strip())
        start_time, end_time, activity = line.split(' - ')
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M') 
        if start_time <= current_time <= end_time:
            if not activity == "free":
                activities_found = True
            if print_output == True:
                try:
                    with open(JobDB, 'r') as file:
                        data = json.load(file)
                        tasks = data.get('tasks', [])
                        if tasks:
                            first_entry = tasks[0]
                except:
                    pass
                print(f"{colors.space*7}{colors.CYAN}got scheduled activity: {colors.WPURPLE}{line}{colors.PURPLE} /{first_entry}{colors.RESET}") 
            return activities_found
            
    if print_output == True:
        if not activities_found:
            print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")
            return False


def get_schedule_output(lastl):
    output = []
    free_activities_hours = {}

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    print_schedule = False
    for line in lines:
        line = line.strip()
        if line.startswith('#') and day_names[current_day] in line:
            current_day_name = day_names[current_day]
            print_schedule = True
            output.append(f"{colors.CYAN}{line}{colors.RESET}")
            free_activities_hours[current_day_name] = 0  
        elif print_schedule and line:
            if line.endswith('*'):
                output.append(f"{colors.space*2}{colors.WPURPLE}{line}{colors.RESET}")
            elif line.endswith('course studies'):
                output.append(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}")
            elif line.endswith('$'):
                output.append(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}")
            elif line.endswith('free'):
                output.append(f"{colors.space*2}{colors.YELLOW}{line}{colors.RESET}")
            else:
                output.append(f"{colors.space*2}{colors.BLUE}{line}{colors.RESET}")

            start_time, end_time, activity = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if activity.strip() == "free":
                free_activities_hours[current_day_name] += activity_hours

        elif print_schedule and not line:
            break
    
    if lastl == True:
        for day, total_hours in free_activities_hours.items():
            output.append(f"{colors.space*2}{colors.WPURPLE}{day} - Total Free Hours: {total_hours:.2f} hours{colors.RESET}")

    return '\n'.join(output)


def parse_schedule(JobDB):
    schedule = {}
    with open(JobDB, 'r') as file:
        lines = file.readlines()
        current_day = None
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                current_day = line[2:]
                schedule[current_day] = []
            elif line:  
                start_time, end_time, activity = line.split(' - ')
                schedule[current_day].append((start_time.strip(), end_time.strip(), activity.strip()))
    return schedule

def plot_schedule():
    schedule = parse_schedule(SCH_TXT)
    days = list(schedule.keys())
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xticks(range(len(days)))
    ax.set_xticklabels(days)
    ax.set_xticks([x - 0.5 for x in range(1, len(days))], minor=True)
    ax.invert_yaxis()  

    for i, (day, activities) in enumerate(schedule.items()):
        for start, end, activity in activities:
            start_time = datetime.strptime(start, '%H:%M')
            end_time = datetime.strptime(end, '%H:%M')
            duration = end_time - start_time
            color = random.choice(['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightsteelblue', 'lightpink'])
            rect = plt.Rectangle((i - 1.0 / 2, start_time.hour + start_time.minute / 60), 1.0, duration.seconds / 3600, color=color, edgecolor='black')
            ax.add_patch(rect)
            ax.text(i, start_time.hour + start_time.minute / 60 + duration.seconds / 7200, activity, ha='center')

    ax.set_ylabel('')
    ax.set_title('weekly schedule',y=-0.08)
    ax.xaxis.tick_top()
    plt.grid(axis='x', linestyle='--', linewidth=0.7, color='gray', which='minor')  
    plt.ylim(24, 0)
    plt.grid(False)
    ax.autoscale(enable=True, axis='both', tight=True)
    ax.use_sticky_edges = False
    plt.show()

 
def schedleft(lastl=False):
    schedule_lines = get_schedule_output(lastl=False).strip().split('\n')
    print(f"\n\n{colors.space*2}{schedule_lines[0]}")
    schedule_output = '\n'.join(schedule_lines[1:])
    current_time = datetime.now().strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    activities_found = False  
    for line in schedule_output.split('\n'):
        line = remove_color_codes(line.strip())
        start_time, end_time, activity = line.split(' - ')
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M') 
        if current_time <= end_time:
            activities_found = True 
            if line.endswith('*'):
                print(f"{colors.space*2}{colors.WPURPLE}{line}{colors.RESET}") 
            elif line.endswith('course studies'):
                print(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}")
            elif line.endswith('$'):
                print(f"{colors.space*2}{colors.GREEN}{line}{colors.RESET}") 
            elif line.endswith('free'):
                print(f"{colors.space*2}{colors.YELLOW}{line}{colors.RESET}") 
            else:
                print(f"{colors.space*2}{colors.BLUE}{line}{colors.RESET}") 

    if not activities_found:
        print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")

    input(f"\n\n{colors.space*3}{colors.YELLOW}Press any key to continue...{colors.RESET}")

def select_task_from_jobs():
    clear_terminal()
    with open(JOB_TXT, 'r') as file:
        tasks = file.readlines()

    graph = {}
    for task in tasks:
        nodes = task.strip().split(' - ')
        current_node = graph
        for node in nodes:
            if node not in current_node:
                current_node[node] = {}
            current_node = current_node[node]

    print("\n"+colors.WPURPLE+"Available tasks:")
    print(json.dumps(graph, indent=4)) 
    selected_task = input(f"{colors.YELLOW}Enter the new task: {colors.RESET}")
    try:
        with open(JobDB, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'tasks': []}

    data['tasks'].append(selected_task)
    with open(JobDB, 'w') as file:
        json.dump(data, file)
    clear_terminal()
    print(f"Task '{selected_task}' saved in JobDB.")


def swap_tasks_in_jobdb():
    clear_terminal()
    with open(JobDB, 'r') as file:
        try:
            data = json.load(file)
        except FileNotFoundError:
            print(f"{colors.RED}JobDB not found. Please create tasks first.{colors.RESET}")
            return
    tasks = data.get('tasks', [])
    print(f"\n{colors.YELLOW}Current tasks in JobDB:{colors.RESET}")
    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.CYAN}{idx}. {task}{colors.RESET}")

    while True:
        try:
            task_index1 = int(input(f"\nEnter the index of the first task to swap:"))
            task_index2 = int(input(f"Enter the index of the second task to swap:"))
            if 1 <= task_index1 <= len(tasks) and 1 <= task_index2 <= len(tasks):
                tasks[task_index1 - 1], tasks[task_index2 - 1] = tasks[task_index2 - 1], tasks[task_index1 - 1]
                data['tasks'] = tasks

                with open(JobDB, 'w') as file:
                    json.dump(data, file)
                clear_terminal()
                print(f"Tasks at positions {task_index1} and {task_index2} swapped successfully.")
                break
            else:
                clear_terminal()
                print(f"{colors.RED}Invalid task indices. Please enter valid indices.{colors.RESET}")
        except ValueError:
            clear_terminal()
            print(f"{colors.RED}Invalid input. Please enter valid numbers.{colors.RESET}")

def show_and_mark_tasks():
    with open(JobDB, 'r') as file:
        data = json.load(file)
    
    tasks = data['tasks']

    with open(JOB_TXT, 'r') as file:
        words = file.readlines()

    words = [word.strip().split(' - ') for word in words]

    
    if not tasks:
        print(f"{colors.YELLOW}No tasks saved in JobDB.{colors.RESET}")
        return
    
    print(f"{colors.CYAN}Tasks saved in JobDB:")
    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.YELLOW}{idx}. {task}{colors.RESET}")

    while True:
        try:
            task_index = int(input(f"\n{colors.WWITE}Select a task number to mark as done (0 to cancel): {colors.RESET}"))
            if task_index == 0:
                clear_terminal()
                break
            elif 1 <= task_index <= len(tasks):
                selected_task = tasks[task_index - 1]
                print(f"{colors.YELLOW}You selected task: {selected_task}")
                mark_as_done = input(f"{colors.WPURPLE}Have you done this task? (yes/no): {colors.RESET}").lower()
                if mark_as_done == 'yes':
                    mark_as_done_task(str(selected_task))
                    time_taken = input(f"{colors.WPURPLE}How many minutes did it take you to finish the task? {colors.RESET}")
                    try:
                        time_taken = int(time_taken)
                    except ValueError:
                        print(f"{colors.RED}Invalid input. Please enter a number.{colors.RESET}")
                        continue

                    completed_task = {
                        "task": selected_task,
                        "time_taken": time_taken,
                        "completed_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    if not os.path.exists(TIMEJC):
                        with open(TIMEJC, 'w') as time_file:
                            json.dump([completed_task], time_file, indent=4)
                    else:
                        with open(TIMEJC, 'r+') as time_file:
                            time_data = json.load(time_file)
                            time_data.append(completed_task)
                            time_file.seek(0)
                            json.dump(time_data, time_file, indent=4)
                    
                    matching_word = None
                    for word in words:
                        if selected_task in word:
                            matching_word = word
                            break

                    if matching_word:
                        if selected_task == matching_word[-1]:
                            pass
                        else:
                            print(f"{colors.WPURPLE}The selected task matches a word in your list: {matching_word}{colors.RESET}")
                            replace_task = input(f"{colors.WPURPLE}Do you want to replace it with the next word? (yes/no): {colors.RESET}").lower()
                            if replace_task == 'yes':
                                replace_index = matching_word.index(selected_task)
                                next_word_index = (replace_index + 1) % len(matching_word)
                                selected_task = matching_word[next_word_index]
                                clear_terminal()
                                print(f"\n\nTask replaced with: {selected_task}")

                                tasks[task_index - 1] = selected_task
                                data['tasks'] = tasks

                                with open(JobDB, 'w') as file:
                                    json.dump(data, file, indent=4)
                                break



                    tasks.pop(task_index - 1)
                    clear_terminal()  
                    print(f"\n\nTask '{selected_task}' removed from JobDB.")
                with open(JobDB, 'w') as file:
                    json.dump(data, file)
            else:
                print(f"Task '{selected_task}' not marked as done.")
            break
        except ValueError:
            print(f"{colors.RED}Invalid input. Please enter a number.{colors.RESET}")


def print_first_entry_from_json():
    line = show_schedule_by_time(print_output=False)
    if line == True:
       show_schedule_by_time(print_output=True)
    else:
        try:
            with open(JobDB, 'r') as file:
                data = json.load(file)
                tasks = data.get('tasks', [])
                if tasks:
                    first_entry = tasks[0]
                    print(f"{colors.space*7}{colors.WPURPLE}Active task: {first_entry}{colors.RESET}")
                else:
                    print(f"{colors.space*7}{colors.BLUE}JobDB is empty")
        except FileNotFoundError:
            print(f"{colors.RED}{colors.space*7}JobDB not found. Please create tasks first.{colors.RESET}")


def view_statistics():
    clear_terminal()

    try:
        with open(TIMEJC, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{colors.RED}No data available in TIMEJC. Please complete tasks first.{colors.RESET}")
        input("\n\nPress any key to continue...")
        clear_terminal()
        return

    total_time = 0
    task_count = len(data)
    tracker_time = {}

    for task in data:
        time_taken = int(task["time_taken"])
        total_time += time_taken

        task_name = task["task"]
        if task_name in tracker_time:
            tracker_time[task_name] += time_taken
        else:
            tracker_time[task_name] = time_taken

    avg_time = total_time / task_count if task_count > 0 else 0

    clear_terminal()
    print(f"\n\nTotal time spent on completed tasks: {total_time} minutes / {total_time / 60:.2f} hours")
    print(f"Average time spent on tasks: {avg_time:.2f} minutes / {avg_time / 60:.2f} hours")
    if tracker_time:
        print("\n\n----------------------")
        print("Top 5 completed tasks:")
        print("----------------------")
        sorted_tasks = sorted(tracker_time, key=tracker_time.get, reverse=True)
        for i, task_name in enumerate(sorted_tasks[:5]):
            if tracker_time[task_name] < 60:
                print(f"{i + 1}. {task_name}: {tracker_time[task_name]} minutes")
            else:
                print(f"{i + 1}. {task_name}: {tracker_time[task_name] / 60:.2f} hours")

    input("\n\nPress any key to continue...")
    clear_terminal()

def mark_as_done_task(task_name):
    try:
        with open(EBDB, 'r') as file:
            endeavors_data = json.load(file)
    except FileNotFoundError:
        return

    for endeavor in endeavors_data:
        if endeavor.get("name") == task_name:
            endeavor["done"] = True
            break

    with open(EBDB, 'w') as file:
        json.dump(endeavors_data, file, indent=4)


def calculate_and_print_free_hours():
    workperday = estimation.tracker_greedy(rint=False)
    free_activities_hours = {day_name: 0 for day_name in day_names.values()}  
    project_activities_hours = {day_name: 0 for day_name in day_names.values()}  

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    current_day_name = None
    for line in lines:
        line = line.strip()
        if line.startswith('#') and line[2:] in day_names.values():
            current_day_name = line[2:]
        elif current_day_name and line:
            start_time, end_time, activity = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if activity.strip() == "free":
                free_activities_hours[current_day_name] += activity_hours
            elif activity.strip() == "project time":
                project_activities_hours[current_day_name] += activity_hours

    print(f"\n\n{colors.YELLOW}{colors.space*2}||Total Free Hours for Each Day||")
    total_sum_free = 0
    total_sum_project = 0
    for day, total_hours in free_activities_hours.items():
        total_sum_free += total_hours
    for day, total_hours_project in project_activities_hours.items():
        total_sum_project += total_hours_project
    workamount_free = workperday*7/total_sum_free
    workamount_project = workperday*7/total_sum_project
    for day, total_hours in free_activities_hours.items():
        total_hours_project = project_activities_hours.get(day, 0)
        print(f"{colors.space*3}{day} - {total_hours:.2f} hours {colors.GREEN}(and can do work is {workamount_free*total_hours:.2f}){colors.WPURPLE} (P:{total_hours_project:.2f}) {colors.RESET}")
        
    print(f"\n{colors.CYAN}{colors.space*2}Total Free Hours for the Week: {total_sum_free:.2f} hours")
    print(f"{colors.WPURPLE}{colors.space*2}Total Project Hours for the Week: {total_sum_project:.2f} hours")
    print(f"{colors.CYAN}{colors.space*2}work per average and week: {workperday:.2f} and {workperday*7:.2f}")
    print(f"{colors.CYAN}{colors.space*2}work per hour is: {workamount_free:.2f}")
    return total_sum_free


def sum_and_print_activities():
    activity_sums = {
        "Free": 0,
        "Project Time": 0,
        "Classes": 0,
        "course studies": 0,
        "Assigned tasks": {},
        "Other stuff": 0,
        "Sleep": 42
    }

    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.endswith('$'):
            start_time, end_time, task = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            if task in activity_sums["Assigned tasks"]:
                activity_sums["Assigned tasks"][task] += activity_hours
            else:
                activity_sums["Assigned tasks"][task] = activity_hours
        elif line.endswith('*'):
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["Classes"] += activity_hours
        elif "course studies" in line.lower():
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["course studies"] += activity_hours
        elif "free" in line.lower():
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["Free"] += activity_hours
        elif "project time" in line.lower():
            start_time, end_time, _ = line.split(' - ')
            activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
            activity_sums["Project Time"] += activity_hours
        else:
            if len(line.split(' - ')) == 3:
                start_time, end_time, _ = line.split(' - ')
                #print(_)
                activity_hours = (datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')).seconds / 3600
                activity_sums["Other stuff"] += activity_hours

    print(f"\n{colors.CYAN}{colors.space*2}Activity Sums for the Week:")
    for activity, total_hours in sorted(activity_sums.items(), key=lambda x: sum(x[1].values()) if isinstance(x[1], dict) else x[1], reverse=True):
        if activity == "Assigned tasks":
            total_assigned_hours = sum(total_hours.values())
            print(f"{colors.space*3}{activity}: {total_assigned_hours:.2f} hours{{")
            for task, hours in sorted(total_hours.items(), key=lambda x: x[1], reverse=True):
                print(f"{colors.CYAN}{colors.space*7}{task[:-1]}: {hours:.2f} hours {colors.RESET}")
            print(f"{colors.space*5}}}")
        else:
            print(f"{colors.space*3}{activity}: {total_hours:.2f} hours")

def show_tasks():
    with open(JobDB, 'r') as file:
        data = json.load(file)
    
    tasks = data['tasks']

    with open(JOB_TXT, 'r') as file:
        words = file.readlines()

    words = [word.strip().split(' - ') for word in words]

    
    if not tasks:
        print(f"{colors.YELLOW}No tasks saved in JobDB.{colors.RESET}")
        return
    
    print(f"\n\n{colors.space*7}{colors.CYAN}Tasks saved in JobDB")
    print(f"{colors.space*7}{colors.CYAN}{colors.line2*50}")
    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.space*8}{colors.GREEN}{idx}.{colors.YELLOW} {task}{colors.RESET}")

def show_schedule_py():
    activities_found = None  # Initialize the variable before the loop
    schedule_lines = get_schedule_output(lastl=False).strip().split('\n')
    schedule_output = '\n'.join(schedule_lines[1:])
    current_time = datetime.now().strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    
    for line in schedule_output.split('\n'):
        line = remove_color_codes(line.strip())
        start_time, end_time, activity = line.split(' - ')
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M') 
        if start_time <= current_time <= end_time:
            if not activity == "free":
                activities_found = line
            print(f"{colors.space*7}{colors.CYAN}got scheduled activity: {colors.WPURPLE}{line}{colors.RESET}") 
    if activities_found is None:
        print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")
    return activities_found


def main():
    while True:
        print("\n\n")
        print_first_entry_from_json()
        print(f"\n{colors.YELLOW}||Schedule Program||{colors.RESET}\n")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Change Schedules{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show Schedules{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Show Tody's left schedule{colors.RESET}")
        print(f"{colors.CYAN}p.{colors.RESET} {colors.YELLOW}Show Chart{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Show Schedule by Current Time{colors.RESET}")
        print(f"{colors.CYAN}w.{colors.RESET} {colors.YELLOW}Swap places{colors.RESET}")
        print(f"{colors.CYAN}k.{colors.RESET} {colors.YELLOW}Select a task{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Complete a task{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET} {colors.YELLOW}Show statistics{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Print week's free time and activities.{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Print week's time{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter choice: ")
        if choice == "s":
            clear_terminal()
            print("\n\n"+get_schedule_output(lastl=True))
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "n":
            clear_terminal()
            edit_notes()
            clear_terminal()
        elif choice == "l":
            clear_terminal()
            schedleft()
            clear_terminal()
        elif choice == "d":
            clear_terminal()
            view_statistics()
            clear_terminal()
        elif choice == "t": 
            clear_terminal()
            print("\n\n")
            show_schedule_by_time(print_output=True)
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "g": 
            clear_terminal()
            print("\n\n")
            sum_and_print_activities()
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "p":
            clear_terminal()
            plot_schedule()
            clear_terminal()
        elif choice == "k":
            select_task_from_jobs()
        elif choice == "w":
            swap_tasks_in_jobdb()
        elif choice == "f":
            clear_terminal()
            calculate_and_print_free_hours()
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "c":
            clear_terminal()
            show_and_mark_tasks()
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()