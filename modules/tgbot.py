import requests
import json
import os
from utils import colors
from modules import schedule
from utils.clearterminal import clear_terminal

PYJSON = os.path.join(colors.notes_file, 'PYJSON.JSON')
SCH_TXT = os.path.join(colors.notes_file, 'plan.txt')
JOB_TXT = os.path.join(colors.notes_file, 'jobtodo.txt')
JobDB = os.path.join(colors.notes_file, 'jobdo.json')
TIMEJC = os.path.join(colors.notes_file, 'timejc.json')
EBDB = os.path.join(colors.notes_file, 'endeavors.json')

def check_and_update_json():
    try:
        with open(PYJSON, 'r') as json_file:
            saved_data = json.load(json_file)
    except FileNotFoundError:
        saved_data = {}

    current_output = schedule.show_schedule_py()

    if not saved_data:
        with open(PYJSON, 'w') as json_file:
            json.dump(current_output, json_file)
        pytelbot("bot initialized successfully 🎉✨")
    else:
        # If the file is not empty, compare the saved data with the current output
        if saved_data != current_output:
            # If they don't match, save the current output into a new variable
            new_data = current_output
            # Overwrite PYJSON.JSON with the new output
            with open(PYJSON, 'w') as json_file:
                json.dump(new_data, json_file)
            telegram_output = f"⚠️you got task {current_output} right now!"
            pytelbot(telegram_output)
            
            # Save the scheduled activity line to the pyJSON file
            with open(PYJSON, 'w') as json_file:
                json.dump({"scheduled_activity": current_output}, json_file)
        else:
            # If they match, do nothing
            print("Data in PYJSON.JSON matches the current output.")

def pytelbot(current_output):
    token = "INSET_YOUR_TOKEN_HERE"
    url = f"https://api.telegram.org/bot{token}"
    params = {"chat_id": "INSERT_YOUR_TOKEN_HERE", "text": current_output}
    r = requests.get(url + "/sendMessage", params=params)
# Main menu
def main():
    clear_terminal()
    check_and_update_json()
    clear_terminal()

if __name__ == '__main__':
    main()
