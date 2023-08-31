import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # Import for pop-up message box


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary App")

    def run(self):
        if self.display_learned_words():
            self.root.mainloop()

    def display_learned_words(self):
        try:
            with open('new_words.txt', 'r', encoding='utf-8') as file:
                words = file.read()

                # Create a non-user-changable textbox
                self.textbox = tk.Text(self.root, state=tk.DISABLED)
                self.textbox.pack()
                self.textbox.config(state=tk.NORMAL)
                self.textbox.insert(tk.END, words)
                self.textbox.config(state=tk.DISABLED)

                # Count and display the number of words learned
                word_count = len([line.strip()
                                 for line in words.split('\n') if line.strip()])
                self.word_count_label = tk.Label(
                    self.root, text=f"You are learning {word_count} words.")
                self.word_count_label.pack()
                return True
        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found", "The 'new_words.txt' file was not found.")
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    app.run()
