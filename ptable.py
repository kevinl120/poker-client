import tkinter as tk

class PokerTable:
    def __init__(self, players=None):
        self.players = players
    
    def start(self):
        print("Starting Table")
        self.step = 0
        self.draw()
    
    def draw(self):
        gui = tk.Tk()
        gui.geometry("1002x743")
        gui.title("Poker Table")
        background_image = tk.PhotoImage(file="./resources/table.png")
        background_label = tk.Label(gui, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        gui.mainloop()