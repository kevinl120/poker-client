from ptable import PokerTable, Player
from table_test_draw import draw
import tkinter as tk


img_references = set()
my_player_num = 0
root = None

def main():
    global root

    tblstr = "PokerTable({'sb': 0.01, 'bb': 0.02, 'players': [Player(1.99, [4204049, 16795671], 0.01, []), Player(1.98, [268471337, 134224677], 0.02, []), None, Player(2, [1065995, 67144223], 0, ['fold', 'call', [0.04, 2]]), None, Player(2, [1057803, 98306], 0, [])], 'players_at_table': 4, 'players_in_hand': 4, 'button_pos': 5, 'current_turn': 3, 'board': [], 'pot': 0.03, 'side_pots': {}, 'total_to_call': 0.02, 'last_raise_size': 0.02, 'last_raiser': 1})"
    table = eval(tblstr)

    table.player_folds(3)
    table.add_player_bet(5, 0.04)
    table.add_player_bet(0, 0.03)
    table.add_player_bet(1, 0.02)

    print(table)
    tblstr = str(table)

    root = tk.Tk()
    root.geometry("1002x743")
    root.title("Poker Table")

    draw(root, table, my_player_num, img_references)

    root.mainloop()


if __name__ == '__main__':
    main()