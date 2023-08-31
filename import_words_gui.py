import json
import random
import string
import tkinter as tk
from tkinter import messagebox, Scrollbar, Text, Button


def generate_unique_id():
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(6))
    return unique_id


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Data Entry App")

        self.text_box = Text(root, wrap=tk.WORD, height=10, width=40)
        self.text_box.pack()

        self.scrollbar = Scrollbar(root, command=self.text_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box.config(yscrollcommand=self.scrollbar.set)

        self.process_button = Button(
            root, text="Process Data", command=self.process_data)
        self.process_button.pack()

    def process_data(self):
        # Get the text from the text box
        input_text = self.text_box.get("1.0", "end-1c")
        lines = input_text.strip().split('\n')

        all_word_data = []
        for line in lines:
            data = extract_data(line)
            if data:
                data["unique_id"] = generate_unique_id()
                all_word_data.append(data)

        # Append to JSON file
        append_to_json('german_words_json.json', all_word_data)

        # Append to TXT file
        save_txt_file('german_words_txt.txt', all_word_data)

        messagebox.showinfo("Success", "Word data appended to files.")

        # Automatically exit the program after the message box is closed
        self.root.destroy()


def extract_data(line):
    parts = line.strip().split(' ')
    if len(parts) >= 2:
        gender = parts[0] if parts[0] in ['der', 'die', 'das'] else None
        word_with_parentheses = parts[1] if gender else parts[0]
        
        # Remove content within parentheses
        german_word = word_with_parentheses.split('(')[0].strip()

        english_translation = ''
        if '(' in line:
            translation_start = line.find('(') + 1
            translation_end = line.find(')', translation_start)
            english_translation = line[translation_start:translation_end].strip()

        return {"gender": gender, "german": german_word, "english": english_translation}


def append_to_json(filename, data):
    existing_data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        pass

    existing_data.extend(data)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


def save_txt_file(filename, words_list):
    with open(filename, 'a', encoding='utf-8') as file:
        for word_data in words_list:
            gender = word_data["gender"]
            german_word = word_data["german"]
            english_translation = word_data["english"]

            line = ""
            if gender:
                line += f"{gender} "
            line += f"{german_word} ({english_translation})" if english_translation else german_word

            file.write(line + '\n')


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
