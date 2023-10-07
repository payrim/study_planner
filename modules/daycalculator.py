import datetime as dt
import json
import os
from utils import colors
from utils.clearterminal import clear_terminal

tilldata_str="no reason"
TILL_DB = os.path.join(colors.notes_file, 'tilldata.json')
DATE_DB = os.path.join(colors.notes_file, 'date.json')


def save_tilldata():
    # prompt user for date
    tilldata = input("what is the purpose of this number? ")

    # create dictionary to store date
    data = {"data":tilldata}

    # serialize dictionary to JSON and write to file
    with open(TILL_DB, "w") as f:
        json.dump(data, f)

def tldata():
    try:
        # read data from JSON file
        with open(TILL_DB, "r") as f:
            data = json.load(f)
        # extract tilldata from data dictionary
        tilldata_str = data["data"]
        return data["data"]
    except FileNotFoundError:
        # if file does not exist, prompt user for date and save to file
        save_tilldata()

hours = {
    "Saturday": 12,
    "Sunday":  9,
                    #2-9
    "Monday": 9,
                     #4-9 -2
    "Tuesday": 6,
                     #6-17 +1 at uni
    "Wednesday": 11,
                     #4-9
    "Thursday":12,
    "Friday": 12
}
sum_values = sum([v for v in hours.values() if isinstance(v, int)])


def save_date_to_json():
    # prompt user for date
    while True:
        date = input("Enter the date (today/tomorrow or a number): ")
        if date == "today":
            start = dt.datetime.now().strftime("%Y,%m,%d")
            break
        elif date == "tomorrow":
            start = (dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y,%m,%d")
            break
        elif date.isdigit():
            days = int(date)
            start = (dt.datetime.now() + dt.timedelta(days=days)).strftime("%Y,%m,%d")
            break
        else:
            try:
                start = dt.datetime.strptime(date, "%d-%m-%Y").strftime("%Y,%m,%d")
                break
            except ValueError:
                print("Invalid date format. Try again.")

    # create dictionary to store date
    data = {"date": start}

    # serialize dictionary to JSON and write to file
    with open(DATE_DB, "w") as f:
        json.dump(data, f)

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as e:
            print(f"Error creating directory '{directory_path}': {e}")

def read_date_from_json():
    ensure_directory_exists(os.path.dirname(DATE_DB))

    try:
        # read data from JSON file
        with open(DATE_DB, "r") as f:
            data = json.load(f)
        # extract date from data dictionary
        date_str = data["date"]
        date = dt.datetime.strptime(date_str, "%Y,%m,%d").date()
        return date
    except (FileNotFoundError, KeyError):
        # If the file doesn't exist or doesn't contain the date, prompt user for date and save to file
        print(f"{colors.line2*40}")
        print(f"{colors.YELLOW}\n\nWellcome to the planner!\n{colors.RESET}{colors.GREEN}the warnings above are just warnings, probably..., so don't mind them!{colors.RESET}")
        print(f"{colors.WWITE}and thanks for using this program.")
        print("\nthis is a day counter for some legacy parts of the planner and also a reminder to the user.")
        save_date_to_json()
        print("you must also set a purpose for the number.")
        save_tilldata()
        clear_terminal()
        input(f"\n\n\n{colors.space*3}{colors.CYAN}Also...{colors.WWITE} before you go, please restart the program after launching so that it would cause less harm to your computer.\n{colors.space*3}(jk, no harm done, just bugs may occur!) okay? (okay,no,yea,sure,Fuck You): ")
        # Return a default date or handle this case as needed
        return dt.date.today()

# def read_date_from_json():
#     try:
#         # read JSON data from file
#         with open(DATE_DB, "r") as f:
#             data = json.load(f)
#             return dt.datetime.strptime(data["date"], "%d-%m-%Y").date()
#     except FileNotFoundError:
#         # if file does not exist, save target date to file
#         save_date_to_json()
#         return target_date
# start = target_date.strftime("%d-%m-%Y")

# deadline semester 8
target_date = read_date_from_json()
date = dt.date.today()
delta = target_date - date
days = delta.days

today = dt.datetime.today()
today1 = today + dt.timedelta(days=0)
today_index = today1.weekday()
weektoday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][today_index]
todayhours = hours[weektoday]


now = dt.datetime.now()
end_of_day = now.replace(hour=22, minute=0, second=0, microsecond=0)
time_left = end_of_day - now

total_seconds = int(time_left.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60


