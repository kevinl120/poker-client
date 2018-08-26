from random import randint
import tkinter as tk
from treys import Deck

class PokerTable:
    def __init__(self):
        self.players = [None, None, None, None, None, None]
        self.button_pos = None
        self.current_turn = None

        self.deck = Deck()
        self.board = None

        self.pot = 0
        self.side_pots = []
    
    def __repr__(self):
        return "PokerTable({})".format(self.players)
    
    def start(self):
        print("Starting Table")

    def is_full(self):
        for player in self.players:
            if player is None:
                return False
        return True
    
    def add_player(self, new_player):
        """Places the new player in a random open position"""
        if not self.is_full():
            rand_pos = randint(0, 5)
            while not self.players[rand_pos] is None:
                rand_pos = randint(0, 5)
            self.players[rand_pos] = new_player
    
    def redraw(self):
        gui = tk.Tk()
        gui.geometry("1002x743")
        gui.title("Poker Table")
        background_image = tk.PhotoImage(file="./resources/table.png")
        background_label = tk.Label(gui, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        gui.mainloop()

class Player:
    def __init__(self, stack):
        self.stack = stack
        self.hole_cards = None
        self.current_bet = 0
        self.table_pos = None
    
    def __repr__(self):
        return "Player({})".format(self.stack)