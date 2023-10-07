import json
import os
import random
import subprocess
from utils.clearterminal import clear_terminal
from utils import colors


# Global variable to store flashcards
selected_level = None
selected_dictionary = None
dictionaries = {}  # Dictionary to store dictionary names and filenames
flashcards = []    # Moved flashcards to the global scope to avoid issues
DIC_DB = os.path.join(colors.notes_file,'dictionaries.json')

# Load dictionary names and filenames from JSON file if exists
def load_dictionaries():
    global dictionaries, selected_dictionary  # Add selected_dictionary to global variables
    try:
        with open(DIC_DB, 'r') as f:
            dictionaries = json.load(f)
    except:
        dictionaries = {}

    # Set selected_dictionary to the first dictionary if available
    selected_dictionary = next(iter(dictionaries), None)

# Load data from JSON file if exists
def load_flashcards():
    global flashcards, selected_dictionary
    if selected_dictionary:
        filename = dictionaries[selected_dictionary]
        try:
            with open(filename, 'r') as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, list) and all(isinstance(card, dict) and 'level' in card for card in loaded_data):
                    flashcards = loaded_data
                else:
                    flashcards = []
        except FileNotFoundError:
            flashcards = []
    else:
        flashcards = []
    print(f"Loaded flashcards: {flashcards}")

# Function to save flashcards to the selected dictionary's file
def save_flashcards():
    if selected_dictionary:
        filename = dictionaries[selected_dictionary]
        with open(filename, 'w') as f:
            json.dump(flashcards, f)

# Function to add a new flashcard
def add_flashcard():
    global flashcards  # Add this line to use the global flashcards variable
    word = input('Enter the word: ')
    meaning = input('Enter the meaning: ')
    level = 0
    score = 0
    flashcard = {'word': word, 'meaning': meaning, 'score': score, 'level': level}
    flashcards.append(flashcard)
    save_flashcards()
    clear_terminal()
    print(f'Flashcard for "{word}" added successfully!\n')


# Function to remove a flashcard
def remove_flashcard():
    global flashcards  # Add this line to use the global flashcards variable
    word = input('\nEnter the word to remove: ')
    for flashcard in flashcards:
        if flashcard['word'] == word:
            flashcards.remove(flashcard)
            save_flashcards()
            clear_terminal()
            print(f'Flashcard for "{word}" removed successfully!\n')
            return
    print(f'Flashcard for "{word}" not found!\n')


# Function to flush all flashcards
def flush_flashcards():
    confirm = input("Are you sure you want to delete all cards? (y/n) ")
    if confirm.lower() == "y":
        global flashcards
        flashcards = []
        clear_terminal()
        print("\nAll studies removed successfully. remember to save")
    else:
        clear_terminal()
        print("cancelled.\n")

def update_flashcard_levels():
    for flashcard in flashcards:
        if flashcard['score'] >= 10:
            flashcard['score'] = 0
            flashcard['level'] += 1
        elif flashcard['level'] > 0 and flashcard['score'] < -6:
            flashcard['score'] = 0
            flashcard['level'] -= 1
    save_flashcards()

def show_flashcard():
    min_score = min(flashcards, key=lambda x: x['score'])['score']
    max_score = min(min_score + 3, max(flashcards, key=lambda x: x['score'])['score'] + 1)

    candidates = [
        flashcard for flashcard in flashcards
        if flashcard['level'] == selected_level
    ]
    
    if not candidates:
        print('No flashcards to show!\n')
        return
    
    correct_multiplier = 1
    incorrect_multiplier = 2.1

    flashcard = random.choice(candidates)
    # Ask for meaning
    meaning = input(f'\n\nWhat is the meaning of "{flashcard["word"]}"?\n     :   ')
    #Split the meanings by commas and remove leading/trailing whitespace
    meanings = [m.strip() for m in flashcard['meaning'].split(',')]
    if meaning in meanings:
        if flashcard['level'] == 0:
            flashcard['score'] += correct_multiplier+0.7
        elif flashcard['level'] == 1:
            flashcard['score'] += correct_multiplier+0.6
        elif flashcard['level'] == 2:
            flashcard['score'] += correct_multiplier+0.4
        elif flashcard['level'] == 3:
            flashcard['score'] += correct_multiplier+0.2
        elif flashcard['level'] == 4:
            flashcard['score'] += correct_multiplier+0.1
        elif flashcard['level'] > 4:
            flashcard['score'] += correct_multiplier
        print(f"{colors.YELLOW}Correct!\n{colors.YELLOW}")
    else:
        flashcard['score'] -= incorrect_multiplier
        print(f"{colors.YELLOW}\nIncorrect!{colors.RESET} The correct meanings are:")
        for i, correct_meaning in enumerate(meanings, start=1):
            print(f'- {correct_meaning}')
    # Play sound using mpv if available
    print("")
    if "sound_path" in flashcard:
        sound_file_path = flashcard["sound_path"]
        subprocess.run(['mpv', sound_file_path])
    save_flashcards()


def set_selected_level_to_highest():
    global selected_level, flashcards
    levels = set(flashcard['level'] for flashcard in flashcards)
    if levels:
        selected_level = max(levels)
    else:
        selected_level = None


def select_level():
    global selected_level
    levels = set(flashcard['level'] for flashcard in flashcards)
    print("Available levels:", levels)
    selected_level = int(input("Select a level: "))

def random_flashcard():
    if not flashcards:
        print('No flashcards to show!\n')
        return

    level_flashcards = [flashcard for flashcard in flashcards if flashcard['level'] == selected_level]
    if not level_flashcards:
        print('No flashcards for the selected level!\n')
        return
    flashcard = random.choice(level_flashcards)
    print(f'The word is "{flashcard["word"]}". Its meaning is "{flashcard["meaning"]}".\n')


def show_flashcards():
    if selected_level is None:
        print('Please select a level first!\n')
        return

    if not flashcards:
        print('No flashcards to show!\n')
        return

    level_flashcards = [flashcard for flashcard in flashcards if flashcard['level'] == selected_level]
    if not level_flashcards:
        print(f'No flashcards for level {selected_level}!\n')
        return

    print(f"Flashcards for level {selected_level}:")
    print("---------------------------")
    sorted_flashcards = sorted(level_flashcards, key=lambda x: x['score'])
    print('{:<20} {:<38} {:<10}'.format('Word', 'Meaning', 'Score'))
    for flashcard in sorted_flashcards:
        print('{:<20} {:<38} {:<10}'.format(flashcard['word'], flashcard['meaning'], flashcard['score']))

def show_words_only():
    if selected_level is None:
        print('Please select a level first!\n')
        return

    if not flashcards:
        print('No flashcards to show!\n')
        return

    level_flashcards = [flashcard for flashcard in flashcards if flashcard['level'] == selected_level]
    if not level_flashcards:
        print(f'No flashcards for level {selected_level}!\n')
        return

    print(f"Flashcards for level {selected_level}:")
    print("---------------------------")
    sorted_flashcards = sorted(level_flashcards, key=lambda x: x['score'])
    print('{:<20} {:<10}'.format('Word', 'Score'))
    for flashcard in sorted_flashcards:
        print('{:<20} {:<10}'.format(flashcard['word'], flashcard['score']))

def print_selected_level():
    if not flashcards:
        print("No flashcards available.")
        return

    levels = set(flashcard['level'] for flashcard in flashcards)
    if selected_level is None:
        max_level = max(levels)
        print(f"\n{colors.GREEN}[Selected level is {max_level}]{colors.RESET}")
    else:
        print(f"\n{colors.GREEN}[Selected level is {selected_level}]{colors.RESET}")

# Function to show available dictionaries
def show_available_dictionaries():
    clear_terminal()
    if not dictionaries:
        print('No dictionaries available. Please add a new dictionary.\n')
        return

    print(f"\n\n{colors.BLUE}Available dictionaries:{colors.RESET}")
    for idx, name in enumerate(dictionaries.keys()):
        print(f'{colors.CYAN}{idx + 1}.{colors.RESET}{colors.GREEN} {name}{colors.RESET}')

        

def add_dictionary():
    name = input('Enter the name of the new dictionary: ')
    filename = f'{name.lower()}.json'  # Using lowercase name as the filename
    dictionaries[name] = filename
    with open(filename, 'w') as f:
        json.dump([], f)
    save_dictionaries()
    print(f'Dictionary "{name}" added successfully!\n')

def save_dictionaries():
    with open(DIC_DB, 'w') as f:
        json.dump(dictionaries, f)

# Function to remove a dictionary
def remove_dictionary():
    show_available_dictionaries()
    name = input('Enter the name of the dictionary to remove: ')
    filename = dictionaries.get(name)
    if filename:
        confirm = input(f'Are you sure you want to remove the dictionary "{name}"? (y/n) ')
        if confirm.lower() == 'y':
            del dictionaries[name]
            os.remove(filename)
            save_dictionaries()
            print(f'Dictionary "{name}" removed successfully!\n')
        else:
            print('Canceled.\n')
    else:
        print(f'Dictionary "{name}" not found!\n')

# Function to select a dictionary to work with
def select_dictionary():
    global selected_dictionary
    if not dictionaries:
        print('No dictionaries available. Please add a new dictionary.\n')
        return

    print(f"{colors.YELLOW}Available dictionaries:{colors.RESET}")
    for idx, name in enumerate(dictionaries.keys()):
        print(f'{colors.CYAN}{idx + 1}.{colors.RESET}{colors.YELLOW} {name}{colors.RESET}')

    selected_idx = input('Enter the index of the dictionary you want to use: ')
    try:
        selected_idx = int(selected_idx)
        if 1 <= selected_idx <= len(dictionaries):
            selected_dictionary = list(dictionaries.keys())[selected_idx - 1]
            print(f'Selected dictionary: {selected_dictionary}\n')
            return selected_dictionary  # Return the selected dictionary name
        else:
            print('Invalid index.\n')
    except ValueError:
        print('Invalid input. Please enter a valid index.\n')

def select_dictionaryi(selected_idx):
    global selected_dictionary
    try:
        selected_idx = int(selected_idx)
        if 1 <= selected_idx <= len(dictionaries):
            selected_dictionary = list(dictionaries.keys())[selected_idx - 1]
            print(f'Selected dictionary: {selected_dictionary} \n')
            return selected_dictionary  # Return the selected dictionary name
        else:
            print('Invalid index.\n')
            return None  # Return None when the index is invalid
    except ValueError:
        print('Invalid input. Please enter a valid index.\n')
        return None  # Return None when the input is not a valid index

def extract_meanings(lines):
    meanings = []
    is_translations_section = False

    for line in lines:
        line = line.strip()
        if line == "## Translations":
            is_translations_section = True
        if line.startswith("- en:") and is_translations_section:
            meaning = line[len("- en: "):].strip()
            meanings.append(meaning)


    return ",".join(meanings)

def import_flashcards():
    dictionary_name = input("Enter the name of the dictionary to import: ")
    directory = input("Enter the directory where the .md files are located: ")

    flashcards_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r') as f:
                lines = f.readlines()
                word = filename[:-3]  # Remove the '.md' extension
                meaning = extract_meanings(lines)
                flashcard = {'word': word, 'meaning': meaning, 'score': 0, 'level': 0}
                flashcards_data.append(flashcard)

    return dictionary_name, flashcards_data

def remove_flashcards_without_meaning():
    global flashcards
    flashcards = [flashcard for flashcard in flashcards if flashcard['meaning'].strip() != '']
    save_flashcards()
    clear_terminal()
    print("Flashcards without meaning removed successfully!\n")

def import_flashcards_from_anki():
    dictionary_name = input("Enter the name of the dictionary to import: ")
    directory = input("Enter the path to the Anki JSON file: ")
    flashcards_data = []
    
    with open(directory, 'r', encoding='utf-8') as f:
        anki_data = json.load(f)
    
    notes = anki_data.get("notes", [])
    
    for note in notes:
        k = note.get("fields", [])
        print(k)
    change = input("do you want the meaning to be first or last?(f/l)")

    for note in notes:
        fields = note.get("fields", [])
        
        if len(fields) >= 2:
            if change == "f":
                meaning = fields[0]
                word = fields[1]
            elif change == "l":
                meaning = fields[1]
                word = fields[0]
            
            meaning = meaning.replace("/", ",")  # Convert '/' to ','
            flashcard = {'word': word, 'meaning': meaning, 'score': 0, 'level': 0}
            flashcards_data.append(flashcard)
    
    return dictionary_name, flashcards_data


def import_flashcards_from_anki_complex():
    dictionary_name = input("Enter the name of the dictionary to import: ")
    json_path = input("Enter the path to the Anki JSON file: ")
    flashcards_data = []
    
    with open(json_path, 'r', encoding='utf-8') as f:
        anki_data = json.load(f)
    
    notes = anki_data.get("notes", [])

    for note in notes:
        fields = note.get("fields", [])
        
        if len(fields) >= 2:
            word = fields[0]
            meanings = [field for field in fields[1:] if field and not field.startswith("[sound:")]
            sound_file = [field for field in fields if field.startswith("[sound:")][0]
            
            meanings_str = ",".join(meanings)
            word = word.replace("/", ",")  # Convert '/' to ','
            
            sound_file_name = sound_file.split("[sound:")[1].split("]")[0]
            sound_path = os.path.join(os.path.dirname(json_path), sound_file_name)
            
            flashcard = {'word': word, 'meaning': meanings_str, 'sound_path': sound_path, 'score': 0, 'level': 0}
            flashcards_data.append(flashcard)
    
    return dictionary_name, flashcards_data


def main():
    clear_terminal()
    load_dictionaries()
    selected_dictionary = None  # Initialize selected_dictionary variable here
    while True:
        show_available_dictionaries()
        print(f"\n{colors.YELLOW}||Dictionary Management Menu||\n{colors.RESET}")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add a new dictionary{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove a dictionary{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Load a dictionary{colors.RESET}")
        print(f"{colors.CYAN}i.{colors.RESET} {colors.YELLOW}Import flashcard{colors.RESET}")
        print(f"{colors.CYAN}ia.{colors.RESET} {colors.YELLOW}Import from Anki{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Return to main menu{colors.RESET}")

        choice = input('\nEnter your choice: ')
        if choice == 'a':
            clear_terminal()
            add_dictionary()
        elif choice == 'r':
            clear_terminal()
            remove_dictionary()
        elif choice == "ia":
            clear_terminal()
            complexity = input("is the JSON straightforward or complex(e/c)? ")
            if complexity == "e":
                dictionary_name, flashcards_data = import_flashcards_from_anki()
            elif complexity == "c":
                dictionary_name, flashcards_data = import_flashcards_from_anki_complex()
            dictionaries[dictionary_name] = f'{dictionary_name.lower()}.json'
            with open(dictionaries[dictionary_name], 'w') as f:
                json.dump(flashcards_data, f)
            save_dictionaries()
            selected_dictionary = dictionary_name
            flashcards_menu(selected_dictionary)
        elif choice == 'l':
            clear_terminal()
            selected_dictionary = select_dictionary()  # Update the selected_dictionary variable here
            if selected_dictionary:
                flashcards_menu(selected_dictionary)
        elif choice == 'i':
            clear_terminal()
            dictionary_name, flashcards_data = import_flashcards()
            dictionaries[dictionary_name] = f'{dictionary_name.lower()}.json'
            with open(dictionaries[dictionary_name], 'w') as f:
                json.dump(flashcards_data, f)
            save_dictionaries()
            selected_dictionary = dictionary_name
            flashcards_menu(selected_dictionary)
        elif choice == 'q':
            clear_terminal()
            break
        elif choice.isdigit():
            selected_idx = int(choice)
            select_dictionaryi(selected_idx)
            a = select_dictionaryi(selected_idx) 
            if selected_idx:
                flashcards_menu(a)
                
        else:
            clear_terminal()
            print('Invalid choice!\n')


def flashcards_menu(selected_dictionary):
    # Load flashcards for the selected dictionary
    global selected_level
    selected_level = None  # colors.RESET selected_level when entering the flashcards menu
    load_flashcards()
    set_selected_level_to_highest()
    clear_terminal()
    while True:
        update_flashcard_levels()
        print(f"\n\n{colors.YELLOW}||{selected_dictionary} Flashcards||{colors.RESET}\n")
        print(f"{colors.CYAN}a.{colors.RESET} {colors.YELLOW}Add flashcard{colors.RESET}")
        print(f"{colors.CYAN}r.{colors.RESET} {colors.YELLOW}Remove flashcard{colors.RESET}")
        print(f"{colors.CYAN}f.{colors.RESET} {colors.YELLOW}Flush all flashcards{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Show a flashcard and ask for meaning{colors.RESET}")
        print(f"{colors.CYAN}d.{colors.RESET} {colors.YELLOW}Show a random flashcard{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Select level{colors.RESET}")
        print(f"{colors.CYAN}x.{colors.RESET} {colors.YELLOW}Show flashcards sorted by score with word and meaning{colors.RESET}")
        print(f"{colors.CYAN}z.{colors.RESET} {colors.YELLOW}Show flashcards sorted by score with word only{colors.RESET}")
        print(f"{colors.CYAN}m.{colors.RESET} {colors.YELLOW}Remove flashcards without meaning{colors.RESET}")
        print(f"{colors.CYAN}w.{colors.RESET} {colors.YELLOW}Save{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Exit{colors.RESET}")
        print_selected_level()
        choice = input('\nEnter your choice: ')
        if choice == 'a':
            clear_terminal()
            add_flashcard()
        elif choice == 'r':
            clear_terminal()
            show_words_only()
            remove_flashcard()
            clear_terminal()
        elif choice == 'f':
            clear_terminal()
            flush_flashcards()
        elif choice == 's':
            clear_terminal()
            show_flashcard()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'd':
            clear_terminal()
            random_flashcard()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'x':
            clear_terminal()
            show_flashcards()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'z':
            clear_terminal()
            show_words_only()
            input("\n\npress any key to continue......")
            clear_terminal()
        elif choice == 'w':
            save_flashcards()
            clear_terminal()
            print("file saved!\n")
        elif choice == 'l':
            clear_terminal()
            select_level()
            clear_terminal()
        elif choice == 'm':
            clear_terminal()
            remove_flashcards_without_meaning()
        elif choice == 'q':
            clear_terminal()
            break
        else:
            clear_terminal()
            print('Invalid choice!\n')

if __name__ == '__main__':
    main()
