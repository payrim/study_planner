import json
from datetime import date, datetime, timedelta
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from utils.clearterminal import clear_terminal
from utils import colors

WEIGHT_DB = os.path.join(colors.notes_file, 'weight_data.json')
CAL_DB = os.path.join(colors.notes_file, 'calorie_data.json')

def save_data(data,DB):
    with open(DB, 'w') as file:
        json.dump(data, file)


def load_data(DB):
    try:
        with open(DB, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def add_entry(data):
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    for entry in data:
        if entry["date"] == date_str:
            replace = input(f"\nToday's date ({date_str}) is already added. Do you want to replace it? (y/n): ")
            if replace.lower() == "y":
                weight = float(input("Enter the new weight: "))
                entry["weight"] = weight
                save_data(data,WEIGHT_DB)
                clear_terminal()
                print("Entry replaced successfully.")
            else:
                clear_terminal()
                print("No changes were made.")
            return
    
    weight = float(input("\nEnter the weight: "))
    entry = {"date": date_str, "weight": weight}
    data.append(entry)
    save_data(data,WEIGHT_DB)
    clear_terminal()
    print("Entry saved successfully.")

def add_calorie(data):
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    for entry in data:
            if entry["date"] == date_str:
                replace = input(f"\nToday's date ({date_str}) is already added. Do you want to add to it? (y/n): ")
                if replace.lower() == "y":
                    weight = float(input("Enter calories: "))
                    entry["weight"] += weight
                    save_data(data,CAL_DB)
                    clear_terminal()
                    print("Entry added successfully.")
                else:
                    clear_terminal()
                    print("No changes were made.")
                return
        
    weight = float(input("\nEnter calories: "))
    entry = {"date": date_str, "weight": weight}
    data.append(entry)
    save_data(data,CAL_DB)
    clear_terminal()
    print("Entry saved successfully.")


def plot_graph(data, degree=7, vector_length=16,slope = -0.2):
    try:
        # Extract the features (day) and target variable (weight)
        days = [i for i in range(len(data))]
        weights = [entry["weight"] for entry in data]

        # Create a feature matrix
        X = np.array(days).reshape(-1, 1)

        # Transform features to a polynomial of specified degree
        poly_features = PolynomialFeatures(degree=degree)
        X_poly = poly_features.fit_transform(X)

        model = LinearRegression()
        model.fit(X_poly, weights)

        # Predict weights using the model
        predicted_weights = model.predict(X_poly)

        # Sort the data points for smoother plotting
        sorted_indices = np.argsort(X.flatten())
        X_sorted = X[sorted_indices]
        predicted_weights_sorted = predicted_weights[sorted_indices]

        # Plot the original data
        plt.scatter(days, weights, label="Data", color='blue')
        # Plot the predicted values
        plt.plot(X_sorted, predicted_weights_sorted, label="Line", color='red')

        # Add the vector at the end
        last_day = days[-10]
        last_weight = weights[-10]
        last_day2 = days[-2]
        last_weight2 = weights[-2]

        # Calculate the endpoint of the vector
        vector_endpoint = (last_day + vector_length, last_weight + vector_length * slope)
        vector_endpoint2 = (last_day2 + vector_length*2, last_weight2 + vector_length*2 * slope)

        plt.arrow(
            last_day,
            last_weight,
            vector_endpoint[0] - last_day,
            vector_endpoint[1] - last_weight,
            head_width=0.1,
            head_length=0.1,
            fc='blue',
            ec='blue',
            label="Vector"
        )

        plt.arrow(
        last_day2,
        last_weight2,
        vector_endpoint2[0] - last_day2,
        vector_endpoint2[1] - last_weight2,
        head_width=0.1,
        head_length=0.1,
        fc='red',
        ec='red',
        label="Vector"
    )
        min_x = X_sorted.min()+1
        max_x = X_sorted.max()+2
        min_y = predicted_weights_sorted.min()
        max_y = predicted_weights_sorted.max()+1

        # Set the axis limits to include only the red regression line
        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)

        plt.xlabel("Day")
        plt.ylabel("Weight")
        plt.title(f"Weight Tracker ({degree})")
        plt.legend()
        plt.tight_layout()
        plt.show()
    except IndexError:
        input("need more datapoints!(press any key) ")


def calculate_average_weights(data):
    averages = {}
    print()
    for days in [3, 5, 7, 15]:
        try:
            if len(data) >= days:
                weights = [entry["weight"] for entry in data[-days:]]
                average_weight = sum(weights) / len(weights)
                averages[f"{days} days"] = average_weight
                print(f"{colors.GREEN}[Average weight for {days} days: {average_weight:3f}]{colors.RESET}")
            else:
                averages[f"{days} days"] = "Doesn't exist"
        except ZeroDivisionError:
            averages[f"{days} days"] = 0.0
    return averages


def main():
    clear_terminal()
    data = load_data(WEIGHT_DB)
    caldata = load_data(CAL_DB)

    while True:
        save_data(data,WEIGHT_DB)
        print(f"\n{colors.YELLOW}||Weight Tracker Menu||{colors.RESET}\n")
        print(f"{colors.CYAN}wa.{colors.RESET} {colors.YELLOW}Add weight entry{colors.RESET}")
        print(f"{colors.CYAN}ca.{colors.RESET} {colors.YELLOW}Add calorie entry{colors.RESET}")
        print(f"{colors.CYAN}s.{colors.RESET} {colors.YELLOW}Save data{colors.RESET}")
        print(f"{colors.CYAN}l.{colors.RESET} {colors.YELLOW}Load data{colors.RESET}")
        print(f"{colors.CYAN}wp.{colors.RESET} {colors.YELLOW}Plot weight graph{colors.RESET}")
        print(f"{colors.CYAN}cp.{colors.RESET} {colors.YELLOW}Plot calorie graph{colors.RESET}")
        print(f"{colors.CYAN}q.{colors.RESET} {colors.YELLOW}Exit{colors.RESET}")

        calculate_average_weights(data)

        choice = input("\nEnter your choice: ")

        if choice == "wa":
            add_entry(data)
            clear_terminal()
        if choice == "ca":
            add_calorie(caldata)
            clear_terminal()
        elif choice == "s":
            save_data(data,WEIGHT_DB)
            save_data(data,CAL_DB)
            clear_terminal()
        elif choice == "l":
            data = load_data(WEIGHT_DB)
            caldata = load_data(CAL_DB)
            clear_terminal()
        elif choice == "wp":
            plot_graph(data)
            clear_terminal()
        elif choice == "cp":
            plot_graph(caldata)
            clear_terminal()
        elif choice == "q":
            clear_terminal()
            break
        else:
           clear_terminal()


if __name__ == "__main__":
    main()
