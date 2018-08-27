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
    tblstr = "PokerTable({'sb': 1, 'bb': 2, 'players': [Player(198, [73730, 147715], False, 2, []), None, Player(199, [4228625, 81922], False, 1, ['fold', 'call', [4, 199]]), None, None, None], 'players_at_table': 2, 'players_in_hand': 2, 'button_pos': 0, 'current_turn': 2, 'board': [], 'pot': 3, 'side_pots': {}, 'total_to_call':2, 'last_raise_size': 2, 'last_raiser': 2, 'showdown': False, 'winner': []})"
    table = eval(tblstr)

    table.player_calls(2)
    table.player_checks(0)
    
    table.player_checks(2)
    table.player_checks(0)

    table.player_checks(2)
    table.player_checks(0)

    table.player_checks(2)
    table.player_checks(0)

    table.player_shows(0)

    print(table)

    root = tk.Tk()
    root.geometry("1002x743")
    root.title("Poker Table")

    draw(root, table, my_player_num, img_references)

    root.mainloop()


if __name__ == '__main__':
    main()