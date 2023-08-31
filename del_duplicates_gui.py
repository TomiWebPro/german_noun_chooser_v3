import string
import random
import json
import tkinter as tk
from tkinter import messagebox


class UniqueWordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unique Word Generator App")

        self.button = tk.Button(
            root, text="Generate Unique Words", command=self.generate_unique_words)
        self.button.pack()

    def generate_unique_words(self):
        german_words = load_json_file('german_words_json.json')

        for word_data in german_words:
            word_data["unique_id"] = generate_unique_id()

        unique_words = set()  # Set to store unique German words
        unique_word_data = []

        for word_data in german_words:
            german_word = word_data["german"]
            if german_word not in unique_words:
                unique_words.add(german_word)
                unique_word_data.append(word_data)

        num_duplicates_found = len(german_words) - len(unique_word_data)
        num_unique_words = len(unique_word_data)

        save_json_file('german_words_json.json', unique_word_data)
        save_txt_file('german_words_txt.txt', unique_word_data)

        result_message = f"{num_duplicates_found} duplicates found and removed.\n{num_unique_words} unique words are left.\nAll duplicates removed and saved."
        messagebox.showinfo("Results", result_message)

        # Automatically exit the program after the message box is closed
        self.root.destroy()


def load_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []


def save_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_txt_file(filename, words_list):
    with open(filename, 'w', encoding='utf-8') as file:
        for word_data in words_list:
            gender = word_data["gender"]
            german_word = word_data["german"]
            english_translation = word_data["english"]

            line = ""
            if gender:
                line += f"{gender} "
            line += german_word

            if english_translation:
                line += f" ({english_translation})"

            file.write(line + '\n')


def generate_unique_id():
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(6))
    return unique_id


if __name__ == "__main__":
    root = tk.Tk()
    app = UniqueWordGeneratorApp(root)
    root.mainloop()
