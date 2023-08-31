import tkinter as tk
from tkinter import filedialog
import subprocess  # Import for running external script


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary App")

        button_width = 20  # Width of the buttons

        # Create buttons
        self.view_button = tk.Button(
            root, text="View Learned Words", command=self.view_words, width=button_width)
        self.view_learning_button = tk.Button(
            root, text="View Learning Words", command=self.view_learning_words, width=button_width)
        self.learn_more_button = tk.Button(
            root, text="Learn More Words", command=self.add_new_words, width=button_width)
        self.update_button = tk.Button(
            root, text="Update Memorized", command=self.update_memorized, width=button_width)
        self.import_button = tk.Button(
            root, text="Import Words", command=self.import_words, width=button_width)
        self.remove_duplicate_button = tk.Button(
            root, text="Remove Duplicate Words", command=self.remove_duplicates, width=button_width)
        self.search_button = tk.Button(
            root, text="Search Manual Words", command=self.search_words, width=button_width)

        # Layout buttons
        self.view_button.pack()
        self.view_learning_button.pack()
        self.learn_more_button.pack()
        self.update_button.pack()
        self.import_button.pack()
        self.remove_duplicate_button.pack()
        self.search_button.pack()

    def view_words(self):
        subprocess.run(["python", "view_learned_words_gui.py"])

    def view_learning_words(self):
        subprocess.run(["python", "view_learning_words_gui.py"])

    def add_new_words(self):
        subprocess.run(["python", "get_new_words_gui.py"])

    def update_memorized(self):
        subprocess.run(["python", "update_the memorized_gui.py"])

    def import_words(self):
        subprocess.run(["python", "import_words_gui.py"])

    def remove_duplicates(self):
        subprocess.run(["python", "del_duplicates_gui.py"])

    def search_words(self):
        # Run external script
        subprocess.run(["python", "seartch_manual_words_gui.py"])


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
