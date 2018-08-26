from ptable import PokerTable
from ptable import Player
import tkinter as tk
from treys import Card

import time

img_references = []

def main():
    table = PokerTable()
    # table_str = "PokerTable({'sb': 0, 'bb': 0, 'players': [None, Player(0, [67115551, 270853], 0), Player(1, [268446761, 134236965], 0), Player(2, [134224677, 8406803], 0), None, None], 'active_players': 3, 'button_pos': None, 'current_turn': None, 'board': None, 'pot': 0, 'side_pots': {}})"
    # table = eval(table_str)
    # table_str2 = "PokerTable({'sb': 0, 'bb': 0, 'players': [None, Player(0, [268471337, 1082379], 0), None, None, Player(1, [16783383, 268454953], 0), Player(2, [164099, 8423187], 0)], 'active_players': 3, 'button_pos': None, 'current_turn': None, 'board': None, 'pot': 0, 'side_pots': {}})"
    # table = eval(table_str2)
    # table = ptable.PokerTable({"sb": 0.01, "bb": 0.02})
    for x in range(8):
        player = Player(x)
        table.add_player(player)
    table.start()



    my_player_num = 1

    root = tk.Tk()
    root.geometry("1002x743")
    root.title("Poker Table")
    background_image = tk.PhotoImage(file="./resources/table.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0)

    draw_players(root, table, my_player_num)

    print(table)

    root.mainloop()


def draw_players(window, table, my_player_num):
    # hard-coded hole card coords
    card_coords = [[442, 531], [70, 400], [70, 164], [442, 33], [814, 164], [814, 400]]
    # hard-coded player label coordinates
    label_coords = [[419, 575], [47, 444], [47, 208], [419, 77], [791, 208], [791, 444]]

    players = table.cfg["players"]
    for x in range(len(players)):
        # Start from my player and draw clockwise
        player_iter = (x+my_player_num)%len(players)

        # Draw hole cards
        if players[player_iter] is None:
            continue
        cards_canvas = tk.Canvas(window, width=119, height=86, bd=0, highlightthickness=0)
        cards_canvas.place(x=card_coords[x][0], y=card_coords[x][1])
        if x == 0:
            print(player_iter)
            card0_img = tk.PhotoImage(file="./resources/cards-png/"+Card.int_to_str(players[player_iter].hole_cards[0])+".png")
            card1_img = tk.PhotoImage(file="./resources/cards-png/"+Card.int_to_str(players[player_iter].hole_cards[1])+".png")
        else:
            card0_img = tk.PhotoImage(file="./resources/cards-png/back.png")
            card1_img = tk.PhotoImage(file="./resources/cards-png/back.png")
        cards_canvas.create_image(0, 0, image=card0_img, anchor=tk.NW)
        cards_canvas.create_image(59, 0, image=card1_img, anchor=tk.NW)
        img_references.append(card0_img)
        img_references.append(card1_img)

        # Draw player labels
        player_label_canvas = tk.Canvas(window, width=164, height=44, bd=0, highlightthickness=0)
        player_label_canvas.place(x=label_coords[x][0], y=label_coords[x][1])
        player_label_img = tk.PhotoImage(file="./resources/player_label.png")
        player_label_canvas.create_image(0, 0, image=player_label_img, anchor=tk.NW)
        player_label_canvas.create_text(23, 21, text=str(player_iter), font=("Arial", "16"), fill="white")
        player_label_canvas.create_text(92, 21, text=players[player_iter].stack, font =("Arial", "16"), fill="white")
        img_references.append(player_label_img)


if __name__ == '__main__':
    main()