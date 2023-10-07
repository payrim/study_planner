import datetime
import json
import os
from utils.clearterminal import clear_terminal
from utils import colors

REMINDER_FILE = os.path.join(colors.notes_file, "reminders.json")
REMINDER_NOTES_FILE = os.path.join(colors.notes_file, "remindernotes.json")


def load_reminders():
    try: 
        with open(REMINDER_FILE, 'r') as f:
            reminders = [json.loads(reminder) for reminder in f.readlines()]
    except FileNotFoundError:
        reminders = []
        save_reminders(reminders)
    return reminders


def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as f:
        for reminder in reminders:
            json.dump(reminder, f)
            f.write("\n")

def update_reminder_index():
    reminders = load_reminders()
    for i, reminder in enumerate(reminders):
        reminder['index'] = i + 1
    save_reminders(reminders)

def add_reminder():
    update_reminder_index()
    study_name = input("Enter study name: ")
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    reminder_dates = [(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=12)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=21)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=45)).strftime("%d-%m-%Y"),
                      (datetime.datetime.now() + datetime.timedelta(days=60)).strftime("%d-%m-%Y")]
    reminders = load_reminders()
    index = len(reminders) + 1
    reminder = {
        "index": index,
        "study_name": study_name,
        "current_date": current_date,
        "reminder_dates": reminder_dates
    }
    reminders.append(reminder)
    save_reminders(reminders)
    clear_terminal()
    print("Reminder added successfully!")

def remove_reminder():
    clear_terminal()
    update_reminder_index()
    reminders = load_reminders()
    print("Reminders:\n")
    for reminder in reminders:
        print(f"{reminder['index']}. {reminder['study_name']}")
    index = input("Enter index of the study to remove: ")
    index = int(index)
    reminders = [reminder for reminder in reminders if reminder['index'] != index]
    save_reminders(reminders)
    clear_terminal()
    print("Reminder removed successfully!")

def flush_reminders():
    confirm = input("Are you sure you want to delete all reminders? (y/n) ")
    if confirm.lower() == "y":
        with open(REMINDER_FILE, 'w') as f:
            f.write("")
        clear_terminal()
        print("\nAll reminders removed successfully!")
    else:
        clear_terminal()
        print("cancelled.\n")

def show_reminders():
    print()
    load_reminders()
    update_reminder_index()
    reminders = load_reminders()
    if len(reminders) == 0:
        print(f"\n\n{colors.space*3}{colors.WWITE}Reminders empty.{colors.RESET}")
    today = datetime.date.today()
    date_groups = {}
    for reminder in reminders:
        for i, date_str in enumerate(reminder['reminder_dates'], start=1):
            date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
            if date < today:
                date_group_key = date_str
            elif date == today:
                date_group_key = f"{colors.CYAN}Today{colors.RESET}"
            else:
                days_left = (date - today).days
                date_group_key = f"{colors.YELLOW}{days_left} day{'s' if days_left > 1 else ''} left{colors.RESET}"
            if date not in date_groups:
                date_groups[date] = []
            reminder_with_repetition = f"{reminder['study_name']} {colors.WRED}(Rep {i})"
            date_groups[date].append((reminder['index'], reminder_with_repetition))
    sorted_dates = sorted(date_groups.keys())
    for date in sorted_dates:
        date_group_key = date.strftime('%d-%m-%Y')
        if date < today:
            date_group_header = date_group_key
        elif date == today:
            date_group_header = f"{colors.YELLOW}Today{colors.RESET}"
        else:
            days_left = (date - today).days
            date_group_header = f"{colors.YELLOW}{days_left} day{'s' if days_left > 1 else ''} left{colors.RESET}"
        print(f"\n{colors.space*3}{colors.GREEN}Date: {date_group_header}{colors.RESET}")
        reminders = date_groups[date]
        for reminder in reminders:
            print(f"{colors.space*3}{colors.WWITE}{reminder[0]}.{colors.RESET}{colors.BLUE} {reminder[1]}{colors.RESET}")


def list_reminders():
    clear_terminal()
    reminders = load_reminders()
    if len(reminders) == 0:
        print("\n\nreminders empty.")
    else:
        print(f"\n\n{'Index':<10}{'Study Name':<30}{'Date':<15}")
        for reminder in reminders:
            print(f"{reminder['index']:<10}{reminder['study_name']:<30}{reminder['current_date']:<15}")
    input("\nPress any key to continue....")
    clear_terminal()
 

def modify_reminder():
    update_reminder_index()
    reminders = load_reminders()
    print("Reminders:\n")
    for reminder in reminders:
        print(f"{reminder['index']}. {reminder['study_name']} - {reminder['reminder_dates']}")
    index = input("Enter index of the study to modify: ")
    index = int(index)
    for reminder in reminders:
        if reminder['index'] == index:
            pages = input("Enter number of pages to add (use negative number to remove pages): ")
            pages = int(pages)
            reminder['pages'] += pages
    save_reminders(reminders)
    print("Reminder modified successfully!")

def add_reminder_note():
    clear_terminal()
    reminders = load_reminders()
    
    if not reminders:
        print("No reminders available to add notes to.")
        return
    
    print("Reminders:\n")
    for reminder in reminders:
        # Count the number of notes for each reminder (default to 0 if 'notes' key is missing)
        note_count = len(reminder.get('notes', []))
        print(f"{reminder['index']}. {reminder['study_name']} - {note_count} notes")

    index = input("Enter the index of the reminder to add a note to: ")
    index = int(index)

    for reminder in reminders:
        if reminder['index'] == index:
            note_text = input("Enter your note: ")

            if 'notes' not in reminder:
                reminder['notes'] = []

            reminder['notes'].append({
                'date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'note_text': note_text
            })

            save_reminders(reminders)
            clear_terminal()
            print("Note added successfully!")
            return

    print("Reminder not found.")

# New function to show notes for a selected reminder
def show_reminder_notes():
    clear_terminal()
    reminders = load_reminders()
    if not reminders:
        print(colors.YELLOW + "No reminders available." + colors.RESET)
        return

    print(colors.BLUE + "Reminders with Notes:\n" + colors.RESET)
    for reminder in reminders:
        if 'notes' in reminder:
            print(f"{reminder['index']}. {reminder['study_name']}")

    index = input("\n" + colors.CYAN + "Enter the index of the reminder to show notes for: " + colors.RESET)
    index = int(index)

    for reminder in reminders:
        clear_terminal()
        if 'notes' in reminder and reminder['index'] == index:
            print("\n" + colors.GREEN + "Notes for Reminder:" + colors.RESET)
            for note in reminder['notes']:
                print(f"{colors.YELLOW}Date: {note['date']}{colors.RESET}")
                print(f"{colors.YELLOW}Note: {note['note_text']}{colors.RESET}\n")
                input(colors.YELLOW + "Press any key to continue..." + colors.RESET)
            return

    print(RED + "No notes found for the selected reminder." + colors.RESET)

# New function to remove saved notes for a selected reminder
def remove_reminder_notes():
    clear_terminal()
    reminders = load_reminders()
    if not reminders:
        print("No reminders available.")
        return

    print("Reminders with Notes:\n")
    for reminder in reminders:
        if 'notes' in reminder:
            print(f"{reminder['index']}. {reminder['study_name']}")

    index = input("Enter the index of the reminder to remove notes for: ")
    index = int(index)

    for reminder in reminders:
        if 'notes' in reminder and reminder['index'] == index:
            del reminder['notes']
            save_reminders(reminders)
            clear_terminal()
            print("Notes removed successfully!")
            return

    print("No notes found for the selected reminder.")

# New function to save reminder notes to a file
def save_reminder_notes():
    reminders = load_reminders()
    if not reminders:
        print("No reminders available.")
        return

    with open(REMINDER_NOTES_FILE, 'w') as f:
        json.dump(reminders, f)

# New function to load reminder notes from a file
def load_reminder_notes():
    try:
        with open(REMINDER_NOTES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    while True:
        print(f"\n\n{colors.YELLOW}||Spaced Repetition||\n{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add reminder{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove reminder{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Flush reminders{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show reminders{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET} {colors.YELLOW}List reminders{colors.RESET}")
        print(f"{colors.CYAN}v.{colors.RESET} {colors.YELLOW}Save reminders to file{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Load reminders from file{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Add reminder note{colors.RESET}")
        print(f"{colors.CYAN}o.{colors.RESET} {colors.YELLOW}Show reminder notes{colors.RESET}")
        print(f"{colors.CYAN}x.{colors.RESET} {colors.YELLOW}Remove reminder notes{colors.RESET}")
        print(f"{colors.CYAN}w.{colors.RESET} {colors.YELLOW}Save reminder notes to file{colors.RESET}")
        print(f"{colors.CYAN}z.{colors.RESET} {colors.YELLOW}Load reminder notes from file{colors.RESET}")

        choice = input("\nEnter your choice: ")
        if choice == 'a':
            clear_terminal()
            add_reminder()
        elif choice == 'r':
            clear_terminal()
            remove_reminder()
        elif choice == 'f':
            clear_terminal()
            flush_reminders()
        elif choice == 'd':
            clear_terminal()
            list_reminders()
        elif choice == 's':
            clear_terminal()
            show_reminders()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'v':
            clear_terminal()
            reminders = load_reminders()
            save_reminders(reminders)
        elif choice == 'l':
            clear_terminal()
            reminders = load_reminders()
            print(f"{len(reminders)} reminders loaded from file")
        elif choice == 'n':
            add_reminder_note()
        elif choice == 'o':
            show_reminder_notes()
        elif choice == 'x':
            remove_reminder_notes()
        elif choice == 'w':
            save_reminder_notes()
        elif choice == 'z':
            reminders = load_reminder_notes()
            if reminders:
                save_reminders(reminders)
                print(f"{len(reminders)} reminder notes loaded from file")
            else:
                print("No reminder notes found in the file.")
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()

if __name__ == '__main__':
    main()