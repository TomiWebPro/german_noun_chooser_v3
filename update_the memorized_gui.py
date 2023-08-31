import json
import tkinter as tk
from tkinter import messagebox

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learnt Word Updater")

        self.label = tk.Label(root, text="Have you memorized the words in new_words.txt?")
        self.label.pack()

        self.yes_button = tk.Button(root, text="Yes", command=self.mark_as_learned)
        self.yes_button.pack()

        self.no_button = tk.Button(root, text="No", command=self.no_action)
        self.no_button.pack()

    def mark_as_learned(self):
        learnt_words = load_json_file('learned_words.json')
        new_words_filename = 'new_words.txt'
        
        new_learned_words = mark_words_as_learned(learnt_words, new_words_filename)
        
        if new_learned_words:
            messagebox.showinfo("Success", "Words marked as learned and saved.")
        else:
            messagebox.showinfo("Info", "No new words to mark as learned.")
        
        # Clear contents of new_words.json and new_words.txt
        clear_file_contents('new_words.json')
        clear_file_contents('new_words.txt')
        
        # Automatically exit the program
        self.root.destroy()

    def no_action(self):
        messagebox.showinfo("Info", "No action taken.")
        # Automatically exit the program
        self.root.destroy()

def load_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def mark_words_as_learned(learnt_words, new_words_filename):
    new_learned_words = []
    try:
        with open(new_words_filename, 'r', encoding='utf-8') as file:
            new_words_lines = file.readlines()

        for line in new_words_lines:
            parts = line.strip().split(' ')
            if parts:
                german_word = parts[0].strip('()')
                if any(german_word == w["german"].lower() for w in learnt_words):
                    continue

                new_learned_words.append({"gender": parts[0] if parts[0] in ['der', 'die', 'das'] else None,
                                          "german": parts[1] if parts[0] in ['der', 'die', 'das'] else parts[0],
                                          "english": ' '.join(parts[2:]).strip('()') if '(' in line else parts[-1]})

        if new_learned_words:
            learnt_words.extend(new_learned_words)
            save_json_file('learned_words.json', learnt_words)
            save_txt_file('learned_words.txt', new_learned_words)

            with open('learned_words.txt', 'a', encoding='utf-8') as file:
                file.write('\n')

    except FileNotFoundError:
        pass  # File not found, no action needed

    return new_learned_words

def save_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def save_txt_file(filename, words_list):
    with open(filename, 'a', encoding='utf-8') as file:
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

def clear_file_contents(filename):
    with open(filename, 'w', encoding='utf-8') as file:
        pass  # Creates an empty file

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
