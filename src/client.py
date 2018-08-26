"""Script for Poker client"""
from ptable import PokerTable
from ptable import Player
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from treys import Card


img_references = []


def main():
    global root

    root = tk.Tk()
    root.geometry("1002x743")
    root.title("Poker Table")
    background_image = tk.PhotoImage(file="./resources/table.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0)

    connect_to_server()
    my_player_num = 1

    root.mainloop()


### SOCKETS ###
def connect_to_server():
    global HOST, PORT, BUFSIZ, client_socket, receive_thread

    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()


def receive():
    """Handles receiving of messages."""
    global my_player_num
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            if msg[0:3] == "mpn":
                my_player_num = int(msg[3])
            else:
                table = eval(msg)
                draw_players(root, table)
        except OSError:  # Possibly client has left the chat.
            break



### TKINTER ###

def draw_players(window, table):
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
        elif not players[player_iter].hole_cards is None:
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