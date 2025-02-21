import tkinter as tk
import random

# List of Thai consonants with their Romanized names
thai_consonants = [
    ("ก", "Gor Gai"),  # ก - Chicken
    ("ข", "Khor Khai"), # ข - Egg
    ("ฃ", "Khor Khuat"), # ฃ - Bottle
    ("ค", "Khor Khwai"), # ค - Buffalo
    ("ฅ", "Khor Khon"),  # ฅ - Person
    ("\u0e06", "Khor Rakhang"),  # ฆ - Bell
    ("\u0e07", "Ngor Ngu"),  # ง - Snake
    ("\u0e08", "Jor Jan"),  # จ - Plate
    ("\u0e0a", "Chor Chang"),  # ช - Elephant
    ("\u0e0b", "Sor So"),  # ซ - Chain
]

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thai Consonant Flashcards")
        
        self.current_card = None
        
        self.label = tk.Label(root, text="Click 'Next' to begin", font=("Arial", 50))
        self.label.pack(pady=50)
        
        self.flip_button = tk.Button(root, text="Flip", command=self.flip_card, font=("Arial", 20))
        self.flip_button.pack()
        
        self.next_button = tk.Button(root, text="Next", command=self.next_card, font=("Arial", 20))
        self.next_button.pack(pady=20)
        
        self.next_card()
    
    def next_card(self):
        self.current_card = random.choice(thai_consonants)
        self.label.config(text=self.current_card[0], font=("Arial", 100))
        
    def flip_card(self):
        if self.current_card:
            self.label.config(text=self.current_card[1], font=("Arial", 40))

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()