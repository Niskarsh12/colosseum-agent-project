import tkinter as tk
import random
from tkinter import messagebox

class SolanaCatcherGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Colosseum: Solana Block Catcher")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, bg="#121212", height=500, width=400)
        self.canvas.pack()

        self.score = 0
        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 12))
        
        self.basket = self.canvas.create_rectangle(175, 450, 225, 470, fill="#9945FF") # Solana Purple
        self.blocks = []
        
        self.root.bind("<Left>", lambda e: self.move_basket(-20))
        self.root.bind("<Right>", lambda e: self.move_basket(20))
        
        self.spawn_block()
        self.update_game()

    def move_basket(self, dx):
        coords = self.canvas.coords(self.basket)
        if coords[0] + dx >= 0 and coords[2] + dx <= 400:
            self.canvas.move(self.basket, dx, 0)

    def spawn_block(self):
        x = random.randint(20, 380)
        block = self.canvas.create_oval(x, 0, x+20, 20, fill="#14F195") # Solana Green
        self.blocks.append(block)
        self.root.after(1500, self.spawn_block)

    def update_game(self):
        for block in self.blocks[:]:
            self.canvas.move(block, 0, 5)
            bc = self.canvas.coords(block)
            bk = self.canvas.coords(self.basket)

            # Collision detection
            if bc[3] >= bk[1] and bk[0] <= bc[0] <= bk[2]:
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                self.canvas.delete(block)
                self.blocks.remove(block)
            elif bc[3] > 500:
                self.canvas.delete(block)
                self.blocks.remove(block)

        self.root.after(30, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = SolanaCatcherGame(root)
    root.mainloop()