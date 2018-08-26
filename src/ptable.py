from random import randint
import tkinter as tk
import treys


class PokerTable:

    evaluator = treys.Evaluator()

    def __init__(self, sb, bb):
        self.players = [None, None, None, None, None, None]
        self.active_players = 0
        self.button_pos = None
        self.current_turn = None

        self.deck = treys.Deck()
        self.board = None

        self.sb = sb
        self.bb = bb
        self.pot = 0
        self.side_pots = {}
    

    def __repr__(self):
        return "PokerTable({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(self.players, self.active_players, self.button_pos, self.current_turn, self.deck.cards, self.board, self.sb, self.bb, self.pot, self.side_pots)
    

    def start(self):
        """Start a new table"""
        print("Starting Table")

        if self.active_players < 2:
            print("Cannot start with less than two players")
            return

        # Assign button to a random player
        rand_pos = randint(0, len(self.players)-1)
        while self.players[rand_pos] is None:
            rand_pos = randint(0, len(self.players)-1)
        self.button_pos = rand_pos

        self.deal()
    

    def deal(self):
        """Start a new hand"""
        self.deck.shuffle()
        for player in self.players:
            if not player is None:
                player.hole_cards = self.deck.draw(2)
        
        # Set blinds and start betting round
        sb_pos = self.next_active_pos(self.button_pos)
        bb_pos = self.next_active_pos(sb_pos)
        self.add_player_bet(sb_pos, self.sb)
        self.add_player_bet(bb_pos, self.bb)
        self.current_turn = self.next_active_pos(bb_pos)


    def add_player_bet(self, player_pos, bet):
        """Make player in player_pos bet with size bet"""
        self.players[player_pos].current_bet = bet
        self.pot += bet

    def is_full(self):
        return self.active_players >= len(self.players)
    

    def add_player(self, new_player):
        """Places the new player in a random open position"""
        if not self.is_full():
            rand_pos = randint(0, len(self.players)-1)
            while not self.players[rand_pos] is None:
                rand_pos = randint(0, len(self.players)-1)
            self.players[rand_pos] = new_player
            self.active_players += 1
    

    def redraw(self):
        gui = tk.Tk()
        gui.geometry("1002x743")
        gui.title("Poker Table")
        background_image = tk.PhotoImage(file="./resources/table.png")
        background_label = tk.Label(gui, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        gui.mainloop()
    

    ### HELPERS ########################
    def next_active_pos(self, pos):
        """Returns the table position of the next active player"""
        while self.players[(pos+1) % len(self.players)] is None:
            pos = pos + 1
        return pos + 1


class Player:
    def __init__(self, stack):
        self.stack = stack
        self.hole_cards = None
        self.current_bet = 0
        self.table_pos = None
    

    def __repr__(self):
        # return "Player({})".format(self.stack)
        return "Player({}, {}, {}, {})".format(self.stack, self.hole_cards, self.current_bet, self.table_pos)