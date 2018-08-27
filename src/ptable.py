from random import randint
import tkinter as tk
import treys

# TODO: Make exception for heads up order

class PokerTable:

    evaluator = treys.Evaluator()
    
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = {}

        default_cfg = {}
        default_cfg["sb"] = 0
        default_cfg["bb"] = 0

        default_cfg["players"] = [None, None, None, None, None, None] # required for drawing
        default_cfg["players_at_table"] = 0
        default_cfg["players_in_hand"] = 0
        default_cfg["button_pos"] = None # required for drawing
        default_cfg["current_turn"] = None # required for drawing

        default_cfg["deck"] = treys.Deck()
        default_cfg["board"] = [] # required for drawing

        default_cfg["pot"] = 0 # required for drawing
        default_cfg["side_pots"] = {} # required for drawing

        ### Helpers in a hand
        default_cfg["total_to_call"] = None # Highest bet on a street
        default_cfg["last_raise_size"] = None # Size of last bet/raise
        default_cfg["last_raiser"] = None

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
        if self.cfg["players_at_table"] < 2:
            print("Cannot start with less than two players")
            return

        print("Starting Table")
        # Assign button to a random player
        rand_pos = randint(0, len(self.cfg["players"])-1)
        while self.cfg["players"][rand_pos] is None:
            rand_pos = randint(0, len(self.cfg["players"])-1)
        self.cfg["button_pos"] = rand_pos

        self.deal()
    

    def deal(self):
        """Start a new hand"""
        self.cfg["deck"].shuffle()
        for player in self.cfg["players"]:
            if not player is None:
                player.hole_cards = self.cfg["deck"].draw(2)
                self.cfg["players_in_hand"] += 1
        
        # Set blinds and start betting round
        self.cfg["current_turn"] = self.next_active_player(self.cfg["button_pos"])
        self.cfg["total_to_call"] = 0
        self.add_player_bet(self.cfg["current_turn"], self.cfg["sb"])
        self.cfg["last_raiser"] = self.cfg["current_turn"]
        self.add_player_bet(self.cfg["current_turn"], self.cfg["bb"])
        self.cfg["last_raise_size"] = self.cfg["bb"]

        self.get_player_options()

        # Workaround because bb didn't really raise
        self.cfg["last_raiser"] = self.cfg["current_turn"]
    

    def get_player_options(self):
        """Details current player actions"""
        if self.cfg["current_turn"] == self.cfg["last_raiser"]:
            # Everyone checked/called
            # Set all bets to 0
            for _ in range(self.cfg["players_in_hand"]):
                self.cfg["players"][self.cfg["current_turn"]].current_bet = 0
                self.cfg["current_turn"] = self.next_active_player(self.cfg["current_turn"])
            # Go to next street
            if len(self.cfg["board"]) == 5:
                # TODO: go to showdown
                pass
            elif len(self.cfg["board"]) == 4:
                # Deal river
                self.cfg["board"].append(self.cfg["deck"].draw(1))
            elif len(self.cfg["board"]) == 3:
                # Deal turn
                self.cfg["board"].append(self.cfg["deck"].draw(1))
            elif len(self.cfg["board"]) == 0:
                # Deal flop
                cards = self.cfg["deck"].draw(3)
                self.cfg["board"].append(cards[0])
                self.cfg["board"].append(cards[1])
                self.cfg["board"].append(cards[2])
            self.cfg["last_raise_size"] = self.cfg["bb"]
            self.cfg["total_to_call"] = 0
            self.cfg["current_turn"] = self.next_active_player(self.cfg["button_pos"])
            self.cfg["last_raiser"] = self.cfg["current_turn"]

        if self.cfg["total_to_call"] == self.cfg["players"][self.cfg["current_turn"]].current_bet:
            # Player has option of checking
            self.cfg["players"][self.cfg["current_turn"]].possible_actions = ["fold", "check", [min(self.cfg["last_raise_size"], self.cfg["players"][self.cfg["current_turn"]].stack), self.cfg["players"][self.cfg["current_turn"]].stack]]
            return
        else:
            # Player is facing a raise
            # TODO: if player is facing all in, create side pot
            self.cfg["players"][self.cfg["current_turn"]].possible_actions = ["fold", "call", [min(self.cfg["last_raise_size"]+self.cfg["total_to_call"], self.cfg["players"][self.cfg["current_turn"]].stack), self.cfg["players"][self.cfg["current_turn"]].stack]]
            return


    def player_folds(self, player_pos):
        if player_pos == self.cfg["current_turn"]:
            self.cfg["players"][player_pos].possible_actions = []

            if self.cfg["players_in_hand"] == 2:
                self.player_wins(self.next_active_player(player_pos))
                return
                # TODO:
                # Provide option for folder to show/muck hand
                # Provide option for winner to show/muck hand

            self.cfg["players"][player_pos].hole_cards = None
            self.cfg["players"][player_pos].current_bet = 0
            self.cfg["players_in_hand"] -= 1
            self.cfg["current_turn"] = self.next_active_player(self.cfg["current_turn"])
            self.get_player_options()

            # Pre-flop the player who is "last_raiser" could fold
            # Similar workaround to the one in self.draw()
            if self.cfg["last_raiser"] == player_pos:
                self.cfg["last_raiser"] = self.next_active_player(player_pos)



    def player_checks(self, player_pos):
        if player_pos == self.cfg["current_turn"]:
            self.cfg["players"][player_pos].possible_actions = []
            self.cfg["current_turn"] = self.next_active_player(self.cfg["current_turn"])
            self.get_player_options()


    def player_calls(self, player_pos):
        if player_pos == self.cfg["current_turn"]:
            self.cfg["players"][player_pos].possible_actions = []
            self.add_player_bet(player_pos, self.cfg["total_to_call"]-self.cfg["players"][player_pos].current_bet)


    def add_player_bet(self, player_pos, bet):
        """Make player in player_pos bet with size bet"""
        if player_pos == self.cfg["current_turn"]:
            self.cfg["players"][player_pos].possible_actions = []
            self.cfg["players"][player_pos].current_bet += bet
            if self.cfg["players"][player_pos].current_bet - self.cfg["total_to_call"] > 0:
                # Player raised
                self.cfg["last_raise_size"] = self.cfg["players"][player_pos].current_bet - self.cfg["total_to_call"]
                self.cfg["last_raiser"] = self.cfg["current_turn"]
            self.cfg["total_to_call"] = self.cfg["players"][player_pos].current_bet
            self.cfg["players"][player_pos].stack -= bet
            self.cfg["pot"]+= bet

            self.cfg["current_turn"] = self.next_active_player(self.cfg["current_turn"])
            self.get_player_options()


    def player_wins(self, player_pos):
        for _ in range(self.cfg["players_in_hand"]):
            self.cfg["players"][self.cfg["current_turn"]].current_bet = 0
            self.cfg["current_turn"] = self.next_active_player(self.cfg["current_turn"])
        self.cfg["players_in_hand"] = 0
        self.cfg["players"][player_pos].stack += self.cfg["pot"]
        self.cfg["board"] = []
        self.cfg["pot"] = 0
        self.cfg["side_pots"] = {}
        self.cfg["button_pos"] = self.next_active_player(self.cfg["button_pos"])
        self.deal()


    ### General table functions ### 


    def is_full(self):
        return self.cfg["players_at_table"] >= len(self.cfg["players"])
    

    def add_player(self, new_player):
        """Places the new player in a random open position. Returns the position."""
        if not self.is_full():
            rand_pos = randint(0, len(self.cfg["players"])-1)
            while not self.cfg["players"][rand_pos] is None:
                rand_pos = randint(0, len(self.cfg["players"])-1)
            self.cfg["players"][rand_pos] = new_player
            self.cfg["players_at_table"] += 1
            return rand_pos
    

    def remove_player(self, player_num):
        """Removes the player in the given position"""
        self.cfg["players"][player_num] = None
        self.cfg["players_at_table"] -= 1
        # TODO: check if hand is over
        # TODO: check if player was currently playing in hand


    ### HELPERS ########################

    def next_player(self, pos):
        """Returns the table position of the next player at table"""
        pos = (pos + 1) % len(self.cfg["players"])
        while self.cfg["players"][pos] is None:
            pos = (pos + 1) % len(self.cfg["players"])
        return pos


    def next_active_player(self, pos):
        """Returns the table position of the next player with a hand at table"""
        pos = (pos + 1) % len(self.cfg["players"])
        while self.cfg["players"][pos] is None or self.cfg["players"][pos].hole_cards is None:
            pos = (pos + 1) % len(self.cfg["players"])
        return pos
    

    def last_active_player(self, pos):
        pos = (pos - 1) % len(self.cfg["players"])
        while self.cfg["players"][pos] is None or self.cfg["players"][pos].hole_cards is None:
            pos = (pos - 1) % len(self.cfg["players"])
        return pos


class Player:
    def __init__(self, stack, hole_cards=None, current_bet=0, possible_actions=None):
        self.stack = stack
        self.hole_cards = hole_cards
        self.current_bet = current_bet
        # possible_actions: list of 2 or 3 elements.
        # [muck/fold, show/check/call, [min_bet, max_bet]]
        if possible_actions is None:
            self.possible_actions = []
        else:
            self.possible_actions = possible_actions
    

    def __repr__(self):
        # return "Player({})".format(self.stack)
        return "Player({}, {}, {}, {})".format(self.stack, self.hole_cards, self.current_bet, self.possible_actions)