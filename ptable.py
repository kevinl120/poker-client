from tkinter import *

class PokerTable:
    def __init__(self, players):
        self.players = players
    
    def start(self):
        print("Starting Table")
        self.step = 0
        self.draw()
    
    def draw(self):
        gui = Tk()
        gui.title("Poker Table")
        gui.mainloop()