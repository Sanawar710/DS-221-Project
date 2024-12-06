import numpy as np  # Used to perform numerical operations on the data
import pandas as pd  # Used to open CSV files and perform the operation (such as editing the data)
import time as tm  # Imported for using sleep function


def authenticate(name, password):
    username, Password = "admin", "ABC"
    return name == username and password == Password


def Interface():
    # User interface for login
    name = input("Enter your username: ")
    password = input("Enter your password: ")

    if authenticate(name, password):
        tm.sleep(1)
        print("\nLogin Successful")
        choice = input("Do you want to enter grades of students (y/n): ").lower()
        if choice == "y":
            Grading()  # Call the grading function
        else:
            print("Exiting...")
    else:
        tm.sleep(1)
        print("Login Failed")


def open_file():
    # Allow user to open an existing file or create a new one
    while True:
        try:
            option = int(
                input(
                    "Do you want to (0) open an existing file, or (1) create a new file? Enter 0 or 1: "
                )
            )

            if option == 0:
                file_path = input("Enter the path of your file (CSV): ")
                df = pd.read_csv(file_path)  # Load the file into a DataFrame
                print("File loaded successfully!")
                print(df)
                return df

            elif option == 1:
                file_name = input(
                    "Enter the name for the new file (without extension): "
                )
                columns = input(
                    "Enter the column names separated by commas (e.g., Name, Marks): "
                ).split(",")
                df = pd.DataFrame(columns=columns)
                df.to_csv(file_name + ".csv", index=False)
                print(f"New file '{file_name}.csv' created successfully!")
                return df

            else:
                print("Invalid input. Please enter 0 or 1.")
        except ValueError:
            print("Invalid input. Please enter a number (0 or 1).")
        except FileNotFoundError:
            print("File not found. Please check the path and try again.")


def Grading():
    # Function to handle grading logic
    df = open_file()
    if df is not None:
        while True:
            try:
                print("\nEnter student details:")
                name = input("Name: ")
                marks = float(input("Marks: "))
                new_row = {"Name": name, "Marks": marks}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                print("Student details added successfully!")

                more = input("Do you want to add another student? (y/n): ").lower()
                if more != "y":
                    save_path = input(
                        "Enter the file name to save (e.g., grades.csv): "
                    )
                    df.to_csv(save_path, index=False)
                    print(f"Data saved to '{save_path}' successfully!")
                    break
            except ValueError:
                print("Invalid marks. Please enter a numeric value.")

 
Interface()