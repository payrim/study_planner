from datetime import datetime, timedelta
import os
import json
from utils import colors, foldermaker
from utils.clearterminal import clear_terminal
from estimations import estimation, freeplanner, xestimation, bookplanner
from modules import (activity, calendar, daycalculator, endeavor, exercise,
                     flashcard, goals, newbook, notes, project, tasks,
                     repetition, subjects, weighttracker , videolecture,
                     Streaktracker, schedule, notewriter, gpt)

start_file = os.path.join(colors.notes_file, 'start.json')

def main():
    activity.check_work_finished()
    start_time = None
    if os.path.exists(start_file):
        with open(start_file, "r") as file:
            start_data = json.load(file)
        start_time = datetime.strptime(start_data["start_time"], "%Y-%m-%d %H:%M:%S")
    if start_time:
                if start_time.date() != datetime.now().date():
                    start_time = None
                    os.remove(start_file)
    clear_terminal()

    while True:
        #print("{:+^80}\n".format(""))
        print(colors.WWITE+"\n")
        print(colors.space*9+"{:^80}".format("VISION GUIDE"))
        #print("{:+^84}".format(""))
        print(colors.space*7+colors.plus*42)
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" a. activity  - activity log",   " m. flashcard - language flashcard"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" r. remind    - spaced repetition",  " b. books     - current books repo(n)"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" d. Endeavor  - daily planner",      " v. video     - video lecture"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" w. weight    - weight tracker",     " t. project   - project estimation(t/tfb)"))
        print(colors.space*7+colors.plus+colors.line*19+" "+colors.line*21+colors.plus)
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" k. tasks     - kanban board", " g. goals     - modify goals"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" p. project   - project automation", " u. subject   - subject selector"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" s. schedule  - weekly schedule",      " o. notes     - description note(no) "))
        print(colors.space*7+colors.plus+colors.line*19+" "+colors.line*21+colors.plus)
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" c. calendar  - calendar program      ", " x. exercises - exercise planner"))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" j. date      - change cycle date", " y. streaks   - streak tracker "))
        print(colors.space*7+"‖{:<39}‖{:<42}‖".format(" e. task      - show active task(f)", " i. prompts   - gpt prompts "))
        print(colors.space*7+"‖"+colors.plus*19+"  "+colors.plus*21+"‖")
        print("")
        print(colors.space*7+"{:<50}{:>30}".format(f"{daycalculator.days} days left {daycalculator.tldata()}", f"Today is {daycalculator.weektoday}"))
    
        #print(f"hours in a week is {daycalculator.sum_values}, estimated work is {daycalculator.todayhours} hour and {round(books.pages_per_today)} pages.")


        try:
            if activity.work_finished == False:           
                print()
                schedule.print_first_entry_from_json()
                if start_time:
                    time_elapsed = str(datetime.now() - start_time).split('.')[0]
                    print(f"{colors.space*7}{colors.CYAN}Start Time: {colors.WWITE}{start_time.strftime('%H:%M:%S')}{colors.CYAN} - Elapsed Time: {colors.WWITE}{str(time_elapsed)}{colors.RESET}")
                else:
                    print(f"{colors.space*7}{colors.RED}Start Button{colors.RESET} - {colors.YELLOW}Press [sa] {colors.RESET}{colors.YELLOW}to start the button.{colors.RESET}")
                #activity.calculate_activity_rating()
                activity.check_work_finished()
            else:
                activity.check_work_finished()

            print(colors.space*7+colors.cline*15)
            print(colors.space*7+colors.folder+"(tr) trackers"+colors.space*7+colors.folder+"(re) reminders")
            print(colors.space*7+colors.folder+"(ex) exercises"+colors.space*6+colors.folder+"(ta) tasks")
            print(colors.space*7+colors.folder2+"(sc/pc) schedule"+colors.space*4+colors.folder2+"(ro) routine")
            print(colors.space*7+colors.folder2+"(sg) goals"+colors.space*10+colors.folder2+"(ss) subgoals")
            print(colors.space*7+colors.folder2+"(sf) streaks"+colors.space*8+colors.plus+"(q)  quit")
        except:
            print("\n\nERROR: PROCESS UNIDENTIFIED")
        print(f"\n{colors.space*7}time left till end of the day: {daycalculator.hours} hours, {daycalculator.minutes} minutes.")
        select = input(colors.space*7+"what you wanna do(cc to clock out)?:   ")

        if select == "d":
            clear_terminal()
            endeavor.main()
        elif select == "k":
            clear_terminal()
            tasks.main()
        elif select == "e":
            clear_terminal()
            schedule.select_task_from_jobs()
            clear_terminal()
        elif select == "f":
            schedule.swap_tasks_in_jobdb()
            clear_terminal()
        elif select == "o":
            clear_terminal()
            notewriter.main()
        elif select == "i":
            clear_terminal()
            gpt.main()
        elif select == "sc":
            clear_terminal()
            print(f"\n\n{schedule.get_schedule_output()}")
            input(f"\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "scp":
            clear_terminal()
            schedule.plot_schedule()
            clear_terminal()
        elif select == "scc":
            clear_terminal()
            schedule.schedleft()
            clear_terminal()
        elif select == "sg":
            clear_terminal()
            print("\n\n")
            loaded_goals = goals.load_goals()
            saved_dates = goals.load_or_create_daygoals()
            date_differences = goals.calculate_date_difference(saved_dates)
            goals.remove_days_from_active_goals(loaded_goals, date_differences)
            goals.print_active_goals(loaded_goals, date_differences)
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "sf":
            clear_terminal()
            Streaktracker.show_streaks()
            input(f"{colors.YELLOW}\n\nPress any key to continue...")
            clear_terminal()
        elif select == "ss":
            clear_terminal()
            subgoals = goals.load_subgoals()
            goals.show_first_unchecked_subgoal(subgoals)
            input(f"\n\n{colors.space*5}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "re":
            clear_terminal()
            repetition.show_reminders()
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "s":
            clear_terminal()
            schedule.main()
            clear_terminal()
        elif select =="x":
            clear_terminal()
            exercise.main()
        elif select == "g":
            clear_terminal()
            goals.main()
        elif select == "ro":
            clear_terminal()
            endeavor.show_endeavors()
            clear_terminal()
        elif select == "sa":
            clear_terminal()
            start_time = datetime.now()
            start_data = {"start_time": start_time.strftime("%Y-%m-%d %H:%M:%S")}
            with open(start_file, "w") as file:
                json.dump(start_data, file)
        elif select == "no":
            clear_terminal()
            print("\n\n||list of notes||")
            print("\n" + colors.GREEN + "~~~"+colors.CYAN +"informative notes"+colors.GREEN+"~~~" + colors.RESET)
            print(colors.BLUE + "1. trackers and tasks" + colors.RESET)
            print(colors.BLUE + "2. reminders" + colors.RESET)
            print("\n" + colors.GREEN + "~~~"+colors.CYAN+"long notes"+colors.GREEN+"~~~" + colors.RESET)
            print(colors.BLUE + "3. goals" + colors.RESET)
            print(colors.BLUE + "4. books and notes" + colors.RESET)
            print(colors.BLUE + "5. trackers" + colors.RESET)
            print(colors.BLUE + "6. tasks" + colors.RESET)
            print(colors.BLUE + "7. video lectures" + colors.RESET)
            print(colors.WPURPLE + "8. Main NOTES" + colors.RESET)
            note_choice = input("\n" + colors.YELLOW + "What note do you want to select?" + colors.RESET + " ")
            if note_choice == "1":
                clear_terminal()
                notewriter.show_note()
                clear_terminal()   
            elif note_choice == "2":
                clear_terminal()
                repetition.show_reminder_notes()  
                clear_terminal()   
            elif note_choice == "3":
                goals.edit_notes()
                clear_terminal()   
            elif note_choice == "4":
                clear_terminal()
                print("\n\n" + colors.CYAN + "~~~~~~~\nb. book\nn. note" + colors.RESET)
                bn = input("\n" + colors.YELLOW + "Book or note (b/n)?" + colors.RESET + " ")
                if bn == 'b':
                    newbook.edit_notes()
                    clear_terminal()   
                elif bn == 'n':
                    notes.edit_notes()
                    clear_terminal()
                else:
                    clear_terminal()
            elif note_choice == "5":
                estimation.edit_notes()
                clear_terminal()
            elif note_choice == "6":
                tasks.edit_notes()
                clear_terminal()
            elif note_choice == "7":
                videolecture.edit_notes()
                clear_terminal()
            elif note_choice == "8":
                notewriter.edit_notes()
                clear_terminal()
        elif select == "ta":
            clear_terminal()
            tasks.taskfile(show=False)
        elif select == "cc":
            choices = input(colors.space*7+"Are you sure(y/n)? ")
            if choices.lower() == 'y':
                activity.calculate_and_save_activity_rating()
            else:
                clear_terminal()
        elif select == "tr":
            clear_terminal()
            try:
                estimation.tracker_greedy()
                xestimation.tracker_greedy()
                freeplanner.tracker_greedy()
                bookplanner.tracker_greedy()
            except:
                print("\n\nERROR: PROCESS UNIDENTIFIED")
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "ex":
            clear_terminal()
            print()
        #try:
            today_index = (datetime.today().weekday() + 2) % 7
            exercise_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            today = exercise_days[today_index]
            exercise_data = exercise.load_data()
            print()
            exercise.show_exercise(exercise_data, today)
        # except:
        #     print("\n\nERROR: PROCESS UNIDENTIFIED")
            input(f"\n\n{colors.space*3}{colors.YELLOW}press any key to continue...{colors.RESET}")
            clear_terminal()
        elif select == "p":
            clear_terminal()
            project.main()
        elif select == "t":
            clear_terminal()
            estimation.main()
        elif select == "tt":
            clear_terminal()
            xestimation.main()
        elif select == "tb":
            clear_terminal()
            bookplanner.main()
        elif select == "tf":
            clear_terminal()
            freeplanner.main()
        elif select == "v":
            clear_terminal()
            videolecture.main()
            clear_terminal()  
        elif select == "a":
            clear_terminal()
            activity.main()
        elif select == "r":
            clear_terminal()
            repetition.main()
        elif select == "u":
            clear_terminal()
            subjects.main()
        elif select == "b":
            clear_terminal()
            newbook.main()
        elif select == "m":
            clear_terminal()
            flashcard.main()
        elif select == "c":
            clear_terminal()
            calendar.main()
        elif select == "j":
            clear_terminal()
            daycalculator.save_date_to_json()
            daycalculator.save_tilldata()
            clear_terminal()
            print("!day changed, please reload the program\n")
        elif select == "n":
            clear_terminal()
            notes.main()
        elif select == "w":
            clear_terminal()
            weighttracker.main()
        elif select == "y":
            clear_terminal()
            Streaktracker.main()
        elif select == "q":
            clear_terminal()
            break
        else:
            clear_terminal()


if __name__ == '__main__':
    main()