import tkinter as tk
from tkinter import filedialog


def get_file_paths():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Prompt for the input file
    input_file_path = filedialog.askopenfilename(
        title="Select input CSV file",
        filetypes=[("CSV files", "*.csv")])

    # Prompt for the output file
    output_file_path = filedialog.asksaveasfilename(
        title="Select output CSV file",
        filetypes=[("CSV files", "*.csv")],
        defaultextension=".csv")

    return input_file_path, output_file_path