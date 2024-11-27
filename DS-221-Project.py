# Importing the essential libraries / modules

import numpy as np  # Used to perform numerical operations on the data
import pandas as pd  # Used to open CSV files and perform the operation (such as editing the data)


def openFile():
    option = bool(
        input(
            "Do you want to enter marks into an existing Excel file, or create a new file for another section?(0/1): "
        )
    )

    if option == 0:
        try:
            filePath = input("Enter the path of your file: ")
            df = pd.read_csv(filePath)
            return df

        except FileNotFoundError:
            print("File Not Found")
    elif option == 1:
        csv_File = input("Enter the name of your file: ")
        # df.csv_File()
    else:
        print("Invalid Option")


def Authenticate(name, password):
    username, Password = "admin", "ABC"
    if username == name and Password == password:
        return True
    else:
        return False


def Interface():
    name = input("Enter your name: ")
    password = input("Enter the password: ")
    if Authenticate(name, password):
        print("\nLogin Sucessful")

    else:
        print("Login Failed")


Interface()
