import json
from datetime import datetime, timedelta
from utils.clearterminal import clear_terminal
from utils import colors
import os

subjects = []
inactive_subjects = [] 

SUB_DB = os.path.join(colors.notes_file, "subjects.json")
INACTIVE_DB = os.path.join(colors.notes_file, "inactivesubs.json")


def load_data():
    global subjects
    try:
        with open(SUB_DB, "r") as f:
            subjects = json.load(f)
        print("Data loaded successfully!\n")
    except FileNotFoundError:
        print("No saved data found.\n")

def save_data():
    with open(SUB_DB, "w") as f:
        json.dump(subjects, f)
    print("Data saved successfully!\n")

def update_subject_indexes():
    global subjects
    n = len(subjects)
    for i in range(n):
        subjects[i]['index'] = i + 1
    

def load_inactive_data():
    global inactive_subjects
    try:
        with open(INACTIVE_DB, "r") as f:
            inactive_subjects = json.load(f)
    except FileNotFoundError:
        inactive_subjects = []

def save_inactive_data():
    with open(INACTIVE_DB, "w") as f:
        json.dump(inactive_subjects, f)

def change_index():
    clear_terminal()
    if len(subjects) == 0:
        print("No subjects added yet.")
        return
    print("List of subjects:")
    for subject in subjects:
        print(f"{subject['index']}. {subject['name']}")
    old_index = int(input("Enter the old index of the subject: "))
    new_index = int(input("Enter the new index for the subject: "))
    for subject in subjects:
        if subject["index"] == new_index:
            subject["index"] = old_index
        elif subject["index"] == old_index:
            subject["index"] = new_index
    print("Index changed successfully!\n")

def add_subject():
    update_subject_indexes()
    subject_index = len(subjects)
    subject_name = input("Enter subject name: ")
    subjects.append({"index": subject_index, "name": subject_name, "status": "Haven't studied"})
    print("Subject added successfully!")
    show_subjects()

def remove_subject():
    clear_terminal()
    update_subject_indexes()
    show_subjects_Pindexes()
    subject_index = int(input("Enter subject index to remove: "))
    for subject in subjects:
        if subject["index"] == subject_index:
            subjects.remove(subject)
            print(f"{subject['name']} removed successfully.")
            return
    print(f"Subject with index {subject_index} not found.")
    input("Press any key to continue...")
    clear_terminal()
    show_subjects()

def show_subjects_Pindexes():
    if len(subjects) == 0:
        print("No subjects added yet.")
    else:
        print("\n\n")
        print(" {:<5} {:<30} {:<20}".format("Index", f"{colors.YELLOW}Name{colors.RESET}", f"{colors.YELLOW}Status{colors.RESET}"))
        print(colors.CYAN + "-" * 60 + colors.RESET)
        count = {"haven't studied": 0, "studying right now": 0, "study accomplished": 0}
        board = {"haven't studied": [], "studying right now": [], "study accomplished": []}
        for subject in subjects:
            count[subject["status"].lower()] += 1
            board[subject["status"].lower()].append(subject)

        for i in range(count["haven't studied"]):
            subject = board["haven't studied"][i]
            print("{:<5} {:<40} {:<20}".format(subject["index"], colors.YELLOW + subject["name"] + colors.RESET, subject["status"]))

        # if count["haven't studied"] > 0:
        #     print("{:<5} {:<30} {:<20}".format("...", "", ""))

        for i in range(count["haven't studied"] + count["studying right now"], len(board["haven't studied"])):
            subject = board["haven't studied"][i]
            print("{:<5} {:<40} {:<20}".format(subject["index"], colors.YELLOW + subject["name"] + colors.RESET, subject["status"]))

        print(colors.CYAN + "-" * 60 + colors.RESET)

        for subject in board["studying right now"]:
            print("{:<5} {:<40} {:<20}".format(subject["index"], colors.BLUE + subject["name"] + colors.RESET, subject["status"]))

        print(colors.CYAN + "-" * 60 + colors.RESET)

        for subject in board["study accomplished"]:
            print("{:<5} {:<40} {:<20}".format(subject["index"], colors.YELLOW + subject["name"] + colors.RESET, subject["status"]))

def move_subject():
    clear_terminal()
    update_subject_indexes()
    show_subjects_Pindexes()
    subject_index = int(input("\nEnter subject index to move: "))
    for subject in subjects:
        if subject["index"] == subject_index:
            current_status = subject['status']
            if current_status == "Haven't studied":
                subject['status'] = "Studying right now"
            elif current_status == "Studying right now":
                subject['status'] = "Study accomplished"
            else:
                print(f"{subject['name']} already accomplished.")
            save_data()
            clear_terminal()
            return

    print(f"Subject with index {subject_index} not found.")
    input("Press any key to continue...")
    clear_terminal()
    show_subjects()

def update_subject():
    clear_terminal()
    update_subject_indexes()
    if len(subjects) == 0:
        print("No subjects added yet.")
    else:
        print("List of subjects:")
        for subject in subjects:
            print(f"{subject['index']}. {subject['name']} - Status: {subject['status']}")
        subject_index = int(input("Enter subject index to update: "))
        for subject in subjects:
            if subject["index"] == subject_index:
                new_name = input("Enter new name for subject: ")
                subject['name'] = new_name
                return
        print(f"Subject with index {subject_index} not found.")
        input("Press any key to continue...")
        clear_terminal()
        show_subjects()

def show_subjects():
    update_subject_indexes()
    if len(subjects) == 0:
        clear_terminal()
        print(f"\n{colors.space*3}No subjects added yet.\n\n")
    else:
        clear_terminal()
        print("\n\n")
        print(" {:<30} {:<20}".format( f"{colors.space*3}{colors.YELLOW}Name{colors.RESET}", f"{colors.YELLOW}Status{colors.RESET}"))
        print(colors.space * 3 + colors.CYAN + "-" * 60 + colors.RESET)
        count = {"haven't studied": 0, "studying right now": 0, "study accomplished": 0}
        board = {"haven't studied": [], "studying right now": [], "study accomplished": []}
        for subject in subjects:
            count[subject["status"].lower()] += 1
            board[subject["status"].lower()].append(subject)

        for i in range(count["haven't studied"]):
            subject = board["haven't studied"][i]
            print("{:<40} {:<20}".format( colors.space * 3 + colors.YELLOW + subject["name"] + colors.RESET, subject["status"]))

        # if count["haven't studied"] > 0:
        #     print("{:<30} {:<20}".format("...", "", ""))

        for i in range(count["haven't studied"] + count["studying right now"], len(board["haven't studied"])):
            subject = board["haven't studied"][i]
            print(" {:<40} {:<20}".format(colors.space * 3 + colors.YELLOW + subject["name"] + colors.RESET, subject["status"]))

        print(colors.space * 3 + colors.CYAN + "-" * 60 + colors.RESET)

        for subject in board["studying right now"]:
            print(" {:<39} {:<20}".format( colors.space * 2 + colors.BLUE+subject["name"]+colors.RESET, subject["status"]))

        print(colors.space * 3 + colors.CYAN + "-" * 60 + colors.RESET)

        for subject in board["study accomplished"]:
            print("{:<40} {:<20}".format( colors.space * 3 + colors.YELLOW+subject["name"]+colors.RESET, subject["status"]))

        input("\n\nPress any key to continue...")
        clear_terminal()

def summarize_subjects():
    with open('subjects.json') as f:
        subjects = json.load(f)

    not_studied = []
    studying = []
    studied = []
    hibernated = []

    for subject in subjects:
        if subject['status'] == "Haven't studied":
            not_studied.append(subject)
        elif subject['status'] == 'Studying right now':
            studying.append(subject)
        elif subject['status'] == 'Study accomplished':
            studied.append(subject)
    
    for subject in inactive_subjects:
        hibernated.append(subject)

    print(f"\n{colors.YELLOW}Haven't Studied ({len(not_studied)} subjects):{colors.RESET}")
    if len(not_studied) > 10:
        for subject in not_studied[:5]:
            print(f"{colors.CYAN}{subject['index']}. {colors.RESET}{colors.BLUE}{subject['name']}{colors.RESET}")
        print("...")
        for subject in not_studied[-5:]:
            print(f"{colors.CYAN}{subject['index']}. {colors.RESET}{colors.BLUE}{subject['name']}{colors.RESET}")
    else:
        for subject in not_studied:
            print(f"{colors.CYAN}{subject['index']}. {colors.RESET}{colors.BLUE}{subject['name']}{colors.RESET}")

    print(f"\n{colors.YELLOW}Studying ({len(studying)} subjects):{colors.RESET}")
    for subject in studying:
        print(f"{colors.CYAN}{subject['index']}.{colors.RESET}{colors.BLUE} {subject['name']}{colors.RESET}")

    print(f"\n{colors.YELLOW}Study Hibernated ({len(hibernated)} subjects):{colors.RESET}")
    for subject in hibernated:
        print(f"{colors.CYAN}{subject['index']}.{colors.RESET}{colors.BLUE} {subject['name']}{colors.RESET}")

    print(f"\n{colors.YELLOW}Study Accomplished ({len(studied)} subjects):{colors.RESET}")
    for subject in studied:
        print(f"{colors.CYAN}{subject['index']}.{colors.RESET}{colors.BLUE} {subject['name']}{colors.RESET}")

def update_subject_indexes():
    global subjects
    n = len(subjects)
    for i in range(n):
        subjects[i]['index'] = i + 1

def hibernate_subject():
    clear_terminal()
    load_data()
    if len(subjects) == 0:
        print("No subjects added yet.")
        return

    print("List of subjects:")
    for subject in subjects:
        if subject['status'] == 'Studying right now':
            print(f"{colors.WWITE}{subject['index']}. {colors.CYAN}{subject['name']} - {subject['status']}")
        elif subject['status'] == "Haven't studied":
            print(f"{colors.WWITE}{subject['index']}. {colors.YELLOW}{subject['name']} - {subject['status']}")
        elif subject['status'] == 'Study accomplished':
            print("")

    subject_index = int(input("\nEnter index of subject to hibernate: "))
    for subject in subjects:
        if subject["index"] == subject_index:
            subjects.remove(subject)
            global inactive_subjects
            if subject not in inactive_subjects:
                inactive_subjects.append(subject)
            save_inactive_data()
            print(f"{subject['name']} hibernated successfully.")
            update_subject_indexes()
            save_data()
            return

    print(f"Subject with index {subject_index} not found.")
    input("Press any key to continue...")
    clear_terminal()


def activate_subject():
    load_inactive_data()
    if len(inactive_subjects) == 0:
        print("No subjects to activate.")
        return

    print(colors.YELLOW+"\n\n"+colors.space*3+"Inactive Subjects\n"+colors.RESET+colors.CYAN+colors.space*3+"-"*18+colors.RESET)
    for i, subject in enumerate(inactive_subjects):
        print(f"{colors.CYAN}{colors.space*3}{i + 1}. {colors.RESET}{colors.WWITE}{subject['name']}")

    subject_index = int(input("\nEnter index of subject to activate: "))-1
    if 0 <= subject_index < len(inactive_subjects):
        subject = inactive_subjects.pop(subject_index)
        subjects.append(subject)
        update_subject_indexes()
        save_data()
        save_inactive_data()
        clear_terminal()
        print(f"{subject['name']} activated successfully.")
    else:
        print("Invalid index.")

def main():
    while True:
        load_data()
        load_inactive_data()
        update_subject_indexes()
        save_data()
        save_inactive_data()
        clear_terminal()
        print(f"\n\n{colors.YELLOW}||Study Subjects||{colors.RESET}\n")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add subject{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET} {colors.YELLOW}Move subject{colors.RESET}")
        print(f"{colors.CYAN}u.{colors.RESET} {colors.YELLOW}Update subject{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show subjects{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove subject{colors.RESET}")
        print(f"{colors.CYAN}ss.{colors.RESET} {colors.YELLOW}Summarize{colors.RESET}")
        print(f"{colors.CYAN}c.{colors.RESET} {colors.YELLOW}Change index{colors.RESET}")
        print(f"{colors.CYAN}h.{colors.RESET} {colors.YELLOW}Hibernate subject{colors.RESET}")
        print(f"{colors.CYAN}t.{colors.RESET} {colors.YELLOW}Activate subject{colors.RESET}")
        print(f"{colors.CYAN}v.{colors.RESET} {colors.YELLOW}Save data{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Load data{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")

        choice = input("\nEnter choice: ")
        if choice == "a":
            clear_terminal()
            add_subject()
            update_subject_indexes()
            save_data()
        elif choice == "m":
            clear_terminal()
            move_subject()
            save_data()
        elif choice == "u":
            clear_terminal()
            update_subject()
            save_data()
        elif choice == "s":
            clear_terminal()
            show_subjects()
        elif choice == "r":
            clear_terminal()
            remove_subject()
            update_subject_indexes()
            save_data()
        elif choice == "c":
            clear_terminal()
            change_index()
            save_data()
        elif choice == "v":
            clear_terminal()
            update_subject_indexes()
            save_data()
        elif choice == "l":
            clear_terminal()
            load_data()
        elif choice == "ss":
            clear_terminal()
            summarize_subjects()
            input("\n press any key to continue...")
        elif choice == "h":
            clear_terminal()
            hibernate_subject()
        elif choice == "t":
            clear_terminal()
            activate_subject()
        elif choice == "q":
            clear_terminal()
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()