import csv
from collections import Counter  # Counter is imported for task B calculations
from graphics import GraphWin, Rectangle, Text, Point  # Import for Task D

# Task A starts here

# Function to read the CSV file and return a list of rows
def read_csv_file(file_name):
    """
    Reads the CSV file with vehicle data and returns a list of rows.
    Skips the header row and stores each subsequent row as a list of strings.
    """
    data_list = []
    try:
        with open(file_name, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header
            for row in csv_reader:
                data_list.append(row)
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found. Please check the file path.")
        return []  # Return an empty list if the file is not found
    return data_list


# Task B starts here

def total_vehicles(data):
    return len(data)

def total_trucks(data):
    return sum(1 for row in data if row[8] == 'Truck')

def total_electric_vehicles(data):
    return sum(1 for row in data if row[9] == 'TRUE')  # Electric Hybrid column

def total_two_wheeled(data):
    return sum(1 for row in data if row[8] in ['Bike', 'Motorbike', 'Scooter'])

def total_buses_north(data):
    return sum(1 for row in data if row[0] == 'Elm Avenue/Rabbit Road' and row[3] == 'N' and row[8] == 'Bus')

def total_no_turns(data):
    """
    Calculates the number of vehicles that enter and exit a junction without turning.
    Rows with missing direction data are skipped.
    """
    return sum(1 for row in data if row[3] == row[4])  # Direction in equals direction out

def percentage_trucks(data):
    total = len(data)
    trucks = total_trucks(data)
    return round((trucks / total) * 100)

def avg_bikes_per_hour(data):
    """
    Calculates the average number of bikes per hour for the selected date.
    """
    bike_hours = Counter(row[2][:2] for row in data if row[8] == 'Bike')  # First 2 chars of timeOfDay = hour
    total_bikes = sum(bike_hours.values())  # Total bikes across all hours
    return round(total_bikes / 24)  # Average per hour

def total_over_speed_limit(data):
    """
    Calculates the total number of vehicles recorded as over the speed limit.
    """
    count = 0
    for row in data:
        try:
            speed_limit = int(row[5])  # Convert speed limit to integer
            vehicle_speed = int(row[6])  # Convert vehicle speed to integer
            if vehicle_speed > speed_limit:
                count += 1
        except ValueError:
            # Skip rows with non-numeric data in the relevant columns
            continue
    return count

def total_vehicles_at_junction(data, junction_name):
    return sum(1 for row in data if row[0] == junction_name)

def percentage_scooters_elm(data):
    elm_total = total_vehicles_at_junction(data, 'Elm Avenue/Rabbit Road')
    scooters_elm = sum(1 for row in data if row[0] == 'Elm Avenue/Rabbit Road' and row[8] == 'Scooter')
    return round((scooters_elm / elm_total) * 100)

def busiest_hour_hanley(data):
    hanley_data = [row for row in data if row[0] == 'Hanley Highway/Westway']
    hourly_traffic = Counter(row[2][:2] for row in hanley_data)
    peak_traffic = max(hourly_traffic.values())
    peak_hours = [f"Between {hour}:00 and {int(hour)+1}:00" for hour, count in hourly_traffic.items() if count == peak_traffic]
    return peak_traffic, peak_hours

def total_rain_hours(data):
    rain_hours = set(row[2][:2] for row in data if row[7] == 'Rain')
    return len(rain_hours)


# Task D starts here

def plot_histogram(data, date):
    """
    Plot a histogram comparing traffic volume by hour for each junction.
    :param data: A dictionary with hours as keys and traffic counts for both junctions as values.
    :param date: The selected date as a string (e.g., "25/06/2024").
    """
    win = GraphWin("Histogram", 800, 600)
    win.setCoords(0, 0, 24, 100)  # Adjust scale as needed

    # Add title
    title = Text(Point(12, 95), f"Histogram of Vehicle Frequency per Hour - {date}")
    title.setSize(18)
    title.draw(win)

    # Add x-axis labels
    for hour in range(24):
        label = Text(Point(hour + 0.5, 5), str(hour))
        label.setSize(10)
        label.draw(win)

    # Plot bars for each junction
    bar_width = 0.4
    colors = {"Elm Avenue": "green", "Hanley Highway": "red"}
    for hour, counts in data.items():
        # Elm Avenue bar
        elm_bar = Rectangle(Point(hour, 10), Point(hour + bar_width, 10 + counts["Elm Avenue"]))
        elm_bar.setFill(colors["Elm Avenue"])
        elm_bar.draw(win)

        # Hanley Highway bar
        hanley_bar = Rectangle(Point(hour + bar_width, 10), Point(hour + 2 * bar_width, 10 + counts["Hanley Highway"]))
        hanley_bar.setFill(colors["Hanley Highway"])
        hanley_bar.draw(win)

    # Add legend
    elm_legend = Rectangle(Point(2, 85), Point(4, 87))
    elm_legend.setFill(colors["Elm Avenue"])
    elm_legend.draw(win)
    Text(Point(6, 86), "Elm Avenue").draw(win)

    hanley_legend = Rectangle(Point(10, 85), Point(12, 87))
    hanley_legend.setFill(colors["Hanley Highway"])
    hanley_legend.draw(win)
    Text(Point(14, 86), "Hanley Highway").draw(win)

    # Wait for user to close window
    win.getMouse()
    win.close()

def process_hourly_data(data):
    """
    Processes the CSV data and calculates traffic counts by hour for each junction.
    Returns a dictionary with hours as keys and traffic counts for both junctions as values.
    """
    hourly_data = {hour: {"Elm Avenue": 0, "Hanley Highway": 0} for hour in range(24)}
    for record in data:
        hour = int(record[2][:2])  # Extract hour from timeOfDay
        junction = record[0]
        if "Elm Avenue" in junction:
            hourly_data[hour]["Elm Avenue"] += 1
        elif "Hanley Highway" in junction:
            hourly_data[hour]["Hanley Highway"] += 1
    return hourly_data

# Function to save results to a text file
def save_results_to_file(results):
    with open("results.txt", "a") as file:
        for result in results:
            file.write(result + "\n")


# Main function to run the program and display results
def main():
    # Prompt user for the day of the survey
    while True:
        try:
            print("Please enter the day of the survey in the format dd: ", end="")
            survey_day = int(input().strip())
            if not (1 <= survey_day <= 31):
                print("Out of range - values must be in the range 1 and 31.")
            else:
                break
        except ValueError:
            print("Integer required")

    # Prompt user for the month of the survey
    while True:
        try:
            print("Please enter the month of the survey in the format MM: ", end="")
            survey_month = int(input().strip())
            if not (1 <= survey_month <= 12):
                print("Out of range - values must be in the range from 1 to 12.")
            else:
                break
        except ValueError:
            print("Integer required")

    # Prompt user for the year of the survey
    while True:
        try:
            print("Please enter the year of the survey in the format YYYY: ", end="")
            survey_year = int(input().strip())
            if not (2000 <= survey_year <= 2024):
                print("Out of range - values must range from 2000 and 2024.")
            else:
                break
        except ValueError:
            print("Integer required")

    file_name = f"traffic_data15062024.csv"  # CSV file for testing
    data_list = read_csv_file(file_name)

    if not data_list:
        print("No data available.")
        return

    # Collecting results into a list
    results = [
        f"Data file selected: {file_name}",
        f"The total number of vehicles recorded for this date is: {total_vehicles(data_list)}",
        f"The total number of trucks recorded for this date is: {total_trucks(data_list)}",
        f"The total number of electric vehicles for this date is: {total_electric_vehicles(data_list)}",
        f"The total number of two-wheeled vehicles for this date is: {total_two_wheeled(data_list)}",
        f"The total number of busses leaving Elm Avenue/Rabbit Road heading North is: {total_buses_north(data_list)}",
        f"The total number of vehicles through both junctions not turning left or right is: {total_no_turns(data_list)}",
        f"The percentage of total vehicles recorded that are trucks for this date is: {percentage_trucks(data_list)}%",
        f"The average number of Bikes per hour for this date is: {avg_bikes_per_hour(data_list)}",
        f"The total number of Vehicles recorded as over the speed limit for this date is: {total_over_speed_limit(data_list)}",
        f"The total number of Vehicles recorded through Elm Avenue/Rabbit Road is: {total_vehicles_at_junction(data_list, 'Elm Avenue/Rabbit Road')}",
        f"The total number of Vehicles recorded through Hanley Highway/Westway Junction is: {total_vehicles_at_junction(data_list, 'Hanley Highway/Westway')}",
        f"Percentage of scooters at Elm Avenue/Rabbit Road: {percentage_scooters_elm(data_list)}%",
    ]

    peak_traffic, peak_hours = busiest_hour_hanley(data_list)
    results.append(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {peak_traffic}")
    results.append(f"The most vehicles through Hanley Highway/Westway were recorded {', '.join(peak_hours)}")


    # Print results to console
    for result in results:
        print(result)

    # Save the results to the text file
    save_results_to_file(results)

    # Task D: Generate and display the histogram
    hourly_data = process_hourly_data(data_list)
    plot_histogram(hourly_data, f"{survey_day:02d}/{survey_month:02d}/{survey_year}")

    # Ask the user if they want to run the program again
    while True:
        user_input = input("Do you want to run the program again? (Y/N): ").strip().lower()
        if user_input == "Y":
            main()  # Recursively call the main function to restart the program
            break
        elif user_input == "N":
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            continue

if __name__ == "__main__":
    main()
