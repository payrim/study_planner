import json
import os
import re
import fitz
import PyPDF4
from modules import daycalculator
from utils.clearterminal import clear_terminal
from utils import colors


NOTE_DB = os.path.join(colors.notes_file, 'noteprime.json')

def edit_notes():
    if os.name == 'nt':
        notes_file = "C:\\Program Files\\Planner\\notenote.md"
        editor = 'notepad'
    else:
        notes_file = os.path.join(colors.notes_file,"notenote.md")
        editor = 'nvim'
    os.system(f"{editor} {notes_file}")

# Initialize an empty list to hold the notes
notes = []

# Load the notes data from a JSON file
def load_notes():
    global notes
    try:
        with open(NOTE_DB, 'r') as f:
            notes = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist yet, create an empty one
        save_notes()

# Save the notes data to a JSON file
def save_notes():
    with open(NOTE_DB, 'w') as f:
        json.dump(notes, f)

# Remove a note from the list
def remove_note():
    print_notes()
    index = int(input("\n\nEnter index of note to remove: "))
    try:
        del notes[index]
        clear_terminal()
        print("note removed successfully.")
    except IndexError:
        print("Invalid index.")

# Add a new note to the list
def add_note():
    name = input("\n\nEnter note name: ")
    pages = int(input("Enter number of pages: "))
    chapters = int(input("Enter number of chapters: "))
    exercises = int(input("Enter number of exercises: "))
    active = input("Active or Deactive? (A/D): ").upper() == "A"  # Added active status
    note = {
        "name": name,
        "pages": pages,
        "chapters": chapters,
        "exercises": exercises,
        "pages_read": 0,
        "chapters_read": 0,
        "exercises_read": 0,
        "exercises_time": 0,
        "chapters_time": 0,
        "pages_time": 0,
        "active": active
    }  # Added active key
    notes.append(note)
    save_notes()  # Save the updated list of notes to the JSON file
    clear_terminal()
    print("note added successfully.")

def show_on_hold_notes():
    clear_terminal()
    on_hold_notes = [note for note in notes if not note.get('active', True)]  # Get on-hold notes

    if not on_hold_notes:
        clear_terminal()
        print("No notes are currently on hold.\n")
        return

    print("\n\nIndex\tName\t\t\t      Pages\t\t Status")
    for i, note in enumerate(on_hold_notes):
        print(f"{i}\t{note['name'].ljust(30)}{note['pages']}\t\t On Hold")

    index = int(input("\n\nEnter index of note to modify: "))
    try:
        note = on_hold_notes[index]
        print("Selected note:", note["name"])
        print("Current status: On Hold")
        activate = input("Activate this note? (Y/N): ").upper() == "Y"
        note["active"] = activate
        clear_terminal()
        clear_terminal()
        print("note status modified successfully.\n")
    except IndexError:
        clear_terminal()
        print("Invalid index.")

# Display a list of all the notes
def print_notes():
    total_pages = sum(note['pages'] for note in notes if note.get('active', True))  # Calculate total pages only for active notes
    if total_pages == 0:
        clear_terminal()
        print("No notes found.")
        return
    print("\n\nIndex\tName\t\t\tChapters\tPages\tExercises\tProgress")
    total_pages_read = sum(note.get('pages_read', 0) for note in notes if note.get('active', True))  # Calculate total pages read only for active notes
    #total_exercises = sum(note['exercises'] for note in notes if note.get('active', True))  # Calculate total exercises only for active notes
    #total_chapters = sum(note['chapters'] for note in notes if note.get('active', True))  # Calculate total chapters only for active notes
    #total_exercises_read = sum(note.get('exercises_read', 0) for note in notes if note.get('active', True))  # Calculate total pages read only for active notes
    #total_chapters_read = sum(note.get('chapters_read', 0) for note in notes if note.get('active', True))  # Calculate total pages read only for active notes
    progress_bar_length = 20
    progress_bar_fill = '█'

    for i, note in enumerate(notes):
        if note.get('active', True):  # Only display active notes
            pages_read = note.get('pages_read', 0)
            progress = int(pages_read * 100 / note['pages']) if total_pages != 0 else 0
            print(f"{i}\t{note['name'].ljust(19)}\t{note['chapters']}\t\t{note['pages']}\t{note['exercises']}\t\t{progress}%")

    progress_bar_fill_count = int(total_pages_read / total_pages * progress_bar_length)
    progress_bar = f"[{progress_bar_fill * progress_bar_fill_count}{' ' * (progress_bar_length - progress_bar_fill_count)}]"
    print(f"\nProgress: {progress_bar} {int(total_pages_read / total_pages * 100)}%")

# Show notes divided into a time interval t
def show_notes_by_time_interval():
    t = int(daycalculator.days)
    total_pages_read = sum([note.get("pages_read", 0) for note in notes if note.get('active', True)])  # Calculate total pages read only for active notes
    total_pages_left = sum([note["pages"] - note.get("pages_read", 0) for note in notes if note.get('active', True)])  # Calculate total pages left only for active notes
    pages_per_week = total_pages_left / (t / 7)
    pages_per_day = total_pages_left / t
    pages_per_hour = total_pages_left / (t * int(daycalculator.sum_values) / 7)
    pages_per_today = pages_per_hour * daycalculator.todayhours
    #chapters
    total_chapters_read = sum([note.get("chapters_read", 0) for note in notes if note.get('active', True)])  # Calculate total chapters read only for active notes
    total_chapters_left = sum([note["chapters"] - note.get("chapters_read", 0) for note in notes if note.get('active', True)])  # Calculate total chapters left only for active notes
    chapters_per_week = total_chapters_left / (t / 7)
    chapters_per_day = total_chapters_left / t
    chapters_per_hour = total_chapters_left / (t * int(daycalculator.sum_values) / 7)
    chapters_per_today = chapters_per_hour * daycalculator.todayhours
    #exercises
    total_exercises_read = sum([note.get("exercises_read", 0) for note in notes if note.get('active', True)])  # Calculate total exercises read only for active notes
    total_exercises_left = sum([note["exercises"] - note.get("exercises_read", 0) for note in notes if note.get('active', True)])  # Calculate total exercises left only for active notes
    exercises_per_week = total_exercises_left / (t / 7)
    exercises_per_day = total_exercises_left / t
    exercises_per_hour = total_exercises_left / (t * int(daycalculator.sum_values) / 7)
    exercises_per_today = exercises_per_hour * daycalculator.todayhours

    # print(f"\n\n{'='*30}\n{' '*2}noteS BY TIME INTERVAL\n{'='*30}\n")
    # print(f"Time interval: {t} days")
    # print(f"Total pages: {sum([note['pages'] for note in notes if note.get('active', True)])}")  # Calculate total pages only for active notes
    # print(f"Total pages read: {total_pages_read}")
    # print(f"Total pages left: {total_pages_left}")
    # print(f"Pages per week: {pages_per_week:.2f}")
    # print(f"Pages per day: {pages_per_day:.2f}")
    # print(f"Pages per hour: {pages_per_hour:.2f}")
    # print(f"Pages per today: {pages_per_today:.2f}\n\n")

    # # Print information for chapters
    # print(f"Total chapters read: {total_chapters_read}")
    # print(f"Total chapters left: {total_chapters_left}")
    # print(f"Chapters per week: {chapters_per_week:.2f}")
    # print(f"Chapters per day: {chapters_per_day:.2f}")
    # print(f"Chapters per hour: {chapters_per_hour:.2f}")
    # print(f"Chapters per today: {chapters_per_today:.2f}\n\n")

    # # Print information for exercises
    # print(f"Total exercises read: {total_exercises_read}")
    # print(f"Total exercises left: {total_exercises_left}")
    # print(f"Exercises per week: {exercises_per_week:.2f}")
    # print(f"Exercises per day: {exercises_per_day:.2f}")
    # print(f"Exercises per hour: {exercises_per_hour:.2f}")
    # print(f"Exercises per today: {exercises_per_today:.2f}\n\n")

    print(f"\n\n{'='*70}\n{' '*15}noteS BY TIME INTERVAL\n{'='*70}\n")
    print(f"Time interval: {t} days\n")
    print(f"{'-'*70}")
    print(f"{'': <23}{'Pages': <15}{'Chapters': <15}{'Exercises': <15}")
    print(f"{'-'*70}")
    print(f"Total: {'': <17}{sum([note['pages'] for note in notes if note.get('active', True)]): <16}{sum([note['chapters'] for note in notes if note.get('active', True)]): <16}{sum([note['exercises'] for note in notes if note.get('active', True)]): <16}")
    print(f"Read: {'': <18}{total_pages_read: <16}{total_chapters_read: <16}{total_exercises_read: <16}")
    print(f"Left: {'': <18}{total_pages_left: <16}{total_chapters_left: <16}{total_exercises_left: <16}")
    print(f"Per week: \t\t{pages_per_week:.2f}\t\t{chapters_per_week:.2f}\t\t{exercises_per_week:.2f}{'': <12}")
    print(f"Per day: \t\t{pages_per_day:.2f}\t\t{chapters_per_day:.2f}\t\t{exercises_per_day:.2f}{'': <12}")
    print(f"Per hour: \t\t{pages_per_hour:.2f}\t\t{chapters_per_hour:.2f}\t\t{exercises_per_hour:.2f}{'': <12}")
    print(f"Per today: \t\t{pages_per_today:.2f}\t\t{chapters_per_today:.2f}\t\t{exercises_per_today:.2f}{'': <12}\n\n")

    print(f"{'Name':<30} {'Chapters read':<15} {'Chapters left':<15} {'Chapters per week':<20} {'Chapters per day':<20}")
    print("-" * 100)
    for note in notes:
        if note.get('active', True):  # Only display active notes
            #chapters
            chapters_read = note.get("chapters_read", 0)
            chapters_left = note["chapters"] - chapters_read
            chapters_per_week = chapters_left / (t / 7)
            chapters_per_day = chapters_left / t
            print(
                f"{note['name']:<30} {chapters_read:<15} {chapters_left:<15} {chapters_per_week:<20.2f} {chapters_per_day:<20.2f}")
    print("\n\n")
    print(f"{'Name':<30} {'Pages read':<15} {'Pages left':<15} {'Pages per week':<20} {'Pages per day':<20}")
    print("-" * 100)
    for note in notes:
        if note.get('active', True):  # Only display active notes
            pages_read = note.get("pages_read", 0)
            pages_left = note["pages"] - pages_read
            pages_per_week = pages_left / (t / 7)
            pages_per_day = pages_left / t
            print(
                f"{note['name']:<30} {pages_read:<15} {pages_left:<15} {pages_per_week:<20.2f} {pages_per_day:<20.2f}")
    print("\n\n")
    print(f"{'Name':<30} {'Exercises done':<15} {'Exercises left':<15} {'Exercises per week':<20} {'Exercises per day':<20}")
    print("-" * 100)
    for note in notes:
        if note.get('active', True):  # Only display active notes
            #exercises
            exercises_read = note.get("exercises_read", 0)
            exercises_left = note["exercises"] - exercises_read
            exercises_per_week = exercises_left / (t / 7)
            exercises_per_day = exercises_left / t
            print(
                f"{note['name']:<30} {exercises_read:<15} {exercises_left:<15} {exercises_per_week:<20.2f} {exercises_per_day:<20.2f}")
    input("\n\nPress any key to continue...")
    clear_terminal()

# Show notes divided into a time interval t
def show_notes_by_length_interval():
    t = int(daycalculator.days)
    total_pages_read = sum([note.get("pages_read", 0) for note in notes if note.get('active', True)])  # Calculate total pages read only for active notes
    total_pages_left = sum([note["pages"] - note.get("pages_read", 0) for note in notes if note.get('active', True)])  # Calculate total pages left only for active notes
    total_pages_time = sum([note["pages_time"] for note in notes if note.get('active', True)])  

    #chapters
    total_chapters_read = sum([note.get("chapters_read", 0) for note in notes if note.get('active', True)])  # Calculate total chapters read only for active notes
    total_chapters_left = sum([note["chapters"] - note.get("chapters_read", 0) for note in notes if note.get('active', True)])  # Calculate total chapters left only for active notes
    total_chapters_time = sum([note["chapters_time"] for note in notes if note.get('active', True)])  


    #exercises
    total_exercises_read = sum([note.get("exercises_read", 0) for note in notes if note.get('active', True)])  # Calculate total exercises read only for active notes
    total_exercises_left = sum([note["exercises"] - note.get("exercises_read", 0) for note in notes if note.get('active', True)])  # Calculate total exercises left only for active notes
    total_exercises_time = sum([note["exercises_time"] for note in notes if note.get('active', True)])  


    print(f"\n\n{'='*70}\n{' '*15}noteS BY LENGTH INTERVAL\n{'='*70}\n")
    print(f"time studied pages: {(total_pages_time)/60} hour(s)")
    print(f"time studied chapters: {(total_chapters_time)/60} hour(s)")
    print(f"time studied exercises: {(total_exercises_time)/60} hour(s)")
    print(f"Total time studied: {(total_pages_time+total_exercises_time)/60} hour(s)\n")
    


    print(f"{'Name':<30} {'Chapters read':<15} {'Chapters left':<15} {'Chapters estimation':<20} ")
    print("-" * 100)
    chapters_time_saved =0
    exercises_time_saved =0
    pages_time_saved =0
    for note in notes:
        if note.get('active', True):  # Only display active notes
            #chapters
            chapters_read = note.get("chapters_read", 0)
            chapters_left = note["chapters"] - chapters_read
            chapters_time = note.get("chapters_time",0)
            if chapters_read ==0:
                chapters_read = 1
            chapters_time_estimated = chapters_time / chapters_read * chapters_left /60
            chapters_time_saved += chapters_time_estimated
            print(
                f"{note['name']:<30} {chapters_read:<15} {chapters_left:<15} {chapters_time_estimated:.2f} hours  ")
    print("-" * 100)
    print(f"{'TOTAL':<30}  {total_chapters_read:<15} {total_chapters_left:<15} {chapters_time_saved:.2f} hours")
    print("-" * 100)
    print("\n\n")
    print(f"{'Name':<30} {'Pages read':<15} {'Pages left':<15} {'Pages estimation':<20}")
    print("-" * 100)
    for note in notes:
        if note.get('active', True):  # Only display active notes
            pages_read = note.get("pages_read", 0)
            pages_left = note["pages"] - pages_read
            pages_time = note.get("pages_time",0)
            if pages_read ==0:
                pages_read = 1
            pages_time_estimated = pages_time / pages_read * pages_left /60
            pages_time_saved += pages_time_estimated
            print(
                f"{note['name']:<30} {pages_read:<15} {pages_left:<15} {pages_time_estimated:.2f} hours  ")
    print("-" * 100)
    print(f"{'TOTAL':<30}  {total_pages_read:<15} {total_pages_left:<15} {pages_time_saved:.2f} hours")
    print("-" * 100)
    print("\n\n")
    print(f"{'Name':<30} {'Exercises done':<15} {'Exercises left':<15} {'Exercises estimation':<20}")
    print("-" * 100)
    for note in notes:
        if note.get('active', True):  # Only display active notes
            #exercises
            exercises_read = note.get("exercises_read", 0)
            exercises_left = note["exercises"] - exercises_read
            exercises_time = note.get("exercises_time",0)
            if exercises_read == 0:
                exercises_read = 1
            exercises_time_estimated = exercises_time / exercises_read * exercises_left /60
            exercises_time_saved += exercises_time_estimated
            print(
                f"{note['name']:<30} {exercises_read:<15} {exercises_left:<15} {exercises_time_estimated:.2f} hours  ")
    print("-" * 100)
    print(f"{'TOTAL':<30}  {total_exercises_read:<15} {total_exercises_left:<15} {exercises_time_saved:.2f} hours")
    print("-" * 100)
    input("\n\nPress any key to continue...")
    clear_terminal()

def modify_note():
    print_notes()
    index = int(input("\n\nEnter index of note to modify: "))
    try:
        note = notes[index]
        print("Selected note:", note["name"])
        print("Current number of pages:", note["pages"])
        print("Active status:", "Active" if note.get("active", True) else "Inactive")
        pages = input("Enter number of pages to add or remove(r//n): ")
        if pages =="r":
            pages = input(": ")
            note["pages"] = int(pages)
        elif pages != "":
            note["pages"] += int(pages)
        else:
            pass
        chapters = input("Enter number of chapters to add or remove(r//n): ")
        if chapters == "r":
            chapters = input(": ")
            note["chapters"] = int(chapters)
        elif chapters != "":
            note["chapters"] += int(chapters)
        else:
            pass
        exercises = input("Enter number of exercises to add or remove(r//n): ")
        if exercises == "r":
            exercises = input(": ")
            note["exercises"] = int(exercises)
        elif exercises != "":
            note["exercises"] += int(exercises)
        else:
            pass
        active = input("Activate or Deactivate? (A/D): ").upper() == "A"
        note["active"] = active
        clear_terminal()
        print("note modified successfully.")
    except IndexError:
        print("Invalid index.")


# Update the number of pages read for a note
def update_pages_read():
    clear_terminal()
    print("List of notes:")
    for i, note in enumerate(notes):
        print(f"{i}: {note['name']} - {note['pages']} pages")
    index = int(input("\n\nEnter the index of the note you want to update: "))
    pages_read = int(input("Enter the number of pages read: "))
    if pages_read > 0:
        pages_time = int(input("Enter the time of pages worked: "))
    exercises_read = int(input("Enter the number of exercises worked: "))
    if exercises_read > 0:
        exercises_time = int(input("Enter the time of exercises worked: "))
    chapters_read = int(input("Enter the number of chapters read: "))
    if chapters_read > 0:
        chapters_time = int(input("Enter the time of chapters read: "))
    if 0 <= index < len(notes):
        notes[index]["pages_read"] += pages_read
        notes[index]["exercises_read"] += exercises_read
        notes[index]["chapters_read"] += chapters_read
        if pages_read > 0:
            notes[index]["pages_time"] += pages_time
        if chapters_read > 0:
            notes[index]["chapters_time"] += chapters_time
        if exercises_read > 0:
            notes[index]["exercises_time"] += exercises_time
        save_notes()
        clear_terminal()
        print("note status updated successfully.")
    else:
        clear_terminal()
        print("Invalid index.")

# Extract chapter information from a PDF using PyMuPDF
def extract_chapters_from_pdf(file_path):
    doc = fitz.open(file_path)
    chapters = []

    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        text = page.get_text()

        # Implement your logic here to identify chapter titles from the extracted text
        # You might need to use regular expressions or other techniques to find chapters
        # For simplicity, let's assume that chapters start with "Chapter" followed by a number
        chapter_matches = re.findall(r"Chapter\s+(\d+)", text)

        for chapter_number in chapter_matches:
            chapters.append(int(chapter_number))

    doc.close()
    return chapters

# Save PDF notes from a directory to a JSON file
def save_pdf_notes(directory):
    global notes
    # Check if the directory exists
    if not os.path.isdir(directory):
        print("Error: directory does not exist.")
        return
    # Find PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    # Add each PDF note to the notes list
    for i, pdf_file in enumerate(pdf_files):
        with open(os.path.join(directory, pdf_file), 'rb') as f:
            pdf_reader = fitz.open(f)
            note_name = os.path.splitext(pdf_file)[0]
            note_name = input(f"the note name is {note_name}\n what do you want it to be? ")
            note_pages = pdf_reader.page_count
            note_chapters = extract_chapters_from_pdf(os.path.join(directory, pdf_file))
            note = {
                "name": note_name,
                "pages": note_pages,
                "chapters": len(note_chapters),  # Get the number of chapters from the extracted list
                "exercises": 0,  # Since we don't have exercise info for PDF notes, set it to 0
                "pages_read": 0,
                "chapters_read": 0,
                "exercises_read": 0,
                "exercises_time": 0,
                "chapters_time": 0,
                "pages_time": 0,
                "active": True  # By default, set the note as active
            }
            notes.append(note)
    # Save the notes to a JSON file
    save_notes()
    print(f"{len(pdf_files)} PDF notes saved successfully.")


# Clear the list of notes
def flush_notes():
    confirm = input("Are you sure you want to delete all notes? (y/n) ")
    if confirm.lower() == "y":
        global notes
        notes = []
        print("notes flushed successfully. remember to save!")
        clear_terminal()
        print("\nAll notes removed successfully.")
    else:
        clear_terminal()
        print("cancelled.\n")

# Load the notes data from the file at program start
load_notes()
clear_terminal()

# Main menu loop
def main():
    while True:
        print(f"\n{colors.YELLOW}||Currently Working Notes||{colors.RESET}\n\n")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add note{colors.RESET}")
        print(f"{colors.CYAN}u.{colors.RESET} {colors.YELLOW}Update page{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show notes{colors.RESET}")
        print(f"{colors.CYAN}dt.{colors.RESET} {colors.YELLOW}Show time interval{colors.RESET}")
        print(f"{colors.CYAN}dl.{colors.RESET} {colors.YELLOW}Show Length interval{colors.RESET}")
        print(f"{colors.CYAN}n.{colors.RESET} {colors.YELLOW}Edit notes{colors.RESET}")
        print(f"{colors.CYAN}h.{colors.RESET} {colors.YELLOW}Change Status{colors.RESET}")
        print(f"{colors.CYAN}v.{colors.RESET} {colors.YELLOW}Save notes{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Flush notes{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET} {colors.YELLOW}Modify note{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove note{colors.RESET}")
        print(f"{colors.CYAN}y.{colors.RESET} {colors.YELLOW}Import notes from directory{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Quit{colors.RESET}")
        choice = input("\nEnter choice: ")

        if choice == "a":
            clear_terminal()
            add_note()
            save_notes()
        elif choice == "r":
            clear_terminal()
            remove_note()
            save_notes()
        elif choice == "m":
            clear_terminal()
            modify_note()
            save_notes()
        elif choice == "s":
            clear_terminal()
            print_notes()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == "f":
            clear_terminal()
            flush_notes()
        elif choice == "u":
            update_pages_read()
        elif choice == "dt":
            clear_terminal()
            show_notes_by_time_interval()
        elif choice == "dl":
            clear_terminal()
            show_notes_by_length_interval()
        elif choice == "v":
            clear_terminal()
            save_notes()
        elif choice == "h":
            show_on_hold_notes()
            save_notes()
        elif choice == "n":
            clear_terminal()
            edit_notes()
        elif choice == "y":
            directory = input("Enter directory path: ")
            save_pdf_notes(directory)
        elif choice == "q":
            clear_terminal()
            break
        else:
            clear_terminal()

t = int(daycalculator.days)
try:
    pages_per_hour = sum([note["pages"] for note in notes]) / (t*int(daycalculator.sum_values)/7)
    pages_per_today = pages_per_hour * daycalculator.todayhours
    total_chapters_left = sum([note["chapters"] - note.get("chapters_read", 0) for note in notes if note.get('active', True)])  # Calculate total chapters left only for active notes
    chapters_per_hour = total_chapters_left / (t * int(daycalculator.sum_values) / 7)
    chapters_per_today = chapters_per_hour * daycalculator.todayhours
except ZeroDivisionError:
    print("it will resolve after a restart of the program..")
    
if __name__ == '__main__':
    main()

