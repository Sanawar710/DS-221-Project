import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Global DataFrame to hold student data
df = pd.DataFrame()


# Authentication function
def authenticate(name, password):
    username, Password = "admin", "ABC"
    return name == username and password == Password


# Login function
def login():
    name = username_entry.get()
    password = password_entry.get()

    if authenticate(name, password):
        messagebox.showinfo("Login Successful", "Welcome to the Grading System!")
        login_frame.pack_forget()  # Hide login frame
        main_menu_frame.pack()  # Show main menu frame
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


# Open/Create file function
def open_file(option):
    global df

    if option == "open":
        file_path = filedialog.askopenfilename(
            title="Open CSV File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
        )
        try:
            df = pd.read_csv(file_path)
            messagebox.showinfo("File Loaded", "File loaded successfully!")
            file_frame.pack_forget()
            grading_frame.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
    elif option == "create":
        file_name = file_name_entry.get()
        columns = columns_entry.get().split(",")
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_name + ".csv", index=False)
        messagebox.showinfo("File Created", f"New file '{file_name}.csv' created!")
        file_frame.pack_forget()
        grading_frame.pack(fill="both", expand=True)


# Add student grades
def add_student():
    global df
    if df.empty:
        messagebox.showerror(
            "Error", "No dataset found. Please create or load a dataset."
        )
        return
    try:
        name = name_entry.get()
        marks = float(marks_entry.get())
        new_row = {"Name": name, "Marks": marks}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        messagebox.showinfo("Success", "Student details added successfully!")
        name_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid marks. Please enter a numeric value.")


# Apply absolute grading
def absolute_grading():
    global df
    if df.empty:
        messagebox.showerror(
            "Error", "The dataset is empty. Please load or create a dataset first."
        )
        return
    try:
        df["Grade"] = pd.cut(
            df["Marks"],
            bins=[0, 50, 60, 70, 80, 100],
            labels=["F", "D", "C", "B", "A"],
            right=False,
        )
        messagebox.showinfo("Grading Successful", "Absolute grading applied!")
    except KeyError:
        messagebox.showerror("Error", "Marks column not found in the dataset.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Apply relative grading
def relative_grading():
    global df
    if df.empty:
        messagebox.showerror(
            "Error", "The dataset is empty. Please load or create a dataset first."
        )
        return
    try:
        mean = df["Marks"].mean()
        std_dev = df["Marks"].std()

        def calculate_grade(marks):
            z_score = (marks - mean) / std_dev
            if z_score >= 1:
                return "A"
            elif 0.5 <= z_score < 1:
                return "B"
            elif -0.5 <= z_score < 0.5:
                return "C"
            elif -1 <= z_score < -0.5:
                return "D"
            else:
                return "F"

        df["Grade"] = df["Marks"].apply(calculate_grade)
        messagebox.showinfo("Grading Successful", "Relative grading applied!")
    except KeyError:
        messagebox.showerror("Error", "Marks column not found in the dataset.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Save grades to file
def save_grades():
    global df
    if df.empty:
        messagebox.showerror(
            "Error", "The dataset is empty. Please load or create a dataset first."
        )
        return
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
    )
    try:
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"Data saved to '{save_path}' successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")


# # Function to display histogram
def plot_histogram():
    global df
    if df.empty:
        messagebox.showerror(
            "Error", "The dataset is empty. Please load or create a dataset first."
        )
        return
    try:
        plt.hist(df["Marks"], bins=10, edgecolor="black")
        plt.title("Marks Distribution")
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.show()
    except KeyError:
        messagebox.showerror("Error", "Marks column not found in the dataset.")


# Function to display normal distribution curve
def plot_normal_curve():
    global df
    if df.empty:
        messagebox.showerror(
            "Error", "The dataset is empty. Please load or create a dataset first."
        )
        return
    try:
        mean = df["Marks"].mean()
        std_dev = df["Marks"].std()
        xmin, xmax = df["Marks"].min(), df["Marks"].max()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mean, std_dev)
        plt.plot(x, p, "k", linewidth=2)
        plt.title("Normal Distribution Curve for Marks")
        plt.xlabel("Marks")
        plt.ylabel("Probability Density")
        plt.show()
    except KeyError:
        messagebox.showerror("Error", "Marks column not found in the dataset.")


# GUI Setup
root = tk.Tk()
root.title("Grading System")
root.geometry("400x400")

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack()

tk.Label(login_frame, text="Username:").pack(pady=5)
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password:").pack(pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=5)

tk.Button(login_frame, text="Login", command=login).pack(pady=20)

main_menu_frame = tk.Frame(root)  # Main Menu Frame

tk.Label(main_menu_frame, text="Main Menu", font=("Helvetica", 16)).pack(pady=20)
tk.Button(
    main_menu_frame,
    text="Open Existing File",
    command=lambda: open_file("open"),
).pack(pady=10)
tk.Button(
    main_menu_frame,
    text="Create New File",
    command=lambda: open_file("create"),
).pack(pady=10)
tk.Button(main_menu_frame, text="Exit", command=root.quit).pack(pady=10)

file_frame = tk.Frame(root)  # File Handling Frame

tk.Label(file_frame, text="File Options", font=("Helvetica", 16)).pack(pady=20)

tk.Label(file_frame, text="Create New File:").pack(pady=10)
file_name_entry = tk.Entry(file_frame)
file_name_entry.pack(pady=5)

tk.Label(file_frame, text="Enter Columns (comma-separated):").pack(pady=10)
columns_entry = tk.Entry(file_frame)
columns_entry.pack(pady=5)

# Grading Frame
grading_frame = tk.Frame(root)

tk.Label(grading_frame, text="Enter Student Details", font=("Helvetica", 16)).pack(
    pady=20
)
tk.Label(grading_frame, text="Name:").pack(pady=5)
name_entry = tk.Entry(grading_frame)
name_entry.pack(pady=5)

tk.Label(grading_frame, text="Marks:").pack(pady=5)
marks_entry = tk.Entry(grading_frame)
marks_entry.pack(pady=5)

tk.Button(grading_frame, text="Add Student", command=add_student).pack(pady=10)
tk.Button(grading_frame, text="Apply Absolute Grading", command=absolute_grading).pack(
    pady=10
)
tk.Button(grading_frame, text="Apply Relative Grading", command=relative_grading).pack(
    pady=10
)
tk.Button(grading_frame, text="Save Grades", command=save_grades).pack(pady=10)

graph_frame = tk.Frame(root)  # Graphing Frame (For Viewing Graphs)

tk.Label(graph_frame, text="Graphs", font=("Helvetica", 16)).pack(pady=20)
tk.Button(graph_frame, text="Show Histogram", command=plot_histogram).pack(pady=10)
tk.Button(
    graph_frame, text="Show Normal Distribution Curve", command=plot_normal_curve
).pack(pady=10)

# Start the GUI
root.mainloop()
