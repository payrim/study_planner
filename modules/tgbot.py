import requests
import json
import os
from utils import colors
from modules import schedule
from utils.clearterminal import clear_terminal

PYJSON = os.path.join(colors.notes_file, 'PYJSON.JSON')

def check_and_update_json():
    try:
        with open(PYJSON, 'r') as json_file:
            saved_data = json.load(json_file)
    except FileNotFoundError:
        saved_data = {}

    current_output = schedule.show_schedule_py()

    if not saved_data:
        with open(PYJSON, 'w') as json_file:
            json.dump({"scheduled_activity": current_output}, json_file)  # Save the current output in the same format
        pytelbot("bot initialized successfully 🎉✨")
    else:
        # If the file is not empty, compare the saved data with the current output
        if saved_data != {"scheduled_activity": current_output}:  # Compare in the same format
            # If they don't match, save the current output into a new variable
            new_data = {"scheduled_activity": current_output}
            # Overwrite PYJSON.JSON with the new output
            with open(PYJSON, 'w') as json_file:
                json.dump(new_data, json_file)
                
            telegram_output = f"⚠️you got task {current_output} right now!"
            pytelbot(telegram_output)
        else:
            # If they match, do nothing
            print("Data in PYJSON.JSON matches the current output.")

def pytelbot(current_output):
    token = "YOURTOKEN"
    url = f"https://api.telegram.org/bot{token}"
    params = {"chat_id": "YOURCHATID", "text": current_output}
    r = requests.get(url + "/sendMessage", params=params)
# Main menu
def main():
    clear_terminal()
    check_and_update_json()
    clear_terminal()

if __name__ == '__main__':
    main()