import logging
import argparse
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


if __name__ == "__main__":
    input_path, output_path = get_file_paths()
    if not input_path or not output_path:
        print("Operation cancelled by the user.")
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        RealEstateDataFetcher.generate_grantor_grantee_csv(input_file_path=input_path, output_file_path=output_path)