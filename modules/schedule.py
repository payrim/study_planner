import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from utils.clearterminal import clear_terminal
from utils import colors
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
    schedule_lines = get_schedule_output().strip().split('\n')
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
            activities_found = True 
            if print_output == True:
                print(f"{colors.space*7}{colors.CYAN}got scheduled activity: {colors.WPURPLE}{line}{colors.RESET}") 
            return activities_found
            
    if print_output == True:
        if not activities_found:
            print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")
            return False


def get_schedule_output():
    output = []
    with open(SCH_TXT, 'r') as file:
        lines = file.readlines()
    
    print_schedule = False
    for line in lines:
        line = line.strip()  
        if line.startswith('#') and day_names[current_day] in line:
            print_schedule = True
            output.append(f"{colors.CYAN}{line}{colors.RESET}")
        elif print_schedule and line: 
            output.append(f"{colors.BLUE}{line}{colors.RESET}")  
        elif print_schedule and not line: 
            break
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

def plot_schedule(schedule):
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


def select_task_from_jobs():
    schedule_lines = get_schedule_output().strip().split('\n')
    schedule_output = '\n'.join(schedule_lines[1:])
    current_time = datetime.now().strftime('%H:%M')
    current_time = datetime.strptime(current_time, '%H:%M')
    activities_found = False

    try:
        for line in schedule_output.split('\n'):
            line = remove_color_codes(line.strip())
            start_time, end_time, activity = line.split(' - ')
            start_time = datetime.strptime(start_time, '%H:%M')
            end_time = datetime.strptime(end_time, '%H:%M')
            if start_time <= current_time <= end_time:
                clear_terminal()
                print(f"\n\n\n{colors.YELLOW}you already have a schedule:{colors.RESET}")
                print(f"{colors.CYAN}{line}{colors.RESET}")
                activities_found = True
    except: 
        activities_found = False


    if not activities_found:
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

        print(f"\n{colors.YELLOW}Available tasks:{colors.RESET}")
        print(json.dumps(graph, indent=4))  
        print(f"\n{colors.WPURPLE}0. Add a New Task{colors.RESET}")
        while True:
            selected_option = input(f"{colors.YELLOW}Select a task or choose 0 to manually add a new task: {colors.RESET}")
            if selected_option == '0':
                new_task = input(f"Enter the new task: ")
                selected_task = new_task
                break
            elif selected_option in graph:
                selected_task = selected_option
                break
            else:
                print(f"{colors.RED}Invalid selection. Please select a valid task or 0 to add a new task.{colors.RESET}")
        
        print(f"You selected task: {selected_task}")
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


def show_and_mark_tasks():
    with open(JobDB, 'r') as file:
        data = json.load(file)
    
    tasks = data['tasks']
    
    if not tasks:
        print(f"{colors.YELLOW}No tasks saved in JobDB.{colors.RESET}")
        return
    
    print("Tasks saved in JobDB:")
    for idx, task in enumerate(tasks, start=1):
        print(f"{colors.YELLOW}{idx}. {task}{colors.RESET}")

    while True:
        try:
            task_index = int(input(f"\n{colors.YELLOW}Select a task number to mark as done (0 to cancel): {colors.RESET}"))
            if task_index == 0:
                break
            elif 1 <= task_index <= len(tasks):
                selected_task = tasks[task_index - 1]
                print(f"You selected task: {selected_task}")
                mark_as_done = input(f"Have you done this task? (yes/no): ").lower()
                if mark_as_done == 'yes':
                    # Mark the task as done
                    print(f"Task '{selected_task}' marked as done.")
                    # Check if there's a connected node after the task
                    if task_index < len(tasks):
                        connected_node = tasks[task_index]
                        print(f"Connected node: {connected_node}")
                        replace_with_connected_node = input(f"Do you want to work on '{connected_node}' next? (yes/no): ").lower()
                        if replace_with_connected_node == 'yes':
                            tasks[task_index - 1] = connected_node
                            tasks.pop(task_index)  # Remove the connected node from the list
                            print(f"Task '{connected_node}' added to the task list.")
                        else:
                            clear_terminal()
                            tasks.pop(task_index - 1)  # Remove the current task from the list
                            print(f"Task '{selected_task}' removed from JobDB.")
                    else:
                        tasks.pop(task_index - 1)  # Remove the current task from the list
                        print(f"Task '{selected_task}' removed from JobDB.")
                    # Save the updated tasks back to JobDB
                    with open(JobDB, 'w') as file:
                        json.dump(data, file)
                else:
                    print(f"Task '{selected_task}' not marked as done.")
                break
            else:
                print(f"{colors.RED}Invalid task number. Please select a valid task number.{colors.RESET}")
        except ValueError:
            print(f"{colors.RED}Invalid input. Please enter a number.{colors.RESET}")


def schedleft():
    schedule_lines = get_schedule_output().strip().split('\n')
    print("\n\n"+schedule_lines[0])
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
            print(f"{colors.BLUE}{line}{colors.RESET}") 
            activities_found = True 

    if not activities_found:
        print(f"\n\n{colors.space*3}{colors.WWITE}No scheduled activities for today at the current time.{colors.RESET}")

    input(f"\n\n{colors.space*3}{colors.YELLOW}Press any key to continue...{colors.RESET}")



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
                    print(f"JobDB is empty.")
        except FileNotFoundError:
            print(f"{colors.RED}JobDB not found. Please create tasks first.{colors.RESET}")


def main():
    while True:
        print(f"\n{colors.YELLOW}||Schedule Program||{colors.RESET}\n")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}change Schedules{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show Schedules{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Show Tody's left schedule{colors.RESET}")
        print(f"{colors.CYAN}p.{colors.RESET} {colors.YELLOW}Show Chart{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Show Schedule by Current Time{colors.RESET}")
        print(f"{colors.CYAN}w.{colors.RESET} {colors.YELLOW}swap places{colors.RESET}")
        print(f"{colors.CYAN}k.{colors.RESET} {colors.YELLOW}select a task{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}complete a task{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}print first task{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}quit{colors.RESET}")
        choice = input("\nEnter choice: ")
        if choice == "s":
            clear_terminal()
            print("\n\n"+get_schedule_output())
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
        elif choice == "t": 
            clear_terminal()
            show_schedule_by_time(print_output=True)
            input(f"\n{colors.space*2}{colors.YELLOW}Press any key to continue...{colors.RESET}")
            clear_terminal()
        elif choice == "p":
            clear_terminal()
            schedule = parse_schedule(SCH_TXT)
            plot_schedule(schedule)
            clear_terminal()
        elif choice == "k":
            select_task_from_jobs()
        elif choice == "w":
            swap_tasks_in_jobdb()
        elif choice == "f":
            clear_terminal()
            print("\n\n")
            print_first_entry_from_json()
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