import tkinter as tk
from tkinter import Listbox, Scrollbar, messagebox
import json

class WordSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search and Add")

        self.search_label = tk.Label(root, text="Search Word (German/English):")
        self.search_label.pack()

        self.search_entry = tk.Entry(root)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search_word)
        self.search_button.pack()

        self.results_listbox = Listbox(root, width=50)
        self.results_listbox.pack()

        self.scrollbar = Scrollbar(root, orient="vertical")
        self.scrollbar.config(command=self.results_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.results_listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = tk.Button(root, text="Add to Learned Words", command=self.add_word)
        self.add_button.pack()

        self.update_button = tk.Button(root, text="Update Files", command=self.update_files)
        self.update_button.pack()

        self.load_data()
        self.files_updated = False

    def load_data(self):
        try:
            with open("german_words_json.json", "r", encoding="utf-8") as file:
                self.german_words = json.load(file)
        except FileNotFoundError:
            self.german_words = []

        try:
            with open("learned_words.json", "r", encoding="utf-8") as file:
                self.learned_words = json.load(file)
        except FileNotFoundError:
            self.learned_words = []

    def search_word(self):
        self.results_listbox.delete(0, "end")  # Clear previous results
        search_query = self.search_entry.get().lower()

        for word in self.german_words:
            if (search_query in word["german"].lower()) or (search_query in word["english"].lower()):
                self.results_listbox.insert("end", f"{word['german']} ({word['english']})")

    def add_word(self):
        selected_indices = self.results_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_word = self.results_listbox.get(selected_index)

            # Parse the selected word and extract the German word and English translation
            german_word, english_translation = selected_word.split(" (")
            english_translation = english_translation.rstrip(")")
            
            # Check if the word is already learned
            if any(german_word == w["german"] for w in self.learned_words):
                print(f"{german_word} is already learned.")
            else:
                # Search for the selected word in german_words
                selected_german_word = german_word
                word_to_add = next((word for word in self.german_words if word["german"] == selected_german_word), None)

                if word_to_add:
                    # Append the word to learned_words and update the JSON file
                    self.learned_words.append(word_to_add)
                    with open("learned_words.json", "w", encoding="utf-8") as file:
                        json.dump(self.learned_words, file, ensure_ascii=False, indent=4)
                    print(f"{selected_german_word} added to learned_words")

    def update_files(self):
        if not self.files_updated:
            with open("learned_words.txt", "a", encoding="utf-8") as file:
                if self.learned_words:
                    file.write("\n")  # Add an empty line before updating
                    for word_data in self.learned_words:
                        gender = word_data.get("gender")
                        german_word = word_data["german"]
                        english_translation = word_data["english"]
                        if gender:
                            line = f"{gender} {german_word} ({english_translation})\n"
                        else:
                            line = f"{german_word} ({english_translation})\n"
                        file.write(line)

                self.files_updated = True
                messagebox.showinfo("Files Updated", "Learned words files have been updated.")
        else:
            messagebox.showinfo("Files Already Updated", "Files have already been updated.")


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordSearchApp(root)
    app.run()
