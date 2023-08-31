import json
import random
import tkinter as tk
from tkinter import messagebox, Entry


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Learning App")

        self.label = tk.Label(
            root, text="Enter the number of new words to learn:")
        self.label.pack()

        self.entry = Entry(root)
        self.entry.pack()

        self.button = tk.Button(
            root, text="Learn New Words", command=self.learn_new_words)
        self.button.pack()

    def learn_new_words(self):
        num_new_words = self.entry.get()
        try:
            num_new_words = int(num_new_words)
            if num_new_words <= 0:
                messagebox.showerror(
                    "Error", "Number of new words must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        german_words = load_json_file('german_words_json.json')
        learnt_words = load_json_file('learnt_words.json')

        if not german_words:
            messagebox.showinfo("Info", "No input files found.")
            return

        learnt_word_set = set(word_data["german"].lower()
                              for word_data in learnt_words)

        potential_new_words = [
            word_data for word_data in german_words if word_data["german"].lower() not in learnt_word_set]

        if len(potential_new_words) < num_new_words:
            messagebox.showerror(
                "Error", "Not enough unique words available for learning.")
            return

        random.shuffle(potential_new_words)
        new_words = potential_new_words[:num_new_words]

        new_words_json_filename = 'german_words_json.json'
        new_words_txt_filename = 'new_words.txt'

        german_words.extend(new_words)
        save_json_file(new_words_json_filename, german_words)
        save_txt_file(new_words_txt_filename, new_words)

        messagebox.showinfo(
            "Success", f"{num_new_words} new words appended to {new_words_json_filename} and saved to {new_words_txt_filename}.")

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


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
