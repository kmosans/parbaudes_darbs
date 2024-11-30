import tkinter as tk
from tkinter import messagebox
import random

# Pieejamie vārdi spēlei
WORDS = ["python", "tkinter", "programming", "developer", "hangman", "interface", "widget", "function"]

class WordGuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Word Game")

        # Spēles mainīgie
        self.secret_word = random.choice(WORDS)
        self.guessed_word = ["_"] * len(self.secret_word)
        self.remaining_attempts = 6
        self.used_letters = set()

        # GUI veidošana
        self.create_widgets()

    def create_widgets(self):
        # Galvenais virsraksts
        tk.Label(self.root, text="Guess the Word!", font=("Arial", 20)).pack(pady=10)

        # Rāda uzminētos burtus
        self.word_label = tk.Label(self.root, text=" ".join(self.guessed_word), font=("Arial", 18))
        self.word_label.pack(pady=10)

        # Ievades lauks burtam
        tk.Label(self.root, text="Enter a letter:").pack()
        self.letter_entry = tk.Entry(self.root, font=("Arial", 14), width=5)
        self.letter_entry.pack()

        # Poga burtu pārbaudei
        self.check_button = tk.Button(self.root, text="Check", font=("Arial", 14), command=self.check_letter)
        self.check_button.pack(pady=10)

        # Rāda atlikušo mēģinājumu skaitu
        self.attempts_label = tk.Label(self.root, text=f"Remaining attempts: {self.remaining_attempts}", font=("Arial", 14))
        self.attempts_label.pack(pady=10)

        # Rāda izmantotos burtus
        self.used_letters_label = tk.Label(self.root, text="Used letters: ", font=("Arial", 12))
        self.used_letters_label.pack()

    def check_letter(self):
        # Iegūst ievadīto burtu
        letter = self.letter_entry.get().lower()
        self.letter_entry.delete(0, tk.END)  # Notīra ievades lauku

        # Validācija
        if not letter.isalpha() or len(letter) != 1:
            messagebox.showerror("Error", "Please enter a single letter!")
            return
        if letter in self.used_letters:
            messagebox.showerror("Error", "You already used this letter!")
            return

        # Pievieno burtu izmantotajiem burtiem
        self.used_letters.add(letter)
        self.used_letters_label.config(text=f"Used letters: {', '.join(self.used_letters)}")

        # Pārbauda, vai burts ir vārdā
        if letter in self.secret_word:
            for i, char in enumerate(self.secret_word):
                if char == letter:
                    self.guessed_word[i] = letter
            self.word_label.config(text=" ".join(self.guessed_word))

            # Uzvaras pārbaude
            if "_" not in self.guessed_word:
                messagebox.showinfo("Congratulations!", f"You guessed the word: {self.secret_word}")
                self.reset_game()
        else:
            self.remaining_attempts -= 1
            self.attempts_label.config(text=f"Remaining attempts: {self.remaining_attempts}")

            # Zaudējuma pārbaude
            if self.remaining_attempts == 0:
                messagebox.showinfo("Game Over", f"You lost! The word was: {self.secret_word}")
                self.reset_game()

    def reset_game(self):
        # Atiestata spēli
        self.secret_word = random.choice(WORDS)
        self.guessed_word = ["_"] * len(self.secret_word)
        self.remaining_attempts = 6
        self.used_letters = set()

        # Atjauno GUI
        self.word_label.config(text=" ".join(self.guessed_word))
        self.attempts_label.config(text=f"Remaining attempts: {self.remaining_attempts}")
        self.used_letters_label.config(text="Used letters: ")

# Palaid spēli
if __name__ == "__main__":
    root = tk.Tk()
    game = WordGuessGame(root)
    root.mainloop()
