from random import randint
import tkinter as tk
import treys

class PokerTable:

    evaluator = treys.Evaluator()
    
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = {}

        default_cfg = {}
        default_cfg["sb"] = 0
        default_cfg["bb"] = 0

        default_cfg["players"] = [None, None, None, None, None, None] # required for drawing
        default_cfg["active_players"] = 0
        default_cfg["button_pos"] = None # required for drawing
        default_cfg["current_turn"] = None # required for drawing

        default_cfg["deck"] = treys.Deck()
        default_cfg["board"] = None # required for drawing

        default_cfg["pot"] = 0 # required for drawing
        default_cfg["side_pots"] = {} # required for drawing

        # overwrite default cfg with new cfg
        self.cfg = dict(default_cfg, **cfg)


    def __repr__(self):
        # WARNING: treys.Deck() has no __repr__, prints out location in memory
        # Returns PokerTable with cfg minus "deck" key
        temp_cfg = dict(self.cfg)
        temp_cfg.pop("deck")
        return "PokerTable({})".format(temp_cfg)
    

    def start(self):
        """Start a new table"""
        print("Starting Table")
        if self.cfg["active_players"] < 2:
            print("Cannot start with less than two players")
            return

        # Assign button to a random player
        rand_pos = randint(0, len(self.cfg["players"])-1)
        while self.cfg["players"][rand_pos] is None:
            rand_pos = randint(0, len(self.cfg["players"])-1)
        self.button_pos = rand_pos

        self.deal()
    

    def deal(self):
        """Start a new hand"""
        self.cfg["deck"].shuffle()
        for player in self.cfg["players"]:
            if not player is None:
                player.hole_cards = self.cfg["deck"].draw(2)
        
        # Set blinds and start betting round
        sb_pos = self.next_active_pos(self.button_pos)
        bb_pos = self.next_active_pos(sb_pos)
        self.add_player_bet(sb_pos, self.cfg["sb"])
        self.add_player_bet(bb_pos, self.cfg["bb"])
        self.current_turn = self.next_active_pos(bb_pos)


    def add_player_bet(self, player_pos, bet):
        """Make player in player_pos bet with size bet"""
        self.cfg["players"][player_pos].current_bet = bet
        self.cfg["pot"]+= bet

    def is_full(self):
        return self.cfg["active_players"] >= len(self.cfg["players"])
    

    def add_player(self, new_player):
        """Places the new player in a random open position. Returns the position."""
        if not self.is_full():
            rand_pos = randint(0, len(self.cfg["players"])-1)
            while not self.cfg["players"][rand_pos] is None:
                rand_pos = randint(0, len(self.cfg["players"])-1)
            self.cfg["players"][rand_pos] = new_player
            self.cfg["active_players"] += 1
            return rand_pos
    

    def redraw(self):
        gui = tk.Tk()
        gui.geometry("1002x743")
        gui.title("Poker Table")
        background_image = tk.PhotoImage(file="./resources/table.png")
        background_label = tk.Label(gui, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        gui.update()
    

    ### HELPERS ########################

    def next_active_pos(self, pos):
        """Returns the table position of the next active player"""
        pos = (pos + 1) % len(self.cfg["players"])
        while self.cfg["players"][pos] is None:
            pos = (pos + 1) % len(self.cfg["players"])
        return pos


class Player:
    def __init__(self, stack, hole_cards=None, current_bet=0):
        self.stack = stack
        self.hole_cards = hole_cards
        self.current_bet = current_bet
    

    def __repr__(self):
        # return "Player({})".format(self.stack)
        return "Player({}, {}, {})".format(self.stack, self.hole_cards, self.current_bet)