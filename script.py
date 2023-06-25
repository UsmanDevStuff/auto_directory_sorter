import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class SorterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Directory Sorter | Muhammad Usman")
        master.geometry("400x150")

        # Create a progress bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=20, padx=20)

        # Create a button to select a directory
        self.select_button = tk.Button(master, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=7)

        # Create a button to sort the directory
        self.sort_button = tk.Button(master, text="Sort Directory", command=self.sort_directory, state="disabled")
        self.sort_button.pack(pady=7)

        # Disable the sort button initially
        self.disable_sort_button()

    def select_directory(self):
        # Open a file dialog to select a directory
        self.directory = filedialog.askdirectory()

        # Enable the sort button if a directory is selected
        if self.directory:
            self.enable_sort_button()
        else:
            self.disable_sort_button()

    def enable_sort_button(self):
        self.sort_button.config(state="normal")

    def disable_sort_button(self):
        self.sort_button.config(state="disabled")

    def sort_directory(self):
        # Disable the select button and enable the progress bar
        self.disable_sort_button()
        self.progress.start(10)

        # Get the list of files in the directory
        files = os.listdir(self.directory)

        # Create a dictionary to store the files in each category
        categories = {
            "Image": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
            "Video": [".mp4", ".avi", ".mov", ".wmv", ".mkv"],
            "Audio": [".mp3", ".wav", ".ogg"],
            "Documents": [".pdf", ".doc", ".docx", ".txt"],
            "Executables": [".exe", ".msi"],
            "Compressed": [".gz", ".zip", ".rar", ".7z"]
        }

        # Loop through each file in the directory
        for file in files:
            # Get the file extension
            extension = os.path.splitext(file)[1]

            # Loop through each category in the dictionary
            for category, extensions in categories.items():
                # If the extension is in the list of extensions for the category, move the file to the category folder
                if extension in extensions:
                    category_folder = os.path.join(self.directory, category)
                    os.makedirs(category_folder, exist_ok=True)
                    old_path = os.path.join(self.directory, file)
                    new_path = os.path.join(category_folder, file)
                    shutil.move(old_path, new_path)
                    break

        # Delete any empty folders
        for root, dirs, files in os.walk(self.directory, topdown=False):
            for name in dirs:
                path = os.path.join(root, name)
                if not os.listdir(path):
                    os.rmdir(path)

        # Enable the select button and stop the progress bar
        self.enable_sort_button()
        self.progress.stop()

        # Show a message box to indicate that the directory has been sorted
        tk.messagebox.showinfo("Success", "The directory has been sorted into individual folders based on category and any empty folders have been deleted.")

root = tk.Tk()
gui = SorterGUI(root)
root.mainloop()