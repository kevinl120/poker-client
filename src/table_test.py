from ptable import PokerTable, Player
from table_test_draw import draw
import tkinter as tk


img_references = set()
my_player_num = 0
root = None

def main():
    global root

    # table = PokerTable({'sb': 1, 'bb': 2})
    # for _ in range(2):
    #     table.add_player(Player(200))
    # table.start()

    # for _ in range(100):
    tblstr = "PokerTable({'sb': 1, 'bb': 2, 'players': [Player(193, [69634, 268454953], False, 5, ['show', 'muck']), None, None, Player(198, None, False, 0, []), None, None], 'players_at_table': 2, 'players_in_hand': 1, 'button_pos': 3, 'current_turn': 0, 'board': [1057803, 16783383, 8406803, 268442665, 1082379], 'pot': 9, 'side_pots': {}, 'total_to_call': 5, 'last_raise_size': 5, 'last_raiser': 0, 'showdown': False, 'winner': [0, 0], 'end_of_hand': False})"
    table = eval(tblstr)

    print(table)

    root = tk.Tk()
    root.geometry("1002x743")
    root.title("Poker Table")

    draw(root, table, my_player_num, img_references)

    root.mainloop()


if __name__ == '__main__':
    main()