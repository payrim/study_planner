import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from moviepy.editor import VideoFileClip
from tabulate import tabulate
from tqdm import tqdm
from utils.clearterminal import clear_terminal
from utils import colors

    
LECTURES_FILE = os.path.join(colors.notes_file, "lectures.json")

def init():
    try:
        with open(LECTURES_FILE, 'r') as f:
            lectures = json.load(f)
            for d in lectures:
                d["deadline"] = datetime.strptime(d["deadline"], "%Y-%m-%d").date()
            update_index(lectures)
            return lectures
    except FileNotFoundError:
        return []

def update_index(lectures):
    for i, lecture in enumerate(lectures):
        lecture["index"] = i + 1

def save(lectures):
    clear_terminal()
    with open(LECTURES_FILE, 'w') as f:
        lectures_copy = lectures.copy()
        for lec in lectures_copy:
            if isinstance(lec['deadline'], datetime):
                lec['deadline'] = lec['deadline'].strftime('%d-%m-%Y')
        json.dump(lectures_copy, f, indent=4, default=str)

def get_video_duration(filepath):
    try:
        exiftool_cmd = [
            "exiftool", "-n", "-q", "-p",
            "${Duration;our $sum;$_=ConvertDuration($sum+=$_)}",
            filepath
        ]
        result = subprocess.run(exiftool_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return 0

def get_video_duration_ffprobe(filepath):
    try:
        ffprobe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filepath]
        result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        duration = float(result.stdout.strip())/60
        return round(duration)  # Round the duration to the nearest second
    except Exception as e:
        print(f"Error: {e}")
        return 0

def scan_directory(directory):
    video_files = {}
    total_files = sum([len(files) for _, _, files in os.walk(directory)])

    progress_bar = tqdm(total=total_files, desc="Scanning videos", unit="file", dynamic_ncols=True)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                filepath = os.path.join(root, file)
                duration = get_video_duration_ffprobe(filepath)
                video_files[filepath] = duration
                progress_bar.update(1)

    progress_bar.close()
    return video_files

def add_lecture(lectures):
    clear_terminal()
    name = input("\nEnter video name: ")

    # Ask if the user wants to add the duration manually or scan the video file
    duration_choice = input("Do you want to add the duration manually (Y/N)? ").lower()
    if duration_choice == "y":
        duration_str = input("Enter video duration (HH:MM): ")
        duration_hour, duration_minute = map(int, duration_str.split(":"))
        duration = duration_hour * 60 + duration_minute
        manual = 1  # Added manually
    else:
        directory = input("Enter the directory path for the video files: ")
        video_files = scan_directory(directory)
        duration = sum(video_files.values())
        manual = 0  # Added from a directory
        time_left_str = f"{duration // 60:02d}:{duration % 60:02d}"  # format the time_left as HH:MM
        print(f"the duration is: {time_left_str}")


    # Ask for the deadline (same as before)
    deadline_input = input("Enter deadline (DD-MM-YYYY or +n): ")
    if re.match(r'\+\d+', deadline_input):
        days_from_now = int(deadline_input[1:])
        deadline = datetime.now().date() + timedelta(days=days_from_now)
    else:
        deadline = datetime.strptime(deadline_input, "%d-%m-%Y").date()

    # If duration is added manually, set an empty string for the directory
    if duration_choice == "y":
        directory = ""
        time_scanned = ""
    else:
        time_scanned = datetime.now().strftime('%H:%M')

    lectures.append({
        "name": name,
        "duration": duration,
        "amount_watched": 0,
        "deadline": deadline,
        "amount_done": 0,
        "active_status": 1,
        "directory": directory,
        "time_scanned": time_scanned,
        "manual": manual  # Added manually (1) or from a directory (0)
    })

    lectures.sort(key=lambda x: x["deadline"])
    update_index(lectures)  # Update the lecture indexes
    save(lectures)

def scan_and_update_directories(lectures):
    clear_terminal()

    # Display lectures that were added from a directory (not added manually)
    eligible_lectures = [lec for lec in lectures if lec.get("manual", 0) == 0]

    if not eligible_lectures:
        print("No lectures added from a directory found.")
        return

    print("Select the index of the lecture you want to update the video files for:\n")

    # Display eligible lectures for updating
    for lecture in eligible_lectures:
        print(f"{lecture['index']}. {lecture['name']}")

    # Ask for the index of the lecture to update
    while True:
        try:
            selected_index = int(input("\nEnter the index of the lecture to update: "))
            selected_lecture = next((lec for lec in eligible_lectures if lec['index'] == selected_index), None)
            if selected_lecture:
                break
            else:
                print("Invalid selection. Please choose an index of a lecture added from a directory.")
        except (ValueError, IndexError):
            print("Invalid selection. Please choose a valid index.")

    # Update the video files for the selected lecture
    directory = selected_lecture["directory"]
    video_files = scan_directory(directory)
    selected_lecture["duration"] = sum(video_files.values())

    # Recalculate the time_scanned based on the new duration
    time_scanned = sum(lec["duration"] for lec in lectures if lec.get("time_scanned"))

    # Update the corresponding lecture with the new time_scanned
    for lecture in lectures:
        if lecture.get("time_scanned"):
            lecture["time_scanned"] = time_scanned

    save(lectures)
    print(f"Lecture '{selected_lecture['name']}' video files updated.")
    


def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\video.md"
        editor = 'notepad'
    else:
        notes_file = os.path.join(colors.notes_file,"videonote.md")
        editor = 'nvim'
    os.system(f"{editor} {notes_file}")

def flush_database(lectures):
    clear_terminal()
    confirm = input("Are you sure you want to flush the database? This action cannot be undone. (y/n): ")
    if confirm.lower() == 'y':
        lectures.clear()
        save(lectures)
        print("All lectures removed from the database.")
    else:
        print("Database flush cancelled.")


def show_lectures(lectures):
    clear_terminal()
    print("\n\nIndex\tName\t\t\tTime left\tDeadline")
    total_amount = sum(lecture["duration"] for lecture in lectures if lecture["active_status"] == 1)
    if total_amount == 0:
        clear_terminal()
        print("No Videos found.")
        return
    total_amount_watched = sum(lecture["amount_watched"] for lecture in lectures if lecture["active_status"] == 1)
    progress_bar_length = 20
    progress_bar_fill = '█'
    
    for i, lecture in enumerate(lectures):
        if lecture["active_status"] == 1:
            time_left = lecture["duration"] - lecture["amount_watched"]
            time_left_str = f"{time_left // 60:02d}:{time_left % 60:02d}"  # format the time_left as HH:MM
            deadline = lecture["deadline"].strftime("%d-%m-%Y")
            print(f"{i+1}\t{lecture['name']}\t\t{time_left_str}\t\t{deadline}")
    
    progress_bar_fill_count = int(total_amount_watched / total_amount * progress_bar_length)
    progress_bar = f"[{progress_bar_fill * progress_bar_fill_count}{' ' * (progress_bar_length - progress_bar_fill_count)}]"
    print(f"\nProgress: {progress_bar} {int(total_amount_watched / total_amount * 100)}%")


def modify_lecture(lectures):
    clear_terminal()
    print("\n\nSelect lecture to modify:\n")
    for lecture in lectures:
        if lecture["active_status"] == 1:
            print(f"{lecture['index']}. {lecture['name']}\t\tT: {lecture['duration']-lecture['amount_watched']}")
    lecture_index = int(input("\nEnter lecture index: ")) - 1
    amount_watched = int(input("Enter amount watched(r//n): "))
    if amount_watched == "r":
        amount_watched = input(": ")
        lectures[lecture_index]["amount_watched"] = amount_watched
    elif amount_watched != "":
        lectures[lecture_index]["amount_watched"] += amount_watched
    else:
        pass
    save(lectures)


def change_deadline(lectures):
    clear_terminal()
    print("\n\nSelect lecture to change the deadline:\n")
    for lecture in lectures:
        if lecture["active_status"] == 1:
            print(f"{lecture['index']}. {lecture['name']}\t\tT: {lecture['duration']-lecture['amount_watched']}")
    lecture_index = int(input("\nEnter lecture index: ")) - 1
    
    if lecture_index < 0 or lecture_index >= len(lectures):
        print("Invalid lecture index")
        return
    
    days = int(input("Enter the number of days to add or subtract from the deadline: "))
    lecture = lectures[lecture_index]
    current_deadline = lecture["deadline"]
    new_deadline = current_deadline + timedelta(days=days)
    lecture["deadline"] = new_deadline
    save(lectures)
    print(f"Deadline for {lecture['name']} changed from {current_deadline} to {new_deadline}")


def remove_lecture(lectures):
    clear_terminal()
    for lecture in lectures:
        if lecture["active_status"] == 1:
            print(f"\n{lecture['index']}. {lecture['name']}\t\tT: {lecture['duration']-lecture['amount_watched']}")
    index = input("\nEnter the index of the lecture you want to remove: ")
    for lecture in lectures:
        if lecture['index'] == int(index) and lecture["active_status"] == 1:
            lectures.remove(lecture)
            print(f"Lecture with index {index} removed successfully.")
            save(lectures)
            break
    else:
        print(f"No lecture found with index {index}.")

def daily_workload(lectures):
    clear_terminal()
    today = datetime.now().date()
    total_workload_minutes = 0

    print("\n\nVideo\t\tTime left\tDays left\tDaily workload\tWatched (%)")
    print("---------------------------------------------------------------------------")
    
    for lecture in lectures:
        if lecture["active_status"] == 1:
            time_left = lecture["duration"] - lecture["amount_watched"]
            time_left_str = f"{time_left // 60:02d}:{time_left % 60:02d}"
            days_left = (lecture["deadline"] - today).days
            
            if days_left < 1:
                print(
                    f"{lecture['name']}\t\t{time_left_str}\t\t- \t\tOverdue!\t{int(lecture['amount_watched'] / lecture['duration'] * 100)}%"
                )
            else:
                daily_workload = int(time_left / days_left)
                daily_workload_str = f"{daily_workload // 60:02d}:{daily_workload % 60:02d}"
                print(
                    f"{lecture['name']}\t{time_left_str}\t\t{days_left}\t\t{daily_workload_str}\t\t{int(lecture['amount_watched'] / lecture['duration'] * 100)}%"
                )
                total_workload_minutes += daily_workload
    
    total_workload_hours = total_workload_minutes // 60
    total_workload_minutes %= 60
    total_workload_str = f"{total_workload_hours:02d}:{total_workload_minutes:02d}"
    
    print("---------------------------------------------------------------------------")
    print(f"Daily estimate: {total_workload_str}")




def hibernate_lecture(lectures):
    clear_terminal()
    print("\n\nSelect lecture to hibernate or activate:\n")
    for lecture in lectures:
        status = "Hibernated" if lecture["active_status"] == 0 else "Active"
        print(f"{lecture['index']}.\t {lecture['name']}\t\tStatus: {status}")
    lecture_index = int(input("\nEnter lecture index: ")) - 1
    
    if lecture_index < 0 or lecture_index >= len(lectures):
        print("Invalid lecture index")
        return
    
    lecture = lectures[lecture_index]
    lecture["active_status"] = 0 if lecture["active_status"] == 1 else 1
    status = "Hibernated" if lecture["active_status"] == 0 else "Active"
    save(lectures)
    print(f"Lecture '{lecture['name']}' is now {status}")

def main():
    clear_terminal()
    lectures = init()
    while True:
        print(f"\n{colors.YELLOW}||Lecture Videos||{colors.RESET}\n")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add lecture{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Load lectures{colors.RESET}")
        print(f"{colors.CYAN}v.{colors.RESET} {colors.YELLOW}Save lectures{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show lectures{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET} {colors.YELLOW}Daily workload{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET} {colors.YELLOW}Modify lecture{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Change deadline{colors.RESET}")
        print(f"{colors.CYAN}h.{colors.RESET} {colors.YELLOW}Hibernate a lecture{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove a lecture{colors.RESET}")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Lecture notes{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Flush database{colors.RESET}")
        print(f"{colors.CYAN}u.{colors.RESET} {colors.YELLOW}Scan and update directories{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Exit{colors.RESET}")

        choice = input("\nEnter your choice: ")
        if choice == "a":
            add_lecture(lectures)
        elif choice == "l":
            lectures = init()
            clear_terminal()
        elif choice == "v":
            save(lectures)
        elif choice == "s":
            show_lectures(lectures)
            input("\n\nPress any key to continue.....")
            clear_terminal()
        elif choice == "d":
            daily_workload(lectures)
            input("\n\nPress any key to continue.....")
            clear_terminal()
        elif choice == "m":
            modify_lecture(lectures)
        elif choice == "r":
            remove_lecture(lectures)
        elif choice == "c":
            change_deadline(lectures)
        elif choice == "h":
            clear_terminal()
            hibernate_lecture(lectures)
        elif choice == "n":
            edit_notes()
            clear_terminal()
        elif choice == "f":
            flush_database(lectures)
        elif choice == "u":
            scan_and_update_directories(lectures)
        elif choice == "q":
            break
        else:
            clear_terminal()


if __name__ == "__main__":
    main()
